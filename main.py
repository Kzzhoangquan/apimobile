from typing import List
from fastapi import FastAPI, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Option, Question, Quiz, QuizResult, User, Course
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import cloudinary
import cloudinary.uploader

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
    google_id: str  # Nhận google_id thay vì id_token
    email: str
    display_name: str | None
    photo_url: str | None

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    phone: str

class PhoneCheckRequest(BaseModel):
    phone: str

class PasswordResetRequest(BaseModel):
    phone: str
    new_password: str

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

class ProfileUpdate(BaseModel):
    user_id: int
    full_name: str
    email: str
    phone: str

class PasswordChange(BaseModel):
    user_id: int
    current_password: str
    new_password: str

class QuizResultRequest(BaseModel):
    user_id: int
    question_id: int
    score: str

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
        full_name=request.display_name or "Google User",
        avatar_url=request.photo_url,
        role="user",
        password=None  # Không cần password cho Google login
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@app.post("/auth/register", response_model=UserResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Kiểm tra username hoặc email đã tồn tại
    existing_user = db.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()
    if existing_user:
        if existing_user.username == request.username:
            raise HTTPException(status_code=400, detail="Username đã tồn tại")
        # if existing_user.email == request.email:
        #     raise HTTPException(status_code=400, detail="Email đã tồn tại")

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
    user.password = request.new_password
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
    try:
        user = db.query(User).filter(User.user_id == profile.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

        user.full_name = profile.full_name
        user.email = profile.email
        user.phone = profile.phone
        db.commit()
        return {"message": "Cập nhật thông tin thành công"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

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

        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)