# Trinity-s3ai — План улучшений (ROADMAP)

Документ синтезирует результаты Wave 1-3 (выполнено) и литературный обзор (NCG, E8/H4, формулы масс, формализация в Coq/Lean) в дорожную карту на Wave 4-7.

---

## Где мы сейчас (статус после Wave 1-3, merged в main: [670aa5c](https://github.com/gHashTag/trinity-s3ai/commit/670aa5c))

| Метрика | Значение |
|---|---|
| Coq файлов | 34 |
| Qed теорем | 436 (+203 в этом цикле) |
| Admitted | 25 (5 новых, все с `(* HONEST: ... *)`) |
| Axiom | 12 (2 новых, явно задекларированы) |
| validate_v4.py | 25/25 = 100% |
| MD-нарративов | 16 (включая 4 литературных обзора в `derivations/literature/`) |

**Жёсткая правда из аудита (`derivations/catalog_audit/audit_report.md`):**
- Из 25 формул каталога: 0 (R) выведены из первых принципов, 8 (S) структурно мотивированы, 17 (NF) — чистая подгонка
- Coq-теорема `alpha_from_H4_refuted: Qed.` доказывает математическую ложность ключевого claim
- δ_CP=65.66° vs NuFit 6.0 ~177° — за пределами 3σ, DUNE 2028 фальсифицирует
- Koide: H4 даёт Q≈0.834, физика 0.6667 — расхождение 25%

**Литература показывает:**
- H4/600-cell ↔ E8 — математически строгая связь (McKay, икосиане; см. [e8_h4_in_physics.md](derivations/literature/e8_h4_in_physics.md))
- Trinity-s3ai является **первой** попыткой вывести массы фермионов из H4-структуры (нет prior art)
- Программа Connes NCG жива, но имеет нерешённые проблемы (Lorentz signature, gravity, neutrino sector); см. [ncg_state_of_art.md](derivations/literature/ncg_state_of_art.md)
- F-theory Pati-Salam 2025 нашла 2 модели, воспроизводящие массы; модулярные A4/S4 модели предсказывают всю лептонную структуру одним параметром τ; см. [mass_formulas_state_of_art.md](derivations/literature/mass_formulas_state_of_art.md)
- Уровень формализации NCG в Coq/Lean ~ нулевой — Trinity-s3ai потенциально в авангарде; см. [formalization_state_of_art.md](derivations/literature/formalization_state_of_art.md)

---

## Wave 4 — Очистка и переименование (1-2 недели)

**Цель**: устранить ложные claims без потери структурного содержания. Это критическая фаза доверия.

1. **Переименовать NF-формулы в `*_phenomenological_fit`** во всех `.v` файлах. Удалить ★SG=0% маркировку для CMB01-04, INF01-06 в `FORMULAS.md` (они дают ошибку 26-97%, не 0%; см. [cosmology_origins.md](derivations/cosmology/cosmology_origins.md))
2. **Удалить или переименовать `alpha_from_H4` и `alpha_s_from_H4`** — заменить на `restated_*` теоремы из `RGRunningExtras.v` (Qed). Старые Admitted уже опровергнуты теоремой `alpha_from_H4_refuted`
3. **Структурировать `Admitted` по таксономии** (урок 1 из formalization обзора):
   - `[PHYSICAL_AXIOM]` — физическое допущение (RG boundary)
   - `[NUMERICAL_FIT]` — без вывода
   - `[MATH_TODO]` — доказуемо но не доказано
   - `[LIBRARY_GAP]` — ограничение coq-interval
4. **Создать `admitted_log.md`** — живой реестр всех Admitted с обоснованием
5. **Использовать `Print Assumptions` после каждой основной теоремы** — публиковать минимальные наборы аксиом

**Acceptance**: 0 ложных claims о точности, каждый Admitted имеет тег и обоснование

---

## Wave 5 — Connes-style вывод алгебры A_F из H4 (4-8 недель, исследовательская)

**Цель**: ответить на ключевой вопрос «почему именно эта алгебра?» способом, который Connes принимает.

