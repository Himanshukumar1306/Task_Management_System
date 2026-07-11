
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Enum, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import enum

class PriorityEnum(str, enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class StatusEnum(str, enum.Enum):
    Pending = "Pending"
    In_Progress = "In Progress"
    Completed = "Completed"
    Overdue = "Overdue"

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    assigned_to = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, index=True)
    assigned_by = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.Medium)
    status = Column(Enum(StatusEnum), default=StatusEnum.Pending, index=True)
    completed = Column(Boolean, default=False, nullable=False)
    due_date = Column(Date, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

