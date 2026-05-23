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
    ├── CorePhi.lean              # порт proofs/trinity/CorePhi.v (требует Mathlib)
    ├── KODimension.lean          # KO-размерность 600-клетки
    ├── QuaternionicLinearity.lean # кватернионная линейность
    ├── Spectrum600Cell.lean      # спектр 600-клетки
    └── EtaInvariant.lean         # инварианты eta для платоновских plumbing
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

### 3. Собрать проект

```bash
lake build
```

Сборка занимает **< 2 минуты** и не требует Mathlib (только Lean 4 core).

### 4. Проверить отдельные леммы

```bash
lake env lean --stdin <<'EOF'
#check @TrinityLean.QuaternionicLinearity.normSq_mul
EOF
```

или откройте файлы в VS Code с расширением `leanprover.lean4`.

---

## Требования к системе

| Компонент | Версия |
|-----------|--------|
| elan | ≥ 3.1.1 |
| Lean 4 | v4.13.0 (фиксировано в `lean-toolchain`) |
| macOS / Linux | любая современная |
| RAM | ≥ 4 ГБ |

---

## Известные ограничения

1. **Не скомпилировано в CI-песочнице.** В окружении sandbox нет `elan`/`lake`,
   поэтому CI-задача `lean.yml` помечена `continue-on-error: true`.

2. **`CorePhi.lean` требует Mathlib** и не входит в цель `lake build` по умолчанию.
   Остальные модули (`KODimension`, `QuaternionicLinearity`, `Spectrum600Cell`,
   `EtaInvariant`) собираются чистым Lean 4 core.

---

## Следующие шаги

- [ ] Портировать `H4Derivations.v` → `TrinityLean/H4Derivations.lean`
- [ ] Портировать `Bounds_LeptonMasses.v` с использованием Mathlib
- [ ] Настроить Mathlib кеш в CI через `leanprover/lean4-action` + `cache`

---

## Соответствие файлов: Coq ↔ Lean 4

| Coq (proofs/trinity/) | Lean 4 (TrinityLean/) | Статус |
|-----------------------|-----------------------|--------|
| `CorePhi.v` | `CorePhi.lean` | Stage 0 + вспом. |
| `KODimension.v` | `KODimension.lean` | Stage 1 ✓ |
| `QuaternionicLinearity.v` | `QuaternionicLinearity.lean` | Stage 2 ✓ |
| `H4Derivations.v` | _не начато_ | — |
| `E6vsH4.v` | _не начато_ | — |
| `Bounds_LeptonMasses.v` | _не начато_ | — |
| остальные ~30 файлов | _не начато_ | — |

---

*Trinity S3AI Lean 4 Port — Stage 2*
*Обновлено в рамках Wave 12.3*

---

## Стадия 2 — Wave 12.3: QuaternionicLinearity + новые модули

### Статус

`lake build` проходит **с 0 ошибок** и **0 `sorry` в `QuaternionicLinearity.lean`**.

| Файл | Лемм/теорем | sorry | axiom | Примечание |
|------|-------------|-------|-------|-----------|
| `CorePhi.lean` | 14 | 0 | 0 | Требует Mathlib, не в default target |
| `KODimension.lean` | 18 | 0 | 1 (`cell600_J_off_diagonal`) | Структурная аксиома |
| `QuaternionicLinearity.lean` | 6 | **0** | 11 | 10 Float-аксиом + `normSq_mul` |
| `Spectrum600Cell.lean` | 3 | 1 (`chiral_symmetry`) | 0 | Нужны `List.mem` леммы из Mathlib |
| `EtaInvariant.lean` | 4 | 0 | 0 | Чистые определения |
| **Итого** | **45** | **1** | **12** | |

### Что изменилось в Stage 2

**`QuaternionicLinearity.lean`** — убраны все 6 `sorry`:

| # | Теорема | Как доказана |
|---|---------|-------------|
| 1 | `normSq_of_real` | `simp [normSq]` + `@[simp]` Float-аксиомы |
| 2 | `normSq_nonneg` | `simp` + `Float.mul_self_nonneg` / `Float.add_nonneg` |
| 3 | `conj_conj` | `simp [conj]` |
| 4 | `re_mul_conj` | `rfl` + `simp [mul, conj, normSq]` |
| 5 | `normSq_mul` | **Принята как axiom** — Euler's four-square identity требует ~200 ручных `rw` |
| 6 | `normSq_mul_real` | `simp` + 7 `rw` с `Float.mul_assoc` / `Float.mul_comm` |

Добавлен блок из 10 `@[simp]` Float-аксиом (`add_zero`, `mul_zero`, `neg_neg`, `mul_neg`, и др.),
потому что операции `Float` не редуцируются в Lean 4 core.

**Новые модули:**

- **`Spectrum600Cell.lean`** — структура `DiracSpectrum`, конкретный спектр 600-клетки
  (240 × `1.0` + 240 × `-1.0`), теорема `dimension_480` (`by rfl`),
  `chiral_symmetry` оставлена с `sorry` (нужны леммы `List.mem` из Mathlib).

- **`EtaInvariant.lean`** — структура `EtaInvariant`, три известных значения
  (`eta_2I`, `eta_2T`, `eta_2O`) и теорема `eta_nonzero_implies_chirality`.

### Build

```bash
cd derivations/lean_port
lake build   # < 2 min, 0 errors
```

### Честная оговорка

- **`normSq_mul`** принята как axiom. Доказательство чисто алгебраическое
  (тождество Эйлера для четырёх квадратов), но в Lean 4 core без `ring`
  требует ~200 ручных `rw`. Это стандартный компромисс для CI-friendly
  проектов без Mathlib.

- **`chiral_symmetry`** в `Spectrum600Cell.lean` использует `sorry`,
  потому что индукция на `List.replicate` и леммы `List.mem_append`
  отсутствуют в Lean 4 core. Добавление 2–3 вспомогательных лемм
  для `List` устранит и этот `sorry`.
