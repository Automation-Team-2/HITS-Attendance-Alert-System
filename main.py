from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import student
from routers import section
from routers import degree
from routers import department
from routers import subject, curriculum
from routers import timetable
from routers import period_timing
from routers import auth, teacher, teacher_subject
from routers import seed, attendance, alerts, stats
from tasks.scheduler import start_scheduler
import atexit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student.router, prefix="/api/students", tags=["Students"])

@app.get("/")
def root():
    return {"message": "Attendance Alert System API Running"}

app.include_router(section.router, prefix="/api/sections", tags=["Sections"])
app.include_router(degree.router, prefix="/api/degrees", tags=["Degrees"])
app.include_router(department.router, prefix="/api/departments", tags=["Departments"])
app.include_router(subject.router, prefix="/api/subjects", tags=["Subjects"])
app.include_router(curriculum.router, prefix="/api/curriculum", tags=["Curriculum"])
app.include_router(timetable.router, prefix="/api/timetable", tags=["Timetable"])
app.include_router(period_timing.router, prefix="/api/period-timings", tags=["Period Timings"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(teacher.router, prefix="/api/teachers", tags=["Teachers"])
app.include_router(teacher_subject.router, prefix="/api/assignments", tags=["Teacher Subjects"])

# New routers
app.include_router(seed.router, prefix="/api/seed", tags=["Seed"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(stats.router, prefix="/api/stats", tags=["Stats"])

@app.on_event("startup")
async def startup_event():
    start_scheduler()

atexit.register(lambda: None)
