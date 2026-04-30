
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as auth_router
from controllers.ai_controller import router as ai_router

# ---------------------------
# CREATE APP
# ---------------------------
app = FastAPI(
    title="Smart AI Assistant",
    description="AI-powered Resume Analyzer, Email Generator & Chatbot",
    version="1.0.0"
)

# ---------------------------
# ADD CORS MIDDLEWARE (HERE)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# ROUTERS
# ---------------------------

@app.get("/")
def root():
    return {
        "message": "Smart AI Assistant API is running 🚀"
    }
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(ai_router, prefix="/ai", tags=["AI"])
