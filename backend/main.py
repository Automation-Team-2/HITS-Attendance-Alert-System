"""
HITS Attendance Alert System — FastAPI Data API
Runs on port 8001. Django serves pages on 8000.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="HITS Attendance Alert System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", "*"],
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


# ─── Students CRUD ───────────────────────────────────────────────────────────

@app.get("/api/students/")
def get_all_students():
    return [
        {"id": sid, **s.model_dump()}
        for sid, s in students_db.items()
    ]


@app.post("/api/students/")
def create_student(student: Student):
    global student_counter
    student_counter += 1
    sid = str(student_counter)
    students_db[sid] = student
    return {"id": sid, **student.model_dump()}


@app.get("/api/students/{student_id}")
def get_student(student_id: str):
    if student_id not in students_db:
        raise HTTPException(404, "Student not found")
    return {"id": student_id, **students_db[student_id].model_dump()}


@app.put("/api/students/{student_id}")
def update_student(student_id: str, student: Student):
    if student_id not in students_db:
        raise HTTPException(404, "Student not found")
    students_db[student_id] = student
    return {"id": student_id, **student.model_dump()}


@app.delete("/api/students/{student_id}")
def delete_student(student_id: str):
    if student_id not in students_db:
        raise HTTPException(404, "Student not found")
    del students_db[student_id]
    return {"detail": "Student deleted"}


# ─── Sections CRUD ───────────────────────────────────────────────────────────

@app.get("/api/sections/")
def get_all_sections():
    return [
        {"id": sid, **s.model_dump()}
        for sid, s in sections_db.items()
    ]


@app.post("/api/sections/")
def create_section(section: Section):
    global section_counter
    section_counter += 1
    sid = str(section_counter)
    sections_db[sid] = section
    return {"id": sid, **section.model_dump()}


@app.get("/api/sections/{section_id}")
def get_section(section_id: str):
    if section_id not in sections_db:
        raise HTTPException(404, "Section not found")
    return {"id": section_id, **sections_db[section_id].model_dump()}


@app.put("/api/sections/{section_id}")
def update_section(section_id: str, section: Section):
    if section_id not in sections_db:
        raise HTTPException(404, "Section not found")
    sections_db[section_id] = section
    return {"id": section_id, **section.model_dump()}


@app.delete("/api/sections/{section_id}")
def delete_section(section_id: str):
    if section_id not in sections_db:
        raise HTTPException(404, "Section not found")
    del sections_db[section_id]
    return {"detail": "Section deleted"}


# ─── Dashboard Stats ─────────────────────────────────────────────────────────

@app.get("/api/stats/")
def get_stats():
    all_students = list(students_db.values())
    total = len(all_students)
    at_risk = [s for s in all_students if s.attendance < 75]
    at_risk_count = len(at_risk)
    avg_attendance = (
        round(sum(s.attendance for s in all_students) / total)
        if total else 0
    )

    class_counts = {}
    for s in all_students:
        if s.roll.startswith("26CU"):
            key = "B.Tech CSE"
        elif s.roll.startswith("26AU"):
            key = "B.Tech AERO"
        elif s.roll.startswith("26IT"):
            key = "B.Tech IT"
        else:
            key = "Other"
        class_counts[key] = class_counts.get(key, 0) + 1

    class_at_risk = {}
    for s in at_risk:
        if s.roll.startswith("26CU"):
            key = "B.Tech CSE"
        elif s.roll.startswith("26AU"):
            key = "B.Tech AERO"
        elif s.roll.startswith("26IT"):
            key = "B.Tech IT"
        else:
            key = "Other"
        class_at_risk[key] = class_at_risk.get(key, 0) + 1

    return {
        "total_students": total,
        "at_risk_count": at_risk_count,
        "avg_attendance": avg_attendance,
        "class_counts": class_counts,
        "class_at_risk": class_at_risk,
        "total_sections": len(sections_db),
    }


# ─── Seed Endpoint (full 80-student dataset) ────────────────────────────────

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
        # ── CSE (27) ──
        {"roll": "26CU0310001", "name": "Naveen",  "contact": "9104332181", "attendance": 55},
        {"roll": "26CU0310002", "name": "Payal",   "contact": "9600133890", "attendance": 62},
        {"roll": "26CU0310003", "name": "Preeti",  "contact": "9386379402", "attendance": 48},
        {"roll": "26CU0310004", "name": "Lakshya", "contact": "9654235116", "attendance": 58},
        {"roll": "26CU0310005", "name": "Dhruv",   "contact": "9559407816", "attendance": 65},
        {"roll": "26CU0310006", "name": "Kabir",   "contact": "9849593103", "attendance": 52},
        {"roll": "26CU0310007", "name": "Vanshika","contact": "9413164752", "attendance": 60},
        {"roll": "26CU0310008", "name": "Tanish",  "contact": "9534192832", "attendance": 45},
        {"roll": "26CU0310009", "name": "Suman",   "contact": "9648350305", "attendance": 92},
        {"roll": "26CU0310010", "name": "Pallavi", "contact": "9413953767", "attendance": 88},
        {"roll": "26CU0310011", "name": "Devansh", "contact": "9423884969", "attendance": 95},
        {"roll": "26CU0310012", "name": "Raghav",  "contact": "9328710122", "attendance": 90},
        {"roll": "26CU0310013", "name": "Girish",  "contact": "9691669784", "attendance": 87},
        {"roll": "26CU0310014", "name": "Sneha",   "contact": "9018451462", "attendance": 93},
        {"roll": "26CU0310015", "name": "Vidya",   "contact": "9048281489", "attendance": 78},
        {"roll": "26CU0310016", "name": "Saanvi",  "contact": "9252880957", "attendance": 82},
        {"roll": "26CU0310017", "name": "Aditya",  "contact": "9154303911", "attendance": 80},
        {"roll": "26CU0310018", "name": "Palak",   "contact": "9718227824", "attendance": 76},
        {"roll": "26CU0310019", "name": "Ravi",    "contact": "9963834657", "attendance": 79},
        {"roll": "26CU0310020", "name": "Sanjay",  "contact": "9713315098", "attendance": 83},
        {"roll": "26CU0310021", "name": "Anika",   "contact": "9930103105", "attendance": 75},
        {"roll": "26CU0310022", "name": "Rohan",   "contact": "9834738299", "attendance": 75},
        {"roll": "26CU0310023", "name": "Kunal",   "contact": "9376311656", "attendance": 75},
        {"roll": "26CU0310024", "name": "Snehal",  "contact": "9701065133", "attendance": 75},
        {"roll": "26CU0310025", "name": "Myra",    "contact": "9872624731", "attendance": 75},
        {"roll": "26CU0310026", "name": "Radhika", "contact": "9810801326", "attendance": 75},
        {"roll": "26CU0310027", "name": "Vikram",  "contact": "9736026064", "attendance": 75},
        # ── AERO (27) ──
        {"roll": "26AU0310001", "name": "Shreya",  "contact": "9687234309", "attendance": 63},
        {"roll": "26AU0310002", "name": "Ritika",  "contact": "9805009788", "attendance": 50},
        {"roll": "26AU0310003", "name": "Ananya",  "contact": "9081219136", "attendance": 57},
        {"roll": "26AU0310004", "name": "Sarthak", "contact": "9939909169", "attendance": 42},
        {"roll": "26AU0310005", "name": "Komal",   "contact": "9854353462", "attendance": 68},
        {"roll": "26AU0310006", "name": "Tarun",   "contact": "9475107991", "attendance": 55},
        {"roll": "26AU0310007", "name": "Ajay",    "contact": "9384251354", "attendance": 47},
        {"roll": "26AU0310008", "name": "Vishal",  "contact": "9498084124", "attendance": 61},
        {"roll": "26AU0310009", "name": "Yash",    "contact": "9182449353", "attendance": 89},
        {"roll": "26AU0310010", "name": "Sanya",   "contact": "9874016400", "attendance": 91},
        {"roll": "26AU0310011", "name": "Varun",   "contact": "9242786801", "attendance": 96},
        {"roll": "26AU0310012", "name": "Mohit",   "contact": "9280598262", "attendance": 88},
        {"roll": "26AU0310013", "name": "Sai",     "contact": "9450533158", "attendance": 94},
        {"roll": "26AU0310014", "name": "Nandini", "contact": "9356159514", "attendance": 87},
        {"roll": "26AU0310015", "name": "Isha",    "contact": "9232260256", "attendance": 77},
        {"roll": "26AU0310016", "name": "Aman",    "contact": "9433036541", "attendance": 81},
        {"roll": "26AU0310017", "name": "Nisha",   "contact": "9586850142", "attendance": 84},
        {"roll": "26AU0310018", "name": "Anjali",  "contact": "9401965569", "attendance": 76},
        {"roll": "26AU0310019", "name": "Manish",  "contact": "9169340608", "attendance": 82},
        {"roll": "26AU0310020", "name": "Neha",    "contact": "9421607337", "attendance": 79},
        {"roll": "26AU0310021", "name": "Deepak",  "contact": "9465648236", "attendance": 75},
        {"roll": "26AU0310022", "name": "Ayush",   "contact": "9299468044", "attendance": 75},
        {"roll": "26AU0310023", "name": "Aadhya",  "contact": "9699577738", "attendance": 75},
        {"roll": "26AU0310024", "name": "Diya",    "contact": "9148951343", "attendance": 75},
        {"roll": "26AU0310025", "name": "Vihaan",  "contact": "9037917693", "attendance": 75},
        {"roll": "26AU0310026", "name": "Juhi",    "contact": "9676320163", "attendance": 75},
        {"roll": "26AU0310027", "name": "Ishita",  "contact": "9870831727", "attendance": 75},
        # ── IT (26) ──
        {"roll": "26IT0310001", "name": "Rashi",     "contact": "9579868727", "attendance": 59},
        {"roll": "26IT0310002", "name": "Namrata",   "contact": "9434873471", "attendance": 53},
        {"roll": "26IT0310003", "name": "Pooja",     "contact": "9455812236", "attendance": 66},
        {"roll": "26IT0310004", "name": "Harsh",     "contact": "9316658760", "attendance": 44},
        {"roll": "26IT0310005", "name": "Ritu",      "contact": "9690967054", "attendance": 87},
        {"roll": "26IT0310006", "name": "Tanya",     "contact": "9668893734", "attendance": 90},
        {"roll": "26IT0310007", "name": "Bhavna",    "contact": "9706562729", "attendance": 88},
        {"roll": "26IT0310008", "name": "Divya",     "contact": "9990162720", "attendance": 92},
        {"roll": "26IT0310009", "name": "Nikhil",    "contact": "9375564641", "attendance": 86},
        {"roll": "26IT0310010", "name": "Sakshi",    "contact": "9805310033", "attendance": 95},
        {"roll": "26IT0310011", "name": "Rudra",     "contact": "9719374529", "attendance": 89},
        {"roll": "26IT0310012", "name": "Vaishnavi", "contact": "9124190496", "attendance": 91},
        {"roll": "26IT0310013", "name": "Rajat",     "contact": "9314919058", "attendance": 78},
        {"roll": "26IT0310014", "name": "Swati",     "contact": "9518506716", "attendance": 83},
        {"roll": "26IT0310015", "name": "Bhavya",    "contact": "9262849877", "attendance": 80},
        {"roll": "26IT0310016", "name": "Tanvi",     "contact": "9531473799", "attendance": 77},
        {"roll": "26IT0310017", "name": "Siddharth", "contact": "9075273545", "attendance": 81},
        {"roll": "26IT0310018", "name": "Vivaan",    "contact": "9831367837", "attendance": 79},
        {"roll": "26IT0310019", "name": "Suraj",     "contact": "9770143634", "attendance": 76},
        {"roll": "26IT0310020", "name": "Pranav",    "contact": "9957885685", "attendance": 82},
        {"roll": "26IT0310021", "name": "Gaurav",    "contact": "9744431351", "attendance": 75},
        {"roll": "26IT0310022", "name": "Urvashi",   "contact": "9233749894", "attendance": 75},
        {"roll": "26IT0310023", "name": "Kritika",   "contact": "9352408240", "attendance": 75},
        {"roll": "26IT0310024", "name": "Reyansh",   "contact": "9842710947", "attendance": 75},
        {"roll": "26IT0310025", "name": "Rahul",     "contact": "9752047116", "attendance": 75},
        {"roll": "26IT0310026", "name": "Shalini",   "contact": "9022941318", "attendance": 75},
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


# ─── Auto-seed on startup ───────────────────────────────────────────────────

@app.on_event("startup")
def auto_seed():
    seed_data()
