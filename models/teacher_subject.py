from pydantic import BaseModel

class TeacherSubject(BaseModel):
    teacher: str
    section: str
    subject: str
