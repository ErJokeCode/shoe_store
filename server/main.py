from fastapi import FastAPI
import uvicorn
from src.users import router as users_router
from src.auth import router as auth_router


app = FastAPI()
app.include_router(users_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)