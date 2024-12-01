from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime

from enums.reservation_status import ReservationStatus
from models.reservations import Reservations

class ReservationDeleteService:
    def __init__(self, db: Session):
        self.db = db  # 데이터베이스 세션 저장

    def delete_reservation(self,
        id: int
    ):
        
        # 예약 ID 기준 조회
        existing_reservation = self.db.query(Reservations).filter(Reservations.id == id).first()

        # 예약이 존재하지 않을 경우
        if not existing_reservation:
            return {"error": "예약을 찾을 수 없습니다."}

        # 예약 삭제
        try:
            existing_reservation.reservation_type = ReservationStatus.CANCELED
            existing_reservation.canceled_date = datetime.now() # 삭제 시간 설정

            self.db.commit()  # 변경사항 저장

            return {"message": "예약이 성공적으로 삭제되었습니다."}
        except Exception as e:
            print(f'예약 삭제 중 오류 발생: {e}')
            self.db.rollback()  # 오류 발생 시 롤백
            
            return {"error": "예약 삭제 중 오류가 발생했습니다."}