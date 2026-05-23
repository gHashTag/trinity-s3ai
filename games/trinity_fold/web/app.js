// Trinity Fold — browser UI.
//
// Mirrors the scoring rules in src/scoring.rs. If you change one, change the
// other. The catalog itself is loaded from ../fixtures/catalog.json so the
// two implementations cannot drift on data.

"use strict";

const HOLDOUT_IDS = new Set(["o_cosmo_lambda", "o_mt_over_mb"]);

const CLAIM_WEIGHTS = {
  verified: 1.0,
  empirical_fit: 0.4,
  open_conjecture: 0.15,
  high_risk_or_falsified: 0.0,
  unverified: 0.0,
};

const CLAIM_ORDER = {
  verified: 0,
  empirical_fit: 1,
  open_conjecture: 2,
  high_risk_or_falsified: 3,
  unverified: 4,
};

const CLAIM_LABEL = {
  verified: "VERIFIED",
  empirical_fit: "EMPIRICAL_FIT",
  open_conjecture: "OPEN_CONJECTURE",
  high_risk_or_falsified: "HIGH_RISK_OR_FALSIFIED",
  unverified: "UNVERIFIED",
};

const WEIGHTS = {
  consistency: 1.0,
  dimensional_sanity: 1.0,
  observable_fit: 1.5,
  proof_debt_penalty: 1.0,
  falsification_penalty: 4.0,
  simplicity: 0.5,
  symmetry_coherence: 0.75,
  reproducibility: 0.5,
};

const state = {
  catalog: { nodes: [], triangles: [] },
  selected: new Set(),
  benchmark: false,
};

async function loadCatalog() {
  // Allow file:// usage by falling back to an inline catalog if fetch fails.
  try {
    const res = await fetch("../fixtures/catalog.json");
    if (!res.ok) throw new Error("fetch failed");
    return await res.json();
  } catch (_) {
    document.getElementById("notes").innerHTML =
      '<li>Could not load <code>fixtures/catalog.json</code>. Serve this folder over HTTP (see README).</li>';
    return { nodes: [], triangles: [] };
  }
}

function nodeById(id) {
  return state.catalog.nodes.find((n) => n.id === id);
}

function dimensionalSignature() {
  const sig = {};
  for (const id of state.selected) {
    const n = nodeById(id);
    if (!n || !n.dimension) continue;
    for (const [k, v] of Object.entries(n.dimension)) {
      sig[k] = (sig[k] || 0) + v;
    }
  }
  for (const k of Object.keys(sig)) if (sig[k] === 0) delete sig[k];
  return sig;
}

function effectiveValue(node) {
  if (state.benchmark && HOLDOUT_IDS.has(node.id)) return null;
  return node.value;
}

