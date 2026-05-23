# admitted_log.md — Реестр всех Admitted в Trinity S3AI

**Дата последнего обновления:** Wave 12 sprint W12.4 (SHOULD_BE_THEOREM closures — follow-up to W11.7), rebased onto Wave 12 Track B (Cl(8) launch)
**Версия:** Trinity S3AI v4.0
**Состояние на момент аудита (A1, Wave 10.4):**

| Тип | Реальное кол-во | После W11.7 | После W12 Track B | После W12.4 | Заявлено ранее | Расхождение |
|-----|----------------|-------------|-------------------|-------------|----------------|-------------|
| `Axiom` SHOULD_BE_THEOREM rows in CSV | 44 | 32 | 32 | 21 | — | −12 W11.7, −11 W12.4 |
| `Axiom` declarations (proofs/, core) | 88 | 78 | 78 | 68 | не указано | −10 W11.7, −10 W12.4 |
| `Axiom` (TRACK_B_CLIFFORD, proofs/clifford_cl8/) | 0 | 0 | 6 | 6 | — | new in W12 Track B |
| `Admitted` (чистые, core proofs/) | 37 | 35 | 35 | 34 | 7 | **+27** |
| `Admitted` (TRACK_B_CLIFFORD) | 0 | 0 | 4 | 4 | — | new in W12 Track B |
| `admit` (inline) | 17 | 17 | 17 | 17 | 0 | **+17** |
| `Qed` (всего) | 1326 | 1337 | 1340 | 1351 | 326 | **+1025** |

(W11.7 closed 10 Axioms + 2 Admitted = 12 instances; W12 Track B added 6 Axioms + 4 Admitted in a *separate* Cl(8) namespace (`proofs/clifford_cl8/`) with full citations; W12.4 closed 10 core Axioms + 1 Admitted = 11 instances.)

## Sprint W12.4 — SHOULD_BE_THEOREM closures (2026-05, follow-up to W11.7)

Closed 11 axiom/admitted instances (9 CSV row identities accounting for proofs/ ↔ derivations/ mirrors) across 7 files:

| Name | File(s) | Tactic |
|------|---------|--------|
| `ttt_lr_is_phi_inv_cube_scaled` | `proofs/trinity/OptimizerInvariants.v` | `unfold; assert (phi <> 0); field. exact Hne.` (was Admitted Theorem) |
| `DF_chiral_symmetry` | `EtaDFBridge.v` (×2) | `exact I.` (True placeholder) |
| `mass_twist_eta` | `EtaDFBridge.v` (×2) | `intros _; unfold; reflexivity.` (concrete defs collapse) |
| `DF_exact_chirality` | `EtaDFBridge.v` (×2) | `split; reflexivity.` (concrete defs) |
| `iD_selfadjoint` | `DiracOperator.v` (×2) | `exact I.` (True placeholder) |
| `all_irrep_pairs_sv_ratio_is_unity` | `YukawaFrom2I.v` (×2) | `exact I.` (True placeholder) |

Notes:
- The `True` placeholders (`DF_chiral_symmetry`, `iD_selfadjoint`, `all_irrep_pairs_sv_ratio_is_unity`) had only trivial formal content; the *real* numerical/operator-theoretic claims they nodded at remain outside the formalisation and are recorded in surrounding comments.
- `mass_twist_eta` and `DF_exact_chirality` reduce via concrete `Definition`s of `dim_pos_DF = dim_neg_DF = 190` and `dim_ker_L = dim_ker_R = 50` — `reflexivity` discharges them.
- `ttt_lr_is_phi_inv_cube_scaled` was an `Admitted Theorem` whose CSV row is SHOULD_BE_THEOREM (Admitted+admit type). Closed with `field` after asserting `phi <> 0` via `phi_gt_0`. (Initial W12.4 commit asserted `phi^3 <> 0` which `field` does not accept; CI failed; corrected in W12.4-fix.)

## Wave 12 Track B — Cl(8) formalization launch (2026-05)

New directory `proofs/clifford_cl8/` introduces Track B per
`outputs/B_program_T1_T12.md`. The launch PR adds **6 new Axioms** and
**4 new Admitted theorems**, all tagged **`TRACK_B_CLIFFORD`** with full
published citations.

