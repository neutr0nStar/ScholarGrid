from fastapi import APIRouter, UploadFile, HTTPException
from sqlmodel import select

from backend.core.db import SessionDep
from backend.schemas.paper import PaperModel
from backend.util.paper import generate_pdf_hash

router = APIRouter(prefix="/paper", tags=["paper"])

UPLOADS_DIR = "uploads"


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
def create_paper(file: UploadFile, session: SessionDep):
    _hash = generate_pdf_hash(file)
    print("here")

    # Check if file already exists
    paper = session.get(PaperModel, _hash)
    if paper:
        return HTTPException(status_code=400, detail="Paper already exists")

    # Save paper to uploads
    file_path = f"{UPLOADS_DIR}/{_hash}.pdf"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Save paper to database
    paper = PaperModel(
        id=_hash, pdf_path=file_path, title=_hash, authors="John Doe, Jane Doe"
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

    session.delete(paper)
    session.commit()

    return {"message": "Paper deleted successfully"}
