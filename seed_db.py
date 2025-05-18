from models import User, Course, Review, Base
from database import SessionLocal, engine
from datetime import datetime

def seed_database():
    # Tạo tất cả các bảng nếu chưa tồn tại
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Kiểm tra xem đã có dữ liệu chưa
        if db.query(User).count() > 0:
            print("Dữ liệu đã tồn tại, bỏ qua quá trình seed!")
            return
        
        # Tạo người dùng mẫu
        user1 = User(
            username="nguyenvana",
            full_name="Nguyễn Văn A",
            password="password123",
            email="nguyenvana@example.com",
            phone="0123456789",
            avatar_url="https://randomuser.me/api/portraits/men/1.jpg",
            role="instructor"
        )
        
        user2 = User(
            username="tranthib",
            full_name="Trần Thị B",
            password="password123",
            email="tranthib@example.com", 
            phone="0987654321",
            avatar_url="https://randomuser.me/api/portraits/women/1.jpg",
            role="instructor"
        )
        
        db.add(user1)
        db.add(user2)
        db.commit()
        
        # Tạo khóa học mẫu
        from datetime import datetime

        courses = [
            Course(
                owner_id=user1.user_id,
                title="Lập trình Android từ cơ bản đến nâng cao",
                description="Khóa học giúp bạn học lập trình Android từ cơ bản đến nâng cao một cách nhanh chóng",
                thumbnail_url="https://play-lh.googleusercontent.com/PCpXdqvUWfCW1mXhH1Y_98yBpgsWxuTSTofy3NGMo9yBTATDyzVkqU580bfSln50bFU",
                price=299000,
                category="Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Thiết kế UI/UX hiện đại",
                description="Học cách thiết kế giao diện người dùng đẹp mắt và trải nghiệm người dùng tốt nhất",
                thumbnail_url="https://img-c.udemycdn.com/course/750x422/2489934_ebe8_5.jpg",
                price=399000,
                category="Design",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user1.user_id,
                title="Lập trình Web Fullstack với MERN",
                description="Tìm hiểu MongoDB, Express, React và Node.js để xây dựng ứng dụng web hoàn chỉnh",
                thumbnail_url="https://miro.medium.com/v2/resize:fit:1400/1*gdOZZtHcGzIgY1ReLEZd0A.png",
                price=459000,
                category="Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Digital Marketing từ A-Z",
                description="Nắm vững các chiến lược marketing số bao gồm SEO, Ads, Email và Social Media",
                thumbnail_url="https://d1vwxdpzbgdqj.cloudfront.net/s3fs-public/styles/banner_image/public/2023-05/digital_marketing.jpg",
                price=349000,
                category="Marketing",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user1.user_id,
                title="Khóa học Python cho người mới bắt đầu",
                description="Học lập trình Python một cách dễ hiểu, bài bản và có thực hành",
                thumbnail_url="https://images.ctfassets.net/otbh8469j9d3/4O5Q0rYd5u1txazHiXxq3O/e6a9267f3d02e168a71d33ae2057d2ee/python.jpg",
                price=259000,
                category="Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Thiết kế logo chuyên nghiệp bằng Illustrator",
                description="Tạo ra những mẫu logo đẳng cấp chỉ trong vài giờ",
                thumbnail_url="https://99designs-blog.imgix.net/blog/wp-content/uploads/2020/06/logo_design_tips.jpg",
                price=299000,
                category="Design",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user1.user_id,
                title="Quản lý tài chính cá nhân thông minh",
                description="Biết cách kiểm soát chi tiêu và đầu tư hiệu quả",
                thumbnail_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_UvVk98H_sG3hRp_SnhhFzXp6zQPE2hzmLQ&usqp=CAU",
                price=199000,
                category="Business",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Chứng chỉ AWS Certified Cloud Practitioner",
                description="Chuẩn bị đầy đủ kiến thức để thi chứng chỉ đám mây cơ bản của Amazon Web Services",
                thumbnail_url="https://d1.awsstatic.com/training-and-certification/Certification%20Badges/AWS-Certified_Cloud-Practitioner_badge.1f60f6f903e8b7db87d6f6b9c4b2f7bc2f4ae5c0.png",
                price=499000,
                category="IT & Software",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user1.user_id,
                title="Học Java cơ bản cho người mới bắt đầu",
                description="Làm quen với lập trình hướng đối tượng qua ngôn ngữ Java",
                thumbnail_url="https://upload.wikimedia.org/wikipedia/en/3/30/Java_programming_language_logo.svg",
                price=299000,
                category="Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Kỹ năng giao tiếp và thuyết trình chuyên nghiệp",
                description="Nâng cao khả năng nói chuyện, thuyết trình trước đám đông và xây dựng sự tự tin",
                thumbnail_url="https://media.licdn.com/dms/image/C5612AQH7GP4s5dRmwQ/article-cover_image-shrink_720_1280/0/1607617196812?e=2147483647&v=beta&t=ScgUBlzp8f7mrxzscw6Cahv_jVU3b_zN5_GvbhGODCw",
                price=199000,
                category="Personal Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user1.user_id,
                title="React Native - Xây dựng ứng dụng di động đa nền tảng",
                description="Sử dụng React Native để phát triển ứng dụng cho cả Android và iOS",
                thumbnail_url="https://miro.medium.com/v2/resize:fit:720/format:webp/1*70oS53-Rtq3NqUJYslbT7g.png",
                price=379000,
                category="Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Chụp ảnh và chỉnh sửa ảnh chuyên nghiệp",
                description="Học cách tạo ra những bức ảnh đẹp và chỉnh sửa bằng Lightroom, Photoshop",
                thumbnail_url="https://photographycourse.net/wp-content/uploads/2014/11/Best-Photography-Courses.jpg",
                price=319000,
                category="Photography & Video",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user1.user_id,
                title="Tự học Excel từ cơ bản đến nâng cao",
                description="Thành thạo các hàm, biểu đồ, Pivot Table và VBA trong Excel",
                thumbnail_url="https://trungtamexcel.com/wp-content/uploads/2021/03/excel-nang-cao.png",
                price=249000,
                category="Office Productivity",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Laravel Framework cho lập trình viên PHP",
                description="Tạo ứng dụng web mạnh mẽ với Laravel và các kiến thức nâng cao",
                thumbnail_url="https://i.ytimg.com/vi/lGE6YPS1n5k/maxresdefault.jpg",
                price=289000,
                category="Development",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user1.user_id,
                title="Machine Learning cơ bản với Python",
                description="Học cách xây dựng mô hình học máy và thuật toán ML cơ bản",
                thumbnail_url="https://miro.medium.com/v2/resize:fit:1400/1*VgL3cTgXFPz1G4NgyfMX8A.jpeg",
                price=459000,
                category="Data Science",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Hướng dẫn tạo Blog với WordPress",
                description="Tạo blog cá nhân, thiết lập giao diện, cài plugin và tối ưu SEO",
                thumbnail_url="https://colorlib.com/wp/wp-content/uploads/sites/2/wordpress-blog-themes.jpg",
                price=199000,
                category="IT & Software",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user1.user_id,
                title="Blender cơ bản - Dựng hình và hoạt họa 3D",
                description="Học cách sử dụng Blender để dựng mô hình 3D và tạo hoạt họa",
                thumbnail_url="https://static.skillshare.com/uploads/video/thumbnails/1d7b7f2dc7f3cf1eae822bb332642db7/original",
                price=379000,
                category="Design",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Tiếng Anh giao tiếp cơ bản",
                description="Nâng cao khả năng giao tiếp tiếng Anh hàng ngày và nơi công sở",
                thumbnail_url="https://i.ytimg.com/vi/HD1mZ4jLNJc/maxresdefault.jpg",
                price=219000,
                category="Language",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user1.user_id,
                title="Kỹ năng quản lý dự án với Agile Scrum",
                description="Làm chủ phương pháp Agile và quản lý team hiệu quả",
                thumbnail_url="https://agilemania.com/wp-content/uploads/2023/04/ScrumMasterTraining.jpg",
                price=399000,
                category="Business",
                created_at=datetime.utcnow()
            ),
            Course(
                owner_id=user2.user_id,
                title="Làm video TikTok chuyên nghiệp",
                description="Tạo video viral cho mạng xã hội bằng CapCut, Canva và điện thoại",
                thumbnail_url="https://www.veed.io/learn/wp-content/uploads/2023/03/TikTok-Videos.png",
                price=199000,
                category="Photography & Video",
                created_at=datetime.utcnow()
            )
        ]

        for course in courses:
            db.add(course)
        db.commit()
        
        # Tạo đánh giá mẫu
        for course in courses:
            for i in range(5):
                review = Review(
                    user_id=user1.user_id if i % 2 == 0 else user2.user_id,
                    course_id=course.course_id,
                    rating=4 + (i % 2),  # Rating từ 4-5
                    comment=f"Đánh giá số {i+1} cho khóa học này. Rất hay và bổ ích!",
                    created_at=datetime.utcnow()
                )
                db.add(review)
        db.commit()
        
        print("Đã thêm dữ liệu mẫu thành công!")
        
    except Exception as e:
        db.rollback()
        print(f"Lỗi: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()