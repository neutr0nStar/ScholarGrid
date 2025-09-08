from typing import List

from fastapi import APIRouter

from backend.util.llm import LLMAgent, LLMModels

router = APIRouter(prefix="/llm", tags=["llm"])

agent = LLMAgent(model=LLMModels.QWEN3_235_B)


@router.post("/grid")
async def new_grid(paper_id: str, questions: List[str]):
    return await agent.ainvoke(
        md_paper_path=f"uploads/{paper_id}.md", questions=questions
    )
