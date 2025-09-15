from typing import List, Annotated
import asyncio
from fastapi import APIRouter
import pandas as pd

from backend.core.settings import settings
from backend.core.db import SessionDep
from backend.schemas.grid import GridModel
from backend.util.llm import CritiqueAgent, LLMModels

router = APIRouter(prefix="/grid", tags=["grid"])

agent = CritiqueAgent(model=LLMModels.QWEN3_235_B)


@router.get("/")
async def get_grids(session: SessionDep):
    return session.query(GridModel).all()

@router.get("/{grid_id}")
async def get_grid(grid_id: str, session: SessionDep):
    df = pd.read_csv(f"{settings.GRIDS_STORAGE_DIR}/{grid_id}.csv", index_col=0)
    return df.to_dict(orient="index")

@router.post("/")
async def new_grid(
    name: Annotated[str, "Name of the grid"],
    papers: Annotated[List[str], "List of papers"],
    questions: Annotated[List[str], "List of questions"],
    session: SessionDep,
):
    # Critique papers concurrently
    tasks = [
        agent.ainvoke(
            md_paper_path=f"{settings.UPLOADS_DIR}/{paper}.md", questions=questions
        )
        for paper in papers
    ]
    responses = await asyncio.gather(*tasks)

    # extract dataframe
    res = {}
    for paper, response in zip(papers, responses):
        res[paper] = {questions[i]: response[i] for i in range(len(questions))}

    df = pd.DataFrame.from_dict(res, orient="index")

    # Save grid in db
    grid = GridModel(name=name)
    session.add(grid)
    session.commit()
    session.refresh(grid)

    df.to_csv(f"{settings.GRIDS_STORAGE_DIR}/{grid.id}.csv", index=True)

    return res


@router.post("/critique")
async def critique_paper(paper_id: str, questions: List[str]):
    return await agent.ainvoke(
        md_paper_path=f"{settings.UPLOADS_DIR}/{paper_id}.md", questions=questions
    )
