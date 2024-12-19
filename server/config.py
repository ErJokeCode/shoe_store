import dotenv
import os

from db import MongoDataBase, S3Client


dotenv.load_dotenv()

NAME_SUPERUSER = os.getenv('NAME_SUPERUSER')
PASSWORD_SUPERUSER = os.getenv('PASSWORD_SUPERUSER')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
URL_S3 = os.getenv('URL_S3')
REGION_S3 = os.getenv('REGION_S3')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
URL_S3_GET = os.getenv('URL_S3_GET')



DB = MongoDataBase(
    host="serverdb", 
    port=27017, 
    name_db="shoe_store", 
    sp_name=NAME_SUPERUSER,
    sp_password=PASSWORD_SUPERUSER)

WORKER_USER = DB.Worker_user
WORKER_SHOE = DB.Worker_shoe

s3_client = S3Client(
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        endpoint_url=URL_S3, 
        bucket_name=BUCKET_NAME,
        url_files=URL_S3_GET
    )

