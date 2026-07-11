
from sqlalchemy.orm import Session
from app.models.task import Task, StatusEnum
from app.schemas.task_schema import TaskCreate, TaskUpdate

class TaskRepository:
    def get_by_id(self, db: Session, task_id: int) -> Task | None:
        return db.query(Task).filter(Task.task_id == task_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100, assigned_to: int = None, status: StatusEnum = None) -> list[Task]:
        query = db.query(Task)
        if assigned_to:
            query = query.filter(Task.assigned_to == assigned_to)
        if status:
            query = query.filter(Task.status == status)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, task_in: TaskCreate, assigned_by: int) -> Task:
        db_task = Task(
            title=task_in.title,
            description=task_in.description,
            assigned_to=task_in.assigned_to,
            assigned_by=assigned_by,
            priority=task_in.priority,
            due_date=task_in.due_date
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    def update(self, db: Session, db_task: Task, update_data: TaskUpdate) -> Task:
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task
        
    def update_status(self, db: Session, db_task: Task, status: StatusEnum, completed: bool) -> Task:
        db_task.status = status
        db_task.completed = completed
        db.commit()
        db.refresh(db_task)
        return db_task

    def delete(self, db: Session, db_task: Task) -> None:
        db.delete(db_task)
        db.commit()

task_repo = TaskRepository()

