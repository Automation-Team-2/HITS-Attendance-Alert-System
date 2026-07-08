from pydantic import BaseModel

class PeriodTiming(BaseModel):
    period: int
    startTime: str    # "09:00"
    endTime: str        # "09:50"