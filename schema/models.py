from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class UserQueryRequest(BaseModel):
    student_id: str = Field(..., description="Name or unique ID of the student")
    query: str = Field(..., description="The primary user input / question text")
    role: Optional[str] = Field(default="Student", description="User role in the system")
    grade: Optional[str] = Field(default="Grade 5", description="Educational grade/level")
    curriculum: Optional[str] = Field(default="NCERT / CBSE", description="Target curriculum framework")
    learning_style: Optional[str] = Field(
        default="Visual & Diagrammatic", 
        description="Preferred pedagogical style"
    )
    history: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Conversation history context"
    )

    # Enable Pydantic v2 modern settings (allows easy JSON parsing and flexibility)
    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
        extra="ignore"
    )