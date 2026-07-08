from pydantic import BaseModel

class Section(BaseModel):
    department: str
    year: int
    semester: int
    sectionName: str
    strength: int
    subjectProfessor: str | None = None