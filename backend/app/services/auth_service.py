
from sqlalchemy.orm import Session
from app.repositories.user_repo import user_repo
from app.schemas.user_schema import UserLogin, Token, UserCreate, UserOut
from app.core.security import verify_password, create_access_token
from app.core.exceptions import BadRequestException, NotFoundException

class AuthService:
    def login(self, db: Session, login_data: UserLogin) -> Token:
        user = user_repo.get_by_username(db, login_data.username)
        if not user or not verify_password(login_data.password, user.password_hash):
            raise BadRequestException(detail="Incorrect username or password")
        
        if not user.is_active:
            raise BadRequestException(detail="Inactive user")

        access_token = create_access_token(data={"sub": user.username})
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            role=user.role,
            user_id=user.user_id
        )

auth_service = AuthService()

