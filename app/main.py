import dotenv


dotenv.load_dotenv()


import uvicorn
from fastapi import FastAPI, HTTPException
from app.database.engine import create_db_and_tables


from app.models.AppStatus import AppStatus
from app.models.User import User
from fastapi_pagination import  add_pagination
from routers import status, users
# from database import users

app = FastAPI()

app.include_router(users.router)
app.include_router(status.router)

add_pagination(app)


if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="localhost", port=8002)
