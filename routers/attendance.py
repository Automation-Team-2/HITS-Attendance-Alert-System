from fastapi import APIRouter, HTTPException, Query
from database import db
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/section/{section_id}")
async def get_section_attendance(section_id: str):
    section = await db.sections.find_one({"_id": ObjectId(section_id)})
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    students = await db.students.find({"section": section_id}).to_list(200)

    result = []
    for stu in students:
        stu_id = stu["_id"]
        attendance_records = await db.attendance.find(
            {"student": stu_id, "section": ObjectId(section_id)}
        ).to_list(200)

        overall_pct = 0.0
        subject_breakdown = []
        total_attended = 0
        total_classes = 0

        for rec in attendance_records:
            subject = await db.subjects.find_one({"_id": rec["subject"]})
            subject_name = subject.get("subjectName", "Unknown") if subject else "Unknown"
            subject_breakdown.append({
                "subjectId": str(rec["subject"]),
                "subjectName": subject_name,
                "totalClasses": rec["totalClasses"],
                "attendedClasses": rec["attendedClasses"],
                "percentage": rec["percentage"]
            })
            total_attended += rec["attendedClasses"]
            total_classes += rec["totalClasses"]

        if total_classes > 0:
            overall_pct = round((total_attended / total_classes) * 100, 2)

        result.append({
            "id": str(stu_id),
            "rollNo": stu.get("rollNo", ""),
            "name": stu.get("name", ""),
            "email": stu.get("email", ""),
            "phone": stu.get("phone", ""),
            "overallAttendance": overall_pct,
            "isAtRisk": overall_pct < 75.0,
            "subjects": subject_breakdown
        })

    result.sort(key=lambda s: s["rollNo"])
    return result

@router.get("/student/{student_id}")
async def get_student_attendance(student_id: str):
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    attendance_records = await db.attendance.find(
        {"student": ObjectId(student_id)}
    ).to_list(200)

    subjects = []
    total_attended = 0
    total_classes = 0

    for rec in attendance_records:
        subject = await db.subjects.find_one({"_id": rec["subject"]})
        subject_name = subject.get("subjectName", "Unknown") if subject else "Unknown"
        subjects.append({
            "subjectId": str(rec["subject"]),
            "subjectName": subject_name,
            "totalClasses": rec["totalClasses"],
            "attendedClasses": rec["attendedClasses"],
            "percentage": rec["percentage"]
        })
        total_attended += rec["attendedClasses"]
        total_classes += rec["totalClasses"]

    overall_pct = round((total_attended / total_classes) * 100, 2) if total_classes > 0 else 0.0

    return {
        "id": str(student["_id"]),
        "rollNo": student.get("rollNo", ""),
        "name": student.get("name", ""),
        "email": student.get("email", ""),
        "phone": student.get("phone", ""),
        "overallAttendance": overall_pct,
        "isAtRisk": overall_pct < 75.0,
        "subjects": subjects
    }

@router.get("/risk")
async def get_risk_students(section: str | None = Query(None)):
    query = {"percentage": {"$lt": 75.0}}
    if section:
        query["section"] = ObjectId(section)

    at_risk = await db.attendance.find(query).to_list(2000)

    seen = set()
    result = []
    for rec in at_risk:
        stu_id = str(rec["student"])
        if stu_id in seen:
            continue
        seen.add(stu_id)

        student = await db.students.find_one({"_id": rec["student"]})
        if not student:
            continue

        subject = await db.subjects.find_one({"_id": rec["subject"]})
        section_doc = await db.sections.find_one({"_id": rec["section"]})

        result.append({
            "studentId": stu_id,
            "rollNo": student.get("rollNo", ""),
            "name": student.get("name", ""),
            "phone": student.get("phone", ""),
            "subjectId": str(rec["subject"]),
            "subjectName": subject.get("subjectName", "Unknown") if subject else "Unknown",
            "sectionId": str(rec["section"]),
            "sectionName": section_doc.get("sectionName", "") if section_doc else "",
            "attendancePercentage": rec["percentage"]
        })

    return result
