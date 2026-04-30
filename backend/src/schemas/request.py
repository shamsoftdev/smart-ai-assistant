from pydantic import BaseModel

class EmailRequest(BaseModel):
    purpose: str
    tone: str
    context: str

    
class ChatRequest(BaseModel):
    message: str


class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str
