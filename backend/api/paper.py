import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlmodel import select
import shutil

from backend.core.db import SessionDep
from backend.schemas.paper import PaperModel
from backend.util.paper import generate_pdf_hash
from backend.util.pdf_to_md import PDF2MD

router = APIRouter(prefix="/paper", tags=["paper"])

UPLOADS_DIR = "uploads"

pdf_2_md = PDF2MD()

@router.get("/")
def get_all_papers(session: SessionDep, offset: int = 0, limit: int = 10):
    papers = session.exec(select(PaperModel).offset(offset).limit(limit)).all()
    return papers


@router.get("/{paper_id}")
def get_paper(paper_id: str, session: SessionDep):
    paper = session.get(PaperModel, paper_id)

    if not paper:
        return HTTPException(status_code=404, detail="Paper not found")

    return paper


@router.post("/")
def create_paper(session: SessionDep, file: UploadFile = File()):
    # Get file contents
    contents = file.file.read()
    
    _hash = generate_pdf_hash(contents)

    # Check if file already exists
    paper = session.get(PaperModel, _hash)
    if paper:
        return HTTPException(status_code=400, detail="Paper already exists")

    # Save paper to uploads
    pdf_file_path = f"{UPLOADS_DIR}/{_hash}.pdf"
    with open(pdf_file_path, "wb") as f:
        f.write(contents)

    # Save MD file
    md_file_path = f"{UPLOADS_DIR}/{_hash}.md"
    md_file_content = pdf_2_md.convert(pdf_file_path)
    with open(md_file_path, "w", encoding="UTF-8") as f:
        f.write(md_file_content)

    # Save paper to database
    paper = PaperModel(
        id=_hash, title=_hash, authors="John Doe, Jane Doe"
    )
    session.add(paper)
    session.commit()
    session.refresh(paper)

    return paper


@router.delete("/{paper_id}")
def delete_paper(paper_id: str, session: SessionDep):
    paper = session.get(PaperModel, paper_id)

    if not paper:
        return HTTPException(status_code=404, detail="Paper not found")

    # Delet from files
    if os.path.exists(paper.pdf_path):
        os.remove(paper.pdf_path)

    session.delete(paper)
    session.commit()

    return {"message": "Paper deleted successfully"}
