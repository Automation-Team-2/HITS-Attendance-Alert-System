from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="HITS Attendance Alert System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Models ──────────────────────────────────────────────────────────────────

class Student(BaseModel):
    roll: str
    name: str
    contact: str
    attendance: int


class Section(BaseModel):
    name: str
    description: str = ""


# ─── In-memory database ──────────────────────────────────────────────────────

students_db: dict[str, Student] = {}
sections_db: dict[str, Section] = {}

student_counter = 0
section_counter = 0


# ─── Students Router ─────────────────────────────────────────────────────────

@app.get("/api/students/")
def get_all_students():
    return list(students_db.values())


@app.post("/api/students/")
def create_student(student: Student):
    global student_counter
    student_counter += 1
    student_id = str(student_counter)
    students_db[student_id] = student
    return {"id": student_id, **student.model_dump()}


@app.get("/api/students/{student_id}")
def get_student(student_id: str):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"id": student_id, **students_db[student_id].model_dump()}


@app.put("/api/students/{student_id}")
def update_student(student_id: str, student: Student):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    students_db[student_id] = student
    return {"id": student_id, **student.model_dump()}


@app.delete("/api/students/{student_id}")
def delete_student(student_id: str):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    return {"detail": "Student deleted"}


# ─── Sections Router ─────────────────────────────────────────────────────────

@app.get("/api/sections/")
def get_all_sections():
    return list(sections_db.values())


@app.post("/api/sections/")
def create_section(section: Section):
    global section_counter
    section_counter += 1
    section_id = str(section_counter)
    sections_db[section_id] = section
    return {"id": section_id, **section.model_dump()}


@app.get("/api/sections/{section_id}")
def get_section(section_id: str):
    if section_id not in sections_db:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"id": section_id, **sections_db[section_id].model_dump()}


@app.put("/api/sections/{section_id}")
def update_section(section_id: str, section: Section):
    if section_id not in sections_db:
        raise HTTPException(status_code=404, detail="Section not found")
    sections_db[section_id] = section
    return {"id": section_id, **section.model_dump()}


@app.delete("/api/sections/{section_id}")
def delete_section(section_id: str):
    if section_id not in sections_db:
        raise HTTPException(status_code=404, detail="Section not found")
    del sections_db[section_id]
    return {"detail": "Section deleted"}


# ─── Seed Endpoint ───────────────────────────────────────────────────────────

@app.post("/api/seed/")
def seed_data():
    global student_counter, section_counter

    sections_db.clear()
    students_db.clear()
    student_counter = 0
    section_counter = 0

    section_records = [
        {"name": "B.Tech CSE", "description": "Branch: Computer Science & Engineering"},
        {"name": "B.Tech AERO", "description": "Branch: Aerospace Engineering"},
        {"name": "B.Tech IT", "description": "Branch: Information Technology"},
    ]

    student_records = [
        {"roll": "26CU0310001", "name": "Naveen", "contact": "9104332181", "attendance": 55},
        {"roll": "26CU0310002", "name": "Payal", "contact": "9600133890", "attendance": 62},
        {"roll": "26CU0310003", "name": "Preeti", "contact": "9386379402", "attendance": 48},
        {"roll": "26CU0310004", "name": "Lakshya", "contact": "9654235116", "attendance": 58},
        {"roll": "26CU0310005", "name": "Dhruv", "contact": "9559407816", "attendance": 65},
        {"roll": "26CU0310006", "name": "Kabir", "contact": "9849593103", "attendance": 52},
        {"roll": "26CU0310007", "name": "Vanshika", "contact": "9413164752", "attendance": 60},
        {"roll": "26CU0310008", "name": "Tanish", "contact": "9534192832", "attendance": 45},
        {"roll": "26CU0310009", "name": "Suman", "contact": "9648350305", "attendance": 92},
        {"roll": "26CU0310010", "name": "Pallavi", "contact": "9413953767", "attendance": 88},
        {"roll": "26CU0310011", "name": "Devansh", "contact": "9423884969", "attendance": 95},
        {"roll": "26CU0310012", "name": "Raghav", "contact": "9328710122", "attendance": 90},
        {"roll": "26AU0310001", "name": "Shreya", "contact": "9687234309", "attendance": 63},
        {"roll": "26AU0310002", "name": "Ritika", "contact": "9805009788", "attendance": 50},
        {"roll": "26AU0310003", "name": "Ananya", "contact": "9081219136", "attendance": 57},
        {"roll": "26AU0310004", "name": "Sarthak", "contact": "9939909169", "attendance": 42},
        {"roll": "26AU0310005", "name": "Komal", "contact": "9854353462", "attendance": 68},
        {"roll": "26AU0310006", "name": "Tarun", "contact": "9475107991", "attendance": 55},
        {"roll": "26AU0310007", "name": "Ajay", "contact": "9384251354", "attendance": 47},
        {"roll": "26AU0310008", "name": "Vishal", "contact": "9498084124", "attendance": 61},
        {"roll": "26IT0310001", "name": "Rashi", "contact": "9579868727", "attendance": 59},
        {"roll": "26IT0310002", "name": "Namrata", "contact": "9434873471", "attendance": 53},
        {"roll": "26IT0310003", "name": "Pooja", "contact": "9455812236", "attendance": 66},
        {"roll": "26IT0310004", "name": "Harsh", "contact": "9316658760", "attendance": 44},
        {"roll": "26IT0310005", "name": "Ritu", "contact": "9690967054", "attendance": 87},
        {"roll": "26IT0310006", "name": "Tanya", "contact": "9668893734", "attendance": 90},
    ]

    for s in section_records:
        section_counter += 1
        sections_db[str(section_counter)] = Section(**s)

    for s in student_records:
        student_counter += 1
        students_db[str(student_counter)] = Student(**s)

    return {
        "detail": "Database seeded",
        "sections": len(sections_db),
        "students": len(students_db),
    }
