import json
import time
from fastapi import HTTPException
from repositories.ai_provider import AIProvider
from repositories.memory_repository import get_history, save_message
from schemas.response import ChatResponse, EmailResponse, ResumeResponse

class AIService:

    def __init__(self):
        self.provider = AIProvider()

    def generate_email(self, data):
        prompt = f"""
                  Return ONLY JSON:
                  {{
                    "subject": "",
                    "email_body": ""
                  }}
                  
                  Purpose: {data.purpose}
                  Tone: {data.tone}
                  Context: {data.context}
                  """

        for _ in range(3):
            try:
                raw = self.provider.generate(prompt)
                parsed = json.loads(raw)

                if "subject" in parsed and "email_body" in parsed:
                    return EmailResponse(
                            subject=parsed["subject"],
                            email_body=parsed["email_body"]
                        )

            except Exception:
                time.sleep(2)

        return {"error": "Failed to generate email"}
        
    def chat(self, user: str, message: str):

        # Save user message
        save_message(user, "user", message)

        history = get_history(user)

        # Build context
        context = ""
        for msg in history[-10:]:
            context += f"{msg['role']}: {msg['message']}\n"

        prompt = f"""
You are a helpful AI assistant.

Conversation history:
{context}

Now respond to the latest user message.
"""

        response = self.provider.generate(prompt)

        # Save AI response
        save_message(user, "assistant", response)


        return ChatResponse(
                 response=response,
                 history_count=len(history)
            )
    
    def analyze_resume(self, data):
        prompt = f"""
              You are an expert technical recruiter.

              Analyze the resume against the job description.

              Return ONLY valid JSON (no explanation, no markdown):
              {{
                  "match_score": "percentage",
                  "missing_skills": [],
                  "strengths": [],
                  "suggestions": []
              }}

              Resume:
              {data.resume_text}
              
              Job Description:
              {data.job_description}
              """

      

        raw = None  # ✅ ensure defined

        for _ in range(3):  # retry logic
            try:
                raw = self.provider.generate(prompt)   # ✅ already string
                parsed = json.loads(raw)

                # basic validation
                if "match_score" in parsed:
                    return ResumeResponse(analysis=parsed)

            except Exception:
                time.sleep(2)
 
        # fallback
        return ResumeResponse(
            analysis={"error": "Failed to parse AI response", "raw": raw}
        )