| Entity | File | Type | Category | Citation |
|--------|------|------|----------|----------|
| `Cl06_spec` | `Cl6_iso_M8R.v` | `Axiom` (existence of `CliffordSpec 0 6`) | TRACK_B_CLIFFORD | Wieser-Song 2022 §3 |
| `M8R_pair_alg` | `Cl6_iso_M8R.v` | `Axiom` (existence of `RAlgebra` instance for M_8(R)⊕M_8(R)) | TRACK_B_CLIFFORD | stdlib gap (no MathComp) |
| `Cl_n0_spec n` | `Cl8_periodicity.v` | `Axiom` (existence of `CliffordSpec n 0` for every n) | TRACK_B_CLIFFORD | Wieser-Song 2022 §3 |
| `Cl_80_spec` | `Cl8_periodicity.v` | `Axiom` | TRACK_B_CLIFFORD | Wieser-Song 2022 §3 |
| `M16R_alg` | `Cl8_periodicity.v` | `Axiom` | TRACK_B_CLIFFORD | stdlib gap |
| `RAlg_tensor` | `Cl8_periodicity.v` | `Parameter` (tensor product of R-algebras) | TRACK_B_CLIFFORD | stdlib gap; mathlib4 `Mathlib.LinearAlgebra.TensorProduct` ports needed |
| `T1_polarization` | `CliffordAlgebra.v` | `Admitted` | TRACK_B_CLIFFORD / SHOULD_BE_THEOREM | Lounesto 2001 §1.2 |
| `T2_Cl06_iso_M8R_pair` | `Cl6_iso_M8R.v` | `Admitted` | TRACK_B_CLIFFORD / GENUINE_ASSUMPTION (cited math) | Lounesto Table 16.3; Atiyah-Bott-Shapiro 1964 §11; Wieser-Song 2022 §6 |
| `T3_Cl_8periodicity` | `Cl8_periodicity.v` | `Admitted` | TRACK_B_CLIFFORD / GENUINE_ASSUMPTION | Atiyah-Bott-Shapiro 1964 Table 3; Lawson-Michelsohn 1989 Prop. I.4.1 |
| `T3_Cl80_iso_M16R` | `Cl8_periodicity.v` | `Admitted` | TRACK_B_CLIFFORD / GENUINE_ASSUMPTION | Lounesto Table 16.3 row (8,0); Lawson-Michelsohn 1989 I.4.16 |

**Honesty:** All four Admitted statements are well-known published theorems.
Discharging them in Rocq requires (a) a working tensor product of R-algebras
(not in stdlib; available in MathComp-Analysis or mathlib4), (b) explicit
matrix-generator constructions for the spinor representations (mechanical
but multi-week work), and (c) the volume-element computation. The launch PR
provides the scaffolding and the statements; the proofs are tracked as
TRACK_B_CLIFFORD follow-up items.

## Sprint W11.7 — SHOULD_BE_THEOREM closures (2026-05)

Closed via direct proof (12 CSV rows across 6 files):

| Axiom name | File(s) | Tactic used |
|------------|---------|-------------|
| `two_I_order` | `QuaternionicLinearity.v` (×2) | `Definition := 120` |
| `two_I_order_eq` | `QuaternionicLinearity.v` (×2) | `reflexivity` |
| `H4_group_order` | `QuaternionicLinearity.v` (×2) | `Definition := 120*120` |
| `H4_order_eq` | `QuaternionicLinearity.v` (×2) | `reflexivity` |
| `trace_full_D_sq_coxeter` | `DiracOperator.v` (×2) | `reflexivity` (nat 4*120=480) |
| `sigma_candidate_mass_scale` | `UnimodularityAndSigma.v` (×2) | `unfold; interval with (i_prec 60)` |

Note: the `sigma_candidate_mass_scale` closures were `Admitted Theorem` in the source (the A4 CSV classes them as Axiom-equivalent SHOULD_BE_THEOREM); converted to `Qed`.

> ⚠️ **ВАЖНО**: Предыдущий README.md заявлял "0 Admitted". Это НЕВЕРНО.
> Предыдущий admitted_log.md заявлял 25 Admitted. Тоже НЕВЕРНО.
> Настоящий документ отражает реальное состояние после A1-аудита (Wave 10.4).

---

## Таксономия

| Тег | Смысл | Кол-во |
|-----|-------|--------|
| `[PHYSICAL_AXIOM]` | Физическое допущение — граничное условие РГ, масштаб масс, нормировка | 5 |
| `[NUMERICAL_FIT]` | Формула найдена подбором по данным, вывода нет | 3 |
| `[MATH_TODO]` | Математически доказуемо, но вывод ещё не написан | 6 |
| `[LIBRARY_GAP]` | Ограничение coq-interval / stdlib Rocq 9.1.1 | 15 |
| `[REFUTED]` | Утверждение математически ЛОЖНО | 2 |

---

## Полный реестр — Admitted и admit

