import os
from enum import Enum
from typing import Annotated, List
from pydantic import BaseModel, Field

from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()


class LLMModels(Enum):
    GPT_OSS_20B = "openai/gpt-oss-20b:free"
    DEEPSEEK_V_3_1 = "deepseek/deepseek-chat-v3.1:free"
    QWEN3_235_B = "qwen/qwen3-235b-a22b:free" # ATM only this works out of the box
    QWEN3_CODER = "qwen/qwen3-coder:free"


class LLMResponseFormat(BaseModel):
    responses: List[str] = Field(description="list of responses")


class LLMAgent:

    def __init__(self, model: LLMModels):
        self.llm = ChatOpenAI(
            model=model.value,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        ).with_structured_output(LLMResponseFormat)

        self.prompt = ChatPromptTemplate.from_template(
            """You are a helpful assistant. You will be given:  
        1. A list of questions.  
        2. The contents of a research paper in Markdown format.  

        Your task:  
        - Answer each question in **one concise sentence**.  
        - Use **simple, clear language** that avoids jargon.  
        - Make sure each answer is directly supported by the paper. 
        - Only return a python list 

        Questions: {ques_list}  
        Paper: {paper}  
        """
        )

    async def ainvoke(self, md_paper_path: str, questions: List[str]):
        with open(md_paper_path, "r", encoding="utf-8") as f:
            paper_content = f.read()

        chain = self.prompt | self.llm

        res = await chain.ainvoke({"ques_list": questions, "paper": paper_content})

        return res.responses


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    llm = get_llm()
    print(llm.invoke("Hi there").content)
