
from sqlalchemy.orm import Session
from app.repositories.task_repo import task_repo
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskOut, TaskStatusUpdate
from app.models.task import StatusEnum
from app.core.exceptions import NotFoundException, ForbiddenException
from app.models.user import RoleEnum

class TaskService:
    def create_task(self, db: Session, task_in: TaskCreate, assigned_by_user_id: int) -> TaskOut:
        return task_repo.create(db, task_in=task_in, assigned_by=assigned_by_user_id)

    def get_tasks(self, db: Session, current_user, skip: int = 0, limit: int = 100, status: StatusEnum = None, assigned_to: int = None) -> list[TaskOut]:
        if current_user.role == RoleEnum.employee:
            # Employees can only see their own tasks
            # Assuming current_user has employee relation, let's fetch it
            from app.repositories.employee_repo import employee_repo
            employee = employee_repo.get_by_user_id(db, current_user.user_id)
            if not employee:
                return []
            assigned_to = employee.employee_id
            
        return task_repo.get_all(db, skip=skip, limit=limit, status=status, assigned_to=assigned_to)

    def get_task(self, db: Session, task_id: int, current_user) -> TaskOut:
        task = task_repo.get_by_id(db, task_id)
        if not task:
            raise NotFoundException(detail="Task not found")

        if current_user.role == RoleEnum.employee:
            from app.repositories.employee_repo import employee_repo
            employee = employee_repo.get_by_user_id(db, current_user.user_id)
            if not employee or task.assigned_to != employee.employee_id:
                raise ForbiddenException(detail="Not authorized to access this task")

        return task

    def update_task(self, db: Session, task_id: int, task_in: TaskUpdate) -> TaskOut:
        task = task_repo.get_by_id(db, task_id)
        if not task:
            raise NotFoundException(detail="Task not found")
        return task_repo.update(db, task, task_in)

    def update_task_status(self, db: Session, task_id: int, status_update: TaskStatusUpdate, current_user) -> TaskOut:
        task = task_repo.get_by_id(db, task_id)
        if not task:
            raise NotFoundException(detail="Task not found")
            
        if current_user.role == RoleEnum.employee:
            from app.repositories.employee_repo import employee_repo
            employee = employee_repo.get_by_user_id(db, current_user.user_id)
            if not employee or task.assigned_to != employee.employee_id:
                raise ForbiddenException(detail="Not authorized to modify this task")

        return task_repo.update_status(db, task, status=status_update.status, completed=status_update.completed)

    def delete_task(self, db: Session, task_id: int):
        task = task_repo.get_by_id(db, task_id)
        if not task:
            raise NotFoundException(detail="Task not found")
        task_repo.delete(db, task)

task_service = TaskService()

