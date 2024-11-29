from sqlalchemy import Enum, ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from enum import Enum as PyEnum

from database import Base  # SQLAlchemy Base 클래스를 가져옵니다.
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
    
    def insert_reservation(
        db: Session,
        exam_name: str,
        exam_start_date: datetime,  # 적절한 데이터 타입으로 변경
        exam_end_date: datetime,    # 적절한 데이터 타입으로 변경
        exam_participants: int, # 또는 List 등 필요한 데이터 타입으로 변경
        user_id: int           # 또는 str 등 필요한 데이터 타입으로 변경
    ):
        new_reservation = Reservations(
            reservation_type=ReservationStatus.WAITING,
            exam_name=exam_name,
            exam_start_date=exam_start_date,
            exam_end_date=exam_end_date,
            exam_participants=exam_participants,
            user_id=user_id
        )
        
        db.add(new_reservation)  # 새로운 예약 객체를 세션에 추가합니다.
        db.commit()  # 데이터베이스에 커밋하여 변경사항을 저장합니다.
        db.refresh(new_reservation)  # 데이터베이스에서 새로 추가된 객체를 새로고침합니다.
        
        return new_reservation  # 추가된 예약 객체를 반환합니다.