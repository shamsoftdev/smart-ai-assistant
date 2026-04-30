from typing import Any, Dict

from pydantic import BaseModel

class EmailResponse(BaseModel):
    subject: str
    email_body: str


class ChatResponse(BaseModel):
    response: str
    history_count: int

class ResumeResponse(BaseModel):
    analysis: Dict[str, Any]
 
    

