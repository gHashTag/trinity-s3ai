# admitted_log.md — Реестр всех Admitted в Trinity S3AI

**Дата создания:** Wave 4.2  
**Версия:** Trinity S3AI v3.5  
**Всего Admitted:** 25  

## Таксономия

| Тег | Смысл | Кол-во |
|-----|-------|--------|
| `[PHYSICAL_AXIOM]` | Физическое допущение — граничное условие РГ, масштаб масс, нормировка | 4 |
| `[NUMERICAL_FIT]` | Формула найдена подбором по данным, вывода нет | 2 |
| `[MATH_TODO]` | Математически доказуемо, но вывод ещё не написан | 6 |
| `[LIBRARY_GAP]` | Ограничение coq-interval / stdlib Rocq 9.1.1 | 13 |

---

## Полный реестр

| № | Файл | Строка | Теорема/Лемма | Тег | Обоснование | Закрываемость |
|---|------|--------|---------------|-----|-------------|---------------|
| 1 | `A4Conversion.v` | 195 | `conversion_exact` | `[MATH_TODO]` | Алгебраическое тождество: рационализация знаменателя `(448 + 192√5) / (8 + 3√5)` умножением на сопряжённое. Тактики `field`/`ring` не справляются с вложенными `sqrt` в Rocq 9.1.1. | **Высокая** — ручная запись через `sqrt5_sq` + `ring_simplify` |
| 2 | `Bounds_Mixing.v` | 89 | `N04_within_experimental_range` | `[LIBRARY_GAP]` | Численно истинно (65.66° vs. 65.5° ± 4°). `interval` не раскрывает `rad_to_deg` с PI корректно без предварительного `unfold` + оценки PI по интервалу. | **Высокая** — добавить `unfold N04_formula_deg, rad_to_deg, N04_formula_rad, phi; interval with (i_prec 100)` |
| 3 | `Catalog42.v` | 318 | `Q02_is_m_s_over_m_u` | `[LIBRARY_GAP]` | Было `Qed`. `Q02_V = 12 + φ³·e²`, отношение `m_s/m_u ≈ 43.2` — `interval` не укладывается в лимит точности при текущем `i_prec`. | **Высокая** — повысить `i_prec` до 150+ и добавить `simpl` перед `interval` |
| 4 | `Catalog42.v` | 337 | `N03_is_sin2_theta_23` | `[LIBRARY_GAP]` | Было `Qed`. `N03_V = π²/18` — чистая PI-формула, `interval` не раскрывает `powZ` до вызова. | **Высокая** — добавить `simpl` перед `interval`, как в других `N0x`-теоремах |
| 5 | `Catalog42.v` | 376 | `C01_is_V_us` | `[LIBRARY_GAP]` | Было `Qed`. `C01_V = 2φ³e²/(9π³)` — тройное транцендентное произведение, `interval` требует `simpl` для `powZ`. | **Высокая** — `simpl; interval with (i_prec 200)` |
| 6 | `E6vsH4.v` | 107 | `sqrt_5_not_rational` | `[MATH_TODO]` | Стандартный результат теории чисел (бесконечный спуск / единственность разложения). Отсутствует в stdlib Coq; требует ручного доказательства или внешней библиотеки. | **Средняя** — написать вручную через `Zpow_pos` + модульная арифметика |
| 7 | `E6vsH4.v` | 115 | `phi_irrational` | `[MATH_TODO]` | Прямое следствие `sqrt_5_not_rational`; `φ = (1+√5)/2` нерационально стандартно, но `IZR`-арифметика не автоматизирована. | **Высокая** — закроется вместе с № 6 |
| 8 | `E6vsH4.v` | 130 | `E6_no_phi` | `[MATH_TODO]` | Структурное следствие `phi_irrational`: любое рациональное `x ≠ φ`. Контрапозитивный вывод с `existential` — автоматика не справляется. | **Высокая** — закроется вместе с № 7 |
| 9 | `E6vsH4.v` | 194 | `cos_pi_5_quadratic` | `[MATH_TODO]` | Два `admit` внутри: (а) тождество `sin²→1-cos²` в произведении (ring_simplify не применяется), (б) итоговое уравнение `4c²-2c-1=0` через `lra` по гипотезам с cos. | **Средняя** — `rewrite Hsin; ring` для (а), `lra` для (б) после (а) |
| 10 | `GaugeOrigins.v` | 363 | `G01_from_GUT_running` | `[PHYSICAL_AXIOM]` | Требует (1) аксиому `gU2inv_window` из `RGRunning.v` (граничное условие ОТЭ), (2) фактор нормировки гиперзаряда `√(5/3)` из GUT-вложения. Оба — физические допущения, не выводимые из геометрии H4. | **Низкая** — только после импорта `RGRunning` и доработки нормировки |
| 11 | `H4GaugeEmbedding.v` | 74 | `phi_irrational_over_Q` | `[LIBRARY_GAP]` | Стандартное доказательство бесконечным спуском на `√5`; `field`/`IZR`-тактики не работают с конкретными знаменателями в Rocq 9.1.1. | **Средняя** — переиспользовать доказательство из `E6vsH4.v` после закрытия № 6 |
| 12 | `H4Lagrangian.v` | 151 | `L01_lagrangian_order_of_magnitude` | `[LIBRARY_GAP]` | `L01 ≈ 0.017` (между 0 и 1); `interval` не справляется с `1e16/1.22e19` (литералы с плавающей запятой в R) совместно с `exp 1 / PI`. | **Высокая** — разбить на лемму о знаке и оценку числителя/знаменателя |
| 13 | `H4Lagrangian.v` | 188 | `Koide_H4_test` | `[LIBRARY_GAP]` | `Rabs(Koide_H4(1,239,549) - 2/3)/(2/3) < 0.3` — `interval` не раскрывает `Koide_H4` с `sqrt 1 + sqrt 239 + sqrt 549` автоматически. | **Высокая** — `unfold Koide_H4; simpl; interval with (i_prec 150)` |
| 14 | `HiggsOrigins.v` | 475 | `H03_h_half_structural` | `[MATH_TODO]` | Конкретная алгебраическая формула `h/2 = (d3·d4)/(d3+d4-d3²/d4)` некорректна (числа не совпадают). Нужно найти правильное тождество или заменить теорему. | **Низкая** — требует пересмотра формулировки теоремы |
| 15 | `Koide.v` | 186 | `Koide_correct_forms_equal` | `[LIBRARY_GAP]` | `field`/`ring` не работают с `sqrt`-выражениями с конкретными знаменателями в Rocq 9.1.1. Оба выражения алгебраически эквивалентны. | **Высокая** — `field_simplify [sqrt 5 * sqrt 5 = 5]` + `ring` |
| 16 | `LeptonOrigins.v` | 505 | `H4_determines_L01` | `[NUMERICAL_FIT]` | **Честно:** `L01 = 239·e/π` найдено численным поиском, а не выводом из геометрии E8/H4. Целое 239 = \|E8 roots\| - 1 имеет групповую интерпретацию, но трансцендентальный множитель `e/π` необоснован. Конструктивная функция `f` не предоставлена. | **Очень низкая** — требует физического механизма (спектральное действие на 600-клетке?) |
| 17 | `NeutrinoOrigins.v` | 401 | `seesaw_scale_from_v31` | `[PHYSICAL_AXIOM]` | Правосторонняя нейтринная масса Майораны `M_R` не определяется геометрией H4. Формула ножниц `m_лёгкое · M_R = v_EW²` требует отождествления `v_EW` с H4-производимой ВОО — физическое допущение. | **Низкая** — требует derivation of EW VEV from H4 |
| 18 | `NeutrinoOrigins.v` | 414 | `nu_absolute_scale_gap` | `[NUMERICAL_FIT]` | **Честно:** множитель `10⁻⁵` eV² в `v21` вставлен вручную под эксперимент. Trinity не предсказывает абсолютный масштаб масс нейтрино из теории H4. | **Очень низкая** — требует вывода масштаба ЭС/ножниц |
| 19 | `OptimizerInvariants.v` | 96 | `ttt_lr_is_phi_inv_cube_scaled` | `[LIBRARY_GAP]` | `field_simplify` не сводит `phi_inv_cube = 1/φ³` к `reflexivity` — условие ненулевости `φ³` требует отдельной леммы о положительности, не пробрасываемой автоматически. | **Высокая** — `assert (phi3_ne : phi^3 <> 0) by ...; field [phi3_ne]` |
| 20 | `RGRunning.v` | 206 | `alpha_from_H4` | `[PHYSICAL_AXIOM]` | `alpha_inv_at_mZ` суммирует GUT-нормированные константы связи (~0.1 каждая), а не физическую `1/α(m_Z) ≈ 128`. Требует: (1) нормировочный фактор `√(5/3)` из GUT-вложения, (2) однопетлевое РГ-бегание от `Λ_H4` до `m_Z`. | **Низкая** — требует переопределения `alpha_inv_at_mZ` |
| 21 | `RGRunning.v` | 231 | `alpha_s_from_H4` | `[PHYSICAL_AXIOM]` | `α_s(m_Z) ~ (√5-2)/2 ≈ 0.118` требует двухпетлевого бегания + пороговых поправок при массе топ-кварка. Всё это — физические входные данные (коэффициенты бета-функции, `m_top`), не выводимые из H4. | **Низкая** — требует включения двухпетлевых коэффициентов |
| 22 | `UniquenessStructural.v` | 313 | `phi_squared_nat` | `[LIBRARY_GAP]` | `1618 * 1618 = 2618724` — чистая целочисленная арифметика. `vm_compute`/`native_compute` падают с segfault на больших nat-литералах в Rocq 9.1.1. | **Высокая** — использовать `lia` или заменить `nat` на `Z` |
| 23 | `test_scratch.v` | 64 | `VEV_corrected_matches_SM` | `[LIBRARY_GAP]` | `v_corrected = sqrt(v_SM²) = v_SM` требует `sqrt_sq` + `v_SM ≥ 0`; цепочка раскрытий `mu_sq`/`lambda` не автоматизирована. | **Высокая** — `unfold v_corrected, mu_sq_corrected, lambda_corrected; rewrite sqrt_sq; ring` |
| 24 | `test_scratch.v` | 75 | `m_H_corrected_matches_Trinity` | `[LIBRARY_GAP]` | Сводится к `sqrt(m_H_Trinity²) = m_H_Trinity`; нужна `sqrt_sq` + `m_H_Trinity > 0`. Автоматика не связывает цепочку раскрытий. | **Высокая** — аналогично № 23 |
| 25 | `test_scratch.v` | 85 | `Higgs_mass_from_curvature` | `[LIBRARY_GAP]` | `sqrt(2·μ²) = m_H_Trinity`; после раскрытия сводится к `sqrt(m_H_Trinity²) = m_H_Trinity` — та же проблема `sqrt_sq`. | **Высокая** — аналогично № 23, 24 |

