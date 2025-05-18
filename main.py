from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import or_
from database import SessionLocal, get_db
from models import User, Course, Review
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
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

# Model phản hồi
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

# Model phản hồi cho khóa học
class CourseResponse(BaseModel):
    course_id: int
    title: str
    description: str | None
    thumbnail_url: str
    price: float
    rating: float | None
    instructor_name: str
    is_bestseller: bool = False
    category: str | None = None
    
    class Config:
        from_attributes = True

# Model phản hồi có phân trang
class PagedResponse(BaseModel):
    items: List[CourseResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

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

# Danh sách khóa học nổi bật
@app.get("/api/courses/top", response_model=List[CourseResponse])
def get_top_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).join(User, Course.owner_id == User.user_id).limit(10).all()
    
    # Tính rating trung bình cho mỗi khóa học từ bảng reviews
    result = []
    for course in courses:
        # Lấy rating trung bình
        avg_rating = db.query(func.avg(Review.rating)).filter(
            Review.course_id == course.course_id).scalar() or 4.5
        
        # Kiểm tra xem có phải bestseller không (có ít nhất 3 đánh giá và rating >= 4.5)
        is_bestseller = False
        reviews_count = db.query(func.count(Review.review_id)).filter(
            Review.course_id == course.course_id).scalar() or 0
        if reviews_count >= 3 and avg_rating >= 4.5:
            is_bestseller = True
            
        result.append({
            "course_id": course.course_id,
            "title": course.title,
            "description": course.description,
            "thumbnail_url": course.thumbnail_url,
            "price": course.price or 0.0,
            "rating": round(avg_rating, 1),
            "instructor_name": course.instructor.full_name,
            "is_bestseller": is_bestseller,
            "category": course.category
        })
    
    return result

# API CHUNG: lấy danh sách khóa học, có thể tìm kiếm, lọc theo danh mục và phân trang
@app.get("/api/courses", response_model=PagedResponse)
def get_courses(
    page: int = Query(0, ge=0),
    page_size: int = Query(5, ge=1, le=50),
    category: Optional[str] = None,
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Tạo query cơ bản
    base_query = db.query(Course).join(User, Course.owner_id == User.user_id)
    
    # Thêm điều kiện lọc theo category nếu có
    if category:
        base_query = base_query.filter(Course.category == category)
    
    # Thêm điều kiện tìm kiếm nếu có từ khóa
    if query:
        search_term = f"%{query}%"
        base_query = base_query.filter(
            or_(
                Course.title.ilike(search_term),
                Course.description.ilike(search_term)
            )
        )
    
    # Đếm tổng số khóa học thỏa mãn điều kiện
    total = base_query.count()
    
    # Tính toán phân trang
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    # Lấy các khóa học cho trang hiện tại
    courses = base_query.offset(page * page_size).limit(page_size).all()
    
    # Tạo kết quả
    items = []
    for course in courses:
        # Lấy rating trung bình
        avg_rating = db.query(func.avg(Review.rating)).filter(
            Review.course_id == course.course_id).scalar() or 4.5
        
        # Kiểm tra xem có phải bestseller không
        is_bestseller = False
        reviews_count = db.query(func.count(Review.review_id)).filter(
            Review.course_id == course.course_id).scalar() or 0
        if reviews_count >= 3 and avg_rating >= 4.5:
            is_bestseller = True
            
        items.append({
            "course_id": course.course_id,
            "title": course.title,
            "description": course.description,
            "thumbnail_url": course.thumbnail_url,
            "price": course.price or 0.0,
            "rating": round(avg_rating, 1),
            "instructor_name": course.instructor.full_name,
            "is_bestseller": is_bestseller,
            "category": course.category
        })
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

# Lấy chi tiết một khóa học
@app.get("/api/courses/{course_id}", response_model=CourseResponse)
def get_course_detail(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại")
    
    # Lấy rating trung bình
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.course_id == course.course_id).scalar() or 4.5
    
    # Kiểm tra xem có phải bestseller không
    is_bestseller = False
    reviews_count = db.query(func.count(Review.review_id)).filter(
        Review.course_id == course.course_id).scalar() or 0
    if reviews_count >= 3 and avg_rating >= 4.5:
        is_bestseller = True
    
    return {
        "course_id": course.course_id,
        "title": course.title,
        "description": course.description,
        "thumbnail_url": course.thumbnail_url,
        "price": course.price or 0.0,
        "rating": round(avg_rating, 1),
        "instructor_name": course.instructor.full_name,
        "is_bestseller": is_bestseller,
        "category": course.category
    }

# Lấy banner cho trang chủ
@app.get("/api/banners")
def get_banner():
    return {
        "image_url": "https://img-c.udemycdn.com/notices/web_banner/image_udlite/b8f18e5c-c5c0-43e3-803e-4a1b89054543.jpg",
        "title": "Học hỏi không giới hạn!",
        "subtitle": "Khám phá hàng ngàn khóa học chất lượng cao"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)