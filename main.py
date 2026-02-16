from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import uuid

app = FastAPI(title="Mini Resume Management API")

# In-memory storage
candidates = []


# ---------------------------
# Response Model
# ---------------------------
class CandidateResponse(BaseModel):
    id: str
    full_name: str
    dob: date
    contact_number: str
    contact_address: str
    education_qualification: str
    graduation_year: int
    years_of_experience: float
    skill_set: List[str]
    resume_filename: str


# ---------------------------
# Health Check Endpoint
# ---------------------------
@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}


# ---------------------------
# Upload Resume + Metadata
# ---------------------------
@app.post("/candidates", status_code=201)
async def upload_candidate(
    full_name: str = Form(..., min_length=2),
    dob: date = Form(...),
    contact_number: str = Form(..., min_length=8),
    contact_address: str = Form(..., min_length=5),
    education_qualification: str = Form(...),
    graduation_year: int = Form(..., ge=1950, le=2100),
    years_of_experience: float = Form(..., ge=0),
    skill_set: str = Form(...),
    resume: UploadFile = File(...)
):
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]

    if resume.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOC, DOCX files are allowed"
        )

    candidate_id = str(uuid.uuid4())

    new_candidate = {
        "id": candidate_id,
        "full_name": full_name,
        "dob": dob,
        "contact_number": contact_number,
        "contact_address": contact_address,
        "education_qualification": education_qualification,
        "graduation_year": graduation_year,
        "years_of_experience": years_of_experience,
        "skill_set": [skill.strip() for skill in skill_set.split(",")],
        "resume_filename": resume.filename
    }

    candidates.append(new_candidate)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Candidate created successfully",
            "candidate_id": candidate_id
        }
    )


# ---------------------------
# List & Filter Candidates
# ---------------------------
@app.get("/candidates", response_model=List[CandidateResponse])
def list_candidates(
    skill: Optional[str] = Query(None),
    experience: Optional[float] = Query(None, ge=0),
    graduation_year: Optional[int] = Query(None)
):
    result = candidates

    if skill:
        result = [
            c for c in result
            if skill.lower() in [s.lower() for s in c["skill_set"]]
        ]

    if experience is not None:
        result = [
            c for c in result
            if c["years_of_experience"] >= experience
        ]

    if graduation_year is not None:
        result = [
            c for c in result
            if c["graduation_year"] == graduation_year
        ]

    return result


# ---------------------------
# Get Candidate by ID
# ---------------------------
@app.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: str):
    for candidate in candidates:
        if candidate["id"] == candidate_id:
            return candidate

    raise HTTPException(status_code=404, detail="Candidate not found")


# ---------------------------
# Delete Candidate
# ---------------------------
@app.delete("/candidates/{candidate_id}", status_code=200)
def delete_candidate(candidate_id: str):
    for index, candidate in enumerate(candidates):
        if candidate["id"] == candidate_id:
            candidates.pop(index)
            return {"message": "Candidate deleted successfully"}

    raise HTTPException(status_code=404, detail="Candidate not found")
