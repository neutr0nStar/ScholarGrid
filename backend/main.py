from fastapi import FastAPI

from backend.core.db import create_db_and_tables
from backend.api import paper

app = FastAPI()

app.include_router(paper.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def index():
    return {"message": "Hello World"}
