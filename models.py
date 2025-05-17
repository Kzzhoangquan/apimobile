from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Bảng Users
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=True)
    full_name = Column(String(100), nullable=False)
    password = Column(String(128), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=True)
    avatar_url = Column(String(255))
    google_id = Column(String(255), unique=True, nullable=True)
    role = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    wishlists = relationship("Wishlist", back_populates="user")
    enrollments = relationship("Enrollment", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    comments = relationship("Comment", back_populates="user")

# Bảng trung gian user_notifications
user_notifications = Table(
    "user_notifications",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
    Column("notification_id", Integer, ForeignKey("notifications.notification_id"), primary_key=True)
)

# Bảng Notifications
class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(1000), nullable=False)
    message = Column(String(1000), nullable=False)
    is_read = Column(Integer, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    image_url = Column(String(1000), nullable=False)

    users = relationship("User", secondary=user_notifications, back_populates="notifications")

# Cập nhật bảng Users để thêm mối quan hệ nhiều-nhiều
User.notifications = relationship("Notification", secondary=user_notifications, back_populates="users")


# Bảng Wishlists
class Wishlist(Base):
    __tablename__ = "wishlists"
    wishlist_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wishlists")
    course = relationship("Course", back_populates="wishlists")

# Bảng Courses
class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(1000))
    thumbnail_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    price = Column(Float, nullable=True)

    instructor = relationship("User")
    wishlists = relationship("Wishlist", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    lessons = relationship("Lesson", back_populates="course")
    reviews = relationship("Review", back_populates="course")

# Bảng Enrollments
class Enrollment(Base):
    __tablename__ = "enrollments"
    enrollment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Float, default=0.0)

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

# Bảng Lessons
class Lesson(Base):
    __tablename__ = "lessons"
    lesson_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    title = Column(String(100), nullable=False)
    video_url = Column(String(255))
    duration = Column(Integer)  # đơn vị: giây
    position = Column(Integer)

    course = relationship("Course", back_populates="lessons")
    comments = relationship("Comment", back_populates="lesson")

# Bảng Reviews
class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    course = relationship("Course", back_populates="reviews")

# Bảng Comments
class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id"), nullable=False)
    comment = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="comments")
    lesson = relationship("Lesson", back_populates="comments")

# Bảng Quizzes
class Quiz(Base):
    __tablename__ = "quizzes"
    quiz_id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id"), nullable=False)
    title = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    lesson = relationship("Lesson", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")

# Thêm mối quan hệ vào bảng Lessons
Lesson.quizzes = relationship("Quiz", back_populates="lesson")

# Bảng Questions
class Question(Base):
    __tablename__ = "questions"
    question_id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"), nullable=False)
    content = Column(String(1000), nullable=False)
    question_type = Column(String(50), nullable=False)  # Ví dụ: MULTIPLE_CHOICE, TRUE_FALSE, TEXT

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question")
# Bảng Options
class Option(Base):
    __tablename__ = "options"
    option_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)
    content = Column(String(1000), nullable=False)
    is_correct = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)

    question = relationship("Question", back_populates="options")

# Bảng QuizResults
class QuizResult(Base):
    __tablename__ = "quiz_results"
    quiz_result_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"), nullable=False)
    total_score = Column(Float, default=0.0)  # Tổng điểm của quiz
    completed_at = Column(DateTime, default=datetime.utcnow)  # Thời gian hoàn thành

    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="quiz_results")
# Thêm mối quan hệ vào bảng Users và Quizzes
User.quiz_results = relationship("QuizResult", back_populates="user")
Quiz.quiz_results = relationship("QuizResult", back_populates="quiz")