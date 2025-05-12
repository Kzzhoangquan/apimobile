from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Course
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Schema Pydantic để validate dữ liệu
class UserCreate(BaseModel):
    username: str
    full_name: str
    password: str
    email: str
    avatar_url: str | None = None
    role: str
class CourseCreate(BaseModel):
    instructor_id: int
    title: str
    description: str | None = None
    thumbnail_url: str | None = None

# Endpoint tạo người dùng mới
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Endpoint lấy danh sách tất cả người dùng
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Endpoint tạo khóa học mới
@app.post("/courses/")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.dict(), created_at=datetime.utcnow())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Endpoint lấy danh sách tất cả khóa học
@app.get("/courses/")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses

# Endpoint lấy thông tin người dùng theo ID
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user