function computeScore() {
  const br = {
    consistency: 0,
    dimensional_sanity: 0,
    observable_fit: 0,
    proof_debt_penalty: 0,
    falsification_penalty: 0,
    simplicity: 0,
    symmetry_coherence: 0,
    reproducibility: 0,
    total: 0,
    worst_claim: "verified",
    notes: [],
  };
  const n = state.selected.size;
  if (n === 0) {
    br.notes.push("empty board");
    return br;
  }

  // 1. consistency
  let ok = 0,
    bad = 0;
  for (const id of state.selected) {
    const node = nodeById(id);
    if (!node) continue;
    for (const req of node.requires || []) {
      if (state.selected.has(req)) ok++;
      else bad++;
    }
    for (const inc of node.incompatible_with || []) {
      if (state.selected.has(inc)) bad++;
    }
  }
  br.consistency = ok + bad === 0 ? 1 : ok / (ok + bad);
  if (bad > 0) br.notes.push(`${bad} unmet requires/incompatible checks`);

  // 2. dimensional sanity
  const sig = dimensionalSignature();
  const sigKeys = Object.keys(sig);
  if (sigKeys.length === 0) {
    br.dimensional_sanity = 1;
  } else {
    const imbalance = sigKeys.reduce((s, k) => s + Math.abs(sig[k]), 0);
    br.dimensional_sanity = 1 / (1 + imbalance);
    br.notes.push(`dimensional imbalance: ${JSON.stringify(sig)}`);
  }

  // 3. observable fit
  let fitAcc = 0,
    fitN = 0;
  for (const id of state.selected) {
    const node = nodeById(id);
    if (!node || node.kind !== "observable") continue;
    const obs = effectiveValue(node);
    const pred = node.predicted;
    if (obs == null || pred == null) continue;
    const sigma = node.uncertainty && node.uncertainty > 0
      ? node.uncertainty
      : Math.max(Math.abs(obs) * 1e-3, 1e-12);
    const z = Math.abs((pred - obs) / sigma);
    const contrib = 1 / (1 + z * z);
    fitAcc += contrib * CLAIM_WEIGHTS[node.claim];
    fitN++;
    updateWorst(br, node.claim);
  }
  br.observable_fit = fitN === 0 ? 0 : fitAcc / fitN;

  // 4. proof debt
  let debt = 0;
  for (const id of state.selected) {
    const node = nodeById(id);
    if (!node) continue;
    const claimCost = { verified: 0, empirical_fit: 0.2, open_conjecture: 0.5, unverified: 0.7, high_risk_or_falsified: 0 }[node.claim];
    const tagCost = (node.tags || []).includes("proof_debt") ? 0.3 : 0;
    debt += claimCost + tagCost;
    updateWorst(br, node.claim);
  }
  br.proof_debt_penalty = Math.min(1, debt / n);

  // 5. falsification
  let falsified = 0;
  for (const id of state.selected) {
    const node = nodeById(id);
    if (!node) continue;
    const tags = node.tags || [];
    if (
      node.claim === "high_risk_or_falsified" ||
      tags.includes("falsified") ||
      tags.includes("no_go")
    ) {
      falsified++;
      updateWorst(br, "high_risk_or_falsified");
    }
  }
  br.falsification_penalty = Math.min(1, falsified / n);

  // 6. simplicity (peak around 10)
  const target = 10;
  const dev = Math.abs(n - target);
  br.simplicity = Math.max(0, Math.min(1, 1 / (1 + 0.05 * dev * dev)));

  // 7. symmetry coherence
  const hasSym = [...state.selected].some((id) => nodeById(id)?.kind === "symmetry");
  const hasGeo = [...state.selected].some((id) => nodeById(id)?.kind === "geometry");
  const triHits = state.catalog.triangles.filter((tri) =>
    tri.every((id) => state.selected.has(id))
  ).length;
  const triScore = state.catalog.triangles.length === 0
    ? 0.5
    : Math.max(0, Math.min(1, triHits / state.catalog.triangles.length));
  if (hasSym && hasGeo) br.symmetry_coherence = 0.5 + 0.5 * triScore;
  else if (hasSym || hasGeo) br.symmetry_coherence = 0.25 * triScore;
  else br.symmetry_coherence = 0;

  // 8. reproducibility
  let cited = 0;
  for (const id of state.selected) {
    const node = nodeById(id);
    if (node && node.citation) cited++;
  }
  br.reproducibility = cited / n;

  const raw =
    WEIGHTS.consistency * br.consistency +
    WEIGHTS.dimensional_sanity * br.dimensional_sanity +
    WEIGHTS.observable_fit * br.observable_fit +
    WEIGHTS.simplicity * br.simplicity +
    WEIGHTS.symmetry_coherence * br.symmetry_coherence +
    WEIGHTS.reproducibility * br.reproducibility -
    WEIGHTS.proof_debt_penalty * br.proof_debt_penalty -
    WEIGHTS.falsification_penalty * br.falsification_penalty;

  const maxPositive =
    WEIGHTS.consistency +
    WEIGHTS.dimensional_sanity +
    WEIGHTS.observable_fit +
    WEIGHTS.simplicity +
    WEIGHTS.symmetry_coherence +
    WEIGHTS.reproducibility;
  br.total = raw / maxPositive;
  if (falsified > 0) {
    br.total = Math.min(br.total, -0.25);
    br.notes.push(`${falsified} falsified node(s) on board — total capped`);
  }
  return br;
}

function updateWorst(br, claim) {
  if (CLAIM_ORDER[claim] > CLAIM_ORDER[br.worst_claim]) br.worst_claim = claim;
}

// --- Local search in JS (hill-climb + LCG anneal) ---
function scoreOf(set) {
  const saved = state.selected;
  state.selected = set;
  const r = computeScore();
  state.selected = saved;
  return r;
}

function hillClimb(maxIters = 200) {
  let current = new Set(state.selected);
  let best = scoreOf(current);
  for (let it = 0; it < maxIters; it++) {
    let improved = false;
    for (const node of state.catalog.nodes) {
      const cand = new Set(current);
      if (cand.has(node.id)) cand.delete(node.id);
      else cand.add(node.id);
      const s = scoreOf(cand);
      if (s.total > best.total + 1e-12) {
        current = cand;
        best = s;
        improved = true;
        break;
      }
    }
    if (!improved) break;
  }
  state.selected = current;
}

function lcg(seed) {
  let s = BigInt(seed) + 0x9e3779b97f4a7c15n;
  return () => {
    s = (s * 6364136223846793005n + 1442695040888963407n) & 0xffffffffffffffffn;
    return Number(s >> 11n) / 2 ** 53;
  };
}

