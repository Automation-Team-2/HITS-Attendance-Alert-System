from fastapi import APIRouter, HTTPException
from database import db
from models.degree import Degree
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_degree(degree: Degree):
    existing = await db.degrees.find_one({"name": degree.name})
    if existing:
        raise HTTPException(status_code=409, detail="This degree already exists")
    result = await db.degrees.insert_one(degree.dict())
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_degrees():
    degrees = await db.degrees.find().to_list(100)
    for d in degrees:
        d["_id"] = str(d["_id"])
    return degrees

@router.get("/{id}")
async def get_degree(id: str):
    degree = await db.degrees.find_one({"_id": ObjectId(id)})
    if not degree:
        raise HTTPException(status_code=404, detail="Degree not found")
    degree["_id"] = str(degree["_id"])
    return degree

@router.put("/{id}")
async def update_degree(id: str, degree: Degree):
    result = await db.degrees.update_one({"_id": ObjectId(id)}, {"$set": degree.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Degree not found")
    return {"message": "Updated"}

@router.delete("/{id}")
async def delete_degree(id: str):
    result = await db.degrees.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Degree not found")
    return {"message": "Deleted"}