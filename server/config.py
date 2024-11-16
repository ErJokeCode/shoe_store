import dotenv
import os

from db import MongoDataBase


dotenv.load_dotenv()

NAME_SUPERUSER = os.getenv('NAME_SUPERUSER')
PASSWORD_SUPERUSER = os.getenv('PASSWORD_SUPERUSER')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

DB = MongoDataBase(
    host="serverdb", 
    port=27017, 
    name_db="shoe_store", 
    sp_name=NAME_SUPERUSER,
    sp_password=PASSWORD_SUPERUSER)

WORKER_USER = DB.worker_user_collection()
WORKER_SHOE = DB.worker_shoe_collection()

