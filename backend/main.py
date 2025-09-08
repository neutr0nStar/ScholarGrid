from fastapi import FastAPI

from backend.core.db import create_db_and_tables
from backend.api import paper, llm

app = FastAPI()

app.include_router(paper.router)
app.include_router(llm.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def index():
    return {"message": "Hello World"}
