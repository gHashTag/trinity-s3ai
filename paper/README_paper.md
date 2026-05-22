# README: Статья Trinity-s3ai для arXiv (Wave 10.1)

**Файл статьи:** `wave10_paper.tex`  
**Библиография:** `wave10_paper.bib`  
**Статус:** Черновик, готов к компиляции и проверке  
**Дата подготовки:** Июнь 2026  
**Принцип:** «Не врать!! Честным будь!»

---

## 1. Описание статьи

**Заголовок:**  
*Trinity-s3ai: A Constructive Negative Result on H4-Based Standard Model Unification*  
*(Подзаголовок: Four No-Go Theorems for NCG Approaches Founded on the 600-Cell)*

**Авторы:** `[Anonymous, gHashTag]` — заполнить перед отправкой.

**Аннотация (250 слов):** Представлен в секции `abstract` файла `wave10_paper.tex`.  
Ключевой тезис: H4/600-клетка в текущей формулировке **не может** вывести параметры  
Стандартной модели — четыре теоремы о невозможности (NGT-1–4) доказывают это.  
Шесть позитивных структурных результатов выживают.

---

## 2. Как скомпилировать

### 2.1 Требования

- **TeX-дистрибутив:** TeX Live 2023 или MiKTeX 24 (полная установка)
- **Компилятор:** `pdflatex` или `lualatex` (рекомендуется `pdflatex`)
- **Обработчик библиографии:** `biber` (НЕ `bibtex` — используется `biblatex`)
- **Основные пакеты:** amsmath, amssymb, hyperref, biblatex, listings, booktabs,
  longtable, lmodern, microtype, geometry, xcolor, caption

### 2.2 Команды компиляции

Выполнять строго в указанном порядке:

```bash
cd /home/user/workspace/trinity-s3ai/paper

# Шаг 1: первый проход pdflatex (создаёт .aux)
pdflatex wave10_paper.tex

# Шаг 2: biber обрабатывает библиографию
biber wave10_paper

# Шаг 3: второй проход pdflatex (вставляет ссылки)
pdflatex wave10_paper.tex

# Шаг 4: третий проход pdflatex (окончательное оглавление)
pdflatex wave10_paper.tex
```

### 2.3 Один скрипт (bash)

```bash
#!/bin/bash
set -e
cd "$(dirname "$0")"  # перейти в директорию paper/
NAME="wave10_paper"
pdflatex "$NAME.tex"
biber "$NAME"
pdflatex "$NAME.tex"
pdflatex "$NAME.tex"
echo "Done: $NAME.pdf"
```

### 2.4 Makefile (опционально)

```makefile
NAME = wave10_paper
.PHONY: all clean

all: $(NAME).pdf

$(NAME).pdf: $(NAME).tex $(NAME).bib
	pdflatex $(NAME)
	biber $(NAME)
	pdflatex $(NAME)
	pdflatex $(NAME)

clean:
	rm -f *.aux *.bbl *.blg *.bcf *.log *.out *.run.xml *.toc *.lof *.lot
```

### 2.5 Проверка синтаксиса без LaTeX

```bash
# Проверка несбалансированных фигурных скобок
python3 -c "
content = open('wave10_paper.tex').read()
d = 0
for i, ch in enumerate(content):
    if ch == '{': d += 1
    elif ch == '}': d -= 1
    if d < 0:
        print(f'Unmatched }} at position {i}'); break
print(f'Final depth: {d}')
"
```

Ожидаемый результат: `Final depth: 0`

---

## 3. Статус отправки на arXiv

**Текущий статус:** ❌ Ещё НЕ отправлено.

Необходимые шаги до отправки:

- [ ] Заполнить поле автора (заменить `[Anonymous, gHashTag]`)
- [ ] Добавить ORCID, если есть
- [ ] Скомпилировать PDF и проверить форматирование
- [ ] Проверить все ссылки в библиографии (DOI активны)
- [ ] Запросить эндорсмент (см. раздел 5)
- [ ] Написать письмо с объяснением содержания (для рецензента arXiv)

---

## 4. Категории arXiv

**Первичная категория:** `hep-th`  
Обоснование: статья о теориях физики высоких энергий, некоммутативной геометрии,  
операторе Дирака, попытке унификации Стандартной модели.

**Вторичные категории:**
- `math-ph` — математическая физика: теоремы о KO-размерности, η-инвариант, группы Кокстера
- `cs.LO` — логика в информатике: формализация Coq, ~730 Qed, Lean 4 скаффолд

**Как указать при отправке:**  
На шаге "Subject Class" в arXiv submission interface:
```
Primary:   hep-th
Secondary: math-ph cs.LO
```

---

## 5. Требования к эндорсменту

arXiv требует **эндорсмент** для первой отправки в категорию `hep-th`.

### 5.1 Кто может эндорсировать

Любой действующий arXiv-автор с ≥ 3 публикациями в `hep-th` за последние 5 лет.

### 5.2 Как запросить

1. Зарегистрироваться на https://arxiv.org
2. Попытаться отправить статью — система попросит указать эндорсера
3. Написать эндорсеру письмо (образец ниже)

### 5.3 Образец письма эндорсеру (английский)

