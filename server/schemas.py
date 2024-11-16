from typing import Annotated, List
from fastapi import Form
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    is_admin: bool = True
    is_superuser: bool = False


class UserInDB(User):
    hashed_password: str


class UserLogin(BaseModel):
    username: str
    password: str


class ShoeInDB(BaseModel):
    number: int
    title: str
    discr: str | None = None
    sizes: List[str]
    sales: bool = False
    price: int