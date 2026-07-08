from fastapi import APIRouter, HTTPException
from database import db
from models.teacher import Teacher
from passlib.hash import bcrypt
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_teacher(teacher: Teacher):
    existing = await db.teachers.find_one({"username": teacher.username})
    if existing:
        raise HTTPException(status_code=409, detail="A teacher with this username already exists")
    result = await db.teachers.insert_one(teacher.dict())
    return {"id": str(result.inserted_id)}

@router.post("/seed")
async def seed_teacher(data: dict):
    username = data.get("username")
    password = data.get("password")
    isAdmin = data.get("isAdmin", False)
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    existing = await db.teachers.find_one({"username": username})
    if existing:
        raise HTTPException(status_code=409, detail="Already exists")
    hashed = bcrypt.hash(password)
    result = await db.teachers.insert_one({
        "username": username,
        "password_hash": hashed,
        "isAdmin": isAdmin
    })
    return {"id": str(result.inserted_id), "username": username, "isAdmin": isAdmin}

@router.get("/")
async def get_teachers():
    teachers = await db.teachers.find().to_list(100)
    for t in teachers:
        t["_id"] = str(t["_id"])
        del t["password_hash"]
    return teachers

@router.get("/{id}")
async def get_teacher(id: str):
    teacher = await db.teachers.find_one({"_id": ObjectId(id)})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    teacher["_id"] = str(teacher["_id"])
    del teacher["password_hash"]
    return teacher

@router.delete("/{id}")
async def delete_teacher(id: str):
    result = await db.teachers.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Deleted"}
