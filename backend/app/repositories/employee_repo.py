
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee_schema import EmployeeUpdate

class EmployeeRepository:
    def get_by_id(self, db: Session, employee_id: int) -> Employee | None:
        return db.query(Employee).filter(Employee.employee_id == employee_id).first()

    def get_by_user_id(self, db: Session, user_id: int) -> Employee | None:
        return db.query(Employee).filter(Employee.user_id == user_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[Employee]:
        return db.query(Employee).offset(skip).limit(limit).all()

    def create(self, db: Session, user_id: int, full_name: str, department: str = None, designation: str = None, phone: str = None) -> Employee:
        db_employee = Employee(
            user_id=user_id,
            full_name=full_name,
            department=department,
            designation=designation,
            phone=phone,
            date_joined=None 
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee

    def update(self, db: Session, db_employee: Employee, update_data: EmployeeUpdate) -> Employee:
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_employee, key, value)
        db.commit()
        db.refresh(db_employee)
        return db_employee

    def delete(self, db: Session, db_employee: Employee) -> Employee:
        db_employee.is_active = False
        db.commit()
        db.refresh(db_employee)
        return db_employee

employee_repo = EmployeeRepository()

