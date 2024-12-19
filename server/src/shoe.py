from datetime import datetime, timedelta, timezone
from typing import Annotated, List, Optional

import jwt
from fastapi import Depends, APIRouter, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from schemas import ShoeInDB, User, UserInDB, Token, TokenData
from src.auth import oauth2_scheme
from config import ALGORITHM, SECRET_KEY, WORKER_USER, WORKER_SHOE, s3_client


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
    prefix="/shoe",
    tags=["Shoe"]
    )

@router.get("/")
async def get_all_shoes(limit: int = None)->List[ShoeInDB]:
    return WORKER_SHOE.get_all(limit)
    

@router.get("/sales")
async def get_sales_shoes(limit: int = None):
    return WORKER_SHOE.get_all(limit, sales=True)

@router.get("/{number}")
async def get_one_shoe(number: int):
    return WORKER_SHOE.get_one(number=number)


@router.post("/")
async def add_shoe(
    shoe: Annotated[ShoeInDB, Depends()],
    current_user: Annotated[User, Depends(get_current_active_user)],
    files: list[UploadFile]
):
    if current_user.is_admin:
        shoe = WORKER_SHOE.insert_one(shoe)
        for i in range(len(files)):
            res = await s3_client.upload_file(files[i], f"{shoe.number}{i}")
            print(res)
        return shoe
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')