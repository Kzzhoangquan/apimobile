from sqlite3 import IntegrityError
from typing import List
from fastapi import FastAPI, Depends, File, Form, HTTPException, UploadFile,Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import or_
from database import SessionLocal, get_db
from models import Option, Question, Quiz, QuizResult, User, Course
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import cloudinary
import cloudinary.uploader
from models import User, Course, Lesson, Review, Comment, Enrollment
from schemas import (
    CourseBase, LessonBase, ReviewBase, CommentBase,
    ReviewCreate, CommentCreate, EnrollmentResponse
)

app = FastAPI()


cloudinary.config(
    cloud_name="diyonw6md",
    api_key="324758519181249",
    api_secret="GSt3Ttptm9N4Wi4aTmBwodCuc5U",
    secure=True
)

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
    google_id: str
    email: str
    full_name: str | None 
    avatar_url: str | None

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    phone: str

class PhoneCheckRequest(BaseModel):
    phone: str

class PasswordResetRequest(BaseModel):
    phone: str
    password: str

# Model trả về cho Android
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

# class QuizRequest(BaseModel):
#     lesson_id: int

# class OptionResponse(BaseModel):
#     option_id: int
#     content: str
#     is_correct: int

# class QuestionResponse(BaseModel):
#     question_id: int
#     content: str
#     options: List[OptionResponse]

# class QuizResponse(BaseModel):
#     quizzes: List[QuestionResponse]

class ProfileUpdate(BaseModel):
    user_id: int
    full_name: str
    email: str
    phone: str

class PasswordChange(BaseModel):
    user_id: int
    current_password: str
    new_password: str


class QuizRequest(BaseModel):
    lesson_id: int

class OptionResponse(BaseModel):
    option_id: int
    content: str
    is_correct: int

class QuestionResponse(BaseModel):
    question_id: int
    content: str
    options: List[OptionResponse]

class QuizResponse(BaseModel):
    quizzes: List[QuestionResponse]
    
class QuizResultRequest(BaseModel):
    user_id: int
    question_id: int
    score: str

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

class ScoreItem(BaseModel):
    course_id: int
    course_url: Optional[str]
    course_title: str
    lesson_id: int
    lesson_title: str
    quiz_id: int
    quiz_title: str
    score: str
    ngaylambai: str

class PagedResponse_Score(BaseModel):
    items: list[ScoreItem]
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
    # Kiểm tra xem google_id đã tồn tại chưa
    user = db.query(User).filter(User.google_id == request.google_id).first()
    
    if user:
        # Nếu đã có, trả về user
        return user
    
    # Nếu chưa, tạo user mới
    user = User(
        username=request.email.split("@")[0],  # Tạo username từ email
        email=request.email,
        google_id=request.google_id,
        full_name=request.full_name or "Google User",
        avatar_url=request.avatar_url,
        role="user",
        password=None,
        phone = "không có"  
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@app.post("/auth/register", response_model=UserResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Kiểm tra username hoặc email đã tồn tại
    existing_user = db.query(User).filter(
        (User.username == request.username) | (User.phone == request.phone)
    ).first()
    if existing_user:
        if existing_user.username == request.username:
            raise HTTPException(status_code=400, detail="Username đã tồn tại")
        if existing_user.phone == request.phone:
            raise HTTPException(status_code=400, detail="Số điện thoại đã tồn tại")

    # Tạo user mới
    user = User(
        username=request.username,
        email=request.email,
        password=request.password,
        phone=request.phone,
        full_name=request.username,  # Dùng username làm full_name
        role="user",
        avatar_url=None,
        google_id=None
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/password-recovery/check-phone")
def check_phone(request: PhoneCheckRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == request.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản với số điện thoại này")
    return {"detail": "Số điện thoại hợp lệ"}

@app.post("/password-recovery/reset")
def reset_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == request.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản với số điện thoại này")
    user.password = request.password
    db.commit()
    db.refresh(user)
    return {"detail": "Đặt lại mật khẩu thành công"}

@app.post("/quizzes", response_model=List[QuestionResponse])
async def get_quizzes(request: QuizRequest):
    db = SessionLocal()
    try:
        # Query quizzes với lesson_id
        quizzes = db.query(Quiz).filter(Quiz.lesson_id == request.lesson_id).all()
        if not quizzes:
            raise HTTPException(status_code=404, detail="Không tìm thấy quiz cho lesson_id")

        questions_response = []
        for quiz in quizzes:
            # Lấy câu hỏi MULTIPLE_CHOICE
            questions = db.query(Question).filter(
                Question.quiz_id == quiz.quiz_id,
                Question.question_type == "MULTIPLE_CHOICE"
            ).all()
            for question in questions:
                # Lấy 4 options
                options = db.query(Option).filter(
                    Option.question_id == question.question_id
                ).order_by(Option.position).limit(4).all()
                if len(options) != 4:
                    continue  # Bỏ qua nếu không đủ 4 lựa chọn
                question_response = QuestionResponse(
                    question_id=question.question_id,
                    content=question.content,
                    options=[
                        OptionResponse(
                            option_id=option.option_id,
                            content=option.content,
                            is_correct=option.is_correct
                        ) for option in options
                    ]
                )
                questions_response.append(question_response)
        if not questions_response:
            raise HTTPException(status_code=404, detail="Không tìm thấy câu hỏi")
        return questions_response
    finally:
        db.close()


@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...), user_id: int = Form(...)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

        result = cloudinary.uploader.upload(
            file.file,
            public_id=f"user_{user_id}",
            overwrite=True,
            resource_type="image"
        )
        avatar_url = result["secure_url"]
        print(avatar_url)
        user.avatar_url = avatar_url
        db.commit()

        return {"url": avatar_url}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/update-profile")
async def update_profile(profile: ProfileUpdate):
    db = SessionLocal()
    check = db.query(User).filter((User.phone ==  profile.phone) & (User.user_id != profile.user_id)).first()
    if check:
        raise HTTPException(status_code=400, detail="Số điện thoại đã tồn tại")
    user = db.query(User).filter(User.user_id == profile.user_id).first()
    user.full_name = profile.full_name
    user.email = profile.email
    user.phone = profile.phone
    db.commit()
    return {"message": "Cập nhật thông tin thành công"}

    

@app.post("/change-password")
async def change_password(password_change: PasswordChange):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == password_change.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail={"error": "Người dùng không tồn tại"})

        # Kiểm tra mật khẩu hiện tại (so sánh trực tiếp)
        if user.password != password_change.current_password:
            raise HTTPException(status_code=400, detail={"error": "Mật khẩu hiện tại không đúng"})

        # Lưu mật khẩu mới (plaintext)
        user.password = password_change.new_password
        db.commit()
        return {"message": "Đổi mật khẩu thành công"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"error": str(e)})
    finally:
        db.close()


@app.post("/save-quiz-result")
async def save_quiz_result(result: QuizResultRequest):
    db = SessionLocal()
    try:
        # Kiểm tra user
        user = db.query(User).filter(User.user_id == result.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail={"error": "Người dùng không tồn tại"})

        # Tìm quiz_id từ question_id
        question = db.query(Question).filter(Question.question_id == result.question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail={"error": "Câu hỏi không tồn tại"})

        quiz_id = question.quiz_id

        # Kiểm tra định dạng score
        if not result.score or "/" not in result.score:
            raise HTTPException(status_code=400, detail={"error": "Định dạng điểm không hợp lệ, cần dạng 'X/Y'"})

        # Lưu kết quả vào quiz_results
        quiz_result = QuizResult(
            user_id=result.user_id,
            quiz_id=quiz_id,
            total_score=result.score, 
            completed_at=datetime.utcnow()
        )
        db.add(quiz_result)
        db.commit()

        return {"message": "Lưu kết quả quiz thành công"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"error": str(e)})
    finally:
        db.close()


