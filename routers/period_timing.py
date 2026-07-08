from fastapi import APIRouter, HTTPException
from database import db
from models.period_timing import PeriodTiming
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_period_timing(timing: PeriodTiming):
    existing = await db.period_timings.find_one({"period": timing.period})
    if existing:
        raise HTTPException(status_code=409, detail="Timing for this period already exists")
    result = await db.period_timings.insert_one(timing.dict())
    return {"id": str(result.inserted_id)}

@router.get("/")
async def get_period_timings():
    timings = await db.period_timings.find().sort("period", 1).to_list(20)
    for t in timings:
        t["_id"] = str(t["_id"])
    return timings