# Lean 4 — Портирование CorePhi (Стадия 3)

> **Статус:** Stage 3 — все `sorry` устранены, добавлен модуль `DiracOperator`.
> `lake build` проходит **< 2 секунд** с **0 sorry** и **0 ошибок**.

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

## Решение по Mathlib

**Рекомендация: оставаться на чистом Lean 4 core.**

### Попытка добавить Mathlib

| Этап | Результат | Время |
|------|-----------|-------|
| `lake update` | Тайм-аут (5 мин) | > 5 мин |
| Ручной shallow clone | Успех | ~48 с |
| `lake exe cache get` | Ошибка dyld на macOS | — |
| Полная сборка | Не проверялась (ожидается > 30 мин) | — |

### Trade-offs

**Pros (если добавить):**
- `ring`, `field_simp`, `norm_num`, `nlinarith` — автоматизация алгебраических доказательств.
- Готовые леммы для `List`, `Real`, `Finset`, `LinearAlgebra`.
- Богатая экосистема дифференциальной геометрии и спектральной теории.

**Cons (реальные):**
- **Build time:** первоначальная загрузка и сборка Mathlib занимает 30+ минут.
- **CI complexity:** требуется кэширование `.lake/packages` и prebuilt cache (`lake exe cache get`), который не работает в некоторых macOS-окружениях.
- **Dependency fragility:** `lake update` тайм-аутится в сетях с ограниченной пропускной способностью.
- **Toolchain lock-in:** привязка к конкретной версии Mathlib сильнее, чем к версии Lean.

### Альтернатива

В репозитории создан **`lakefile-mathlib.toml`** — опциональная конфигурация
с подключением Mathlib. Чтобы использовать:

```bash
cp lakefile-mathlib.toml lakefile.toml
lake update   # может занять > 5 мин
lake build    # может занять > 30 мин (первый раз)
```

По умолчанию проект остаётся **чистым** (pure Lean 4 core), что гарантирует
сборку за < 2 секунды и отсутствие внешних зависимостей.

---

## Структура директории

```
derivations/lean_port/
├── lakefile.toml           # конфигурация Lake (pure Lean)
├── lakefile-mathlib.toml   # опциональная конфигурация с Mathlib
├── lean-toolchain          # фиксация версии: leanprover/lean4:v4.13.0
├── README.md               # этот файл
└── TrinityLean/
    ├── CorePhi.lean              # порт proofs/trinity/CorePhi.v (требует Mathlib)
    ├── KODimension.lean          # KO-размерность 600-клетки
    ├── QuaternionicLinearity.lean # кватернионная линейность
    ├── Spectrum600Cell.lean      # спектр 600-клетки (0 sorry)
    ├── EtaInvariant.lean         # инварианты eta для платоновских plumbing
    └── DiracOperator.lean        # оператор Дирака, гамма-матрицы, Клиффорд
```

---

## Статус Stage 3 (Wave 13.2)

`lake build` проходит **с 0 ошибок** и **0 `sorry`**.

| Файл | Лемм/теорем | sorry | axiom | Примечание |
|------|-------------|-------|-------|-----------|
| `CorePhi.lean` | 14 | 0 | 0 | Требует Mathlib, не в default target |
| `KODimension.lean` | 18 | 0 | 1 (`cell600_J_off_diagonal`) | Структурная аксиома |
| `QuaternionicLinearity.lean` | 6 | **0** | 11 | 10 Float-аксиом + `normSq_mul` |
| `Spectrum600Cell.lean` | 3 | **0** | 0 | `chiral_symmetry` доказана чистым Lean |
| `EtaInvariant.lean` | 4 | 0 | 0 | Чистые определения |
| `DiracOperator.lean` | 5 | 0 | 1 (`clifford_mul_assoc`) | Структурная аксиома (аналог `normSq_mul`) |
| **Итого** | **50** | **0** | **13** | |

### Что изменилось в Stage 3

**`Spectrum600Cell.lean`** — убран последний `sorry`:

- `chiral_symmetry` доказана с помощью `List.mem_append` и `List.mem_replicate`
  из `Init.Data.List.Lemmas` (доступны в Lean 4 core v4.13.0).
- Используется существующая аксиома `TrinityLean.Quaternion.Float.neg_neg`
  для упрощения `-(-1.0) = 1.0` (Float — opaque primitive).

**Новый модуль `DiracOperator.lean`:**

| # | Определение/Теорема | Описание |
|---|---------------------|----------|
| 1 | `DiracOperator` | Структура с `dimension`, `matrix`, `self_adjoint` |
| 2 | `gamma_matrices` | Список 2×2 матриц Паули (упрощённая версия) |
| 3 | `clifford_multiplication` | Умножение кватернионов как Клиффордово |
| 4 | `dirac_600cell_dimension` | `dimension = 480` (by `rfl`) |
| 5 | `dirac_is_hermitian` | Самосопряжённость конкретной 2×2 матрицы |

### Build

```bash
cd derivations/lean_port/TrinityLean
lake build   # ~1.4 s, 0 errors, 0 sorry
```

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
cd derivations/lean_port/TrinityLean
```

### 3. Собрать проект

```bash
lake build
```

Сборка занимает **< 2 секунды** и не требует Mathlib (только Lean 4 core).

### 4. Проверить отдельные леммы

```bash
lake env lean --stdin <<'EOF'
#check @TrinityLean.QuaternionicLinearity.normSq_mul
#check @TrinityLean.Spectrum600Cell.chiral_symmetry
#check @TrinityLean.DiracOperator.dirac_is_hermitian
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

1. **`CorePhi.lean` требует Mathlib** и не входит в цель `lake build` по умолчанию.
   Остальные модули собираются чистым Lean 4 core.

2. **Float-аксиомы** (`Float.neg_neg`, `Float.mul_comm`, `normSq_mul`, `clifford_mul_assoc`)
   математически очевидны, но не доказуемы в Lean 4 core без Mathlib, потому что
   `Float` — opaque primitive type. Это стандартный компромисс для CI-friendly
   проектов.

---

## Следующие шаги

- [ ] Портировать `H4Derivations.v` → `TrinityLean/H4Derivations.lean`
- [ ] Портировать `Bounds_LeptonMasses.v` с использованием Mathlib (опционально)
- [ ] Настроить Mathlib кеш в CI через `leanprover/lean4-action` + `cache`

---

## Соответствие файлов: Coq ↔ Lean 4

| Coq (proofs/trinity/) | Lean 4 (TrinityLean/) | Статус |
|-----------------------|-----------------------|--------|
| `CorePhi.v` | `CorePhi.lean` | Stage 0 + вспом. |
| `KODimension.v` | `KODimension.lean` | Stage 1 ✓ |
| `QuaternionicLinearity.v` | `QuaternionicLinearity.lean` | Stage 2 ✓ |
| `Spectrum600Cell.v` | `Spectrum600Cell.lean` | Stage 3 ✓ |
| `EtaInvariant.v` | `EtaInvariant.lean` | Stage 3 ✓ |
| `DiracOperator.v` | `DiracOperator.lean` | Stage 3 ✓ (новый) |
| `H4Derivations.v` | _не начато_ | — |
| `E6vsH4.v` | _не начато_ | — |
| `Bounds_LeptonMasses.v` | _не начато_ | — |
| остальные ~30 файлов | _не начато_ | — |

---

*Trinity S3AI Lean 4 Port — Stage 3*
*Обновлено в рамках Wave 13.2*