@app.get("/api/scores", response_model=PagedResponse_Score)
def get_scores(
    user_id: int,
    page: int = Query(0, ge=0),
    page_size: int = Query(5, ge=1, le=50),
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    base_query = db.query(QuizResult).join(Quiz, QuizResult.quiz_id == Quiz.quiz_id)\
                                   .join(Lesson, Quiz.lesson_id == Lesson.lesson_id)\
                                   .join(Course, Lesson.course_id == Course.course_id)\
                                   .filter(QuizResult.user_id == user_id)\
                                   .order_by(QuizResult.completed_at.desc())  # Sort by most recent first
    
    if query:
        search_term = f"%{query}%"
        base_query = base_query.filter(
            or_(
                Course.title.ilike(search_term),
                Lesson.title.ilike(search_term),
                Quiz.title.ilike(search_term)
            )
        )
    
    total = base_query.count()
    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    scores = base_query.offset(page * page_size).limit(page_size).all()
    
    items = []
    for score in scores:
        lesson = db.query(Lesson).filter(Lesson.lesson_id == score.quiz.lesson_id).first()
        course = db.query(Course).filter(Course.course_id == lesson.course_id).first()
        items.append({
            "course_id": course.course_id,
            "course_url": course.thumbnail_url,
            "course_title": course.title,
            "lesson_id": lesson.lesson_id,
            "lesson_title": lesson.title,
            "quiz_id": score.quiz_id,
            "quiz_title": score.quiz.title,
            "score": score.total_score,
            "ngaylambai": score.completed_at.strftime("%d/%m/%Y")
        })
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

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

# POST /courses/{courseId}/enrollments API
@app.post("/courses/{courseId}/enrollments", response_model=EnrollmentResponse, status_code=201)
async def enroll_in_course(
    courseId: int,
    request: dict,  # Accept raw JSON body
    db: Session = Depends(get_db)
):
    # Validate user_id in request
    user_id = request.get("user_id")
    if not user_id or not isinstance(user_id, int):
        raise HTTPException(status_code=400, detail="Invalid or missing user_id")

    # Check if the user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the course exists
    course = db.query(Course).filter(Course.course_id == courseId).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if the user is already enrolled
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == courseId
    ).first()
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="User is already enrolled in this course")

    # Create new enrollment
    enrollment = Enrollment(
        user_id=user_id,
        course_id=courseId,
        enrolled_at=datetime.utcnow(),
        progress=0.0
    )

    # Add to database
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    # Create response dictionary
    response = {
        "enrollment_id": enrollment.enrollment_id,
        "user_id": enrollment.user_id,
        "course_id": enrollment.course_id,
        "enrolled_at": enrollment.enrolled_at,
        "progress": enrollment.progress,
        "user": {
            "user_id": user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "avatar_url": user.avatar_url
        },
        "course": {
            "course_id": course.course_id,
            "title": course.title,
            "description": course.description,
            "thumbnail_url": course.thumbnail_url
        }
    }

    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)