---

## Сводка по тегам

| Тег | Кол-во | Теоремы |
|-----|--------|---------|
| `[PHYSICAL_AXIOM]` | 4 | `G01_from_GUT_running`, `seesaw_scale_from_v31`, `alpha_from_H4`, `alpha_s_from_H4` |
| `[NUMERICAL_FIT]` | 2 | `H4_determines_L01`, `nu_absolute_scale_gap` |
| `[MATH_TODO]` | 6 | `conversion_exact`, `sqrt_5_not_rational`, `phi_irrational`, `E6_no_phi`, `cos_pi_5_quadratic` (×2), `H03_h_half_structural` |
| `[LIBRARY_GAP]` | 13 | `N04_within_experimental_range`, `Q02_is_m_s_over_m_u`, `N03_is_sin2_theta_23`, `C01_is_V_us`, `phi_irrational_over_Q`, `L01_lagrangian_order_of_magnitude`, `Koide_H4_test`, `Koide_correct_forms_equal`, `ttt_lr_is_phi_inv_cube_scaled`, `phi_squared_nat`, `VEV_corrected_matches_SM`, `m_H_corrected_matches_Trinity`, `Higgs_mass_from_curvature` |

---

## Приоритеты закрытия

### Высокий приоритет (закрываемы за 1–2 часа)
- №№ 2–5: Catalog42 + Bounds_Mixing — добавить `simpl; interval with (i_prec 150+)`
- №№ 22–25: UniquenessStructural + test_scratch — `lia` / `sqrt_sq` + `ring`
- № 19: OptimizerInvariants — добавить леммы ненулевости
- № 15: Koide — `field_simplify [sqrt5_sq]`
- № 13: H4Lagrangian Koide_test — `unfold; simpl; interval`

### Средний приоритет (требует ручных доказательств)
- №№ 6–9: E6vsH4 — написать доказательство иррациональности √5 вручную
- № 11: H4GaugeEmbedding — переиспользовать после E6vsH4
- № 1: A4Conversion — ручная рационализация через кольцевые леммы
- № 12: H4Lagrangian L01 — разбить на оценки

### Низкий приоритет (требует физического/концептуального прогресса)
- №№ 10, 20, 21: RGRunning/GaugeOrigins — переопределение `alpha_inv_at_mZ`
- №№ 16, 18: NUMERICAL_FIT — нужна физическая деривация
- № 17: seesaw — нужен вывод ВОО из H4
- № 14: HiggsOrigins — нужно исправить формулировку теоремы

---

*Документ создан автоматически в рамках Wave 4.2. Все теги проверены по контексту файлов.*
