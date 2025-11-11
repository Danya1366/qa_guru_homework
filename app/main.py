import logging
from contextlib import asynccontextmanager

import dotenv

dotenv.load_dotenv()

import uvicorn
from fastapi import FastAPI, HTTPException
from app.database.engine import create_db_and_tables

from fastapi_pagination import  add_pagination
from app.routers import status, users

@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.warning("On start up")
    create_db_and_tables()
    yield

    logging.warning("On shut down")



app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(status.router)
add_pagination(app)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)
