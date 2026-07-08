from pydantic import BaseModel

class Teacher(BaseModel):
    username: str
    password_hash: str
    isAdmin: bool = False
