
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.employee_schema import EmployeeCreate, EmployeeUpdate, EmployeeOut
from app.services.employee_service import employee_service
from app.core.dependencies import get_current_active_manager, get_current_active_admin

router = APIRouter(prefix="/api/v1/employees", tags=["employees"])

@router.post("", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(employee_in: EmployeeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_admin)):
    return employee_service.create_employee(db, employee_in)

@router.get("", response_model=list[EmployeeOut])
def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_active_manager)):
    return employee_service.get_employees(db, skip, limit)

@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_manager)):
    return employee_service.get_employee(db, employee_id)

@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, employee_in: EmployeeUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_active_admin)):
    return employee_service.update_employee(db, employee_id, employee_in)

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_employee(employee_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_active_admin)):
    employee_service.deactivate_employee(db, employee_id)

