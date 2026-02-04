from fastapi import FastAPI
from auth.routes import auth
from core.db import create_db_on_start
from contextlib import asynccontextmanager
from todo.routes import todo_route



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_on_start()

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth)
app.include_router(todo_route)



@app.get("/")
def hello():
    return {"msg" : "Hello from root of fastapi"}