| № | Файл | Теорема/Лемма | Тег | Категория (A4) | Обоснование | Закрываемость |
|---|------|---------------|-----|----------------|-------------|---------------|
| 1 | `A4Conversion.v` | `conversion_exact` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Алгебраическое тождество: рационализация знаменателя. `field`/`ring` не справляются с `sqrt` в Rocq 9.1.1. | **Высокая** — `assert H5: sqrt 5 * sqrt 5 = 5; field_simplify [H5]; ring` |
| 2 | `Bounds_Mixing.v` | `N04_within_experimental_range` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | 65.66° vs. 65.5° ± 4°. `interval` не раскрывает `rad_to_deg` без `unfold`. | **Высокая** — `unfold N04_formula_deg rad_to_deg N04_formula_rad phi; interval with (i_prec 100)` |
| 3 | `Catalog42.v` | `Q02_is_m_s_over_m_u` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Было Qed. `powZ` unfold missing. | **Высокая** — `simpl; interval with (i_prec 150)` |
| 4 | `Catalog42.v` | `N03_is_sin2_theta_23` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Было Qed. `powZ` unfold. | **Высокая** — `simpl; interval with (i_prec 150)` |
| 5 | `Catalog42.v` | `C01_is_V_us` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Было Qed. Тройное трансцендентное произведение. | **Высокая** — `simpl; interval with (i_prec 200)` |
| 6 | `ChiralityAnalysis.v` | `phi_eq_2cos_pi5` | `[MATH_TODO]` | SHOULD_BE_THEOREM | phi=2*cos(pi/5); алгебраическое доказательство через минимальный многочлен. **НЕ был в admitted_log.md.** | **Высокая** — импортировать из E6vsH4.v |
| 7 | `E6vsH4.v` | `sqrt_5_not_rational` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Стандартный результат теории чисел. Нет в stdlib Coq. | **Средняя** — бесконечный спуск на Z |
| 8 | `E6vsH4.v` | `phi_irrational` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Следствие `sqrt_5_not_rational`. | **Высокая** — закроется вместе с №7 |
| 9 | `E6vsH4.v` | `E6_no_phi` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Контрапозитив `phi_irrational`. | **Высокая** — закроется вместе с №8 |
| 10 | `E6vsH4.v` | `cos_pi_5_quadratic` | `[MATH_TODO]` | SHOULD_BE_THEOREM | Два sub-admits: sin²→1-cos² + lra. | **Средняя** — `rewrite Hsin; ring; nlinarith` |
| 11 | `GaugeOrigins.v` | `G01_from_GUT_running` | `[PHYSICAL_AXIOM]` | GENUINE_ASSUMPTION | Требует `sqrt(5/3)` + однопетлевое РГ — не выводимо из H4. | **Низкая** — физическое допущение |
| 12 | `H4GaugeEmbedding.v` | `phi_irrational_over_Q` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Дублирует доказательство из E6vsH4.v. | **Средняя** — переиспользовать |
| 13 | `H4Lagrangian.v` | `L01_lagrangian_order_of_magnitude` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | `interval` не справляется с `1e16/1.22e19`. | **Высокая** — разбить на оценки |
| 14 | `H4Lagrangian.v` | `Koide_H4_test` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | `sqrt` внутри `interval`. | **Высокая** — `unfold Koide_H4; simpl; interval with (i_prec 150)` |
| 15 | `HiggsOrigins.v` | `H03_h_half_structural` | `[REFUTED → RESOLVED v4.0-wave10.4 / wave11]` | **RESOLVED** | Заменён на `H03_h_half_structural_refuted` (Qed) в `proofs/trinity/HiggsOrigins.v` и `derivations/higgs/HiggsOrigins.v`. Доказывает h/2 ≠ (d3·d4)/(d3+d4-d3²/d4). Структурный факт h/2=15 остаётся отдельной теоремой `h_half_is_15`. | **Закрыто** |
| 16 | `Koide.v` | `Koide_correct_forms_equal` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | `field`/`ring` не работают с `sqrt` в знаменателе. | **Высокая** — `field_simplify [sqrt5_sq]; ring` |
| 17 | `LeptonOrigins.v` | `H4_determines_L01` | `[NUMERICAL_FIT]` | GENUINE_ASSUMPTION | L01 = 239·e/π найдено численно, не выведено из H4. Конструктивная f не предоставлена. | **Очень низкая** |
| 18 | `NeutrinoOrigins.v` | `seesaw_scale_from_v31` | `[PHYSICAL_AXIOM]` | GENUINE_ASSUMPTION | M_R не определяется геометрией H4. | **Низкая** |
| 19 | `NeutrinoOrigins.v` | `nu_absolute_scale_gap` | `[NUMERICAL_FIT]` | GENUINE_ASSUMPTION | Множитель 10⁻⁵ eV² вставлен вручную. | **Очень низкая** |
| 20 | `OptimizerInvariants.v` | `ttt_lr_is_phi_inv_cube_scaled` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | `field` не сводит phi^3 ненулевое условие автоматически. | **Высокая** — `assert Hphi3_ne; field [Hphi3_ne]` |
| 21 | `RGRunning.v` | `alpha_from_H4` | `[PHYSICAL_AXIOM]` | GENUINE_ASSUMPTION | Нужен sqrt(5/3) + однопетлевое РГ. | **Низкая** |
| 22 | `RGRunning.v` | `alpha_s_from_H4` | `[PHYSICAL_AXIOM]` | GENUINE_ASSUMPTION | Нужно двухпетлевое бегание + топ-пороговые поправки. | **Низкая** |
| 23 | `UnimodularityAndSigma.v` | `sigma_candidate_mass_scale` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Rabs((2/30)*1.5e16 - 1e15) < 1e10; чистая рациональная R, большие числа. | **Высокая** — `lra` или `ring_simplify; lra` |
| 24 | `UniquenessStructural.v` | `phi_squared_nat` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | 1618*1618=2618724; `vm_compute` segfault на больших `nat` в Rocq 9.1.1. | **Высокая** — `lia` или заменить `nat` на `Z` |
| 25 | `test_scratch.v` | `VEV_corrected_matches_SM` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | Нужна `sqrt_sq` + `v_SM >= 0`. | **Высокая** |
| 26 | `test_scratch.v` | `m_H_corrected_matches_Trinity` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | sqrt(m_H_Trinity²)=m_H_Trinity. | **Высокая** |
| 27 | `test_scratch.v` | `Higgs_mass_from_curvature` | `[LIBRARY_GAP]` | SHOULD_BE_THEOREM | sqrt(2·μ²)=m_H_Trinity; та же цепочка. | **Высокая** |

