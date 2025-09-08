from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

DB_URL='sqlite:///test.db'

engine = create_engine(DB_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]