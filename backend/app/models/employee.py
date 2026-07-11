
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    department = Column(String(50))
    designation = Column(String(50))
    phone = Column(String(15))
    date_joined = Column(Date)
    is_active = Column(Boolean, default=True, nullable=False)

