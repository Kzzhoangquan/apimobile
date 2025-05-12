from models import Base
from database import engine


# Tạo tất cả các bảng trong cơ sở dữ liệu
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_db()