### Новые записи (не в предыдущем admitted_log.md)

| № | Файл | Теорема/Лемма | Тег | Обоснование |
|---|------|---------------|-----|-------------|
| 28 | `ChiralityAnalysis.v` | `phi_eq_2cos_pi5` | `[MATH_TODO]` | phi=2*cos(pi/5) — обнаружен A1-аудитом. Не был задокументирован. |
| 29 | `UnimodularityAndSigma.v` | `sigma_candidate_mass_scale` | `[LIBRARY_GAP]` | Обнаружен A1-аудитом. Не был задокументирован. |

---

## Сводка по тегам (обновлённая)

| Тег | Кол-во | Категория A4 |
|-----|--------|-------------|
| `[PHYSICAL_AXIOM]` | 5 | GENUINE_ASSUMPTION |
| `[NUMERICAL_FIT]` | 3 | GENUINE_ASSUMPTION |
| `[MATH_TODO]` | 6 | SHOULD_BE_THEOREM |
| `[LIBRARY_GAP]` | 15 | SHOULD_BE_THEOREM |
| `[REFUTED]` | 2 | REFUTED |

---

## Приоритеты закрытия

### Высокий приоритет (1–2 часа, pure library fixes)
- №№ 2–5, 23–27: Catalog42, Bounds_Mixing, UnimodularityAndSigma, test_scratch, sigma_candidate_mass_scale
- №№ 20, 14, 16: OptimizerInvariants, Koide, H4Lagrangian Koide_test
- № 6: ChiralityAnalysis phi_eq_2cos_pi5 (импорт из E6vsH4.v)

### Средний приоритет (требует ручных доказательств)
- №№ 7–10: E6vsH4 — иррациональность √5 + следствия
- № 12: H4GaugeEmbedding — переиспользование после E6vsH4
- № 1: A4Conversion — рационализация знаменателя

### Низкий приоритет (требует физического прогресса)
- №№ 11, 21, 22, 18: RGRunning/GaugeOrigins/NeutrinoOrigins — физические допущения
- №№ 17, 19: NUMERICAL_FIT — нужна физическая деривация
- № 15: HiggsOrigins H03 — REFUTED, требует переформулировки

---

## Статус заголовочных комментариев

| Файл | Старый заголовок | Факт | Действие |
|------|-----------------|------|---------|
| `E6vsH4.v` | "ALL theorems: QED, 0 Admitted." | **4 Admitted+admit** | Исправить (патч E6vsH4_header_patch.diff) |
| `README.md` | "Admitted: 0" | **37 Admitted + 17 admit** | Исправить (патч README_patch.diff) |
| `admitted_log.md` (старый) | "Всего Admitted: 25" | **37 Admitted** | Заменить настоящим документом |

---

*Документ создан A4-аудитом (Wave 10.4). Полная стратификация: `proofs/trinity/FOUNDATIONS.md` и `outputs/A4/A4_axiom_stratification.csv`.*
