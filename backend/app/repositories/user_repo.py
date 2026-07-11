
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash

class UserRepository:
    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.user_id == user_id).first()

    def create(self, db: Session, user_in: UserCreate) -> User:
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            password_hash=get_password_hash(user_in.password),
            role=user_in.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

user_repo = UserRepository()

