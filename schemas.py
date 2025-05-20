# backend/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    user_id: int
    username: Optional[str] = None
    full_name: str
    email: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    google_id: Optional[str] = None
    role: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    course_id: int
    owner_id: int
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: datetime
    price: Optional[float] = None
    instructor: UserBase

    class Config:
        orm_mode = True

class LessonBase(BaseModel):
    lesson_id: int
    course_id: int
    title: str
    video_url: Optional[str] = None
    duration: Optional[int] = None
    position: Optional[int] = None

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    review_id: int
    course_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    user: UserBase

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    comment_id: int
    lesson_id: int
    user_id: int
    comment: str
    created_at: datetime
    user: UserBase

    class Config:
        orm_mode = True

class EnrollmentBase(BaseModel):
    enrollment_id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress: Optional[float] = 0.0
    user: UserBase

    class Config:
        orm_mode = True

class ReviewCreate(BaseModel):
    course_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime

class CommentCreate(BaseModel):
    lesson_id: int
    user_id: int
    comment: str
    created_at: datetime

class NotificationSchema(BaseModel):
    notification_id: int
    title: str
    message: str
    is_read: int
    created_at: datetime
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

class NotificationCreate(BaseModel):
    title: str
    message: str
    image_url: Optional[str] = None

class FCMTokenSchema(BaseModel):
    token_id: int
    user_id: int
    token: str
    device_type: Optional[str] = None
    last_updated: datetime

    class Config:
        orm_mode = True

class FCMTokenCreate(BaseModel):
    token: str
    device_type: Optional[str] = None