from fastapi import APIRouter, HTTPException
from database import db
from passlib.hash import bcrypt
from bson import ObjectId

router = APIRouter()

@router.post("/login")
async def login(data: dict):
    username = data.get("username", "").strip()
    password = data.get("password", "")

    teacher = await db.teachers.find_one({"username": username})
    if not teacher:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not bcrypt.verify(password, teacher["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "_id": str(teacher["_id"]),
        "username": teacher["username"],
        "isAdmin": teacher.get("isAdmin", False)
    }
