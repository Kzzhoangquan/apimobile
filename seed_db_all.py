from models import User, Course, Review, Lesson, Comment, Quiz, Question, Option, Enrollment, Wishlist, Notification, Base, user_notifications
from database import SessionLocal, engine
from datetime import datetime, timedelta
import random

def seed_database():
    # Tạo tất cả các bảng nếu chưa tồn tại
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Kiểm tra xem đã có dữ liệu chưa
        if db.query(User).count() > 0:
            print("Dữ liệu đã tồn tại, bỏ qua quá trình seed!")
            return
        
        # Tạo 20 người dùng mẫu
        print("Đang tạo 20 người dùng...")
        users = []
        for i in range(1, 21):
            # Xác định vai trò (5 instructor, 15 student)
            role = "instructor" if i <= 5 else "user"
            
            # Xác định giới tính cho ảnh đại diện
            gender = "men" if i % 2 == 0 else "women"
            
            user = User(
                username=f"user{i}",
                full_name=f"Người dùng {i}",
                password="password123",
                email=f"user{i}@example.com",
                phone=f"01234{56789+i}",
                avatar_url=f"https://randomuser.me/api/portraits/{gender}/{i % 30}.jpg",
                role=role,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365))
            )
            db.add(user)
            users.append(user)
        db.commit()
        
        # Tạo danh sách danh mục
        categories = ["Design", "Development", "Marketing", "IT & Software", "Health & Fitness", "Business"]
        
        # Tạo 20 khóa học mẫu
        print("Đang tạo 20 khóa học...")
        courses = []
        course_titles = [
            "Lập trình Python cơ bản đến nâng cao",
            "Web Development với React JS",
            "Thiết kế UI/UX với Figma",
            "Marketing Online hiệu quả",
            "Quản lý dự án chuyên nghiệp",
            "Data Science với Python",
            "Machine Learning cơ bản",
            "SEO & Content Marketing",
            "Yoga cho người mới bắt đầu",
            "Tài chính cá nhân",
            "Thiết kế đồ họa với Adobe Photoshop",
            "Docker & Kubernetes cơ bản",
            "Lập trình Java Spring Boot",
            "Phát triển ứng dụng mobile với Flutter",
            "AWS Solutions Architect",
            "Digital Marketing từ A-Z",
            "Thiết kế Logo chuyên nghiệp",
            "Lập trình game với Unity",
            "Copywriting chuyên nghiệp",
            "DevOps cho người mới bắt đầu"
        ]
        
        thumbnail_urls = [
            "https://img-c.udemycdn.com/course/480x270/629302_8a2d_2.jpg",
            "https://img-c.udemycdn.com/course/480x270/1565838_e54e_12.jpg",
            "https://img-c.udemycdn.com/course/480x270/1643044_e281_5.jpg",
            "https://img-c.udemycdn.com/course/480x270/1659806_801a_7.jpg",
            "https://img-c.udemycdn.com/course/480x270/1361790_2eb7.jpg",
            "https://img-c.udemycdn.com/course/480x270/903744_8eb2.jpg",
            "https://img-c.udemycdn.com/course/480x270/950390_270f_3.jpg",
            "https://img-c.udemycdn.com/course/480x270/1259404_72d4_7.jpg",
            "https://img-c.udemycdn.com/course/480x270/938480_4a2e_3.jpg",
            "https://img-c.udemycdn.com/course/480x270/321410_d9c5_4.jpg",
            "https://img-c.udemycdn.com/course/480x270/828496_b73d_3.jpg",
            "https://img-c.udemycdn.com/course/480x270/969900_3614_9.jpg",
            "https://img-c.udemycdn.com/course/480x270/647428_be28_2.jpg",
            "https://img-c.udemycdn.com/course/480x270/1708340_7108_4.jpg",
            "https://img-c.udemycdn.com/course/480x270/1481104_de23_6.jpg",
            "https://img-c.udemycdn.com/course/480x270/1675708_3471_5.jpg",
            "https://img-c.udemycdn.com/course/480x270/1652826_9772_2.jpg",
            "https://img-c.udemycdn.com/course/480x270/812628_ead6_3.jpg",
            "https://img-c.udemycdn.com/course/480x270/1373542_4a1f_3.jpg",
            "https://img-c.udemycdn.com/course/480x270/1137254_a3cc_4.jpg"
        ]
        
        for i in range(20):
            # Chọn instructor từ danh sách instructor đã tạo
            instructor_id = i % 5 + 1  # Chỉ chọn từ 5 instructor
            
            # Chọn danh mục ngẫu nhiên
            category = random.choice(categories)
            
            course_description = f"""
Khóa học {course_titles[i]} sẽ giúp bạn từ người mới bắt đầu đến thành thạo.
Nội dung khóa học bao gồm:
- Những kiến thức cơ bản và nâng cao
- Các dự án thực tế
- Bài tập và thực hành
- Certificate khi hoàn thành khóa học

Khóa học được thiết kế dành cho cả người mới bắt đầu và người đã có kinh nghiệm.
Học viên sẽ được hỗ trợ 24/7 từ giảng viên.
            """
            
            # Tạo giá tiền ngẫu nhiên từ 199k đến 799k
            price = random.randint(199, 799) * 1000
            
            course = Course(
                owner_id=instructor_id,
                title=course_titles[i],
                description=course_description.strip(),
                thumbnail_url=thumbnail_urls[i],
                price=price,
                category=category,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 180))
            )
            db.add(course)
            courses.append(course)
        db.commit()
        
        # Tạo 20 Enrollments (đăng ký khóa học)
        print("Đang tạo 20 đăng ký khóa học...")
        for i in range(20):
            # Chọn ngẫu nhiên user (chỉ chọn học viên, không chọn instructor)
            user_id = random.randint(6, 20)  # Từ user6 đến user20 (học viên)
            
            # Chọn ngẫu nhiên khóa học
            course_id = random.randint(1, 20)
            
            # Tạo ngẫu nhiên tiến độ học từ 0-100%
            progress = random.uniform(0, 100)
            
            enrollment = Enrollment(
                user_id=user_id,
                course_id=course_id,
                enrolled_at=datetime.utcnow() - timedelta(days=random.randint(1, 90)),
                progress=progress
            )
            db.add(enrollment)
        db.commit()
        
        # Tạo 20 Wishlist (danh sách yêu thích)
        print("Đang tạo 20 danh sách yêu thích...")
        for i in range(20):
            # Chọn ngẫu nhiên user
            user_id = random.randint(1, 20)
            
            # Chọn ngẫu nhiên khóa học
            course_id = random.randint(1, 20)
            
            # Kiểm tra xem đã có trong wishlist chưa
            existing = db.query(Wishlist).filter(
                Wishlist.user_id == user_id,
                Wishlist.course_id == course_id
            ).first()
            
            if not existing:
                wishlist = Wishlist(
                    user_id=user_id,
                    course_id=course_id,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 60))
                )
                db.add(wishlist)
        db.commit()
        
        # Tạo 20 Reviews (đánh giá)
        print("Đang tạo 20 đánh giá...")
        for i in range(20):
            # Chọn ngẫu nhiên user (chỉ chọn học viên)
            user_id = random.randint(6, 20)
            
            # Chọn ngẫu nhiên khóa học
            course_id = random.randint(1, 20)
            
            # Tạo ngẫu nhiên rating từ 1-5
            rating = random.randint(3, 5)  # Hầu hết các review là tích cực
            
            # Tạo nội dung đánh giá tùy theo rating
            if rating >= 4:
                comment = "Khóa học rất hay và bổ ích! Tôi đã học được rất nhiều kiến thức mới. Giảng viên dạy rất nhiệt tình và dễ hiểu."
            else:
                comment = "Khóa học tạm được, nội dung khá cơ bản. Giảng viên giảng giải dễ hiểu nhưng cần cập nhật thêm nội dung mới."
                
            review = Review(
                user_id=user_id,
                course_id=course_id,
                rating=rating,
                comment=comment,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(review)
        db.commit()
        
        # Tạo 20 Lessons (bài học)
        print("Đang tạo 20 bài học...")
        lessons = []
        for i in range(20):
            # Chọn ngẫu nhiên khóa học
            course_id = random.randint(1, 20)
            
            # Tạo tiêu đề bài học
            lesson_title = f"Bài {i+1}: Nội dung quan trọng về khóa học"
            
            # Tạo ngẫu nhiên thời lượng bài học từ 5-30 phút
            duration = random.randint(5*60, 30*60)  # seconds
            
            lesson = Lesson(
                course_id=course_id,
                title=lesson_title,
                video_url=f"https://example.com/videos/lesson_{i+1}.mp4",
                duration=duration,
                position=i % 5 + 1  # Position from 1-5
            )
            db.add(lesson)
            lessons.append(lesson)
        db.commit()
        
        # Tạo 20 Comments (bình luận)
        print("Đang tạo 20 bình luận...")
        for i in range(20):
            # Chọn ngẫu nhiên user
            user_id = random.randint(1, 20)
            
            # Chọn ngẫu nhiên bài học
            lesson_id = random.randint(1, 20)
            
            # Tạo nội dung bình luận
            comment_content = [
                "Bài học rất hay và bổ ích!",
                "Tôi có câu hỏi về phần này...",
                "Giảng viên giải thích rất dễ hiểu.",
                "Tôi vẫn chưa hiểu rõ lắm về phần này.",
                "Cảm ơn giảng viên rất nhiều!",
                "Làm thế nào để thực hành phần này?",
                "Mong được xem thêm nhiều bài học như thế này.",
                "Tôi đã học được rất nhiều điều mới.",
                "Nội dung này có thể áp dụng vào dự án của tôi.",
                "Hơi khó hiểu một chút nhưng vẫn ổn."
            ]
            
            comment = Comment(
                user_id=user_id,
                lesson_id=lesson_id,
                comment=random.choice(comment_content),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(comment)
        db.commit()
        
        # Tạo 20 Quizzes (bài kiểm tra)
        print("Đang tạo 20 bài kiểm tra...")
        quizzes = []
        for i in range(20):
            # Chọn ngẫu nhiên bài học
            lesson_id = random.randint(1, 20)
            
            quiz = Quiz(
                lesson_id=lesson_id,
                title=f"Bài kiểm tra #{i+1}",
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(quiz)
            quizzes.append(quiz)
        db.commit()
        
        # Tạo 20 Questions (câu hỏi)
        print("Đang tạo 20 câu hỏi...")
        questions = []
        for i in range(20):
            # Chọn ngẫu nhiên quiz
            quiz_id = random.randint(1, 20)
            
            # Xác định loại câu hỏi
            question_types = ["MULTIPLE_CHOICE", "TRUE_FALSE", "TEXT"]
            question_type = random.choice(question_types)
            
            # Tạo nội dung câu hỏi
            content = f"Câu hỏi {i+1}: Nội dung liên quan đến bài học?"
            
            question = Question(
                quiz_id=quiz_id,
                content=content,
                question_type=question_type
            )
            db.add(question)
            questions.append(question)
        db.commit()
        
        # Tạo 20 Options (câu trả lời)
        print("Đang tạo 20 câu trả lời...")
        for i in range(20):
            # Chọn ngẫu nhiên question
            question_id = random.randint(1, 20)
            
            # Xác định xem có phải là đáp án đúng không
            is_correct = 1 if i % 4 == 0 else 0
            
            # Tạo nội dung đáp án
            content = f"Đáp án {i % 4 + 1}: " + ("Đây là đáp án đúng." if is_correct else "Đây là đáp án sai.")
            
            option = Option(
                question_id=question_id,
                content=content,
                is_correct=is_correct,
                position=i % 4 + 1  # Position from 1-4
            )
            db.add(option)
        db.commit()
        
        # Tạo 20 Notifications (thông báo)
        print("Đang tạo 20 thông báo...")
        notifications = []
        for i in range(20):
            notification = Notification(
                title=f"Thông báo quan trọng #{i+1}",
                message=f"Nội dung thông báo về các sự kiện và cập nhật mới trên hệ thống.",
                is_read=i % 2,  # 0: chưa đọc, 1: đã đọc
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                image_url=f"https://example.com/notifications/img_{i+1}.jpg"
            )
            db.add(notification)
            notifications.append(notification)
        db.commit()
        
        # Tạo liên kết giữa User và Notification
        print("Đang tạo liên kết giữa người dùng và thông báo...")
        for i in range(20):
            # Chọn ngẫu nhiên user
            user_id = random.randint(1, 20)
            
            # Chọn ngẫu nhiên notification
            notification_id = random.randint(1, 20)
            
            # Thêm vào bảng liên kết
            db.execute(
                user_notifications.insert().values(
                    user_id=user_id,
                    notification_id=notification_id
                )
            )
        db.commit()
        
        print("Đã thêm dữ liệu mẫu thành công!")
        
    except Exception as e:
        db.rollback()
        print(f"Lỗi: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()