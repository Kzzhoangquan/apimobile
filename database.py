from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Kết nối MySQL với thông tin bạn cung cấp
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/elearning"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True để debug SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo tất cả các bảng
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()