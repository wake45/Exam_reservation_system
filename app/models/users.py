from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Users(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, autoincrement=True) # 사용자 ID
    user_name = Column(String(50), nullable=False) # 사용자명
    created_date = Column(DateTime, default=datetime.now) # 생성일
    modified_date = Column(DateTime, default=datetime.now, onupdate=datetime.now) # 수정일

    # Reservations와의 관계 설정
    reservations = relationship("Reservations", back_populates="user")