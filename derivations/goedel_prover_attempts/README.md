# Wave 10.6: Попытки закрытия Admitted (Goedel-Prover / ручная тактика)

## Статус: ПОПЫТКИ, ничего не применено к main

Wave 10.6 не имел доступа к реальному ML-доказателю Goedel-Prover-V2. Все попытки делались субагентом Sonnet через ручные тактики Coq (`lia`, `lra`, `nra`, `field`, `interval`, `nlinarith`, infinite descent).

## Текущее число Admitted

27 Admitted в репозитории (без изменений после Wave 10.6).

| Тег | Кол-во | Прокомментировано |
|---|---|---|
| LIBRARY_GAP | 13 | Не закрыты — нужна полноценная библиотека (Mathcomp / coq-interval extras) |
| MATH_TODO | ~6 | Не закрыты — требуют KK-теории, η-сходимости, дискретного D_P |
| PHYSICAL_AXIOM | 4 | НЕ закрываются по принципу (внешние входы) |
| NUMERICAL_FIT | ~2 | Не закрыты — interval-тактика дала overflow в коэффициентах |

## Какие тактики работали в /tmp/ (но требуют дополнительной работы для интеграции)

| # | Файл | Теорема | Тактика | Статус |
|---|---|---|---|---|
| 1 | OptimizerInvariants.v | `ttt_lr_is_phi_inv_cube_scaled` | `field. apply Rgt_not_eq. apply phi_gt_0.` | работает в /tmp, не применено |
| 2 | A4Conversion.v | `conversion_exact` | cross-mul + `nlinarith [Hs]` | частично — нужен helper `div_eq` |
| 3 | E6vsH4.v | `phi_irrational` | infinite descent (~50 строк) | работает локально |
| 4 | Bounds_Mixing.v | `N04_within_experimental_range` | `interval with (i_prec 100)` | работает локально |
| 5 | Catalog42.v | `Q02_is_m_s_over_m_u` | `interval with (i_prec 150)` | работает локально |
| 6 | H4Lagrangian.v | `L01_lagrangian_order_of_magnitude` | `interval` | работает локально |
| 7 | Koide.v | `Koide_correct_forms_equal` | `sqrt_1_div_eq + reflexivity` | работает локально |
| 8 | test_scratch.v | (3 теоремы) | `sqrt_sq + field` | работает локально |

**Потенциал закрытия: 8 Admitted → 27 → 19** (если перенести аккуратно с компиляцией всего проекта).

## Найденные математические ошибки (НЕ закрывать — теоремы ложны)

| # | Файл | Теорема | Реальная погрешность | Действие |
|---|---|---|---|---|
| 22 | (различные) | `phi_squared_nat` | 1618² = 2 617 924, а не 2 618 724 | удалить или Refute |
| 4 | (Bounds_Mixing) | `N03_is_sin2_theta_23` | 0.42% > V_bound 0.1% | заменить на refutation |
| 5 | (Catalog42) | `C01_is_V_us` | 0.96% > V_bound 0.1% | заменить на refutation |

## Стратегия Wave 11

1. Применить 8 рабочих тактик из таблицы выше — должно закрыть LIBRARY_GAP с 13 до ~5
2. Превратить 3 найденные ложные теоремы в `Theorem X_refuted` (как `alpha_from_H4_refuted` в Wave 3)
3. Реальный Goedel-Prover-V2 / lean-proverbot когда будет доступен из коробки

## Честно

Без ML-доказателя или существенно более длинных попыток (несколько часов на каждую Admitted), 13 LIBRARY_GAP останутся открытыми. Это не блокер для научной публикации — все Admitted честно тегированы.
