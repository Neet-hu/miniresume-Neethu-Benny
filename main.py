from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Candidate

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "API running"}


@app.post("/candidates")
async def create_candidate(
    full_name: str = Form(...),
    dob: str = Form(...),
    contact_number: str = Form(...),
    address: str = Form(...),
    education: str = Form(...),
    graduation_year: int = Form(...),
    experience: float = Form(...),
    skill_set: str = Form(...),
    resume: UploadFile = File(...)
):
    db = next(get_db())

    candidate = Candidate(
        full_name=full_name,
        dob=dob,
        contact_number=contact_number,
        address=address,
        education=education,
        graduation_year=graduation_year,
        experience=experience,
        skill_set=skill_set,
        resume_file=resume.filename
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {"message": "Candidate saved", "id": candidate.id}


@app.get("/candidates")
def list_candidates():
    db = next(get_db())
    candidates = db.query(Candidate).all()
    return candidates


@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: int):
    db = next(get_db())
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return candidate


@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: int):
    db = next(get_db())
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    db.delete(candidate)
    db.commit()

    return {"message": "Candidate deleted"}