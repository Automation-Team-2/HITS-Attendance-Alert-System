# HITS Attendance Alert System — Backend

FastAPI-based backend for automated student attendance monitoring and WhatsApp/SMS alert system.

## Architecture

```
Backend/
├── main.py              # FastAPI app entry point
├── database.py          # MongoDB (Motor) async connection
├── config.py            # Environment configuration
├── models/              # Pydantic schemas
│   ├── student.py       # Student (rollNo, name, email, phone, section, etc.)
│   ├── attendance.py    # AttendanceRecord (per-subject attendance)
│   ├── alert_log.py     # AlertLog (sent/failed alert history)
│   ├── section.py        # Section model
│   ├── subject.py        # Subject model
│   ├── teacher.py        # Teacher with bcrypt auth
│   └── ...
├── routers/             # API endpoints
│   ├── auth.py           # POST /api/auth/login
│   ├── student.py        # CRUD /api/students
│   ├── section.py         # CRUD /api/sections
│   ├── attendance.py      # GET attendance per section/student/risk
│   ├── alerts.py          # POST send + GET history/stats
│   ├── seed.py            # POST /api/seed/load-dataset
│   ├── stats.py           # GET /api/stats/dashboard
│   └── ...
├── services/            # Business logic
│   └── messaging_service.py  # WhatsApp abstraction (CallMeBot / Cloud API)
├── tasks/               # Background jobs
│   └── scheduler.py     # APScheduler daily 5PM scan
└── requirements.txt
```

## API Endpoints

### Authentication
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/login` | Login with username/password → returns `{_id, username, isAdmin}` |

### Core Data
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/students/` | List students (with computed attendance % + risk flag) |
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
| GET | `/api/attendance/section/{section_id}` | All students in section with per-subject breakdown + risk |
| GET | `/api/attendance/student/{student_id}` | Single student's full attendance breakdown |
| GET | `/api/attendance/risk` | All at-risk students (< 75%) across all sections |

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
| POST | `/api/seed/load-dataset` | Load `Database/attendance_data.json` → clears & seeds all data |

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

## Setup & Run

```bash
cd Backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

### Environment Variables (`.env`)

```
MONGO_URI=mongodb+srv://...
WHATSAPP_PROVIDER=callmebot
CALLMEBOT_API_KEY=your_key
```

## Daily Automated Scan

The scheduler runs at **5:00 PM daily** and:
1. Scans ALL attendance records
2. Finds students below 75% attendance
3. Sends WhatsApp alert (if phone number + API configured)
4. Logs results to `alert_logs` collection

## Dataset

The `Database/attendance_data.json` file contains 70 students across 7 sections
(CSE, AERO, ECE, EEE) with per-subject attendance records.
30 students are below 75% attendance threshold (demo at-risk data).

## WhatsApp Integration

The messaging service supports two providers (configure via `.env`):
- `callmebot` — Free, simple API (callmebot.com). Set `CALLMEBOT_API_KEY`.
- `cloud_api` — WhatsApp Cloud API (Meta). Set `WHATSAPP_API_KEY` + `WHATSAPP_PHONE_ID`.

## Team Branches

| Branch | Responsibility |
|--------|---------------|
| Backend | API, database, attendance logic, automation |
| Frontend | React/Vite UI, charts, user experience |
| Database | Data models, dataset generation |
| Research | Free API exploration, feasibility |
| Automation-Logic | Scheduler, messaging pipeline |
