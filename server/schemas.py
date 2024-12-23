from typing import Annotated, List, Optional
from typing import TypedDict
from fastapi import Form
from pydantic import BaseModel, BeforeValidator, Field, HttpUrl


PyObjectId = Annotated[str, BeforeValidator(str)]

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    is_admin: bool = True
    is_superuser: bool = False

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserInDB(User):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str



class Shoe(BaseModel):
    title: str = Field(max_length=100)
    discr: str = Field(default="", max_length=3000)
    sizes: List[Annotated[float, Field(ge=10, le=60)]]
    sales: bool = False
    price: float

class ShoeInDB(Shoe):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    photos: list[str] = []
    