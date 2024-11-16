from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.users import router as users_router
from src.auth import router as auth_router
from src.shoe import router as shoe_router


app = FastAPI()

origins = [
    'http://client:3020', 
    'http://localhost:3020'
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(shoe_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)