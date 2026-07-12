from fastapi import APIRouter, HTTPException, Query
from database import db
from models.alert_log import AlertLog
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/send")
async def send_alert(data: dict):
    student_id = data.get("studentId")
    subject_id = data.get("subjectId")
    section_id = data.get("sectionId")

    if not student_id:
        raise HTTPException(status_code=400, detail="studentId is required")

    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    phone = student.get("phone", "")
    student_name = student.get("name", "Unknown")

    subject_name = "Unknown"
    if subject_id:
        subject = await db.subjects.find_one({"_id": ObjectId(subject_id)})
        subject_name = subject.get("subjectName", "Unknown") if subject else "Unknown"

    section_name = ""
    if section_id:
        section = await db.sections.find_one({"_id": ObjectId(section_id)})
        section_name = section.get("sectionName", "") if section else ""

    attendance_pct = 0.0
    att_query = {"student": ObjectId(student_id)}
    if subject_id:
        att_query["subject"] = ObjectId(subject_id)
    attendance_rec = await db.attendance.find_one(att_query)
    if attendance_rec:
        attendance_pct = attendance_rec["percentage"]

    alert_entry = {
        "student": student_id,
        "studentName": student_name,
        "subject": subject_id or "",
        "subjectName": subject_name,
        "section": section_id or "",
        "sectionName": section_name,
        "attendancePercentage": attendance_pct,
        "recipientPhone": phone,
        "channel": "whatsapp",
        "status": "pending" if phone else "failed",
        "sentAt": datetime.now(),
        "errorMessage": None if phone else "No phone number on record"
    }

    if phone:
        from services.messaging_service import send_alert as send_msg, build_alert_message
        message = build_alert_message(student_name, subject_name, section_name, attendance_pct)
        success = await send_msg(phone, message)
        alert_entry["status"] = "sent" if success else "failed"
        if not success:
            alert_entry["errorMessage"] = "Messaging API call failed"

    result = await db.alert_logs.insert_one(alert_entry)

    return {
        "id": str(result.inserted_id),
        "studentName": student_name,
        "phone": phone,
        "status": alert_entry["status"]
    }

@router.get("/history")
async def get_alert_history(
    student: str | None = Query(None),
    section: str | None = Query(None),
    limit: int = Query(100, le=500)
):
    query = {}
    if student:
        query["student"] = student
    if section:
        query["section"] = section

    logs = await db.alert_logs.find(query).sort("sentAt", -1).to_list(limit)
    for log in logs:
        log["_id"] = str(log["_id"])
    return logs

@router.get("/stats")
async def get_alert_stats():
    total_alerts = await db.alert_logs.count_documents({})
    today_start = datetime.now().replace(hour=0, minute=0, second=0)
    today_alerts = await db.alert_logs.count_documents({"sentAt": {"$gte": today_start}})
    sent_alerts = await db.alert_logs.count_documents({"status": "sent"})
    failed_alerts = await db.alert_logs.count_documents({"status": "failed"})

    return {
        "totalAlerts": total_alerts,
        "todayAlerts": today_alerts,
        "sentAlerts": sent_alerts,
        "failedAlerts": failed_alerts
    }
