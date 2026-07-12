from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import db
from datetime import datetime, time

scheduler = AsyncIOScheduler()

async def daily_attendance_scan():
    print(f"[Scheduler] Daily attendance scan started at {datetime.now()}")
    try:
        risk_threshold = 75.0
        at_risk = await db.attendance.find(
            {"percentage": {"$lt": risk_threshold}}
        ).to_list(5000)

        print(f"[Scheduler] Found {len(at_risk)} at-risk records")

        for record in at_risk:
            student = await db.students.find_one({"_id": record["student"]})
            subject = await db.subjects.find_one({"_id": record["subject"]})
            section = await db.sections.find_one({"_id": record["section"]})

            if not student or not subject:
                continue

            student_name = student.get("name", "Unknown")
            subject_name = subject.get("subjectName", "Unknown")
            section_name = section.get("sectionName", "") if section else ""
            phone = student.get("phone", "")

            existing_alert = await db.alert_logs.find_one({
                "student": str(record["student"]),
                "subject": str(record["subject"]),
                "status": "sent",
                "sentAt": {"$gte": datetime.now().replace(hour=0, minute=0, second=0)}
            })

            if existing_alert:
                continue

            alert_entry = {
                "student": str(record["student"]),
                "studentName": student_name,
                "subject": str(record["subject"]),
                "subjectName": subject_name,
                "section": str(record["section"]),
                "sectionName": section_name,
                "attendancePercentage": record["percentage"],
                "recipientPhone": phone,
                "channel": "whatsapp",
                "status": "pending" if phone else "failed",
                "sentAt": datetime.now(),
                "errorMessage": None if phone else "No phone number on record"
            }

            if phone:
                from services.messaging_service import send_alert, build_alert_message
                message = build_alert_message(student_name, subject_name, section_name, record["percentage"])
                success = await send_alert(phone, message)
                alert_entry["status"] = "sent" if success else "failed"
                if not success:
                    alert_entry["errorMessage"] = "API call failed"

            await db.alert_logs.insert_one(alert_entry)

        print(f"[Scheduler] Daily scan completed - {len(at_risk)} records processed")

    except Exception as e:
        print(f"[Scheduler] Error during daily scan: {e}")

def start_scheduler():
    scheduler.add_job(
        daily_attendance_scan,
        "cron",
        hour=17,
        minute=0,
        id="daily_attendance_scan",
        replace_existing=True
    )
    scheduler.start()
    print("[Scheduler] Started - daily scan scheduled for 17:00")
