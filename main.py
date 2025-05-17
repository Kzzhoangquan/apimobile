from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import User, Course
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Cho phép gọi từ Android
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model nhận từ Android
class LoginRequest(BaseModel):
    username: str
    password: str

class GoogleLoginRequest(BaseModel):
    id_token: str
    email: str
    display_name: str | None
    photo_url: str | None

# Model trả về cho Android
class UserResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    phone: str | None
    avatar_url: str | None
    google_id: str | None
    role: str | None

    class Config:
        from_attributes = True

@app.post("/auth/login", response_model=UserResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Sai username hoặc password")
    return user

@app.post("/auth/google", response_model=UserResponse)
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    # Kiểm tra xem google_id (id_token) đã tồn tại chưa
    user = db.query(User).filter(User.google_id == request.id_token).first()
    
    if user:
        # Nếu đã có, trả về user
        return user
    
    # Nếu chưa, tạo user mới
    user = User(
        username=request.email.split("@")[0],  # Tạo username từ email
        email=request.email,
        google_id=request.id_token,
        full_name=request.display_name or "Google User",
        avatar_url=request.photo_url,
        role="user",
        password=None  # Không cần password cho Google login
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)