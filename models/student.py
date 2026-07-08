from pydantic import BaseModel

class Student(BaseModel):
    rollNo: str
    name: str
    department: str
    section: str
    year: int
    semester: int