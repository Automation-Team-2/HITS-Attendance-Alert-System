from fastapi import APIRouter
from database import db
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats():
    total_students = await db.students.count_documents({})
    total_sections = await db.sections.count_documents({})

    at_risk_count = 0
    students_cursor = db.students.find({})
    async for student in students_cursor:
        attendance_records = await db.attendance.find(
            {"student": student["_id"]}
        ).to_list(200)
        total_attended = sum(r["attendedClasses"] for r in attendance_records)
        total_classes = sum(r["totalClasses"] for r in attendance_records)
        if total_classes > 0:
            pct = (total_attended / total_classes) * 100
            if pct < 75:
                at_risk_count += 1

    week_ago = datetime.now() - timedelta(days=7)
    alerts_this_week = await db.alert_logs.count_documents(
        {"sentAt": {"$gte": week_ago}}
    )

    attendance_agg = await db.attendance.aggregate([
        {"$group": {
            "_id": None,
            "totalClassesSum": {"$sum": "$totalClasses"},
            "attendedClassesSum": {"$sum": "$attendedClasses"}
        }}
    ]).to_list(1)

    avg_attendance = 0.0
    if attendance_agg and attendance_agg[0]["totalClassesSum"] > 0:
        avg_attendance = round(
            (attendance_agg[0]["attendedClassesSum"] / attendance_agg[0]["totalClassesSum"]) * 100,
            2
        )

    recent_alerts = await db.alert_logs.find().sort("sentAt", -1).limit(5).to_list(5)
    for a in recent_alerts:
        a["_id"] = str(a["_id"])

    return {
        "totalStudents": total_students,
        "totalSections": total_sections,
        "studentsBelow75": at_risk_count,
        "alertsThisWeek": alerts_this_week,
        "averageAttendance": avg_attendance,
        "recentAlerts": recent_alerts
    }
