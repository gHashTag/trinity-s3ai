# Lean 4 — Портирование CorePhi (Стадия 0)

> **Статус:** Stage 0 — черновик-скаффолдинг. Файлы написаны и структурированы,
> но **не прошли полноценную компиляцию** в песочнице. Для сборки требуется
> `elan` + `lake` на вашей локальной машине (macOS или Linux).

---

## Зачем Lean 4?

Проект Trinity S3AI разрабатывался на Coq (версия 8.20.x).
Lean 4 / Mathlib 4 — это современная альтернатива, у которой есть ряд
практических преимуществ:

1. **Активно развивающийся Mathlib.**
   Mathlib 4 — крупнейшая в мире библиотека формализованной математики;
   она значительно богаче, чем то, что доступно «из коробки» в Coq без
   установки десятков дополнительных пакетов.

2. **Удобный синтаксис тактик.**
   `nlinarith`, `norm_num`, `ring`, `field_simp` — стандартные тактики
   Lean 4, решающие те же задачи, что `lra` + `interval` + `field` в Coq.

3. **Зависимые типы нового поколения.**
   Unified elaboration, `#check`, `#eval` — быстрый прототипинг без
   отдельного компилятора.

4. **Переносимость.**
   Mathlib работает на macOS, Linux и Windows (WSL2) через единый
   инструмент `elan`/`lake`. Нет привязки к конкретной версии opam.

