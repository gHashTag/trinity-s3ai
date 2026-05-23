#!/usr/bin/env python3
"""
generate_claims.py — regenerate README claim table and GOLDEN BRIDGE card
data from the single source of truth at docs/claims.yaml.

Usage:
    python3 scripts/generate_claims.py             # rewrite generated artefacts
    python3 scripts/generate_claims.py --check     # CI mode: exit 1 if stale

Generated outputs:
    * README.md, between the markers
        <!-- CLAIMS_TABLE:START -->
        <!-- CLAIMS_TABLE:END -->
    * games/trinity_fold/fixtures/generated_claim_cards.json

The script is intentionally deterministic: identical input must produce
byte-identical output so the --check mode can be trusted.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "generate_claims.py requires PyYAML. Install with: pip install pyyaml\n"
    )
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAIMS_YAML = REPO_ROOT / "docs" / "claims.yaml"
README = REPO_ROOT / "README.md"
GAME_CARDS = (
    REPO_ROOT / "games" / "trinity_fold" / "fixtures" / "generated_claim_cards.json"
)

VALID_STATUSES = {
    "verified",
    "empirical_fit",
    "open_conjecture",
    "high_risk_or_falsified",
    "retracted_or_unverified",
}

STATUS_LABEL = {
    "verified": "verified",
    "empirical_fit": "empirical_fit",
    "open_conjecture": "open_conjecture",
    "high_risk_or_falsified": "high_risk_or_falsified",
    "retracted_or_unverified": "retracted_or_unverified",
}

VALID_LAYERS = {f"L{i}" for i in range(8)}
VALID_KINDS = {
    "constant",
    "symmetry",
    "geometry",
    "field",
    "constraint",
    "observable",
    "infra",
    "meta",
}

REQUIRED_FIELDS = (
    "id",
    "title",
    "short_label",
    "layer",
    "status",
    "evidence",
    "owner_file",
    "blocking_gap",
    "game_card",
)

REQUIRED_GAME_CARD_FIELDS = ("kind", "description")


def load_ledger(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: top-level YAML must be a mapping")
    if "claims" not in data or not isinstance(data["claims"], list):
        raise SystemExit(f"{path}: `claims:` list missing")
    return data


def validate(data: dict) -> None:
    seen_ids: set[str] = set()
    for idx, claim in enumerate(data["claims"]):
        prefix = f"claims[{idx}]"
        if not isinstance(claim, dict):
            raise SystemExit(f"{prefix}: must be a mapping")
        for field in REQUIRED_FIELDS:
            if field not in claim:
                raise SystemExit(f"{prefix}: missing required field `{field}`")
        cid = claim["id"]
        if not isinstance(cid, str) or not cid:
            raise SystemExit(f"{prefix}: id must be a non-empty string")
        if cid in seen_ids:
            raise SystemExit(f"{prefix}: duplicate id `{cid}`")
        seen_ids.add(cid)
        if claim["status"] not in VALID_STATUSES:
            raise SystemExit(
                f"{prefix} ({cid}): status `{claim['status']}` is not one of "
                f"{sorted(VALID_STATUSES)}"
            )
        if claim["layer"] not in VALID_LAYERS:
            raise SystemExit(
                f"{prefix} ({cid}): layer `{claim['layer']}` is not one of "
                f"{sorted(VALID_LAYERS)}"
            )
        gc = claim["game_card"]
        if not isinstance(gc, dict):
            raise SystemExit(f"{prefix} ({cid}): game_card must be a mapping")
        for field in REQUIRED_GAME_CARD_FIELDS:
            if field not in gc:
                raise SystemExit(
                    f"{prefix} ({cid}): game_card missing field `{field}`"
                )
        if gc["kind"] not in VALID_KINDS:
            raise SystemExit(
                f"{prefix} ({cid}): game_card.kind `{gc['kind']}` is not one of "
                f"{sorted(VALID_KINDS)}"
            )


def _escape_md_cell(text: str) -> str:
    return (
        " ".join(str(text).split())
        .replace("\\", "\\\\")
        .replace("|", "\\|")
    )


def render_readme_block(data: dict) -> str:
    lines: list[str] = []
    lines.append("")
    lines.append(
        "_Generated from [`docs/claims.yaml`](docs/claims.yaml) by "
        "[`scripts/generate_claims.py`](scripts/generate_claims.py). "
        "Do not edit this block by hand._"
    )
    lines.append("")
    lines.append("| Claim | Layer | Status | Evidence | Blocking gap |")
    lines.append("|-------|-------|--------|----------|--------------|")
    for claim in data["claims"]:
        gap = _escape_md_cell(claim["blocking_gap"]) if claim["blocking_gap"] else "—"
        lines.append(
            "| {title} | {layer} | `{status}` | {evidence} | {gap} |".format(
                title=_escape_md_cell(claim["title"]),
                layer=_escape_md_cell(claim["layer"]),
                status=STATUS_LABEL[claim["status"]],
                evidence=_escape_md_cell(claim["evidence"]),
                gap=gap,
            )
        )
    lines.append("")
    return "\n".join(lines)


def update_readme(data: dict) -> str:
    text = README.read_text(encoding="utf-8")
    start_marker = data.get("generated_marker_start", "<!-- CLAIMS_TABLE:START -->")
    end_marker = data.get("generated_marker_end", "<!-- CLAIMS_TABLE:END -->")
    if start_marker not in text or end_marker not in text:
        raise SystemExit(
            f"README.md is missing the generator markers {start_marker} / "
            f"{end_marker}. Insert them before running this script."
        )
    pre, rest = text.split(start_marker, 1)
    _, post = rest.split(end_marker, 1)
    block = render_readme_block(data)
    new_text = f"{pre}{start_marker}\n{block}\n{end_marker}{post}"
    return new_text


def render_game_cards(data: dict) -> str:
    """Deterministic JSON view of the ledger for the GOLDEN BRIDGE.

    Kept intentionally narrow: only the fields the game actually needs.
    The Rust side parses this and uses it to materialise card tiles."""
    cards = []
    for claim in data["claims"]:
        gc = claim["game_card"]
        cards.append(
            {
                "id": claim["id"],
                "kind": gc["kind"],
                "name": claim["short_label"],
                "description": " ".join(str(gc["description"]).split()),
                "claim": claim["status"],
                "layer": claim["layer"],
                "evidence": claim["evidence"],
                "owner_file": claim["owner_file"],
                "blocking_gap": claim["blocking_gap"],
                "tags": list(gc.get("tags", [])),
            }
        )
    payload = {
        "version": data.get("version", 1),
        "source": "docs/claims.yaml",
        "generator": "scripts/generate_claims.py",
        "cards": cards,
    }
    return json.dumps(payload, indent=2, ensure_ascii=True) + "\n"


def write_if_changed(path: Path, new_content: str, *, check: bool) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old == new_content:
        return False
    if check:
        sys.stderr.write(
            f"[stale] {path.relative_to(REPO_ROOT)} would change. "
            "Run `python3 scripts/generate_claims.py` and commit the result.\n"
        )
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_content, encoding="utf-8")
    sys.stdout.write(f"[wrote] {path.relative_to(REPO_ROOT)}\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate only; exit non-zero if generated outputs are stale.",
    )
    args = parser.parse_args()

    data = load_ledger(CLAIMS_YAML)
    validate(data)

    readme_new = update_readme(data)
    cards_new = render_game_cards(data)

    stale = False
    stale |= write_if_changed(README, readme_new, check=args.check)
    stale |= write_if_changed(GAME_CARDS, cards_new, check=args.check)

    if args.check and stale:
        return 1
    if not args.check:
        sys.stdout.write(
            f"OK: ledger validated, {len(data['claims'])} claims, artefacts up to date.\n"
        )
    else:
        sys.stdout.write(
            f"OK: ledger validated, {len(data['claims'])} claims, artefacts already current.\n"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
