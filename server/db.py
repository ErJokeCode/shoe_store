from typing import List
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext
from pymongo.collection import Collection

from schemas import ShoeInDB, UserInDB

class MongoDataBase():
    def __init__(self, host: str, port: int, name_db: str, sp_name: str, sp_password: str):
        self.__host = host
        self.__port = port
        self.__name_db = name_db
        client = MongoClient(f'mongodb://{self.__host}:{self.__port}/')
        self.__db = client[self.__name_db]

        self.__user_collection = WorkerUserCollection(self.__db["users"])
        self.__shoe_collection = WorkerShoeCollection(self.__db["shoe"])

        self.__add_superuser(sp_name, sp_password)


    def __add_superuser(self, sp_name: str, sp_password: str):
        collect = self.worker_user_collection()

        hash_password = self.__get_password_hash(sp_password)
        superuser = UserInDB(
            username=sp_name, 
            email="", 
            hashed_password=hash_password, 
            is_admin=True, 
            is_superuser=True)
        if collect.get_one(superuser.username) == None:
            collect.insert_one(superuser)


    def __get_password_hash(self, password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)


    def worker_user_collection(self):
        return self.__user_collection
    
    
    def worker_shoe_collection(self):
        return self.__shoe_collection
    

class WorkerCollection():
    def __init__(self, collection: Collection, class_in_db: BaseModel):
        self.__collection = collection
        self.__class_in_db = class_in_db
        print(class_in_db.__dict__['model_fields'])


    def get_one(self, dict_keys):
        item = self.__collection.find_one(dict_keys)
        if item == None:
            return None
        return self.__class_in_db(**item)


    def get_all(self, limit: int, find: dict = None):
        if limit == None:
            limit = 10
        i = 1
        items = []
        for item in self.__collection.find(find):
            if i <= limit:
                i+=1
                items.append(self.__class_in_db(**item))
            else:
                break
        return items


    def insert_one(self, item: BaseModel):
        item = self.__collection.insert_one(item.model_dump())
        return item


class WorkerUserCollection(WorkerCollection):
    def __init__(self, collection: Collection):
        super().__init__(collection, UserInDB)

    
    def get_one(self, username: str) -> UserInDB:
        dict = {"username" : username}
        return super().get_one(dict)


    def get_all(self, limit: int) -> List[UserInDB]:
        return super().get_all(limit)
    

    def insert_one(self, user: UserInDB):
        return super().insert_one(user)


class WorkerShoeCollection(WorkerCollection):
    def __init__(self, collection: Collection):
        super().__init__(collection, ShoeInDB)

    
    def get_one(self, number: str) -> ShoeInDB:
        dict = {"number" : number}
        return super().get_one(dict)


    def get_all(self, limit: int) -> List[ShoeInDB]:
        return super().get_all(limit)
    

    def get_sales(self, limit: int):
        dict = {"sales" : True}
        return super().get_all(limit, dict)
    

    def insert_one(self, shoe: ShoeInDB):
        return super().insert_one(shoe)
    