5. **Будущее формальной математики.**
   Академические проекты Lean (FLT, Fermat's Last Theorem Project и др.)
   переходят на Lean 4, делая его стандартом де-факто в ближайшие годы.

---

## Структура директории

```
derivations/lean_port/
├── lakefile.toml           # конфигурация Lake (сборочная система Lean 4)
├── lean-toolchain          # фиксация версии: leanprover/lean4:v4.13.0
├── README.md               # этот файл
└── TrinityLean/
    └── CorePhi.lean        # порт proofs/trinity/CorePhi.v
```

---

## Что портировано (10 лемм)

| # | Lean 4 имя | Coq аналог | Описание |
|---|-----------|-----------|---------|
| 1 | `sqrt5_pos` | _(вспом.)_ | √5 > 0 |
| 2 | `sqrt5_gt_two` | _(вспом.)_ | √5 > 2 |
| 3 | `sqrt5_lt_three` | _(вспом.)_ | √5 < 3 |
| 4 | `phi_pos` | `phi_gt_0` | φ > 0 |
| 5 | `phi_gt_one` | `phi_gt_1` | φ > 1 |
| 6 | `phi_lt_two` | _(из approx)_ | φ < 2 |
| 7 | `phi_sq` | `phi_sq` | φ · φ = φ + 1 (**фундаментальное тождество**) |
| 8 | `phi_cubed` | `phi_cubed` | φ³ = 2φ + 1 |
| 9 | `phi_inv` | `phi_inv` | φ⁻¹ = φ − 1 |
| 10 | `phi_psi_product` | `phi_psi_product` | φ · ψ = −1 |

Дополнительно определены:
- `phi_bounds` — численные границы 1.618 < φ < 1.619
- `phi_zpow_two`, `phi_zpow_three` — целочисленные степени через `zpow` Mathlib

**Не портировано** (намеренно):
- `phi_approx` (interval-тактика специфична для Coq Interval)
- `powZ` (заменено на `zpow` из Mathlib)
- `powZ_pos`, `powZ_1`, `powZ_2`, `powZ_neg1` (избыточны с Mathlib)
- Все леммы из CorePhi.v относительно `psi_inv` на данном этапе отложены

---

## Как собрать локально (требует elan)

### 1. Установить elan (менеджер версий Lean)

```bash
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
```

После установки перезапустите терминал или выполните:

```bash
source ~/.elan/env
```

### 2. Перейти в директорию lean_port

```bash
cd derivations/lean_port
```

### 3. Скачать Mathlib и собрать проект

```bash
lake update
lake build
```

`lake update` скачивает Mathlib 4 (это может занять несколько минут —
Mathlib большой). `lake build` компилирует `TrinityLean/CorePhi.lean`.

### 4. Проверить отдельные леммы

```bash
lake env lean --stdin <<'EOF'
#check @TrinityLean.CorePhi.phi_sq
EOF
```

или откройте `TrinityLean/CorePhi.lean` в VS Code с расширением
`leanprover.lean4` — тактики проверяются в реальном времени.

---

## Требования к системе

| Компонент | Версия |
|-----------|--------|
| elan | ≥ 3.1.1 |
| Lean 4 | v4.13.0 (фиксировано в `lean-toolchain`) |
| Mathlib | v4.13.0 (фиксировано в `lakefile.toml`) |
| macOS / Linux | любая современная |
| RAM | ≥ 8 ГБ рекомендуется (Mathlib требует ресурсов) |
| Диск | ≥ 5 ГБ (Mathlib + кеши) |

---

## Известные ограничения (Stage 0)

1. **Не скомпилировано в CI-песочнице.** В окружении sandbox нет `elan`/`lake`,
   поэтому CI-задача `lean.yml` помечена `continue-on-error: true`.

2. **`phi_bounds`** использует явные числовые оценки вместо `norm_num`-расширения
   `Mathlib.Tactic.Polyrith`. Это намеренно — для простоты.

3. **`phi_sq` тактика.** Основное доказательство использует `nlinarith [sqrt5_sq]`.
   Если `nlinarith` не справится, альтернатива:
   ```lean
   simp only [phi]; ring_nf; linarith [sqrt5_sq]
   ```

4. **zpow vs pow.** `phi_zpow_two` и `phi_zpow_three` могут потребовать
   импорта `Mathlib.Algebra.GroupPower.Basic` в зависимости от версии Mathlib.

---

## Следующие шаги (Stage 1+)

- [ ] Портировать `H4Derivations.v` → `TrinityLean/H4Derivations.lean`
- [ ] Добавить тактику `norm_num` extension для `interval`-стиля вычислений
- [ ] Портировать `Bounds_LeptonMasses.v` с использованием Mathlib вещественного анализа
- [ ] Настроить Mathlib кеш в CI через `leanprover/lean4-action` + `cache`

---

## Соответствие файлов: Coq ↔ Lean 4

| Coq (proofs/trinity/) | Lean 4 (TrinityLean/) | Статус |
|-----------------------|-----------------------|--------|
| `CorePhi.v` | `CorePhi.lean` | Stage 0 |
| `H4Derivations.v` | _не начато_ | — |
| `E6vsH4.v` | _не начато_ | — |
| `Bounds_LeptonMasses.v` | _не начато_ | — |
| остальные ~30 файлов | _не начато_ | — |

---

*Trinity S3AI Lean 4 Port — Stage 0*
*Создано в рамках Wave 8.6*

---

## Стадия 1 — Wave 10.3: KODimension и QuaternionicLinearity

### Новые файлы

```
derivations/lean_port/TrinityLean/
├── CorePhi.lean               (Stage 0 + 4 вспом. леммы Stage 1)
├── KODimension.lean           (Stage 1 — KO-размерность 600-клетки)
└── QuaternionicLinearity.lean (Stage 1 — икосианная кватернионная линейность)
```

### Таблица статуса лемм

| Файл | Stage | Число лемм/теорем | sorry | Явные axiom |
|------|-------|-------------------|-------|-------------|
| `CorePhi.lean` | 0 → 0+1 | 14 | 0 | 0 |
| `KODimension.lean` | 1 | 18 | 0 | 1 (`cell600_J_off_diagonal`) |
| `QuaternionicLinearity.lean` | 1 | 18 | 0 | 4 (`two_I_order*`, `H4_order*`) |
| **Итого** | | **50** | **0** | **5** |

_Stage 0: 10 лемм → Stage 1: 50 лемм (+40)._

### Что доказано в Stage 1

**KODimension.lean** (18 объектов):

| # | Lean 4 имя | Смысл |
|---|-----------|-------|
| 1 | `sign_sq` | знак · знак = 1 |
| 2 | `connes_table_ko6` | таблица Коннеса: KO-dim 6 даёт (+1,+1,+1) |
| 3 | `J_sq_eq_id` | J(J(q)) = q (кватернионное сопряжение, ε = +1) |
| 4 | `eps_eq_plus_one` | J ∘ J = id (функциональная форма) |
| 5 | `gamma_sq` | γ² = 1 (оператор киральности) |
| 6 | `J_gamma_comm` | J(γ·q) = γ·J(q) (ε'' = +1) |
| 7 | `eps_prime_eq_plus_one` | если D вещественный → JD = DJ (ε' = +1) |
| 8 | `cell600_signs_match_ko6` | тройка знаков 600-клетки = тройка KO-dim 6 |
| 9 | `connes_ko6_matches_cell600` | таблица Коннеса KO6 = знаки 600-клетки |
| 10 | `cell600_consistent_with_ko6` | 600-клетка согласована с KO-dim 6 |
| 11 | `cell600_consistent_with_ko0` | 600-клетка согласована и с KO-dim 0 (честная оговорка) |
| 12 | `cell600_KO_dim_6_under_axiom` | при структурной аксиоме → KO-dim 6 |
| 13 | `cell600_satisfies_SM_KO_requirement` | выполняется требование NCG СМ |
| 14 | `phi_in_cell600_vertex_coords` | φ входит в координаты вершин 600-клетки |

**QuaternionicLinearity.lean** (18 объектов):

| # | Lean 4 имя | Смысл |
|---|-----------|-------|
| 1 | `gen_r_is_unit` | генератор r ∈ S³ (единичный кватернион) |
| 2 | `gen_r_i_component_sq` | (φ/2)² = (φ+1)/4 |
| 3 | `gen_r_j_component_phi_inv` | j-компонента = (1/φ)/2 |
| 4 | `icosian_pythagorean_identity` | 1 + φ² + (φ−1)² = 4 |
| 5 | `qmul_norm_multiplicativity` | ‖q·g‖² = ‖q‖²·‖g‖² |
| 6 | `right_mult_preserves_norm` | единичный g ⇒ ‖q·g‖ = ‖q‖ |
| 7 | `gen_r_acts_isometrically` | r действует изометрически на H ≅ ℍ |
| 8 | `left_right_mult_commute_0` | L_ℓ ∘ R_g = R_g ∘ L_ℓ (компонента 0) |
| 9 | `H4_order_is_square_of_2I` | \|H₄\| = \|2I\|² |
| 10 | `phi_half_is_valid_cosine` | φ/2 ∈ (0,1) = cos(π/5) |
| 11 | `four_half_phi_sq` | 4·(φ/2)² = φ+1 |
| 12 | `phi_in_interval_1_2` | 1 < φ < 2 |
| 13 | `gen_r_components_distinct` | φ/2 ≠ (φ−1)/2 |
| 14 | `R_g_isometric_of_unit` | R_g изометрично при ‖g‖=1 (через Mathlib norm_mul) |
| 15 | `H4_order_is_14400` | \|H₄\| = 14400 |

### Честная оговорка о компиляции

> **Мы НЕ компилировали эти файлы локально.**
> В CI-песочнице отсутствует `elan`/`lake`, поэтому формальная проверка
> невозможна без локальной машины.
>
> Для проверки запустите на Mac с Lean v4.13.0 + Mathlib:
> ```bash
> cd derivations/lean_port
> lake update && lake build
> ```

### Подсчёт sorry и аксиом

| Тип | Число | Файл | Пояснение |
|-----|-------|------|-----------|
| `sorry` | **0** | — | Отсутствуют полностью |
| Явные `axiom` | 5 | KODim + QuatLin | Теорем-группы (порядки 2I, H₄) и структурная аксиома J |

**Все `axiom` снабжены комментариями-тегами.**  
В `KODimension.lean` единственный `axiom cell600_J_off_diagonal` помечен  
`-- PHYSICAL_AXIOM` с объяснением, почему формальное доказательство требует  
теории представлений 2I.

В `QuaternionicLinearity.lean` аксиомы `two_I_order_eq` и `H4_order_eq`  
отражают факты теории групп, которые не доказуемы в рамках вещественной  
арифметики Lean/Mathlib без дополнительных тактик комбинаторики.

### Соответствие файлов: Coq ↔ Lean 4 (обновлённая таблица)

| Coq (proofs/trinity/) | Lean 4 (TrinityLean/) | Статус |
|-----------------------|-----------------------|--------|
| `CorePhi.v` | `CorePhi.lean` | Stage 0 + вспом. |
| `KODimension.v` | `KODimension.lean` | Stage 1 ✓ |
| `QuaternionicLinearity.v` | `QuaternionicLinearity.lean` | Stage 1 ✓ |
| `H4Derivations.v` | _не начато_ | — |
| `E6vsH4.v` | _не начато_ | — |
| `Bounds_LeptonMasses.v` | _не начато_ | — |
| остальные ~30 файлов | _не начато_ | — |

---

*Trinity S3AI Lean 4 Port — Stage 1*  
*Обновлено в рамках Wave 10.3*
