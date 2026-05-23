# Подготовка к публикации на Zenodo — Trinity S3AI

**Версия**: v1.0-wave10  
**Дата**: 2026-05-22  
**Статус**: Конструктивный отрицательный результат

> **ВАЖНО**: Прочитайте `SALVAGE.md` перед публикацией. DOI будет ссылаться на
> отрицательный результат (No-Go теоремы), а не на положительное утверждение об унификации.

---

## Часть 1: Подготовка репозитория

### Шаг 1.1 — Проверить состояние
```bash
# Убедиться, что anti-numerology gate проходит
python3 scripts/anti_numerology_gate.py

# Убедиться, что validate_v4.py проходит
python3 validate_v4.py

# Проверить README.md и CITATION.cff
cat README.md | head -20
cat CITATION.cff
```

### Шаг 1.2 — Обновить CITATION.cff
Перед тегом заполнить плейсхолдеры в `CITATION.cff`:
```yaml
# Заменить:
  - family-names: "[AUTHOR_LAST_NAME]"
    given-names: "[AUTHOR_FIRST_NAME]"
    orcid: "https://orcid.org/[YOUR_ORCID]"
# На ваши реальные данные.

# DOI оставить пустым — он появится ПОСЛЕ регистрации на Zenodo:
doi: "[PLACEHOLDER — заполнить после получения DOI]"
```

### Шаг 1.3 — Создать релизный тег
```bash
cd /path/to/trinity-s3ai

# Убедиться, что всё закоммичено
git status
git add -A
git commit -m "Wave 10.5: infrastructure — anti-numerology gate + repo metadata

- Add scripts/anti_numerology_gate.py (CI-level formula honesty checker)
- Add [phenomenological_fit] tags to all formulas in Catalog42.v and related files
- Add .github/workflows/ci.yml: anti_numerology_check job (hard gate)
- Add .github/workflows/release.yml: release artifact builder
- Add CITATION.cff, CONTRIBUTING.md (Russian + English)
- Update .github/PULL_REQUEST_TEMPLATE.md
- Add scripts/prepare_zenodo.md
- Rewrite README.md with honest status"

# Создать аннотированный тег
git tag -a v1.0-wave10 -m "Trinity S3AI v1.0-wave10

Constructive negative result on H4-based Standard Model unification.

Key results:
- 4 formal No-Go Theorems (NGT1-NGT4) in Coq 8.20.1
- 1325 Qed across 79 .v files (50 in proofs/trinity/ + 3 in proofs/clifford_cl8/ + 26 in derivations/) with 123 unproven obligations transparently catalogued (25 Admitted + 18 admit + 73 Axiom + 7 Parameter) — see COQ_HONEST_STATUS.md
- 59 phenomenological formulas cataloged and tagged
- Anti-numerology CI gate operational

See SALVAGE.md for summary."

# Отправить тег на GitHub
git push origin v1.0-wave10
```

---

## Часть 2: Регистрация на Zenodo

### Шаг 2.1 — Подключить репозиторий к Zenodo

**Это должен сделать владелец аккаунта лично** — автоматизация невозможна без токена.

1. Войти на [https://zenodo.org](https://zenodo.org) (аккаунт GitHub или ORCID)
2. Перейти в **Settings → GitHub** (https://zenodo.org/account/settings/github/)
3. Найти `gHashTag/trinity-s3ai` в списке репозиториев
4. Нажать **Enable** (переключить в ON)
5. Вернуться на GitHub и убедиться, что тег `v1.0-wave10` уже создан

### Шаг 2.2 — Проверить, что Zenodo создал запись

После того, как тег `v1.0-wave10` загружен на GitHub и Zenodo подключён:
1. Перейти на https://zenodo.org/deposit
2. Найти новую запись (она появится автоматически через ~5 минут)
3. Статус будет **Draft** — нужно заполнить метаданные и опубликовать

### Шаг 2.3 — Заполнить метаданные Zenodo

В форме редактирования записи:

| Поле | Значение |
|------|---------|
| **Title** | Trinity-s3ai: A Constructive Negative Result on H4-Based Standard Model Unification |
| **Authors** | [Ваши данные] |
| **Description** | Формальная верификация (Coq 8.20.1) четырёх теорем о недостижимости H4/600-cell геометрии. 1325 Qed в 79 .v файлах с 123 недоказанными обязательствами (каталогизированы в COQ_HONEST_STATUS.md). 59 феноменологических формул. Конструктивный отрицательный результат. |
| **Resource type** | Software |
| **License** | MIT |
| **Keywords** | NCG, H4, 600-cell, Standard Model, Coq, formal verification, negative result, golden ratio |
| **Version** | v1.0-wave10 |
| **Related identifiers** | GitHub: https://github.com/gHashTag/trinity-s3ai |

### Шаг 2.4 — Опубликовать и получить DOI

1. Нажать **Publish** в форме Zenodo
2. Дождаться регистрации DOI (обычно мгновенно)
3. Скопировать DOI вида `10.5281/zenodo.XXXXXXX`

---

## Часть 3: Обновить CITATION.cff

После получения DOI:

```bash
# Отредактировать CITATION.cff
nano CITATION.cff

# Заменить плейсхолдер:
# doi: "[PLACEHOLDER — fill after Zenodo deposit; see scripts/prepare_zenodo.md]"
# На:
# doi: "10.5281/zenodo.XXXXXXX"

# Добавить в README.md бейдж:
# [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

git add CITATION.cff README.md
git commit -m "Add Zenodo DOI to CITATION.cff and README.md"
git push origin main
```

---

## Часть 4: Проверка публикации

```bash
# Убедиться, что DOI резолвится
curl -s "https://doi.org/10.5281/zenodo.XXXXXXX" | head -5

# Проверить метаданные через API Zenodo
curl -s "https://zenodo.org/api/records/XXXXXXX" | python3 -m json.tool | head -40
```

---

## Артефакты релиза (автоматические)

Workflow `.github/workflows/release.yml` при создании тега автоматически:
1. Создаёт архив `coq-proofs-v*.tar.gz` из скомпилированных `.vo` файлов
2. Прикрепляет архив к GitHub Release
3. Если найден `paper.pdf` в корне — добавляет его тоже

Проверить: https://github.com/gHashTag/trinity-s3ai/releases/tag/v1.0-wave10

---

## Контрольный список перед публикацией

- [ ] `python3 scripts/anti_numerology_gate.py` → PASS (0 флагов)
- [ ] `python3 validate_v4.py` → PASS
- [ ] CITATION.cff — имена авторов заполнены
- [ ] README.md — раздел «Status» честно описывает отрицательный результат
- [ ] SALVAGE.md существует и актуален
- [ ] Тег `v1.0-wave10` создан и загружен: `git push origin v1.0-wave10`
- [ ] Zenodo подключён к репозиторию
- [ ] DOI получен и добавлен в CITATION.cff
- [ ] Бейдж DOI добавлен в README.md
- [ ] GitHub Release содержит артефакты `.vo` и PDF (если есть)

---

*Wave 10.5 — Trinity S3AI Zenodo Preparation Guide*
