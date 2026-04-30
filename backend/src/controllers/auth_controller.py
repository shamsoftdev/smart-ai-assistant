from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.security import create_token

router = APIRouter()

# Request model
class LoginRequest(BaseModel):
    username: str
    password: str

# Fake user (for now)
fake_user = {
    "username": "admin",
    "password": "admin123"
}

@router.post("/login")
def login(data: LoginRequest):
    if data.username == fake_user["username"] and data.password == fake_user["password"]:
        token = create_token(data.username)
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")