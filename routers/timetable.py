from fastapi import APIRouter, HTTPException
from database import db
from models.timetable import Timetable
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_timetable_slot(slot: Timetable):
    section = await db.sections.find_one({"_id": ObjectId(slot.section)})
    if not section:
        raise HTTPException(status_code=400, detail="Section does not exist")

    curriculum = await db.curriculum.find_one({"_id": ObjectId(slot.curriculum)})
    if not curriculum:
        raise HTTPException(status_code=400, detail="Curriculum entry does not exist")

    existing = await db.timetable.find_one({
        "section": slot.section,
        "dayOfWeek": slot.dayOfWeek,
        "period": slot.period
    })
    if existing:
        raise HTTPException(status_code=409, detail="This section already has a class scheduled in this period")

    result = await db.timetable.insert_one(slot.dict())
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_timetable():
    slots = await db.timetable.find().to_list(1000)
    for s in slots:
        s["_id"] = str(s["_id"])
        try:
            curriculum = await db.curriculum.find_one({"_id": ObjectId(s["curriculum"])})
            if curriculum:
                subject = await db.subjects.find_one({"_id": ObjectId(curriculum["subject"])})
                if subject:
                    s["subjectName"] = subject["subjectName"]
        except Exception:
            s["subjectName"] = None
    return slots

@router.get("/section/{section_id}")
async def get_section_timetable(section_id: str):
    slots = await db.timetable.find({"section": section_id}).to_list(100)
    result = []
    for s in slots:
        s["_id"] = str(s["_id"])
        curriculum = await db.curriculum.find_one({"_id": ObjectId(s["curriculum"])})
        if curriculum:
            subject = await db.subjects.find_one({"_id": ObjectId(curriculum["subject"])})
            if subject:
                s["subjectName"] = subject["subjectName"]
                s["subjectCode"] = subject["subjectCode"]
        timing = await db.period_timings.find_one({"period": s["period"]})
        if timing:
            s["startTime"] = timing["startTime"]
            s["endTime"] = timing["endTime"]
        result.append(s)
    return result


@router.get("/section/{section_id}/subject/{subject_id}/frequency")
async def get_subject_frequency(section_id: str, subject_id: str):
    curricula = await db.curriculum.find({"subject": subject_id}).to_list(50)
    curriculum_ids = [str(c["_id"]) for c in curricula]
    count = await db.timetable.count_documents({
        "section": section_id,
        "curriculum": {"$in": curriculum_ids}
    })
    return {"section": section_id, "subject": subject_id, "classesPerWeek": count}

@router.delete("/{id}")
async def delete_timetable_slot(id: str):
    result = await db.timetable.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Timetable slot not found")
    return {"message": "Deleted"}