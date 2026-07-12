from fastapi import APIRouter, HTTPException
from database import db
from bson import ObjectId
import json
import os
from datetime import datetime

router = APIRouter()

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "Database", "attendance_data.json")

@router.post("/load-dataset")
async def load_dataset():
    if not os.path.exists(JSON_PATH):
        raise HTTPException(status_code=404, detail="attendance_data.json not found at Database/")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    await db.attendance.delete_many({})
    await db.alert_logs.delete_many({})
    await db.students.delete_many({})
    await db.timetable.delete_many({})
    await db.curriculum.delete_many({})
    await db.sections.delete_many({})
    await db.subjects.delete_many({})
    await db.departments.delete_many({})

    meta = data.get("institution_metadata", {})
    year_val = 2
    semester_val = 3

    existing_degree = await db.degrees.find_one({"name": "B.Tech"})
    if not existing_degree:
        result = await db.degrees.insert_one({"name": "B.Tech", "durationYears": 4})
        degree_id = str(result.inserted_id)
    else:
        degree_id = str(existing_degree["_id"])

    # Create subjects from master registry
    course_registry = data.get("master_course_faculty_registry", [])
    subject_map = {}
    for course in course_registry:
        code = course.get("course_code", "")
        name = course.get("course_name", course.get("power_electronics", ""))
        credits = course.get("lecture_credits", 0)
        existing = await db.subjects.find_one({"subjectCode": code})
        if not existing:
            result = await db.subjects.insert_one({
                "subjectCode": code,
                "subjectName": name,
                "credits": credits,
                "facultyCode": course.get("faculty_code", ""),
                "facultyName": course.get("faculty_name", "")
            })
            subject_map[code] = str(result.inserted_id)
        else:
            subject_map[code] = str(existing["_id"])

    # Create departments and sections
    classes = data.get("classes", [])
    dept_map = {}
    section_map = {}

    for cls in classes:
        dept_name = cls.get("department", "")
        section_letter = cls.get("section", "")
        strength = len(cls.get("students", []))

        if dept_name not in dept_map:
            existing_dept = await db.departments.find_one({"name": dept_name, "degree": degree_id})
            if not existing_dept:
                result = await db.departments.insert_one({
                    "name": dept_name,
                    "degree": degree_id
                })
                dept_map[dept_name] = str(result.inserted_id)
            else:
                dept_map[dept_name] = str(existing_dept["_id"])

        dept_id = dept_map[dept_name]
        section_result = await db.sections.insert_one({
            "department": dept_id,
            "year": year_val,
            "semester": semester_val,
            "sectionName": section_letter,
            "strength": strength,
            "subjectProfessor": None
        })
        section_id = str(section_result.inserted_id)
        section_map[cls["class_id"]] = section_id

        # Create curriculum entries from weekly timetable
        tt = cls.get("weekly_timetable", {})
        seen_codes = set()
        for day, slots in tt.items():
            for slot in slots:
                code = slot.get("code", "")
                if code and code in subject_map and code not in seen_codes:
                    seen_codes.add(code)
                    subj_id = subject_map[code]
                    existing_curr = await db.curriculum.find_one({
                        "department": dept_id,
                        "year": year_val,
                        "semester": semester_val,
                        "subject": subj_id
                    })
                    if not existing_curr:
                        await db.curriculum.insert_one({
                            "department": dept_id,
                            "year": year_val,
                            "semester": semester_val,
                            "subject": subj_id
                        })

        # Create students
        students_data = cls.get("students", [])
        for stu in students_data:
            existing_stu = await db.students.find_one({"rollNo": stu["student_id"]})
            if not existing_stu:
                stu_doc = {
                    "rollNo": stu["student_id"],
                    "name": stu["name"],
                    "email": stu.get("email", ""),
                    "phone": "",
                    "department": dept_id,
                    "section": section_id,
                    "year": year_val,
                    "semester": semester_val
                }
                stu_result = await db.students.insert_one(stu_doc)
                student_oid = stu_result.inserted_id

                # Create attendance records
                for att in stu.get("subject_wise_attendance", []):
                    att_code = att.get("course_code", "")
                    if att_code in subject_map:
                        total = att.get("classes_conducted", 0)
                        attended = att.get("classes_attended", 0)
                        pct = att.get("attendance_percentage", 0.0)
                        if total > 0:
                            pct = round((attended / total) * 100, 2)
                        await db.attendance.insert_one({
                            "student": student_oid,
                            "subject": ObjectId(subject_map[att_code]),
                            "section": ObjectId(section_id),
                            "totalClasses": total,
                            "attendedClasses": attended,
                            "percentage": pct,
                            "lastUpdated": datetime.now()
                        })

    summary = {
        "subjects": len(subject_map),
        "departments": len(dept_map),
        "sections": len(section_map),
        "students": await db.students.count_documents({}),
        "attendanceRecords": await db.attendance.count_documents({}),
        "curriculumEntries": await db.curriculum.count_documents({})
    }

    return {"message": "Dataset loaded successfully", "summary": summary}
