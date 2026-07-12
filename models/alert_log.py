from pydantic import BaseModel
from datetime import datetime

class AlertLog(BaseModel):
    student: str
    studentName: str = ""
    subject: str
    subjectName: str = ""
    section: str
    sectionName: str = ""
    attendancePercentage: float
    recipientPhone: str
    channel: str = "whatsapp"
    status: str = "pending"
    sentAt: datetime = datetime.now()
    errorMessage: str | None = None
