from fastapi import APIRouter, HTTPException
from database import db
from models.subject import Subject
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_subject(subject: Subject):
    existing = await db.subjects.find_one({"subjectCode": subject.subjectCode})
    if existing:
        raise HTTPException(status_code=409, detail="A subject with this code already exists")
    result = await db.subjects.insert_one(subject.dict())
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_subjects():
    subjects = await db.subjects.find().to_list(200)
    for s in subjects:
        s["_id"] = str(s["_id"])
    return subjects

@router.get("/{id}")
async def get_subject(id: str):
    subject = await db.subjects.find_one({"_id": ObjectId(id)})
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    subject["_id"] = str(subject["_id"])
    return subject

@router.put("/{id}")
async def update_subject(id: str, subject: Subject):
    result = await db.subjects.update_one({"_id": ObjectId(id)}, {"$set": subject.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Updated"}

@router.delete("/{id}")
async def delete_subject(id: str):
    result = await db.subjects.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Deleted"}