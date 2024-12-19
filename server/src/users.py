from datetime import datetime, timedelta, timezone
from typing import Annotated, List, Optional

import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from schemas import User, UserInDB, Token, TokenData
from src.auth import oauth2_scheme
from config import ALGORITHM, SECRET_KEY, WORKER_USER


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception as e:
        raise credentials_exception
    user = WORKER_USER.get_one(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user




router = APIRouter(
    prefix="/user",
    tags=["User"]
    )


@router.get("/")
async def read_own_items(limit: int = None, current_user: Annotated[User, Depends(get_current_user)] = None)->List[UserInDB]:
    if current_user.is_superuser:
        return WORKER_USER.get_all(limit)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')
    

@router.get("/me", response_model=User)
async def read_users_me(
current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


