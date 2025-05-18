from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import User, Course
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from models import User, Course, Lesson, Review, Comment, Enrollment
from schemas import (
    CourseBase, LessonBase, ReviewBase, CommentBase,
    ReviewCreate, CommentCreate
)

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

# Model trả về cho Android
class UserResponse(BaseModel):
    userId: int
    fullName: str
    email: str
    phone: str | None
    avatarUrl: str | None
    googleId: str | None
    role: str | None

    class Config:
        from_attributes = True

@app.post("/auth/login", response_model=UserResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Sai username hoặc password")
    return user

def get_user(user_id: int, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/courses/{id}", response_model=CourseBase)
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.get("/lessons/{id}", response_model=LessonBase)
def get_lesson_by_id(id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.lesson_id == id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@app.get("/courses/{course_id}/lessons", response_model=list[LessonBase])
def get_lessons_by_course_id(course_id: int, db: Session = Depends(get_db)):
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found for this course")
    return lessons

@app.get("/courses/{course_id}/reviews", response_model=list[ReviewBase])
def get_reviews_by_course_id(course_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.course_id == course_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this course")
    return reviews

@app.get("/lessons/{lesson_id}/comments", response_model=list[CommentBase])
def get_comments_by_lesson_id(lesson_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.lesson_id == lesson_id).all()
    return comments

@app.post("/reviews", response_model=ReviewBase)
def add_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # Validate user
    get_user(review.user_id, db)
    
    # Check enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.course_id == review.course_id,
        Enrollment.user_id == review.user_id
    ).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="User not enrolled in this course")
    
    # Check for duplicate review
    existing_review = db.query(Review).filter(
        Review.course_id == review.course_id,
        Review.user_id == review.user_id
    ).first()
    if existing_review:
        raise HTTPException(status_code=409, detail="User has already reviewed this course")
    
    # Validate rating
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    db_review = Review(
        course_id=review.course_id,
        user_id=review.user_id,
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/comments", response_model=list[CommentBase])
def get_all_comments(db: Session = Depends(get_db)):
    comments = db.query(Comment).all()
    return comments


@app.post("/comments", response_model=CommentBase)
def add_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    # Validate user
    get_user(comment.user_id, db)
    
    # Check lesson exists
    lesson = db.query(Lesson).filter(Lesson.lesson_id == comment.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Check enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.course_id == lesson.course_id,
        Enrollment.user_id == comment.user_id
    ).first()
    if not enrollment:
        raise HTTPException(status_code=403, detail="User not enrolled in this course")
    
    db_comment = Comment(
        lesson_id=comment.lesson_id,
        user_id=comment.user_id,
        comment=comment.comment,
        created_at=comment.created_at
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/courses/{course_id}/users/{user_id}/enrollment", response_model=bool)
def check_enrollment(course_id: int, user_id: int, db: Session = Depends(get_db)):
    # Validate user
    get_user(user_id, db)
    
    enrollment = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.user_id == user_id
    ).first()
    return enrollment is not None