from models import User, Course, Review, Lesson, Comment, Quiz, Question, Option, Enrollment, Wishlist, Notification, QuizResult, Base
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
        
        # 1. Tạo người dùng
        users = [
            User(
                username="nguyenvana",
                full_name="Nguyễn Văn A",
                password="password123",
                email="nguyenvana@example.com",
                phone="0123456789",
                avatar_url="https://randomuser.me/api/portraits/men/1.jpg",
                role="instructor"
            ),
            User(
                username="tranthib",
                full_name="Trần Thị B",
                password="password123",
                email="tranthib@example.com", 
                phone="0987654321",
                avatar_url="https://randomuser.me/api/portraits/women/1.jpg",
                role="instructor"
            ),
            User(
                username="lethic",
                full_name="Lê Thị C",
                password="password123",
                email="lethic@example.com",
                phone="0912345678",
                avatar_url="https://randomuser.me/api/portraits/women/2.jpg",
                role="student"
            ),
            User(
                username="phamvand",
                full_name="Phạm Văn D",
                password="password123",
                email="phamvand@example.com",
                phone="0911223344",
                avatar_url="https://randomuser.me/api/portraits/men/2.jpg",
                role="student"
            ),
            User(
                username="hoange",
                full_name="Hoàng E",
                password="password123",
                email="hoange@example.com",
                phone="0977889900",
                avatar_url="https://randomuser.me/api/portraits/men/3.jpg",
                role="student"
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        # 2. Tạo khóa học
        courses = [
            Course(
                owner_id=users[0].user_id,
                title="Lập trình Android từ cơ bản đến nâng cao",
                description="Khóa học giúp bạn học lập trình Android từ cơ bản đến nâng cao một cách nhanh chóng",
                thumbnail_url="https://play-lh.googleusercontent.com/PCpXdqvUWfCW1mXhH1Y_98yBpgsWxuTSTofy3NGMo9yBTATDyzVkqU580bfSln50bFU",
                price=299000,
                category="Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=users[1].user_id,
                title="Thiết kế UI/UX hiện đại",
                description="Học cách thiết kế giao diện người dùng đẹp mắt và trải nghiệm người dùng tốt nhất",
                thumbnail_url="https://img-c.udemycdn.com/course/750x422/2489934_ebe8_5.jpg",
                price=399000,
                category="Design",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=users[0].user_id,
                title="Lập trình Web Fullstack với MERN",
                description="Tìm hiểu MongoDB, Express, React và Node.js để xây dựng ứng dụng web hoàn chỉnh",
                thumbnail_url="https://miro.medium.com/v2/resize:fit:1400/1*gdOZZtHcGzIgY1ReLEZd0A.png",
                price=459000,
                category="Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=users[1].user_id,
                title="Digital Marketing từ A-Z",
                description="Nắm vững các chiến lược marketing số bao gồm SEO, Ads, Email và Social Media",
                thumbnail_url="https://d1vwxdpzbgdqj.cloudfront.net/s3fs-public/styles/banner_image/public/2023-05/digital_marketing.jpg",
                price=349000,
                category="Marketing",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=users[0].user_id,
                title="Khóa học Python cho người mới bắt đầu",
                description="Học lập trình Python một cách dễ hiểu, bài bản và có thực hành",
                thumbnail_url="https://images.ctfassets.net/otbh8469j9d3/4O5Q0rYd5u1txazHiXxq3O/e6a9267f3d02e168a71d33ae2057d2ee/python.jpg",
                price=259000,
                category="Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=users[1].user_id,
                title="Thiết kế logo chuyên nghiệp bằng Illustrator",
                description="Tạo ra những mẫu logo đẳng cấp chỉ trong vài giờ",
                thumbnail_url="https://99designs-blog.imgix.net/blog/wp-content/uploads/2020/06/logo_design_tips.jpg",
                price=299000,
                category="Design",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=users[0].user_id,
                title="Quản lý tài chính cá nhân thông minh",
                description="Biết cách kiểm soát chi tiêu và đầu tư hiệu quả",
                thumbnail_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_UvVk98H_sG3hRp_SnhhFzXp6zQPE2hzmLQ&usqp=CAU",
                price=199000,
                category="Business",
                created_at=datetime.utcnow()
            ),
        ]

        for course in courses:
            db.add(course)
        db.commit()
        
        # 3. Tạo bài học (Lessons) cho các khóa học
        lessons_data = {
            "Lập trình Android từ cơ bản đến nâng cao": [
                ("Giới thiệu về Android", "https://example.com/video1.mp4", 1800, 1),
                ("Cài đặt môi trường phát triển", "https://example.com/video2.mp4", 2400, 2),
                ("Tạo ứng dụng Android đầu tiên", "https://example.com/video3.mp4", 3000, 3),
                ("Layouts trong Android", "https://example.com/video4.mp4", 2700, 4),
                ("Activities và Intents", "https://example.com/video5.mp4", 3300, 5)
            ],
            "Thiết kế UI/UX hiện đại": [
                ("Nguyên tắc thiết kế UI/UX", "https://example.com/design1.mp4", 2100, 1),
                ("Màu sắc và Typography", "https://example.com/design2.mp4", 1800, 2),
                ("Wireframing và Prototyping", "https://example.com/design3.mp4", 2500, 3),
                ("User Testing", "https://example.com/design4.mp4", 2200, 4)
            ],
            "Lập trình Web Fullstack với MERN": [
                ("Giới thiệu về MERN Stack", "https://example.com/mern1.mp4", 1500, 1),
                ("MongoDB: Cơ sở dữ liệu NoSQL", "https://example.com/mern2.mp4", 2800, 2),
                ("Express.js: Web Framework", "https://example.com/mern3.mp4", 2600, 3),
                ("React.js: Frontend Library", "https://example.com/mern4.mp4", 3200, 4),
                ("Node.js: JavaScript Runtime", "https://example.com/mern5.mp4", 2900, 5)
            ],
            "Digital Marketing từ A-Z": [
                ("Cơ bản về Digital Marketing", "https://example.com/dm1.mp4", 1900, 1),
                ("SEO và SEM", "https://example.com/dm2.mp4", 2300, 2),
                ("Email Marketing", "https://example.com/dm3.mp4", 1700, 3),
                ("Social Media Marketing", "https://example.com/dm4.mp4", 2000, 4)
            ],
            "Khóa học Python cho người mới bắt đầu": [
                ("Python là gì?", "https://example.com/python1.mp4", 1600, 1),
                ("Biến và kiểu dữ liệu", "https://example.com/python2.mp4", 2200, 2),
                ("Cấu trúc điều khiển", "https://example.com/python3.mp4", 2500, 3),
                ("Hàm trong Python", "https://example.com/python4.mp4", 2100, 4),
                ("Lập trình hướng đối tượng", "https://example.com/python5.mp4", 2700, 5)
            ]
        }
        
        lessons = []
        for course in courses:
            course_title = course.title
            if course_title in lessons_data:
                for lesson_data in lessons_data[course_title]:
                    lesson = Lesson(
                        course_id=course.course_id,
                        title=lesson_data[0],
                        video_url=lesson_data[1],
                        duration=lesson_data[2],
                        position=lesson_data[3]
                    )
                    db.add(lesson)
                    lessons.append(lesson)
        db.commit()
        
        # 4. Tạo đánh giá (Reviews) cho các khóa học
        for course in courses:
            for user in users[2:]: # Chỉ học viên đánh giá
                rating = random.randint(3, 5)
                comment_texts = [
                    "Khóa học rất hay và đầy đủ thông tin!",
                    "Giảng viên giảng dạy dễ hiểu và tâm huyết.",
                    "Nội dung cập nhật và thực tế, áp dụng được ngay.",
                    "Tôi đã học được rất nhiều từ khóa học này.",
                    "Rất hài lòng với những kiến thức nhận được."
                ]
                review = Review(
                    user_id=user.user_id,
                    course_id=course.course_id,
                    rating=rating,
                    comment=random.choice(comment_texts),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.add(review)
        db.commit()
        
        # 5. Tạo ghi danh (Enrollments) cho các khóa học
        for user in users[2:]: # Học viên
            for course in courses:
                if random.random() > 0.3: # 70% cơ hội đăng ký
                    enrollment = Enrollment(
                        user_id=user.user_id,
                        course_id=course.course_id,
                        enrolled_at=datetime.utcnow() - timedelta(days=random.randint(30, 60)),
                        progress=random.uniform(0, 100)
                    )
                    db.add(enrollment)
        db.commit()
        
        # 6. Tạo danh sách yêu thích (Wishlists)
        for user in users:
            for course in courses:
                if random.random() > 0.7: # 30% cơ hội thêm vào wishlist
                    wishlist = Wishlist(
                        user_id=user.user_id,
                        course_id=course.course_id,
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 20))
                    )
                    db.add(wishlist)
        db.commit()
        
        # 7. Tạo bình luận (Comments) cho các bài học
        comment_texts = [
            "Cảm ơn giảng viên đã giải thích rõ ràng!",
            "Tôi gặp khó khăn ở phần này, có thể giải thích thêm không?",
            "Rất hữu ích, tôi đã áp dụng được ngay.",
            "Nội dung quá hay, cần thêm nhiều bài tập thực hành.",
            "Tôi thích cách trình bày này, dễ hiểu và súc tích."
        ]
        
        for lesson in lessons:
            for user in users[2:]: # Học viên bình luận
                if random.random() > 0.5: # 50% cơ hội bình luận
                    comment = Comment(
                        user_id=user.user_id,
                        lesson_id=lesson.lesson_id,
                        comment=random.choice(comment_texts),
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
                    )
                    db.add(comment)
        db.commit()
        
        # 8. Tạo thông báo (Notifications)
        notifications = [
            Notification(
                title="Khóa học mới!",
                message="Chúng tôi vừa ra mắt khóa học mới, hãy khám phá ngay!",
                is_read=0,
                created_at=datetime.utcnow() - timedelta(days=3),
                image_url="https://example.com/notification1.jpg"
            ),
            Notification(
                title="Giảm giá đặc biệt",
                message="Nhân dịp kỷ niệm, giảm giá 30% cho tất cả khóa học!",
                is_read=0,
                created_at=datetime.utcnow() - timedelta(days=7),
                image_url="https://example.com/notification2.jpg"
            ),
            Notification(
                title="Cập nhật nội dung",
                message="Chúng tôi vừa cập nhật nội dung mới cho các khóa học.",
                is_read=0,
                created_at=datetime.utcnow() - timedelta(days=10),
                image_url="https://example.com/notification3.jpg"
            )
        ]
        
        for notification in notifications:
            db.add(notification)
        db.commit()
        
        # Kết nối thông báo với người dùng
        for user in users:
            for notification in notifications:
                if random.random() > 0.3: # 70% cơ hội nhận thông báo
                    user.notifications.append(notification)
        db.commit()
        
        # 9. Tạo Quiz, Question và Option
        # Quiz data - chứa các quiz và câu hỏi cho từng bài học
        quiz_data = {
            "Lập trình Android từ cơ bản đến nâng cao": {
                "Giới thiệu về Android": {
                    "title": "Quiz về Android cơ bản",
                    "questions": [
                        {
                            "content": "Android là nền tảng hệ điều hành được phát triển bởi công ty nào?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Apple", "is_correct": 0},
                                {"content": "Google", "is_correct": 1},
                                {"content": "Microsoft", "is_correct": 0},
                                {"content": "Samsung", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "Version đầu tiên của Android có tên là gì?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Cupcake", "is_correct": 0},
                                {"content": "Donut", "is_correct": 0},
                                {"content": "Alpha", "is_correct": 1},
                                {"content": "Eclair", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "Ngôn ngữ lập trình chính được sử dụng trong phát triển Android native là gì?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Java", "is_correct": 0},
                                {"content": "Kotlin", "is_correct": 0},
                                {"content": "C#", "is_correct": 0},
                                {"content": "Cả Java và Kotlin", "is_correct": 1}
                            ]
                        }
                    ]
                },
                "Cài đặt môi trường phát triển": {
                    "title": "Quiz về môi trường phát triển Android",
                    "questions": [
                        {
                            "content": "Công cụ chính để phát triển ứng dụng Android là gì?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Eclipse", "is_correct": 0},
                                {"content": "Android Studio", "is_correct": 1},
                                {"content": "Visual Studio", "is_correct": 0},
                                {"content": "Xcode", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "JDK là viết tắt của?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Java Development Kit", "is_correct": 1},
                                {"content": "Java Deployment Kit", "is_correct": 0},
                                {"content": "Java Design Kit", "is_correct": 0},
                                {"content": "Java Developer Knowledge", "is_correct": 0}
                            ]
                        }
                    ]
                }
            },
            "Thiết kế UI/UX hiện đại": {
                "Nguyên tắc thiết kế UI/UX": {
                    "title": "Quiz về nguyên tắc UI/UX",
                    "questions": [
                        {
                            "content": "Nguyên tắc nào KHÔNG phải là một trong những nguyên tắc cơ bản của thiết kế UI/UX?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Consistency (Nhất quán)", "is_correct": 0},
                                {"content": "Visibility (Khả năng hiện thị)", "is_correct": 0},
                                {"content": "Complexity (Phức tạp)", "is_correct": 1},
                                {"content": "Feedback (Phản hồi)", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "Tính khả dụng (Usability) trong UI/UX đề cập đến điều gì?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Vẻ đẹp của giao diện", "is_correct": 0},
                                {"content": "Khả năng người dùng sử dụng sản phẩm một cách hiệu quả", "is_correct": 1},
                                {"content": "Tốc độ tải trang", "is_correct": 0},
                                {"content": "Số lượng chức năng của sản phẩm", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "Heatmap trong UI/UX được sử dụng để làm gì?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Đo lường thời gian tải trang", "is_correct": 0},
                                {"content": "Theo dõi vị trí con trỏ chuột và sự chú ý của người dùng", "is_correct": 1},
                                {"content": "Kiểm tra tốc độ internet", "is_correct": 0},
                                {"content": "Đánh giá hiệu suất máy chủ", "is_correct": 0}
                            ]
                        }
                    ]
                }
            },
            "Lập trình Web Fullstack với MERN": {
                "Giới thiệu về MERN Stack": {
                    "title": "Quiz về MERN Stack",
                    "questions": [
                        {
                            "content": "MERN stack là viết tắt của những gì?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "MongoDB, Express, React, Node.js", "is_correct": 1},
                                {"content": "MySQL, Express, React, Node.js", "is_correct": 0},
                                {"content": "MongoDB, Ember, React, Node.js", "is_correct": 0},
                                {"content": "MySQL, Express, Ruby, Node.js", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "Trong MERN stack, MongoDB được sử dụng cho mục đích gì?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Front-end development", "is_correct": 0},
                                {"content": "Back-end development", "is_correct": 0},
                                {"content": "Database management", "is_correct": 1},
                                {"content": "Server-side rendering", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "React.js trong MERN stack là một thư viện phát triển?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Back-end", "is_correct": 0},
                                {"content": "Front-end", "is_correct": 1},
                                {"content": "Database", "is_correct": 0},
                                {"content": "Server", "is_correct": 0}
                            ]
                        }
                    ]
                }
            },
            "Khóa học Python cho người mới bắt đầu": {
                "Python là gì?": {
                    "title": "Quiz về cơ bản Python",
                    "questions": [
                        {
                            "content": "Python là ngôn ngữ lập trình thuộc loại nào?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Compiled language", "is_correct": 0},
                                {"content": "Interpreted language", "is_correct": 1},
                                {"content": "Markup language", "is_correct": 0},
                                {"content": "Machine language", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "Ai là người phát triển ngôn ngữ Python?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "Guido van Rossum", "is_correct": 1},
                                {"content": "James Gosling", "is_correct": 0},
                                {"content": "Bjarne Stroustrup", "is_correct": 0},
                                {"content": "Tim Berners-Lee", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "Python được phát hành lần đầu tiên vào năm nào?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "1989", "is_correct": 0},
                                {"content": "1991", "is_correct": 1},
                                {"content": "1995", "is_correct": 0},
                                {"content": "2000", "is_correct": 0}
                            ]
                        }
                    ]
                },
                "Biến và kiểu dữ liệu": {
                    "title": "Quiz về biến và kiểu dữ liệu trong Python",
                    "questions": [
                        {
                            "content": "Trong Python, kiểu dữ liệu nào sau đây là kiểu dữ liệu bất biến (immutable)?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "List", "is_correct": 0},
                                {"content": "Dictionary", "is_correct": 0},
                                {"content": "Tuple", "is_correct": 1},
                                {"content": "Set", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "Cách khai báo biến trong Python như thế nào?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "var name = value", "is_correct": 0},
                                {"content": "name = value", "is_correct": 1},
                                {"content": "dim name as value", "is_correct": 0},
                                {"content": "int name = value", "is_correct": 0}
                            ]
                        },
                        {
                            "content": "Trong Python, kiểu dữ liệu nào được sử dụng để lưu trữ dữ liệu có thứ tự và không thể thay đổi?",
                            "type": "MULTIPLE_CHOICE",
                            "options": [
                                {"content": "List", "is_correct": 0},
                                {"content": "Tuple", "is_correct": 1},
                                {"content": "Dictionary", "is_correct": 0},
                                {"content": "Set", "is_correct": 0}
                            ]
                        }
                    ]
                }
            }
        }
        
        # Tạo Quiz, Question và Option
        for course in courses:
            course_title = course.title
            if course_title in quiz_data:
                # Lấy danh sách lesson của khóa học
                course_lessons = db.query(Lesson).filter(Lesson.course_id == course.course_id).all()
                lesson_dict = {lesson.title: lesson for lesson in course_lessons}
                
                for lesson_title, quiz_info in quiz_data[course_title].items():
                    if lesson_title in lesson_dict:
                        lesson = lesson_dict[lesson_title]
                        
                        # Tạo quiz
                        quiz = Quiz(
                            lesson_id=lesson.lesson_id,
                            title=quiz_info["title"],
                            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                        )
                        db.add(quiz)
                        db.flush()  # Để lấy quiz_id
                        
                        # Tạo câu hỏi và lựa chọn
                        for q_data in quiz_info["questions"]:
                            question = Question(
                                quiz_id=quiz.quiz_id,
                                content=q_data["content"],
                                question_type=q_data["type"]
                            )
                            db.add(question)
                            db.flush()  # Để lấy question_id
                            
                            # Tạo các lựa chọn
                            for idx, opt_data in enumerate(q_data["options"]):
                                option = Option(
                                    question_id=question.question_id,
                                    content=opt_data["content"],
                                    is_correct=opt_data["is_correct"],
                                    position=idx
                                )
                                db.add(option)
                        
                        # Tạo kết quả quiz cho học viên
                        for user in users[2:]:  # Chỉ học viên làm quiz
                            if random.random() > 0.4:  # 60% cơ hội làm quiz
                                correct = random.randint(0, len(quiz_info["questions"]))
                                total = len(quiz_info["questions"])
                                quiz_result = QuizResult(
                                    user_id=user.user_id,
                                    quiz_id=quiz.quiz_id,
                                    total_score=f"{correct}/{total}",
                                    completed_at=datetime.utcnow() - timedelta(days=random.randint(1, 15))
                                )
                                db.add(quiz_result)
        db.commit()
        print("Đã thêm dữ liệu mẫu thành công!")
        
    except Exception as e:
        db.rollback()
        print(f"Lỗi: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()