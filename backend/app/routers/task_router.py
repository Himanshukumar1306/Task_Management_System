
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskOut, TaskStatusUpdate
from app.models.task import StatusEnum
from app.services.task_service import task_service
from app.core.dependencies import get_current_user, get_current_active_manager

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_manager)):
    return task_service.create_task(db, task_in, current_user.user_id)

@router.get("", response_model=list[TaskOut])
def get_tasks(skip: int = 0, limit: int = 100, status: StatusEnum = None, assigned_to: int = None, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return task_service.get_tasks(db, current_user, skip, limit, status, assigned_to)

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return task_service.get_task(db, task_id, current_user)

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_manager)):
    return task_service.update_task(db, task_id, task_in)

@router.patch("/{task_id}/status", response_model=TaskOut)
def update_task_status(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return task_service.update_task_status(db, task_id, status_update, current_user)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_manager)):
    task_service.delete_task(db, task_id)

