from fastapi import APIRouter, HTTPException, Query
from database import db
from models.student import Student
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_student(student: Student):
    existing = await db.students.find_one({"rollNo": student.rollNo})
    if existing:
        raise HTTPException(status_code=409, detail="A student with this roll number already exists.")

    section = await db.sections.find_one({"_id": ObjectId(student.section)})
    if not section:
        raise HTTPException(status_code=400, detail="Section does not exist")

    result = await db.students.insert_one(student.dict())
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_students(section: str | None = Query(None)):
    query = {}
    if section:
        query["section"] = section
    students = await db.students.find(query).to_list(200)
    for s in students:
        s["_id"] = str(s["_id"])
        sectionDoc = await db.sections.find_one({"_id": ObjectId(s["section"])})
        if sectionDoc:
            sectionDoc["_id"] = str(sectionDoc["_id"])
            s["sectionDetails"] = sectionDoc
    students.sort(key=lambda s: s.get("rollNo", ""))
    return students

@router.get("/{id}")
async def get_student(id: str):
    student = await db.students.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student["_id"] = str(student["_id"])
    return student

@router.put("/{id}")
async def update_student(id: str, student: Student):
    result = await db.students.update_one({"_id": ObjectId(id)}, {"$set": student.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Updated"}

@router.delete("/{id}")
async def delete_student(id: str):
    result = await db.students.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Deleted"}