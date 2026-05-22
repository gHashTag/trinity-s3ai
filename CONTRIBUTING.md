# CONTRIBUTING — Trinity S3AI

> **Принцип: «Не врать!! Честным будь!»**  
> *"Do not lie. Be honest."*

---

## Russian / Русский

### Принцип честности (HONESTY-FIRST)

Этот репозиторий является **конструктивным отрицательным результатом**. Четыре теоремы о недостижимости (NGT1–NGT4 в `NoGoTheorems.v`) формально доказывают, что H4/600-cell геометрия *не может* воспроизвести:
- Космологическую постоянную Λ
- σ-поле NCG
- Хиральность фермионов
- Иерархию масс лептонов

Самый большой риск — **тихая регрессия**: новая формула `φ^a · π^b · e^c = X` добавляется в код без явного тега честности и выглядит как вывод из первых принципов, хотя на самом деле является феноменологической подгонкой.

### Правила для новых вкладов

#### 1. Admitted-аксиомы

Каждый `Admitted` должен иметь один из следующих тегов:

| Тег | Значение |
|-----|----------|
| `[PHYSICAL_AXIOM]` | Физическая аксиома из эксперимента (PDG) |
| `[NUMERICAL_FIT]` | Числовая подгонка из Python/Mathematica |
| `[MATH_TODO]` | Математический пробел, будет доказан позже |
| `[LIBRARY_GAP]` | Ограничение библиотеки Coq |

Пример:
```coq
Admitted. (* [NUMERICAL_FIT] значение из Python: bridge_results_v2.json *)
```

#### 2. Феноменологические формулы

Любая формула вида `Definition X := phi^a * PI^b * exp 1 / N` должна иметь тег:

```coq
(* [phenomenological_fit] Это численное совпадение с данными PDG 2024. *)
(* НЕ является выводом из геометрии H4. Ошибка: 0.05%.               *)
Definition my_formula : R := phi^3 * exp 1 / PI.
```

Автоматическая проверка выполняется через `scripts/anti_numerology_gate.py` (CI job `anti_numerology_check`).

#### 3. PR-шаблон

Каждый PR обязан иметь раздел «Что проверено / Что открыто» (см. шаблон `.github/PULL_REQUEST_TEMPLATE.md`).

---

## English

### HONESTY-FIRST Principle

This repository is a **constructive negative result**. See `SALVAGE.md` for a summary of what H4 *can* and *cannot* do. The main findings are four formal No-Go Theorems in `proofs/trinity/NoGoTheorems.v`.

The greatest ongoing risk is **silent regression**: someone adds a new `φ^a · π^b · e^c = X` formula without an explicit honesty tag, and it silently appears to be a first-principles derivation.

### Rules for New Contributions

#### 1. Admitted axioms

Every `Admitted` must carry exactly one tag from:

| Tag | Meaning |
|-----|---------|
| `[PHYSICAL_AXIOM]` | Physical input from experiment (PDG value) |
| `[NUMERICAL_FIT]` | Numeric value from Python/external computation |
| `[MATH_TODO]` | Mathematical gap, to be formalized later |
| `[LIBRARY_GAP]` | Coq library limitation (e.g., interval tactic timeout) |

Example:
```coq
Admitted. (* [PHYSICAL_AXIOM] sin^2(theta_W) = 0.22336, PDG 2024 *)
```

Rationale: `Admitted` without a tag is indistinguishable from a deliberate hole. All gaps must be explained.

#### 2. Numerological formulas

Any `Definition` combining ≥2 of {φ, π, e, √n} in its RHS and matching a physical observable must carry an approved tag. The anti-numerology gate enforces this automatically:

```coq
(* [phenomenological_fit] Numerical coincidence with PDG 2024. Error 0.024%. *)
(* NOT derived from H4 geometry; see NoGoTheorems.v NGT4.                   *)
Definition G01_formula : R := 36 * phi * (exp 1) * (exp 1) / PI.
```

Approved tags: `[phenomenological_fit]`, `[NUMERICAL_FIT]`, `[HONEST: ...]`, `[NCG_AXIOM]`, `[PHYSICAL_AXIOM]`, `[MATH_TODO]`, `[LIBRARY_GAP]`.

Run the gate locally before pushing:
```bash
python3 scripts/anti_numerology_gate.py
```

#### 3. No fake proofs

- Do not remove `Admitted` without adding a real proof.
- Do not replace a correct proof with `Admitted` and claim it is proven elsewhere.
- Do not add a theorem whose statement is vacuously true or trivially unprovable.

#### 4. PR requirements

Every PR must:
1. Fill in the PR template (`.github/PULL_REQUEST_TEMPLATE.md`)
2. Pass `anti_numerology_check` CI job (or include `[skip-numerology-check]` with explanation)
3. Pass `validate_v4.py` (formula error bounds)
4. Have a "What is verified / What is open" section

#### 5. Build instructions (Coq 8.20.1)

```bash
# Prerequisites: opam, Coq 8.20.1, coq-interval, coq-coquelicot
cd proofs/trinity
coq_makefile -f _CoqProject -o Makefile.coq
make -f Makefile.coq -j$(nproc)
```

Or use Docker:
```bash
docker run -it --rm -v $(pwd):/work coqorg/coq:8.20.1-ocaml-4.14-flambda
```

#### 6. Python tests

```bash
pip install mpmath numpy
python3 validate_v4.py
python3 scripts/anti_numerology_gate.py --verbose
```

---

## File Structure

```
proofs/trinity/        — All Coq .v files (23 files, 326 Qed)
scripts/               — Python utilities and gates
  anti_numerology_gate.py   — Formula honesty checker
  README_anti_numerology.md — Gate documentation
.github/workflows/
  ci.yml               — Main CI (anti_numerology_check → build)
  release.yml          — Release artifact builder
SALVAGE.md             — What H4 can/cannot do (read first)
NoGoTheorems.v         — Formal no-go theorems NGT1–NGT4
CITATION.cff           — Citation metadata
CONTRIBUTING.md        — This file
```

---

## Questions?

Open an issue using `.github/ISSUE_TEMPLATE.md`. Describe which formula or theorem is under question, cite the PDG source, and propose a correction if you have one.

*Wave 10.5 — Trinity S3AI*
