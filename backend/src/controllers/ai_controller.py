from fastapi import APIRouter, Depends
from schemas.request import ChatRequest, EmailRequest, ResumeRequest
from schemas.response import ChatResponse, EmailResponse, ResumeResponse
from services.ai_service import AIService
from core.security import verify_token
from core.rate_limiter import rate_limiter

router = APIRouter()
service = AIService()


#@router.get("/",include_in_schema=False)
#def home():
#    return {"message": "Smart-AI-Assistant is running 🚀"}


@router.post("/generate-email",response_model=EmailResponse)
def generate_email(data: EmailRequest, user=Depends(verify_token)):
    rate_limiter(user)
    return service.generate_email(data)


@router.post("/chat",response_model=ChatResponse)
def chat(data: ChatRequest, user=Depends(verify_token)):
    rate_limiter(user)
    return service.chat(user, data.message)


@router.post("/analyze",response_model=ResumeResponse)
def analyze_resume(data: ResumeRequest, user=Depends(verify_token)):
    rate_limiter(user)
    return service.analyze_resume(data)