
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class EmployeeBase(BaseModel):
    full_name: str
    department: Optional[str] = None
    designation: Optional[str] = None
    phone: Optional[str] = None
    date_joined: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    email: EmailStr
    username: str
    password: str

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    employee_id: int
    user_id: int
    is_active: bool

    model_config = {"from_attributes": True}