Урок 11 из NCG обзора: альтернативные геометрические объяснения A_F = ℂ⊕ℍ⊕M₃(ℂ) уже существуют в литературе (KO-размерность = 6 mod 8, кватернионная линейность). Текущий проект А_F **постулирует**, а не **выводит** из H4.

Параллельные субагенты:

1. **Агент A**: Вычислить KO-размерность геометрии H4/600-cell. Если ≠ 6 mod 8 — это серьёзная проблема; если = 6 — мост построен
2. **Агент B**: Проверить кватернионную линейность для 120 вершин 600-cell (они образуют бинарную икосаэдральную группу — кватернионная структура есть!). Это сильный кандидат на rigorous derivation
3. **Агент C**: Унимодулярность определителя для проекций — формальный Coq-доказательство
4. **Агент D**: Найти или опровергнуть аналог σ-поля Chamseddine-Connes (которое исправило m_H в 2012)

**Acceptance**: либо новый файл `H4_to_AF_derivation.v` с теоремой `A_F_from_H4_structure: Qed.`, либо честный `NoGo_theorem.v` показывающий несовместимость

---

## Wave 6 — Хиральность и фальсификация Lisi-pattern (3-5 недель)

**Цель**: ответить на вопрос «попадает ли Trinity под Distler-Garibaldi?»

Уроки 1, 2, 15 из E8 обзора: H4 не алгебра Ли, поэтому теорема Distler-Garibaldi формально не применяется — но проблема хиральности не закрыта.

1. **Сформулировать гипотезу хиральности явно** в `.v` файле: `Definition chiral_embedding := ...` (что именно вкладывается в H4-структуру)
2. **Проверить применимость аналога Distler-Garibaldi** для групп Кокстера: если есть аналог теоремы → опровержение проекта; если нет → обоснование альтернативы
3. **Связать с F-theory подходом** (BHV, Donagi-Wijnholt): если H4 происходит из 6D геометрии (600-cell как сечение CY3 или fibration), хиральность приходит "сверху"
4. **Сравнить с реализациями E8 в природе**: CoNb2O6 (Coldea 2010), BaCo2V2O8 (2024) — там E8 спектр **измерен** в условиях quantum critical Ising. Если Trinity-s3ai даёт похожие предсказания для других материалов — это сильное независимое подтверждение

**Acceptance**: `chirality_analysis.md` + либо `chirality_theorem.v` (Qed), либо честное опровержение проекта

---

## Wave 7 — Тестируемые предсказания и публикация (продолжающаяся)

**Цель**: превратить проект из numerology в фальсифицируемую науку.

1. **δ_CP при DUNE 2028-2032**: текущее предсказание 65.66° = 3/φ² уже >3σ от NuFit 6.0 (~177°). Регистрировать это **до** результата DUNE на arXiv с timestamp
2. **f₀ = 12.8 ТГц предсказание** (урок 14 из mass formulas): искать спектроскопическое подтверждение в материалах с икосаэдральной симметрией (квазикристаллы Al-Mn-Pd)
3. **Cравнение с Koide на 5+ digits** (урок 5 из mass formulas): признать 9.3 ppm точность Koide как benchmark; не пытаться "побить" её на лептонах, использовать как cross-check
4. **Готовить статью для arXiv hep-ph**: один результат — например, формальный Coq-вывод A_F из H4 (если Wave 5 даёт это). Не публиковать каталог 25 формул как "теорию"
5. **Lean 4 port** дифференциально-геометрических частей (урок 6 из формализации): mathlib имеет лучшую поддержку Lie groups / manifolds; Coq оставить для arithmetic identities
6. **AI-ассистент**: подключить Claude+rocq-mcp / Goedel-Prover-V2 (90.4% MiniF2F) для автоматического закрытия Admitted (урок 7 из формализации)

**Acceptance**: 1 arXiv preprint, 1 falsifiable prediction зарегистрированный, 1 Coq → Lean 4 port раздела

---

## Wave 8+ — Долгосрочные исследовательские направления

