
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.task import PriorityEnum, StatusEnum

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: int
    priority: PriorityEnum = PriorityEnum.Medium
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[date] = None

class TaskStatusUpdate(BaseModel):
    status: StatusEnum
    completed: bool

class TaskOut(TaskBase):
    task_id: int
    assigned_by: int
    status: StatusEnum
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

