from fastapi import APIRouter, HTTPException
from database import db
from models.teacher_subject import TeacherSubject
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_assignment(ts: TeacherSubject):
    teacher = await db.teachers.find_one({"_id": ObjectId(ts.teacher)})
    if not teacher:
        raise HTTPException(status_code=400, detail="Teacher does not exist")
    section = await db.sections.find_one({"_id": ObjectId(ts.section)})
    if not section:
        raise HTTPException(status_code=400, detail="Section does not exist")
    subject = await db.subjects.find_one({"_id": ObjectId(ts.subject)})
    if not subject:
        raise HTTPException(status_code=400, detail="Subject does not exist")
    existing = await db.teacher_subjects.find_one({
        "teacher": ts.teacher,
        "section": ts.section,
        "subject": ts.subject
    })
    if existing:
        raise HTTPException(status_code=409, detail="This assignment already exists")
    result = await db.teacher_subjects.insert_one(ts.dict())
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_assignments(teacher: str | None = None):
    query = {}
    if teacher:
        query["teacher"] = teacher
    assignments = await db.teacher_subjects.find(query).to_list(200)
    enriched = []
    for a in assignments:
        a["_id"] = str(a["_id"])
        section = await db.sections.find_one({"_id": ObjectId(a["section"])})
        if section:
            dept = await db.departments.find_one({"_id": ObjectId(section["department"])})
            section["_id"] = str(section["_id"])
            if dept:
                dept["_id"] = str(dept["_id"])
                section["departmentDetails"] = dept
            a["sectionDetails"] = section
        subject = await db.subjects.find_one({"_id": ObjectId(a["subject"])})
        if subject:
            subject["_id"] = str(subject["_id"])
            a["subjectDetails"] = subject
        teacher = await db.teachers.find_one({"_id": ObjectId(a["teacher"])})
        if teacher:
            teacher["_id"] = str(teacher["_id"])
            if "password_hash" in teacher:
                del teacher["password_hash"]
            a["teacherDetails"] = teacher
        enriched.append(a)
    return enriched

@router.delete("/{id}")
async def delete_assignment(id: str):
    result = await db.teacher_subjects.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {"message": "Deleted"}
