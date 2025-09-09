from sqlmodel import SQLModel, Field

class GridModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(description="Name of the grid")