# schemas.py
from pydantic import BaseModel
from typing import Optional

class UserQueryRequest(BaseModel):
    student_id: Optional[str] = "student_01"
    query: str
    role: str                       # 'student' or 'parent'
    grade: Optional[str] = None
    subject: Optional[str] = None
    learning_style: Optional[str] = None