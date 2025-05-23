from models import User, Course, Review, Lesson, Comment, Quiz, Question, Option, Enrollment, Wishlist, Notification, Base, user_notifications
from database import SessionLocal, engine , create_engine , sessionmaker
from datetime import datetime, timedelta
import random



DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/elearning"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_quiz_data():
    db = SessionLocal()
    try:
        # Lấy tất cả lessons có sẵn
        lessons = db.query(Lesson).all()
        
        if not lessons:
            print("Không có lesson nào trong database. Vui lòng seed lessons trước.")
            return
        
        # Danh sách câu hỏi mẫu cho các chủ đề khác nhau
        quiz_templates = {
            "Android Development": {
                "quiz_title": "Android Development Quiz",
                "questions": [
                    {
                        "content": "Activity nào được gọi đầu tiên khi ứng dụng Android khởi động?",
                        "options": [
                            {"content": "MainActivity", "is_correct": 1},
                            {"content": "BaseActivity", "is_correct": 0},
                            {"content": "StartActivity", "is_correct": 0},
                            {"content": "LaunchActivity", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Layout nào được sử dụng để sắp xếp các view theo dạng lưới?",
                        "options": [
                            {"content": "LinearLayout", "is_correct": 0},
                            {"content": "RelativeLayout", "is_correct": 0},
                            {"content": "GridLayout", "is_correct": 1},
                            {"content": "FrameLayout", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Phương thức nào được gọi khi Activity bị tạm dừng?",
                        "options": [
                            {"content": "onCreate()", "is_correct": 0},
                            {"content": "onResume()", "is_correct": 0},
                            {"content": "onPause()", "is_correct": 1},
                            {"content": "onDestroy()", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Intent được sử dụng để làm gì trong Android?",
                        "options": [
                            {"content": "Lưu trữ dữ liệu", "is_correct": 0},
                            {"content": "Giao tiếp giữa các component", "is_correct": 1},
                            {"content": "Tạo layout", "is_correct": 0},
                            {"content": "Quản lý memory", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "RecyclerView được sử dụng để làm gì?",
                        "options": [
                            {"content": "Hiển thị danh sách dữ liệu lớn", "is_correct": 1},
                            {"content": "Lưu trữ dữ liệu", "is_correct": 0},
                            {"content": "Xử lý animation", "is_correct": 0},
                            {"content": "Quản lý network", "is_correct": 0}
                        ]
                    }
                ]
            },
            "Python Programming": {
                "quiz_title": "Python Programming Quiz",
                "questions": [
                    {
                        "content": "Python là ngôn ngữ lập trình thuộc loại nào?",
                        "options": [
                            {"content": "Compiled", "is_correct": 0},
                            {"content": "Interpreted", "is_correct": 1},
                            {"content": "Assembly", "is_correct": 0},
                            {"content": "Machine", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Từ khóa nào được sử dụng để định nghĩa hàm trong Python?",
                        "options": [
                            {"content": "function", "is_correct": 0},
                            {"content": "def", "is_correct": 1},
                            {"content": "fun", "is_correct": 0},
                            {"content": "method", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Cấu trúc dữ liệu nào trong Python có thể thay đổi được?",
                        "options": [
                            {"content": "Tuple", "is_correct": 0},
                            {"content": "String", "is_correct": 0},
                            {"content": "List", "is_correct": 1},
                            {"content": "Frozenset", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Phương thức nào được sử dụng để thêm phần tử vào cuối list?",
                        "options": [
                            {"content": "add()", "is_correct": 0},
                            {"content": "append()", "is_correct": 1},
                            {"content": "insert()", "is_correct": 0},
                            {"content": "push()", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Kết quả của 3 ** 2 trong Python là gì?",
                        "options": [
                            {"content": "6", "is_correct": 0},
                            {"content": "9", "is_correct": 1},
                            {"content": "5", "is_correct": 0},
                            {"content": "8", "is_correct": 0}
                        ]
                    }
                ]
            },
            "Web Development": {
                "quiz_title": "Web Development Quiz",
                "questions": [
                    {
                        "content": "HTML là viết tắt của gì?",
                        "options": [
                            {"content": "Hyper Text Markup Language", "is_correct": 1},
                            {"content": "Home Tool Markup Language", "is_correct": 0},
                            {"content": "Hyperlinks Text Mark Language", "is_correct": 0},
                            {"content": "Hyper Tool Modern Language", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "CSS được sử dụng để làm gì?",
                        "options": [
                            {"content": "Tạo cấu trúc trang web", "is_correct": 0},
                            {"content": "Thêm tính năng tương tác", "is_correct": 0},
                            {"content": "Tạo kiểu dáng cho trang web", "is_correct": 1},
                            {"content": "Quản lý database", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "JavaScript chạy ở đâu?",
                        "options": [
                            {"content": "Chỉ trên server", "is_correct": 0},
                            {"content": "Chỉ trên browser", "is_correct": 0},
                            {"content": "Cả browser và server", "is_correct": 1},
                            {"content": "Chỉ trên mobile", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "HTTP là viết tắt của gì?",
                        "options": [
                            {"content": "Hyper Text Transfer Protocol", "is_correct": 1},
                            {"content": "Home Text Transfer Protocol", "is_correct": 0},
                            {"content": "Hyperlinks Text Transfer Protocol", "is_correct": 0},
                            {"content": "Hyper Tool Transfer Protocol", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Framework nào phổ biến cho front-end development?",
                        "options": [
                            {"content": "Django", "is_correct": 0},
                            {"content": "React", "is_correct": 1},
                            {"content": "Laravel", "is_correct": 0},
                            {"content": "Spring", "is_correct": 0}
                        ]
                    }
                ]
            },
            "Data Science": {
                "quiz_title": "Data Science Quiz",
                "questions": [
                    {
                        "content": "Pandas là gì trong Python?",
                        "options": [
                            {"content": "Một game", "is_correct": 0},
                            {"content": "Thư viện xử lý dữ liệu", "is_correct": 1},
                            {"content": "Framework web", "is_correct": 0},
                            {"content": "Database", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Machine Learning thuộc lĩnh vực nào?",
                        "options": [
                            {"content": "Artificial Intelligence", "is_correct": 1},
                            {"content": "Web Development", "is_correct": 0},
                            {"content": "Mobile Development", "is_correct": 0},
                            {"content": "Network Security", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "SQL được sử dụng để làm gì?",
                        "options": [
                            {"content": "Tạo giao diện", "is_correct": 0},
                            {"content": "Quản lý cơ sở dữ liệu", "is_correct": 1},
                            {"content": "Xử lý hình ảnh", "is_correct": 0},
                            {"content": "Tạo animation", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Numpy được sử dụng cho mục đích gì?",
                        "options": [
                            {"content": "Xử lý văn bản", "is_correct": 0},
                            {"content": "Tính toán khoa học", "is_correct": 1},
                            {"content": "Tạo web", "is_correct": 0},
                            {"content": "Game development", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Visualization trong Data Science có nghĩa là gì?",
                        "options": [
                            {"content": "Lưu trữ dữ liệu", "is_correct": 0},
                            {"content": "Trực quan hóa dữ liệu", "is_correct": 1},
                            {"content": "Xóa dữ liệu", "is_correct": 0},
                            {"content": "Mã hóa dữ liệu", "is_correct": 0}
                        ]
                    }
                ]
            },
            "UI/UX Design": {
                "quiz_title": "UI/UX Design Quiz",
                "questions": [
                    {
                        "content": "UI là viết tắt của gì?",
                        "options": [
                            {"content": "User Interface", "is_correct": 1},
                            {"content": "Universal Interface", "is_correct": 0},
                            {"content": "Unique Interface", "is_correct": 0},
                            {"content": "User Integration", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "UX design tập trung vào điều gì?",
                        "options": [
                            {"content": "Màu sắc", "is_correct": 0},
                            {"content": "Trải nghiệm người dùng", "is_correct": 1},
                            {"content": "Font chữ", "is_correct": 0},
                            {"content": "Hiệu ứng", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Wireframe được sử dụng để làm gì?",
                        "options": [
                            {"content": "Tạo màu sắc", "is_correct": 0},
                            {"content": "Phác thảo layout", "is_correct": 1},
                            {"content": "Viết code", "is_correct": 0},
                            {"content": "Test performance", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Nguyên tắc nào quan trọng trong UI design?",
                        "options": [
                            {"content": "Complexity", "is_correct": 0},
                            {"content": "Simplicity", "is_correct": 1},
                            {"content": "Chaos", "is_correct": 0},
                            {"content": "Confusion", "is_correct": 0}
                        ]
                    },
                    {
                        "content": "Prototype được tạo ra để làm gì?",
                        "options": [
                            {"content": "Test và demo ý tưởng", "is_correct": 1},
                            {"content": "Lưu trữ dữ liệu", "is_correct": 0},
                            {"content": "Marketing", "is_correct": 0},
                            {"content": "Backup", "is_correct": 0}
                        ]
                    }
                ]
            }
        }
        
        # Tạo quiz cho mỗi lesson
        for lesson in lessons:
            print(f"Tạo quiz cho lesson: {lesson.title}")
            
            # Chọn template quiz dựa trên title của lesson hoặc random
            template_key = "Android Development"  # Mặc định
            for key in quiz_templates.keys():
                if key.lower() in lesson.title.lower():
                    template_key = key
                    break
            
            template = quiz_templates[template_key]
            
            # Tạo quiz
            quiz = Quiz(
                lesson_id=lesson.lesson_id,
                title=f"{template['quiz_title']} - {lesson.title}",
                created_at=datetime.utcnow()
            )
            
            db.add(quiz)
            db.flush()  # Để lấy quiz_id
            
            # Tạo câu hỏi cho quiz
            for idx, question_data in enumerate(template["questions"]):
                question = Question(
                    quiz_id=quiz.quiz_id,
                    content=question_data["content"],
                    question_type="MULTIPLE_CHOICE"
                )
                
                db.add(question)
                db.flush()  # Để lấy question_id
                
                # Tạo các option cho câu hỏi
                for pos, option_data in enumerate(question_data["options"]):
                    option = Option(
                        question_id=question.question_id,
                        content=option_data["content"],
                        is_correct=option_data["is_correct"],
                        position=pos + 1
                    )
                    db.add(option)
            
            print(f"Đã tạo quiz với {len(template['questions'])} câu hỏi cho lesson {lesson.title}")
        
        # Commit tất cả thay đổi
        db.commit()
        print(f"Đã tạo thành công quiz cho {len(lessons)} lessons!")
        
    except Exception as e:
        print(f"Lỗi khi tạo quiz data: {str(e)}")
        db.rollback()
    finally:
        db.close()

def add_more_quiz_questions():
    """Thêm nhiều câu hỏi đa dạng hơn"""
    db = SessionLocal()
    try:
        # Lấy tất cả quiz hiện có
        quizzes = db.query(Quiz).all()
        
        additional_questions = [
            {
                "content": "Mô hình MVC trong lập trình có nghĩa là gì?",
                "options": [
                    {"content": "Model-View-Controller", "is_correct": 1},
                    {"content": "Multiple-Virtual-Computer", "is_correct": 0},
                    {"content": "Modern-Video-Control", "is_correct": 0},
                    {"content": "Mobile-Visual-Code", "is_correct": 0}
                ]
            },
            {
                "content": "API là viết tắt của gì?",
                "options": [
                    {"content": "Application Programming Interface", "is_correct": 1},
                    {"content": "Advanced Programming Integration", "is_correct": 0},
                    {"content": "Automated Program Interface", "is_correct": 0},
                    {"content": "Application Process Integration", "is_correct": 0}
                ]
            },
            {
                "content": "Git được sử dụng để làm gì?",
                "options": [
                    {"content": "Quản lý phiên bản code", "is_correct": 1},
                    {"content": "Tạo database", "is_correct": 0},
                    {"content": "Design UI", "is_correct": 0},
                    {"content": "Test performance", "is_correct": 0}
                ]
            },
            {
                "content": "Framework nào phổ biến cho backend development?",
                "options": [
                    {"content": "React", "is_correct": 0},
                    {"content": "Django", "is_correct": 1},
                    {"content": "Bootstrap", "is_correct": 0},
                    {"content": "jQuery", "is_correct": 0}
                ]
            },
            {
                "content": "Debugging có nghĩa là gì?",
                "options": [
                    {"content": "Tìm và sửa lỗi trong code", "is_correct": 1},
                    {"content": "Tạo tài liệu", "is_correct": 0},
                    {"content": "Kiểm tra hiệu suất", "is_correct": 0},
                    {"content": "Backup dữ liệu", "is_correct": 0}
                ]
            }
        ]
        
        # Thêm câu hỏi cho một số quiz ngẫu nhiên
        selected_quizzes = random.sample(quizzes, min(len(quizzes), 3))
        
        for quiz in selected_quizzes:
            # Chọn ngẫu nhiên 2-3 câu hỏi để thêm
            questions_to_add = random.sample(additional_questions, random.randint(2, 3))
            
            for question_data in questions_to_add:
                question = Question(
                    quiz_id=quiz.quiz_id,
                    content=question_data["content"],
                    question_type="MULTIPLE_CHOICE"
                )
                
                db.add(question)
                db.flush()
                
                # Tạo các option cho câu hỏi
                for pos, option_data in enumerate(question_data["options"]):
                    option = Option(
                        question_id=question.question_id,
                        content=option_data["content"],
                        is_correct=option_data["is_correct"],
                        position=pos + 1
                    )
                    db.add(option)
            
            print(f"Đã thêm {len(questions_to_add)} câu hỏi cho quiz: {quiz.title}")
        
        db.commit()
        print("Đã thêm thành công các câu hỏi bổ sung!")
        
    except Exception as e:
        print(f"Lỗi khi thêm câu hỏi: {str(e)}")
        db.rollback()
    finally:
        db.close()

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
    seed_quiz_data()
    add_more_quiz_questions()