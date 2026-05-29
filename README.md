# AI Learning Planner — Backend

FastAPI-бэкенд для сервиса, который генерирует персональные планы обучения с помощью LLM.

## Стек

- **FastAPI** — веб-фреймворк
- **Supabase** — база данных (PostgreSQL)
- **LM Studio** — локальный LLM-сервер (модель qwen3-8b)
- **Python 3.11+**
- **Docker / Docker Compose**

## Быстрый старт через Docker Compose

```bash
cp .env.example .env
# заполни .env своими данными
docker compose up -d
```

Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

> LM Studio должен быть запущен на хосте с моделью `qwen3-8b` на порту `1234`. Системный промпт в LM Studio должен быть пустым — бэкенд отправляет его сам.

## Переменные окружения

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
LM_STUDIO_URL=http://host.docker.internal:1234
LM_API_TOKEN=lm-studio
LM_MODEL=qwen/qwen3-8b
```

## Настройка Supabase

Выполнить SQL из файла `supabase_schema.sql` в SQL-редакторе Supabase (один раз).

## Запуск локально (без Docker)

```bash
python -m venv venv
source venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## API

### Plans

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `POST` | `/plans` | Создать учебный план |
| `GET` | `/plans` | Список всех планов |
| `GET` | `/plans?user_id=xxx` | Планы конкретного пользователя |
| `GET` | `/plans/{plan_id}` | Один план по ID |
| `PATCH` | `/plans/{plan_id}` | Редактировать план |
| `DELETE` | `/plans/{plan_id}` | Удалить план |

### Progress

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `POST` | `/task-progress` | Сохранить прогресс по заданию |
| `GET` | `/plans/{plan_id}/progress` | Прогресс по плану |

## Структура проекта

```
app/
  main.py       — роуты FastAPI
  schemas.py    — Pydantic-модели
  db.py         — работа с Supabase
  llm.py        — интеграция с LM Studio
supabase_schema.sql
tests/
docker-compose.yml
Dockerfile
requirements.txt
.env.example
```

## Что реализовано

- Генерация плана через LM Studio (локальная LLM, qwen3-8b)
- Полный CRUD для планов (создание, чтение, редактирование, удаление)
- Трекинг прогресса по заданиям
- Фильтрация планов по `user_id`
- Валидация входных данных через Pydantic
- CORS для подключения frontend
- Docker Compose

## Что планируется

- Авторизация (JWT)
- Замена LM Studio на облачную LLM (OpenRouter / Claude API)
