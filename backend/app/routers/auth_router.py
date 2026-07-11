
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserLogin, Token, UserOut
from app.services.auth_service import auth_service
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login(db, login_data)

@router.get("/me", response_model=UserOut)
def get_me(current_user = Depends(get_current_user)):
    return current_user

