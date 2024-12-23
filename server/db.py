from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, ParamSpec, Type, TypeVar, Generic, Sequence
from aiohttp import ClientError
from bson import ObjectId
from fastapi import HTTPException, UploadFile, status
from typing_extensions import Unpack, TypedDict
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext
from pymongo.collection import Collection

from aiobotocore.session import get_session
from aiobotocore.client import AioBaseClient

from schemas import Shoe, ShoeInDB, User, UserInDB

class MongoDataBase():
    def __init__(self, host: str, port: int, name_db: str, sp_name: str, sp_password: str):
        self.__host = host
        self.__port = port
        self.__name_db = name_db
        client = MongoClient(f'mongodb://{self.__host}:{self.__port}/')
        self.__db = client[self.__name_db]

        self.Worker_user = WorkerCollection[User, UserInDB](self.__db["users"], User, UserInDB)
        self.Worker_shoe = WorkerCollection[Shoe, ShoeInDB](self.__db["shoe"], Shoe, ShoeInDB)

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
    
    
    
T = TypeVar("T", bound=BaseModel)
V = TypeVar("V", bound=BaseModel)
class WorkerCollection(Generic[V, T]):
    def __init__(self, collection: Collection, class_m: V, class_db: T):
        self.__collection = collection
        self.cls_db = class_db
        self.cls = class_m


    def get_one(self, **kwargs: Unpack[T]) -> T | None:
        if kwargs.get("id") != None:
            kwargs = {"_id": ObjectId(kwargs["id"])}
            
        item = self.__collection.find_one(kwargs)
        if item == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return self.cls_db(**item)


    def get_all(self, limit: int, **kwargs) -> T:
        if limit == None:
            limit = 10
        i = 1
        items = []
        for item in self.__collection.find(kwargs):
            if i <= limit:
                i+=1
                items.append(self.cls_db(**item))
            else:
                break
        return items


    def insert_one(self, item: V) -> T:
        item_id = self.__collection.insert_one(item.model_dump()).inserted_id
        item = self.__collection.find_one({"_id": ObjectId(item_id)})
        return self.cls_db(**item)
    
    
    def update_one(self, item: T) -> T:
        res = self.__collection.update_one({"_id": ObjectId(item.id)}, {"$set": item.model_dump(by_alias=True, exclude="_id")})
        
        item = self.__collection.find_one({"_id": ObjectId(item.id)})
        return self.cls_db(**item)
    
    def delete_one(self, id: str) -> dict[str, str]:
        res = self.__collection.delete_one({"_id": ObjectId(id)})
        if res.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return {"satatus": "success"}
    
    
class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
            url_files: str
    ):
        self.__config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.__bucket_name = bucket_name
        self.__session = get_session()
        self.__url_files = url_files
    
    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[AioBaseClient]:
        async with self.__session.create_client("s3", **self.__config) as client:
            yield client
            
    async def upload_file(
            self,
            file: UploadFile,
            key: str
    ):
        key = key+file.filename
        try:
            async with self.get_client() as client:
                resp = await client.put_object(
                    Bucket=self.__bucket_name,
                    Key=key,    
                    Body=file.file,
                )
                return self.__url_files + "/" + key
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.__bucket_name, Key=object_name)
        except ClientError as e:
            print(f"Error deleting file: {e}")

    # async def get_file(self, object_name: str, destination_path: str):
    #     try:
    #         async with self.get_client() as client:
    #             response = await client.get_object(Bucket=self.__bucket_name, Key=object_name)
    #             data = await response["Body"].read()
    #             with open(destination_path, "wb") as file:
    #                 file.write(data)
    #     except ClientError as e:
    #         print(f"Error downloading file: {e}")