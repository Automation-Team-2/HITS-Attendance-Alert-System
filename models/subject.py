from pydantic import BaseModel

class Subject(BaseModel):
    subjectCode: str
    subjectName: str
    credits: int