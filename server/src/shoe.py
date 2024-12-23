from datetime import datetime, timedelta, timezone
from typing import Annotated, List, Optional

import jwt
from fastapi import Body, Depends, APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from schemas import Shoe, ShoeInDB, User, UserInDB, Token, TokenData
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
async def get_all_shoes(limit: int = None) -> list[ShoeInDB]:
    return WORKER_SHOE.get_all(limit)
    

@router.get("/sales")
async def get_sales_shoes(limit: int = None) -> list[ShoeInDB]:
    return WORKER_SHOE.get_all(limit, sales=True)

@router.get("/{id}")
async def get_one_shoe(id: str) -> ShoeInDB:
    return WORKER_SHOE.get_one(id=id)


@router.post("/")
async def add_shoe(
    current_user: Annotated[User, Depends(get_current_active_user)],
    shoe: Annotated[Shoe, Body()]
) -> ShoeInDB:

    if current_user.is_admin:
        shoe = WORKER_SHOE.insert_one(shoe)        
        return shoe
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

@router.post("/{id}/photos")
async def add_photos_shoe(
    id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    photos: list[UploadFile] = File(default=None)
) -> ShoeInDB:
    
    if photos == None:
        photos = []
        
    if current_user.is_admin:
        shoe = WORKER_SHOE.get_one(id=id)
        for i in range(len(photos)):
            try:
                res = await s3_client.upload_file(photos[i], f"{shoe.id}_{i}")
                shoe.photos.append(res)
            except Exception as e:
                print(e)
        
        shoe = WORKER_SHOE.update_one(shoe)
            
        return shoe
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')


@router.put("/{id}")
async def update_shoe(
    id: str,
    shoe: Annotated[Shoe, Body()],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> ShoeInDB:
    if current_user.is_admin:
        shoe_db = WORKER_SHOE.get_one(id=id)
        
        shoe_db.title = shoe.title
        shoe_db.discr = shoe.discr
        shoe_db.sales = shoe.sales
        shoe_db.price = shoe.price
            
        shoe = WORKER_SHOE.update_one(shoe_db)
        return shoe
        
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

@router.delete("/{id}/photos")
async def update_photos_shoe(
    id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    names_photos: list[str] = None,
) -> ShoeInDB:
    if names_photos == None:
        photos = []
    
    if current_user.is_admin:
        shoe = WORKER_SHOE.get_one(id=id)
        
        for name in names_photos:
            if name in shoe.photos:
                await s3_client.delete_file(name)
                shoe.photos.remove(name)
                
        shoe = WORKER_SHOE.update_one(shoe)
            
        return shoe
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

@router.delete("/{id}")
async def delete_shoe(
    id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> dict:
    
    if current_user.is_admin:
        return WORKER_SHOE.delete_one(id)
        
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')