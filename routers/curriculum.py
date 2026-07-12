from fastapi import APIRouter, HTTPException
from database import db
from models.curriculum import Curriculum
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_curriculum(entry: Curriculum):
    department = await db.departments.find_one({"_id": ObjectId(entry.department)})
    if not department:
        raise HTTPException(status_code=400, detail="Department does not exist")

    subject = await db.subjects.find_one({"_id": ObjectId(entry.subject)})
    if not subject:
        raise HTTPException(status_code=400, detail="Subject does not exist")

    existing = await db.curriculum.find_one({
        "department": entry.department,
        "year": entry.year,
        "semester": entry.semester,
        "subject": entry.subject
    })
    if existing:
        raise HTTPException(status_code=409, detail="This subject is already mapped to this department/year/semester")

    result = await db.curriculum.insert_one(entry.dict())
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_curriculum():
    entries = await db.curriculum.find().to_list(500)
    for e in entries:
        e["_id"] = str(e["_id"])
        try:
            subject = await db.subjects.find_one({"_id": ObjectId(e["subject"])})
            if subject:
                subject["_id"] = str(subject["_id"])
                e["subjectDetails"] = subject
        except Exception:
            e["subjectDetails"] = None
    return entries

@router.get("/lookup")
async def get_subjects_for(department: str, year: int, semester: int):
    entries = await db.curriculum.find({
        "department": department,
        "year": year,
        "semester": semester
    }).to_list(100)
    subjects = []
    for e in entries:
        subject = await db.subjects.find_one({"_id": ObjectId(e["subject"])})
        if subject:
            subject["_id"] = str(subject["_id"])
            subjects.append(subject)
    return subjects