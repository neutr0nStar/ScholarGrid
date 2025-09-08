from typing import List, Annotated
import asyncio
from fastapi import APIRouter

from backend.util.llm import LLMAgent, LLMModels

router = APIRouter(prefix="/llm", tags=["llm"])

agent = LLMAgent(model=LLMModels.QWEN3_235_B)


@router.post("/grid/new")
async def new_grid(papers: Annotated[List[str], "List of papers"], questions: Annotated[List[str], "List of questions"]):
    tasks = [agent.ainvoke(md_paper_path=f"uploads/{paper}.md", questions=questions) for paper in papers]
    return await asyncio.gather(*tasks)

@router.post("/critique")
async def critique_paper(paper_id: str, questions: List[str]):
    return await agent.ainvoke(
        md_paper_path=f"uploads/{paper_id}.md", questions=questions
    )