```
Subject: arXiv endorsement request for hep-th submission

Dear Professor [Name],

I am writing to request arXiv endorsement for a submission to hep-th.

The paper, "Trinity-s3ai: A Constructive Negative Result on H4-Based
Standard Model Unification," presents four machine-verified no-go theorems
showing that the H4 Coxeter group (600-cell symmetry group) cannot serve as
the geometric foundation for deriving Standard Model parameters in the
noncommutative geometry (NCG) framework.

Key features of the paper:
- Four explicit no-go theorems (cosmological impossibility, no sigma-field,
  vector-like spectrum, mass hierarchy obstruction via Schur's lemma)
- Six positive structural results (KO-dim 6 mod 8, eta = -2, first-order
  condition, etc.)
- ~730 machine-verified Coq Qed theorems (73 .v files)
- Honest comparison with Distler-Garibaldi theorem for E8

My arXiv ID: [fill in]
My paper arXiv ID: [fill in after submission system provides it]

Thank you for your consideration.
[Name]
```

### 5.4 Альтернативная категория без эндорсмента

Если в `hep-th` эндорсмент не получен, можно попробовать `math-ph` (требования мягче).  
Перекрёстная ссылка (cross-list) на `hep-th` и `cs.LO` делается автоматически.

---

## 6. Структура статьи

| Раздел | Название | Страниц (оценка) |
|--------|----------|-----------------|
| 1 | Introduction | ~3 |
| 2 | H4 and the 600-Cell | ~3 |
| 3 | Catalog: 25 formulas | ~4 |
| 4 | Positive structural results (P1–P6) | ~5 |
| 5 | No-go theorems (NGT-1–4) | ~7 |
| 6 | Comparison with prior work | ~2 |
| 7 | Coq/Lean 4 formalization | ~2 |
| 8 | Falsifiability | ~2 |
| 9 | Discussion | ~2 |
| 10 | Conclusion | ~1 |
| App A | Coq theorem table | ~2 |
| App B | Reproducibility | ~1 |
| **Итого** | | **~34 страницы** |

---

## 7. Библиография

Файл `wave10_paper.bib` содержит 34 записи (превышает требуемые 30).  
Формат: biblatex (стиль `numeric-comp`).

**Ключевые ссылки:**
- Chamseddine-Connes 1996–2012 (NCG SM) — 6 записей
- Connes NCG book + статья 2006 — 3 записи
- Lisi 2007 + Distler-Garibaldi 2010 — 2 записи
- Coxeter, Conway-Smith (H4, кватернионы) — 2 записи
- APS η-инвариант (Atiyah-Patodi-Singer, Gilkey) — 2 записи
- Planck 2018, DESI 2024, NuFit 6.0, PDG 2022 — 4 записи
- DUNE 2020 — 1 запись
- Coq, Lean 4, Hales (формализация) — 3 записи
- Coleman-Mandula, Haag-Lopuszanski-Sohnius — 2 записи
- Weinberg cosmological constant — 1 запись
- Koide 1983, Shechtman 1984 — 2 записи
- F-theory (Beasley-Heckman-Vafa) — 1 запись
- Krajewski, Barrett, Devastato (NCG classification) — 3 записи
- Boyle-Farnsworth, Furey — 2 записи
- Serre (representations), Loday (Hochschild) — 2 записи

---

## 8. Честность и ключевые предупреждения

Статья следует принципу проекта «Не врать». Основные честные заявления:

1. **Аннотация явно говорит "negative result" и "no-go"** — не смягчать.
2. **0 из 25 формул имеют класс R (строгий вывод)** — это указано в тексте.
3. **754σ** фальсификация барионной плотности — число присутствует в аннотации и тексте.
4. **\(\sigdist = 5.62\)** для NGT-4 — machine-verified, не уменьшать.
5. **7 Admitted** — все перечислены с объяснениями в приложении.
6. **\(\delta_{CP} = 65.66°\)** — явно помечено как NF (Numerical Fit), не "prediction".

---

## 9. Информация об авторе

**Поле автора в статье:** `[Anonymous, gHashTag]`  
**Замените на:** `[Настоящее имя], [Аффилиация]`

Если публикуется анонимно (допускается на arXiv):  
- Репозиторий: `https://github.com/[gHashTag]/trinity-s3ai`
- Контакт: через GitHub Issues

---

## 10. Checklist перед отправкой

- [ ] PDF скомпилирован без ошибок LaTeX
- [ ] Все ссылки \cite{...} резолвируются
- [ ] Таблицы не выходят за поля (проверить longtable)
- [ ] Аннотация ≤ 250 слов (подсчитать: `wc -w abstract.txt`)
- [ ] Файл `wave10_paper.bib` находится в той же директории
- [ ] Автор и дата заполнены
- [ ] Git tag `wave10-submission` создан:
      `git tag -a wave10-submission -m "arXiv submission Wave 10.1"`
- [ ] SHA-256 хеш .vo файлов записан в `checksums.txt`
- [ ] DUNE pre-registration `registered_predictions.md` уже в репозитории ✓

---

*Документ подготовлен в рамках Wave 10.1 проекта Trinity S3AI. Июнь 2026.*
