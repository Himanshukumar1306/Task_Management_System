
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, RoleEnum
from app.repositories.user_repo import user_repo
from app.core.security import ALGORITHM
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = user_repo.get_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def get_current_active_employee(current_user: User = Depends(get_current_user)) -> User:
    return current_user

def get_current_active_manager(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [RoleEnum.manager, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

def get_current_active_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