function anneal(iters = 1000, seed = 42, t0 = 0.25, cooling = 0.999) {
  const rand = lcg(seed);
  let current = new Set(state.selected);
  let curScore = scoreOf(current);
  let bestSet = new Set(current);
  let bestScore = curScore;
  let t = t0;
  for (let i = 0; i < iters; i++) {
    const idx = Math.floor(rand() * state.catalog.nodes.length);
    const id = state.catalog.nodes[idx].id;
    const cand = new Set(current);
    if (cand.has(id)) cand.delete(id);
    else cand.add(id);
    const s = scoreOf(cand);
    const delta = s.total - curScore.total;
    const accept = delta > 0 || rand() < Math.exp(delta / Math.max(t, 1e-9));
    if (accept) {
      current = cand;
      curScore = s;
      if (curScore.total > bestScore.total) {
        bestSet = new Set(current);
        bestScore = curScore;
      }
    }
    t *= cooling;
  }
  state.selected = bestSet;
}

// --- Rendering ---
function render() {
  // Tiles
  const groups = document.querySelectorAll(".kind-group");
  for (const g of groups) {
    const kind = g.getAttribute("data-kind");
    const ul = g.querySelector("ul");
    ul.innerHTML = "";
    for (const n of state.catalog.nodes.filter((x) => x.kind === kind)) {
      const li = document.createElement("li");
      li.dataset.id = n.id;
      if (state.selected.has(n.id)) li.classList.add("selected");
      const claimClass = `claim claim-${n.claim}`;
      let valueChip = "";
      const eff = effectiveValue(n);
      if (n.kind === "observable" && eff != null) {
        valueChip = `<span class="meta">value: ${eff} ${n.unit || ""}</span>`;
      } else if (n.kind === "observable" && eff == null && state.benchmark) {
        valueChip = `<span class="meta">value: <em>hidden (benchmark)</em></span>`;
      }
      li.innerHTML = `
        <span class="name">${escapeHtml(n.name)}</span>
        <span class="meta">
          <span class="${claimClass}">${CLAIM_LABEL[n.claim]}</span>
          <span>${escapeHtml(n.id)}</span>
          ${n.citation ? `<span>· ${escapeHtml(n.citation)}</span>` : ""}
        </span>
        ${valueChip}
        <span class="meta">${escapeHtml(n.description)}</span>
      `;
      li.addEventListener("click", () => {
        if (state.selected.has(n.id)) state.selected.delete(n.id);
        else state.selected.add(n.id);
        render();
      });
      ul.appendChild(li);
    }
  }

  // Score
  const br = computeScore();
  const totalEl = document.getElementById("total");
  totalEl.textContent = br.total.toFixed(3);
  totalEl.style.color =
    br.total >= 0.6
      ? "var(--good)"
      : br.total >= 0.3
      ? "var(--warn)"
      : "var(--bad)";
  document.getElementById("worst-claim").textContent =
    "worst claim: " + CLAIM_LABEL[br.worst_claim];

  const tbody = document.querySelector("#breakdown tbody");
  tbody.innerHTML = "";
  for (const k of [
    "consistency",
    "dimensional_sanity",
    "observable_fit",
    "simplicity",
    "symmetry_coherence",
    "reproducibility",
    "proof_debt_penalty",
    "falsification_penalty",
  ]) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${k}</td><td>${br[k].toFixed(3)}</td>`;
    tbody.appendChild(tr);
  }

  const selUl = document.getElementById("selected");
  selUl.innerHTML = "";
  for (const id of state.selected) {
    const n = nodeById(id);
    const li = document.createElement("li");
    li.textContent = n ? `${n.id} — ${n.name}` : id;
    selUl.appendChild(li);
  }

  const notesUl = document.getElementById("notes");
  notesUl.innerHTML = "";
  for (const note of br.notes) {
    const li = document.createElement("li");
    li.textContent = note;
    notesUl.appendChild(li);
  }

  const triUl = document.getElementById("triangle-list");
  triUl.innerHTML = "";
  for (const tri of state.catalog.triangles) {
    const li = document.createElement("li");
    const complete = tri.every((id) => state.selected.has(id));
    if (complete) li.classList.add("complete");
    li.textContent = tri.join("  ·  ");
    triUl.appendChild(li);
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );
}

document.addEventListener("DOMContentLoaded", async () => {
  state.catalog = await loadCatalog();
  document.getElementById("btn-clear").addEventListener("click", () => {
    state.selected.clear();
    render();
  });
  document.getElementById("btn-search").addEventListener("click", () => {
    hillClimb();
    render();
  });
  document.getElementById("btn-anneal").addEventListener("click", () => {
    anneal();
    render();
  });
  document.getElementById("benchmark-mode").addEventListener("change", (e) => {
    state.benchmark = e.target.checked;
    render();
  });
  render();
});
