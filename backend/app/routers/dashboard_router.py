
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.task import Task, StatusEnum
from app.core.dependencies import get_current_active_manager

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db), current_user = Depends(get_current_active_manager)):
    total_tasks = db.query(func.count(Task.task_id)).scalar()
    completed = db.query(func.count(Task.task_id)).filter(Task.status == StatusEnum.Completed).scalar()
    pending = db.query(func.count(Task.task_id)).filter(Task.status == StatusEnum.Pending).scalar()
    in_progress = db.query(func.count(Task.task_id)).filter(Task.status == StatusEnum.In_Progress).scalar()
    overdue = db.query(func.count(Task.task_id)).filter(Task.status == StatusEnum.Overdue).scalar()

    return {
        "total_tasks": total_tasks,
        "completed": completed,
        "pending": pending,
        "in_progress": in_progress,
        "overdue": overdue
    }

