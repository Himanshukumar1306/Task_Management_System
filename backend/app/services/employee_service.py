
from sqlalchemy.orm import Session
from app.repositories.employee_repo import employee_repo
from app.repositories.user_repo import user_repo
from app.schemas.employee_schema import EmployeeCreate, EmployeeUpdate, EmployeeOut
from app.schemas.user_schema import UserCreate
from app.models.user import RoleEnum
from app.core.exceptions import BadRequestException, NotFoundException
import logging

logger = logging.getLogger(__name__)

class EmployeeService:
    def create_employee(self, db: Session, employee_in: EmployeeCreate) -> EmployeeOut:
        # Check if username or email exists
        if user_repo.get_by_username(db, employee_in.username):
            raise BadRequestException(detail="Username already registered")
        if user_repo.get_by_email(db, employee_in.email):
            raise BadRequestException(detail="Email already registered")

        # 1. Create User
        user_create = UserCreate(
            username=employee_in.username,
            email=employee_in.email,
            password=employee_in.password,
            role=RoleEnum.employee
        )
        user = user_repo.create(db, user_create)

        # 2. Create Employee
        employee = employee_repo.create(
            db=db,
            user_id=user.user_id,
            full_name=employee_in.full_name,
            department=employee_in.department,
            designation=employee_in.designation,
            phone=employee_in.phone
        )
        return employee

    def get_employees(self, db: Session, skip: int = 0, limit: int = 100) -> list[EmployeeOut]:
        return employee_repo.get_all(db, skip=skip, limit=limit)

    def get_employee(self, db: Session, employee_id: int) -> EmployeeOut:
        employee = employee_repo.get_by_id(db, employee_id)
        if not employee:
            raise NotFoundException(detail="Employee not found")
        return employee

    def update_employee(self, db: Session, employee_id: int, employee_in: EmployeeUpdate) -> EmployeeOut:
        employee = employee_repo.get_by_id(db, employee_id)
        if not employee:
            raise NotFoundException(detail="Employee not found")
        return employee_repo.update(db, employee, employee_in)

    def deactivate_employee(self, db: Session, employee_id: int):
        employee = employee_repo.get_by_id(db, employee_id)
        if not employee:
            raise NotFoundException(detail="Employee not found")
        employee_repo.delete(db, employee)

employee_service = EmployeeService()

