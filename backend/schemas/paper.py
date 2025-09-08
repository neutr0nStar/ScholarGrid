from typing import List
from sqlmodel import SQLModel, Field

class PaperBase(SQLModel):
    title: str = Field(description="Title of the paper")
    authors: str = Field(description="List of authors")

class PaperModel(PaperBase, table=True):
    id: str = Field(default=None, primary_key=True)

