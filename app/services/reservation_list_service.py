from sqlalchemy import and_
from sqlalchemy.orm import Session

from enums.reservation_status import ReservationStatus
from models.reservations import Reservations

class ReservationListService:
    def __init__(self, db: Session):
        self.db = db  # 데이터베이스 세션 저장

    def select_reservationList(self, user_id: int):
        if user_id != 999 :
            query = self.db.query(Reservations).filter(Reservations.user_id == user_id)
        else :
            query = self.db.query(Reservations)
        
        # 쿼리 실행 및 결과 가져오기
        results = query.all()  # 쿼리 결과를 한 번만 호출
        
        # 데이터 정제
        for reservation in results:
            if reservation.reservation_type == ReservationStatus.WAITING:
                reservation.reservation_type = 'WAITING'
            elif reservation.reservation_type == ReservationStatus.CONFIRMED:
                reservation.reservation_type = 'CONFIRMED'
            elif reservation.reservation_type == ReservationStatus.CANCELED:
                reservation.reservation_type = 'CANCELED'

        return results


