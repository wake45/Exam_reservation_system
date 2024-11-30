from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime

from models.reservations import Reservations

class ReservationAddService:
    def __init__(self, db: Session):
        self.db = db  # 데이터베이스 세션 저장

    def add_reservation(self,
        id: int,
        additional_exam_participants: int, 
    ):
        existing_reservation = self.db.query(Reservations).filter(Reservations.id == id).first()

        if not existing_reservation:
            return {"error": "예약을 찾을 수 없습니다."}

        # 기존 응시 인원과 추가 인원을 합산하여 5만명 초과 여부 확인
        total_participants = existing_reservation.exam_participants + additional_exam_participants

        if total_participants > 50000:
            return {"error": "응시인원은 5만명까지만 가능합니다."}

        # 예약 수정
        try:
            existing_reservation.exam_participants = total_participants  # 응시 인원 업데이트
            existing_reservation.modified_date = datetime.now()  # 현재 시간을 설정

            self.db.commit()  # 데이터베이스에 커밋

            return {"message": "예약 인원이 성공적으로 추가되었습니다."}
        except Exception as e:
            print(f'예약 등록 중 오류 발생: {e}')
            self.db.rollback()  # 오류 발생 시 롤백
            
            return {"error": "예약 인원 추가 중 오류가 발생했습니다."}