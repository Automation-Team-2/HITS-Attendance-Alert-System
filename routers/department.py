from fastapi import APIRouter, HTTPException
from database import db
from models.department import Department
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_department(department: Department):
    degree = await db.degrees.find_one({"_id": ObjectId(department.degree)})
    if not degree:
        raise HTTPException(status_code=400, detail="Degree does not exist")

    existing = await db.departments.find_one({"name": department.name, "degree": department.degree})
    if existing:
        raise HTTPException(status_code=409, detail="This department already exists for this degree")

    result = await db.departments.insert_one(department.dict())
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_departments():
    departments = await db.departments.find().to_list(100)
    for d in departments:
        d["_id"] = str(d["_id"])
        try:
            degree = await db.degrees.find_one({"_id": ObjectId(d["degree"])})
            if degree:
                degree["_id"] = str(degree["_id"])
                d["degreeDetails"] = degree
        except Exception:
            d["degreeDetails"] = None
    return departments

@router.get("/{id}")
async def get_department(id: str):
    department = await db.departments.find_one({"_id": ObjectId(id)})
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    department["_id"] = str(department["_id"])
    return department

@router.put("/{id}")
async def update_department(id: str, department: Department):
    result = await db.departments.update_one({"_id": ObjectId(id)}, {"$set": department.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Updated"}

@router.delete("/{id}")
async def delete_department(id: str):
    result = await db.departments.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"message": "Deleted"}