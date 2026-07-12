# HITS Attendance Alert System - Backend

FastAPI-based backend for automated student attendance monitoring and WhatsApp/SMS alert system.

## Architecture

```
Backend/
├── main.py
├── database.py
├── config.py
├── models/
│   ├── student.py
│   ├── attendance.py
│   ├── alert_log.py
│   ├── section.py
│   ├── subject.py
│   ├── teacher.py
│   └── ...
├── routers/
│   ├── auth.py
│   ├── student.py
│   ├── section.py
│   ├── attendance.py
│   ├── alerts.py
│   ├── seed.py
│   ├── stats.py
│   └── ...
├── services/
│   └── messaging_service.py
├── tasks/
│   └── scheduler.py
└── requirements.txt
```

## API Endpoints

### Authentication
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/login` | Login with username/password |

### Core Data
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/students/` | List students with computed attendance and risk flag |
| GET | `/api/students/{id}` | Get single student |
| POST | `/api/students/` | Create student |
| PUT | `/api/students/{id}` | Update student (use to set phone numbers) |
| DELETE | `/api/students/{id}` | Delete student |
| GET | `/api/sections/` | List all sections |
| POST | `/api/sections/` | Create section |
| GET | `/api/subjects/` | List all subjects |
| GET | `/api/teachers/` | List teachers |
| POST | `/api/teachers/seed` | Create teacher with auto-hashed password |

### Attendance
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/attendance/section/{section_id}` | Students in section with per-subject breakdown |
| GET | `/api/attendance/student/{student_id}` | Single student attendance breakdown |
| GET | `/api/attendance/risk` | All at-risk students (below 75%) |

### Alerts
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/alerts/send` | Manually trigger alert for a student |
| GET | `/api/alerts/history` | Alert logs (filters: student, section) |
| GET | `/api/alerts/stats` | Alert summary counts |

### Dashboard
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/stats/dashboard` | Total students, at-risk count, alerts this week, avg attendance |

### Data Seeding
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/seed/load-dataset` | Load Database/attendance_data.json |

### Other
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/degrees/` | List degrees |
| GET | `/api/departments/` | List departments |
| GET | `/api/curriculum/lookup` | Get subjects for department/year/semester |
| GET | `/api/timetable/section/{id}` | Get timetable for a section |

## Test Accounts

| Username | Password | Role |
|----------|----------|------|
| Teacher A | Teacher A | Faculty |
| Teacher B | Teacher B | Faculty |
| Admin | Admin | Administrator |

## Setup and Run

```bash
cd Backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

### Environment Variables (.env)

```
MONGO_URI=mongodb+srv://...
WHATSAPP_PROVIDER=callmebot
CALLMEBOT_API_KEY=your_key
```

## Daily Automated Scan

The scheduler runs at 5:00 PM daily and:
1. Scans all attendance records
2. Finds students below 75% attendance
3. Sends WhatsApp alert (if phone number and API configured)
4. Logs results to alert_logs collection

## Dataset

The Database/attendance_data.json file contains 70 students across 7 sections (CSE, AERO, ECE, EEE) with per-subject attendance records. 30 students are below 75% attendance threshold.

## WhatsApp Integration

The messaging service supports two providers (configure via .env):
- callmebot - Free simple API (callmebot.com). Set CALLMEBOT_API_KEY.
- cloud_api - WhatsApp Cloud API (Meta). Set WHATSAPP_API_KEY and WHATSAPP_PHONE_ID.

## Team Branches

| Branch | Responsibility |
|--------|---------------|
| Backend | API, database, attendance logic, automation |
| Frontend | React/Vite UI, charts, user experience |
| Database | Data models, dataset generation |
| Research | Free API exploration, feasibility |
| Automation-Logic | Scheduler, messaging pipeline |
