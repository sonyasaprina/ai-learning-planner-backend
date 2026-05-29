# AI Learning Planner — Backend

FastAPI-бэкенд для сервиса, который генерирует персональные планы обучения с помощью LLM.

## Стек

- **FastAPI** — веб-фреймворк
- **Supabase** — база данных (PostgreSQL)
- **LM Studio** — локальный LLM-сервер (модель qwen3-8b)
- **Python 3.11+**

## Запуск локально

### 1. Создать виртуальное окружение и установить зависимости

macOS / Linux:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):
```bash
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Настроить переменные окружения

Скопировать `.env.example` в `.env` и заполнить своими данными:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
LM_STUDIO_URL=http://localhost:1234
LM_API_TOKEN=lm-studio
LM_MODEL=qwen/qwen3-8b
```

### 3. Создать таблицы в Supabase

Выполнить SQL из файла `supabase_schema.sql` в SQL-редакторе Supabase (один раз).

### 4. Запустить LM Studio

Открыть LM Studio, загрузить модель `qwen/qwen3-8b` и запустить локальный сервер на `http://localhost:1234`.

### 5. Запустить сервер

```bash
uvicorn app.main:app --reload
```

Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

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

### Пример запроса `POST /plans`

```json
{
  "goal": "Изучить Python",
  "level": "beginner",
  "duration_weeks": 4,
  "time_per_week": 5,
  "preferred_format": "practice",
  "user_id": "user-1"
}
```

## Структура проекта

```
app/
  main.py       — роуты FastAPI
  schemas.py    — Pydantic-модели
  db.py         — работа с Supabase
  llm.py        — интеграция с LM Studio
supabase_schema.sql
tests/
requirements.txt
.env.example
Dockerfile
```

## Что реализовано

- Генерация плана через LM Studio (локальная LLM)
- Полный CRUD для планов (создание, чтение, редактирование, удаление)
- Трекинг прогресса по заданиям
- Фильтрация планов по `user_id`
- Валидация входных данных через Pydantic
- CORS для подключения frontend
- Docker-образ

## Что планируется

- Авторизация (JWT)
- Замена LM Studio на облачную LLM (OpenRouter / Claude API)
