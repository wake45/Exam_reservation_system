from sqlalchemy import Enum, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base
from enums.reservation_status import ReservationStatus

class Reservations(Base):
    __tablename__ = 'Reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 예약 ID
    reservation_type = Column(Enum(ReservationStatus), nullable=False)  # 예약 상태
    exam_name = Column(String(100), nullable=False)  # 시험명
    exam_start_date = Column(DateTime, nullable=False)  # 시험 시작 시간
    exam_end_date = Column(DateTime, nullable=False)  # 시험 종료 시간
    exam_participants = Column(Integer, nullable=False)  # 시험 응시 인원 수
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)  # 사용자ID (Users)
    
    # 예약 생성일, 수정일, 취소일
    created_date = Column(DateTime, default=datetime.now())
    modified_date = Column(DateTime)
    canceled_date = Column(DateTime)

    # ForeignKey 관계 정의
    user = relationship("Users", back_populates="reservations")  # User 모델과의 관계