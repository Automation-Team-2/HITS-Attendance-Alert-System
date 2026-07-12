from pydantic import BaseModel
from datetime import datetime

class AttendanceRecord(BaseModel):
    student: str
    subject: str
    section: str
    totalClasses: int
    attendedClasses: int
    percentage: float
    lastUpdated: datetime = datetime.now()
