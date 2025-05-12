from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Bảng Users
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    password = Column(String(128), nullable=False)  # Đủ dài cho mật khẩu hash
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    avatar_url = Column(String(255))
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    wishlists = relationship("Wishlist", back_populates="user")
    enrollments = relationship("Enrollment", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    comments = relationship("Comment", back_populates="user")

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
    instructor_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(1000))
    thumbnail_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

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
