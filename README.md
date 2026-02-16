# Mini Resume Management API

## Python Version
Python 3.10

## Project Overview
This project is a REST API built using FastAPI that allows:

- Resume upload (PDF/DOC/DOCX)
- Candidate metadata storage
- Filtering by skill, experience, and graduation year
- Fetching candidate by ID
- Deleting candidate
- Health check endpoint

Data is stored in memory (no database used).

---

## Installation Steps

1. Clone repository
   git clone <your-repo-url>

2. Navigate into folder
   cd miniresume-neethu-benny

3. Install dependencies
   python -m pip install -r requirements.txt

---

## Run Application

python -m uvicorn main:app --reload

API Base URL:
http://127.0.0.1:8000

Swagger Documentation:
http://127.0.0.1:8000/docs

---

## Example API Usage

### Health Check
GET /health

Response:
{
  "status": "ok"
}

---

### Create Candidate
POST /candidates

Form Data:
- full_name
- dob (YYYY-MM-DD)
- contact_number
- contact_address
- education_qualification
- graduation_year
- years_of_experience
- skill_set (comma separated)
- resume (file upload)

Response:
{
  "message": "Candidate created successfully",
  "candidate_id": "generated-uuid"
}

---

### List Candidates
GET /candidates

Optional Query Parameters:
- skill
- experience
- graduation_year

Example:
GET /candidates?skill=python&experience=2

---

### Get Candidate by ID
GET /candidates/{candidate_id}

---

### Delete Candidate
DELETE /candidates/{candidate_id}