- **Спектр D_F (480×480)**: формальное Coq-доказательство ключевой аксиомы `H01_spectral_key_identity` (HiggsOrigins.v) через прямое вычисление собственных значений
- **Космология честно**: либо вывести Λ, H₀, n_s из H4 на правильных масштабах, либо удалить раздел Tier 3 из FORMULAS.md
- **Связь с интегрируемой Toda-теорией E8**: massы Замолодчикова уже содержат φ — это рецензируемая физика. Может Trinity-s3ai дать предсказания для другой интегрируемой системы H4-типа?
- **53-цикл** (урок 3 из mass formulas): проект упоминает 53-цикл как ключевой artefact, но это не объяснено — структурное объяснение нужно
- **Зеркальные фермионы** (урок 13 из mass formulas): преимущество H4 в том, что он реальный (зеркальных фермионов нет); это можно проверить

---

## Принципы (общие для всех волн)

1. **Честность важнее красоты**: лучше `Admitted` с `(* HONEST: ... *)` чем `Qed` с натяжкой
2. **Falsifiability**: каждая физическая претензия должна иметь экспериментальную проверку
3. **Соразмерность**: численная подгонка φ^a·π^b·e^c → не "вывод", а "корреляция"
4. **Cross-check с established**: Koide (9.3 ppm), Connes (m_H в 2018 предсказание), F-theory Pati-Salam — известные эталоны
5. **Coq как контроль качества, не как маркетинг**: 436 Qed ничего не значат, если они доказывают тривиальности

---

## Метрика успеха

| Wave | Критерий успеха |
|---|---|
| 4 | 0 ложных claims; admitted_log.md полный |
| 5 | Либо derivation A_F из H4, либо честное no-go |
| 6 | Анализ хиральности завершён; pattern Distler-Garibaldi разрешён |
| 7 | 1 arXiv preprint, 1 falsifiable prediction, Lean 4 port одного раздела |

---

## Источники

- [e8_h4_in_physics.md](derivations/literature/e8_h4_in_physics.md) — 15 уроков, 28 КБ
- [ncg_state_of_art.md](derivations/literature/ncg_state_of_art.md) — 18 уроков, 35 КБ
- [mass_formulas_state_of_art.md](derivations/literature/mass_formulas_state_of_art.md) — 15 уроков, 37 arXiv-ссылок
- [formalization_state_of_art.md](derivations/literature/formalization_state_of_art.md) — 15 уроков, 30 КБ

