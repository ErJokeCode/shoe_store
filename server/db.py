from typing import List, ParamSpec, Type, TypeVar, Generic, Sequence
from typing_extensions import Unpack
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext
from pymongo.collection import Collection

from schemas import ShoeInDB, UserInDB

T = TypeVar("T", bound=BaseModel)

class MongoDataBase():
    def __init__(self, host: str, port: int, name_db: str, sp_name: str, sp_password: str):
        self.__host = host
        self.__port = port
        self.__name_db = name_db
        client = MongoClient(f'mongodb://{self.__host}:{self.__port}/')
        self.__db = client[self.__name_db]

        self.Worker_user = WorkerCollection[UserInDB](self.__db["users"], UserInDB)
        self.Worker_shoe = WorkerCollection[ShoeInDB](self.__db["shoe"], ShoeInDB)

        self.__add_superuser(sp_name, sp_password)


    def __add_superuser(self, sp_name: str, sp_password: str):
        collect = self.Worker_user

        hash_password = self.__get_password_hash(sp_password)
        superuser = UserInDB(
            username=sp_name, 
            email="", 
            hashed_password=hash_password, 
            is_admin=True, 
            is_superuser=True)
        if collect.get_one(username = superuser.username) == None:
            collect.insert_one(superuser)


    def __get_password_hash(self, password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    

class WorkerCollection(Generic[T]):
    def __init__(self, collection: Collection, class_db: T):
        self.__collection = collection
        self.cla = class_db


    def get_one(self, **kwargs) -> T:
        item = self.__collection.find_one(kwargs)
        if item == None:
            return None
        return self.cla(**item)


    def get_all(self, limit: int, **kwargs) -> T:
        if limit == None:
            limit = 10
        i = 1
        items = []
        for item in self.__collection.find(kwargs):
            if i <= limit:
                i+=1
                items.append(self.cla(**item))
            else:
                break
        return items


    def insert_one(self, item: T) -> T:
        item = self.__collection.insert_one(item.model_dump())
        return item