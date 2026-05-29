import json
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import CreatePlanRequest, UpdatePlanRequest, TaskProgressRequest
from app.llm import generate_learning_plan
from app.db import (
    save_learning_plan,
    get_learning_plans,
    get_learning_plan_by_id,
    delete_learning_plan_by_id,
    update_learning_plan_by_id,
    upsert_task_progress,
    get_task_progress_by_plan_id,
)

app = FastAPI(title="AI Learning Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/plans")
def create_plan(request: CreatePlanRequest):
    try:
        plan_json = generate_learning_plan(request)
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="LM Studio недоступен. Убедитесь что сервер запущен на localhost:1234")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LM Studio не ответил вовремя. Попробуйте снова")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка от LM Studio: {e.response.status_code}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Модель вернула некорректный ответ. Попробуйте снова")
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))

    saved_plan = save_learning_plan(request, plan_json)

    return {
        "id": saved_plan["id"],
        "user_id": saved_plan["user_id"],
        "title": plan_json["title"],
        "duration_weeks": plan_json["duration_weeks"],
        "weeks": plan_json["weeks"],
        "created_at": saved_plan["created_at"],
    }


@app.get("/plans")
def list_plans(user_id: str | None = None):
    plans = get_learning_plans(user_id=user_id)

    return [
        {
            "id": plan["id"],
            "user_id": plan["user_id"],
            "title": plan["title"],
            "goal": plan["goal"],
            "level": plan["level"],
            "duration_weeks": plan["duration_weeks"],
            "created_at": plan["created_at"],
        }
        for plan in plans
    ]


@app.get("/plans/{plan_id}")
def get_plan(plan_id: str, user_id: str | None = None):
    plan = get_learning_plan_by_id(plan_id, user_id=user_id)

    if plan is None:
        raise HTTPException(status_code=404, detail=f"План {plan_id} не найден")

    return {
        "id": plan["id"],
        "user_id": plan["user_id"],
        "title": plan["title"],
        "goal": plan["goal"],
        "level": plan["level"],
        "duration_weeks": plan["duration_weeks"],
        "time_per_week": plan["time_per_week"],
        "preferred_format": plan["preferred_format"],
        "plan_json": plan["plan_json"],
        "created_at": plan["created_at"],
    }


@app.patch("/plans/{plan_id}")
def update_plan(
    plan_id: str,
    request: UpdatePlanRequest,
    user_id: str | None = None,
):
    update_data = request.model_dump(exclude_none=True)

    if not update_data:
        return {"message": "No data to update"}

    updated_plan = update_learning_plan_by_id(plan_id, update_data, user_id=user_id)

    if not updated_plan:
        return {"message": "Plan not found"}

    return {
        "message": "Plan updated successfully",
        "plan": updated_plan[0],
    }


@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: str, user_id: str | None = None):
    deleted_plan = delete_learning_plan_by_id(plan_id, user_id=user_id)

    if not deleted_plan:
        return {"message": "Plan not found"}

    return {"message": "Plan deleted successfully"}


@app.post("/task-progress")
def save_task_progress(request: TaskProgressRequest):
    progress_data = request.model_dump()
    saved_progress = upsert_task_progress(progress_data)

    return {
        "message": "Task progress saved successfully",
        "progress": saved_progress,
    }


@app.get("/plans/{plan_id}/progress")
def get_plan_progress(plan_id: str):
    progress = get_task_progress_by_plan_id(plan_id)

    return progress