Ключевые arXiv:
- [arXiv:0905.2658](https://arxiv.org/abs/0905.2658) — Distler-Garibaldi, no-go для E8
- [arXiv:1208.1030](https://arxiv.org/abs/1208.1030) — Chamseddine-Connes "Resilience"
- [arXiv:0711.0770](https://arxiv.org/abs/0711.0770) — Lisi E8 ToE
- [arXiv:1103.3694](https://arxiv.org/abs/1103.3694) — Coldea E8 в CoNb2O6
- [arXiv:0806.0102](https://arxiv.org/abs/0806.0102) — BHV F-theory GUTs

---

## Wave 12 Status (2026-05-22)

Wave 12 is a **communication and consolidation wave**. No new physics claims are introduced. The focus is on honest registry of predictions, roadmap update, and preparation of scientific communication artifacts.

### Honest Checklist

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 1 | H₄/600-cell: KO-dim = 6 mod 8 | ✅ Confirmed | `proofs/trinity/KODimension.v` — sign triple (+,+,+) proved (`Qed`); off-diagonal J admitted as `PHYSICAL_AXIOM` |
| 2 | D₄/24-cell: KO-dim = 5 mod 8 | ✅ Confirmed (negative result) | `derivations/trinity_d4/trinity_d4_analysis.md` — explicit numeric computation gives (−,+,+) → KO-dim 5, **not SM-like** |
| 3 | η(2I) = −2 | ✅ Confirmed | `proofs/trinity/EtaInvariant.v` — `eta_poincare_nonzero`, `eta_poincare_negative`, `eta_poincare_magnitude` all `Qed` |
| 4 | η(2T) = −3/2 | ✅ Open (convention-dependent) | `derivations/eta_2t_2o/eta_table_analysis.md` — adopted from plumbing convention η = σ/4; Dedekind-sum cross-check gives different value under natural metric |
| 5 | η(2O) = −7/4 | ✅ Open (convention-dependent) | Same status as η(2T) |
| 6 | Spectral action Higgs: 132.88 GeV | ✅ Refuted | `derivations/higgs_spectral_action/higgs_analysis.md` — PDG 2024: 125.10 ± 0.14 GeV; **55.6σ discrepancy** |
| 7 | 1-loop Higgs correction | ⬜ OPEN | Wave 12.4 — can quantum effects bridge 132.88 → 125.10? |
| 8 | E₆/E₇ explicit D_P | ⬜ OPEN | Wave 12.5 — no positive results yet |
| 9 | All Admitted closed | ⬜ OPEN | **100 Admitted remain** in Coq (`proofs/trinity/*.v`) |
| 10 | Lean port complete | ⬜ OPEN | **6 `sorry` remain** in Lean 4 port (`derivations/lean_port/TrinityLean/`) |

### No-Go Theorems (with citations)

| Theorem | Claim | Status | Source |
|---------|-------|--------|--------|
| **NGT-1** | Cosmological parameters from H₄ formulas | **Refuted** | Wave 8.5; `derivations/no_go_analysis/no_go_theorems.md` — Λ off by 92 orders; Ω_b h² off by 754σ |
| **NGT-2** | σ-field from H₄ geometry | **Proved impossible** | Wave 5.3; `proofs/trinity/UnimodularityAndSigma.v` — `H4_degree2_is_constant_on_orbit` (Qed) |
| **NGT-3** | Chirality from 600-cell alone | **Proved impossible** | Wave 6; `proofs/trinity/ChiralityAnalysis.v` — antipodal symmetry forces vector-like spectrum |
| **NGT-4** | Mass hierarchy from 2I-equivariant D_F | **Proved impossible** | Wave 8.4; `proofs/trinity/DFSpectrum.v` — σ = 5.62 > 5σ from SM spectrum |
| **NGT-5** | D₄/24-cell as SM finite geometry | **Ruled out** | Wave 11.2; `derivations/trinity_d4/trinity_d4_analysis.md` — KO-dim 5 ≠ 6; triality does not yield 3 generations |

### Surviving Positive Results

1. **KO-dim = 6 mod 8 for H₄/600-cell** — structural compatibility with SM NCG (`KODimension.v`, Qed).
2. **η = −2 on S³/2I** — necessary condition for spectral chirality; APS balance verified (`EtaInvariant.v`, Qed).
3. **2I ⊂ SU(2) motivates ℍ ⊂ A_F** — algebraic fact, independent of physical claims (`QuaternionicLinearity.v`, Qed).
4. **25/25 catalog formulas verified numerically** — with honest R/S/NF tags (`validate_v4.py`, `Catalog42.v`).
5. **Machine-verified honesty framework** — 312 Qed theorems + 100 honest Admitted tags.
6. **Four rigorous no-go theorems** — mapping the boundaries of H₄-based unification.

### New Artifacts in Wave 12

| File | Description |
|------|-------------|
| `derivations/falsification/PREDICTIONS_REGISTRY.md` | Falsifiable predictions registry with traceability to source files |
| `derivations/falsification/SEMINAR_TALK_20MIN.md` | 20-minute seminar outline with speaker notes |
| `ROADMAP.md` (this section) | Updated honest checklist and open problems |

---

## Wave 13+ — Tentative Directions

1. **Complete Lean 4 port** — close remaining `sorry` in KODimension and QuaternionicLinearity.
2. **E₆/E₇ scouting** — explicit Dirac operators for E₆ and E₷ plumbing geometries (Wave 12.5 follow-up).
3. **1-loop Higgs computation** — numerical check whether 1-loop corrections can rescue tree-level 132.88 GeV (Wave 12.4 follow-up).
4. **arXiv preprint** — draft *"Trinity S³AI: Constructive Negative Results in H₄-Based Geometric Unification"*.
5. **DUNE 2028 watch** — maintain δ_CP = 65.66° registry until experimental decision.

---

*Wave 12 consolidated: 2026-05-22.*
