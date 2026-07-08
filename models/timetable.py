from pydantic import BaseModel

class Timetable(BaseModel):
    section: str        # Section's _id
    curriculum: str      # Curriculum entry's _id (this carries department+year+semester+subject)
    dayOfWeek: str         # "Monday", "Tuesday"...
    period: int              # 1, 2, 3... (which class slot in the day)
    facultyName: str