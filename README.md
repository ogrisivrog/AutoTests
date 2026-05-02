# QA Automation — тестирование JSONPlaceholder API

[![CI](https://github.com/ВАШ_ЛОГИН/qa-pet/actions/workflows/ci.yml/badge.svg)](https://github.com/ВАШ_ЛОГИН/qa-pet/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-orange)](https://pytest.org)

Пет-проект для отработки навыков QA Automation.  
Тестирую публичный REST API [JSONPlaceholder](https://jsonplaceholder.typicode.com/) — это бесплатный фейковый апи с постами, юзерами и комментариями.

---

## Что умеет проект

- Автоматически тестирует REST API (GET, POST, PUT, PATCH, DELETE)
- Валидирует структуру ответов через Pydantic схемы
- Генерирует тестовые данные через Faker — без хардкода
- Строит HTML-отчёты через Allure
- Запускается в Docker
- Есть CI/CD через GitHub Actions

---

## Стек

| Что            | Зачем                                      |
|----------------|--------------------------------------------|
| Python 3.11    | основной язык                              |
| pytest         | фреймворк для тестов                       |
| requests       | делать http запросы к апи                  |
| pydantic v2    | валидация схем ответов                     |
| faker          | генерация тестовых данных                  |
| allure         | красивые отчёты                            |
| docker         | запуск в изолированной среде               |
| github actions | автозапуск тестов при каждом пуше          |

---

## Структура

```
qa-pet/
├── api/
│   └── client.py          # http клиент — обёртка над requests
├── models/
│   └── schemas.py         # pydantic схемы для валидации ответов
├── utils/
│   ├── проверки.py        # кастомные assert функции
│   └── генератор.py       # faker — генерация данных для запросов
├── tests/
│   ├── conftest.py        # общие фикстуры для всех тестов
│   ├── smoke/             # быстрые проверки что апи живое
│   ├── posts/             # тесты для /posts
│   ├── users/             # тесты для /users
│   └── comments/          # тесты для /comments
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── .github/workflows/
    └── ci.yml
```

---

## Как запустить

```bash
# клонировать и перейти в папку
git clone https://github.com/ВАШ_ЛОГИН/qa-pet.git
cd qa-pet

# создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # на windows: .venv\Scripts\activate

# установить зависимости
pip install -r requirements.txt

# скопировать env файл
cp .env.example .env
```

---

## Запуск тестов

```bash
# все тесты
pytest

# только smoke (быстро)
pytest -m smoke

# только посты
pytest -m posts

# параллельно в 4 потока
pytest -n 4

# конкретный файл
pytest tests/users/test_users.py -v
```

---

## Allure отчёт

Нужен allure cli (`brew install allure` на mac).

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## Docker

```bash
# собрать и запустить
docker build -f docker/Dockerfile -t qa-pet .
docker run --rm qa-pet

# через compose
cd docker && docker-compose up --build
```

---

## CI/CD

При каждом пуше в `main` GitHub Actions автоматически:
1. Ставит зависимости
2. Запускает smoke тесты
3. Запускает полный прогон
4. Сохраняет Allure результаты как артефакт
5. Собирает и проверяет Docker образ
