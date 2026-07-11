import os
import sys
from datetime import date, timedelta

# Add backend directory to python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.database import engine, SessionLocal, Base
from app.models.user import User, RoleEnum
from app.models.employee import Employee
from app.models.task import Task, PriorityEnum, StatusEnum
from app.core.security import get_password_hash

def seed():
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if admin already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            print("Database already contains data. Skipping seeding.")
            return

        print("Seeding database...")

        # Create Admin User
        admin = User(
            username="admin",
            email="admin@taskify.io",
            password_hash=get_password_hash("admin123"),
            role=RoleEnum.admin,
            is_active=True
        )
        db.add(admin)
        db.flush()

        # Create Manager User
        manager = User(
            username="manager",
            email="manager@taskify.io",
            password_hash=get_password_hash("manager123"),
            role=RoleEnum.manager,
            is_active=True
        )
        db.add(manager)
        db.flush()

        # Create Employee 1
        emp1_user = User(
            username="snehal",
            email="snehal@taskify.io",
            password_hash=get_password_hash("snehal123"),
            role=RoleEnum.employee,
            is_active=True
        )
        db.add(emp1_user)
        db.flush()

        emp1_details = Employee(
            user_id=emp1_user.user_id,
            full_name="Snehal Wani",
            department="Engineering",
            designation="Software Engineer Intern",
            phone="9876543210",
            date_joined=date.today(),
            is_active=True
        )
        db.add(emp1_details)
        db.flush()

        # Create Employee 2
        emp2_user = User(
            username="aman",
            email="aman@taskify.io",
            password_hash=get_password_hash("aman123"),
            role=RoleEnum.employee,
            is_active=True
        )
        db.add(emp2_user)
        db.flush()

        emp2_details = Employee(
            user_id=emp2_user.user_id,
            full_name="Aman Gupta",
            department="Engineering",
            designation="Frontend Developer",
            phone="9876543211",
            date_joined=date.today(),
            is_active=True
        )
        db.add(emp2_details)
        db.flush()

        # Create Tasks
        task1 = Task(
            title="Deploy backend API container",
            description="Containerize with docker-compose and set up uvicorn reload configurations.",
            assigned_to=emp1_details.employee_id,
            assigned_by=admin.user_id,
            priority=PriorityEnum.High,
            status=StatusEnum.In_Progress,
            completed=False,
            due_date=date.today()
        )
        db.add(task1)

        task2 = Task(
            title="Design login glassmorphism layout",
            description="Write responsive HTML/CSS using custom variable themes and Outfit fonts.",
            assigned_to=emp2_details.employee_id,
            assigned_by=manager.user_id,
            priority=PriorityEnum.Medium,
            status=StatusEnum.Pending,
            completed=False,
            due_date=date.today() + timedelta(days=1)
        )
        db.add(task2)

        db.commit()
        print("Database seeding completed successfully!")
        print("\nDefault Accounts Created:")
        print(" - Admin account:    username: admin    / password: admin123")
        print(" - Manager account:  username: manager  / password: manager123")
        print(" - Employee (Snehal):username: snehal   / password: snehal123")
        print(" - Employee (Aman):  username: aman     / password: aman123\n")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
