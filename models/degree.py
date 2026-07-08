from pydantic import BaseModel

class Degree(BaseModel):
    name: str
    durationYears: int
    