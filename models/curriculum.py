from pydantic import BaseModel

class Curriculum(BaseModel):
    department: str    
    year: int
    semester: int
    subject: str         