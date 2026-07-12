from pydantic import BaseModel

class Student(BaseModel):
    rollNo: str
    name: str
    email: str = ""
    phone: str = ""
    department: str
    section: str
    year: int
    semester: int