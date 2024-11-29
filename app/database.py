from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy Base 클래스
Base = declarative_base()

# 데이터베이스 연결 URL
DATABASE_URL = "postgresql://postgres:0389@localhost:5432/database"

# 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 로컬
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 기본 클래스 생성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()