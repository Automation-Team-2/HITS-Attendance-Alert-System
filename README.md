# HITS Attendance Alert System

Automated attendance monitoring system for Hindustan Institute of Technology and Science. Detects students below 75% attendance and sends automated WhatsApp/SMS warnings.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI + MongoDB (Motor) + APScheduler |
| Frontend | React 19 + Vite 6 + TypeScript (in progress) |
| Auth | bcrypt password hashing |
| Messaging | WhatsApp Cloud API / CallMeBot (configurable) |
| Database | MongoDB Atlas (async Motor driver) |

## Project Structure

```
HITS-Attendance-Alert-System/
├── Backend/          FastAPI REST API (Backend branch)
├── Frontend/         Web UI (Frontend branch)
├── Database/         Datasets and seed data
└── opencode/         Chat history and workspace config
```

## Team Branches

| Branch | Responsibility |
|--------|---------------|
| Backend | API, database, attendance logic, automation |
| Frontend | React UI, charts, user experience |
| Database | Data models, dataset generation |
| Research | Free API exploration, feasibility |
| Automation-Logic | Scheduler, messaging pipeline |

## Core Workflow

1. ERP Sync (simulated) - Fake attendance data loaded from Database/attendance_data.json
2. Daily Scan - APScheduler runs at 5:00 PM, checks all students attendance
3. Risk Detection - Students with below 75% attendance are flagged
4. Auto Alert - WhatsApp warning message sent automatically
5. Manual Alert - Faculty can also trigger alerts from the dashboard

## API Documentation

Once the backend is running:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Key Endpoints

| Endpoint | Description |
|----------|-------------|
| POST /api/auth/login | Login (Teacher A/B, Admin - password = username) |
| GET /api/sections/ | List all sections |
| GET /api/students/ | List students with attendance percentage |
| GET /api/attendance/section/{id} | Section-wise attendance and risk flags |
| GET /api/attendance/risk | All at-risk students globally |
| POST /api/alerts/send | Manually trigger an alert |
| GET /api/alerts/history | View sent alert history |
| GET /api/stats/dashboard | Summary metrics |
| POST /api/seed/load-dataset | Load fake dataset into MongoDB |

## Running the Project

### Backend
```bash
cd Backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd Frontend
npx vite --port 3000 --host
```

Or open Frontend/index.html directly in a browser.

## Test Credentials

| Username | Password | Role |
|----------|----------|------|
| Teacher A | Teacher A | Faculty |
| Teacher B | Teacher B | Faculty |
| Admin | Admin | Administrator |
