from fastapi import APIRouter, HTTPException
from database import db
from models.section import Section
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_section(section: Section):
    department = await db.departments.find_one({"_id": ObjectId(section.department)})
    if not department:
        raise HTTPException(status_code=400, detail="Department does not exist")

    existing = await db.sections.find_one({
        "department": section.department,
        "year": section.year,
        "semester": section.semester,
        "sectionName": section.sectionName
    })
    if existing:
        raise HTTPException(status_code=409, detail="This section already exists for the selected department, year, and semester.")

    result = await db.sections.insert_one(section.dict())
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_sections():
    sections = await db.sections.find().to_list(200)
    for s in sections:
        s["_id"] = str(s["_id"])
        try:
            department = await db.departments.find_one({"_id": ObjectId(s["department"])})
            if department:
                department["_id"] = str(department["_id"])
                s["departmentDetails"] = department
        except Exception:
            s["departmentDetails"] = None
    sections.sort(key=lambda s: (s.get("year", 0), (s.get("departmentDetails") or {}).get("name", ""), s.get("sectionName", "")))
    return sections

@router.get("/{id}")
async def get_section(id: str):
    section = await db.sections.find_one({"_id": ObjectId(id)})
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    section["_id"] = str(section["_id"])
    return section

@router.put("/{id}")
async def update_section(id: str, section: Section):
    result = await db.sections.update_one({"_id": ObjectId(id)}, {"$set": section.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"message": "Updated"}

@router.delete("/{id}")
async def delete_section(id: str):
    result = await db.sections.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"message": "Deleted"}