from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from enums.reservation_status import ReservationStatus
from models.reservations import Reservations

class ReservationAvailableService:
    def __init__(self, db: Session):
        self.db = db  # 데이터베이스 세션 저장

    def select_available_reservation(self):
        # 오늘 날짜 기준으로 6일 전과 3일 전 계산
        today = datetime.now()
        six_days_ahead = today + timedelta(days=6)
        three_days_ahead = today + timedelta(days=3)

        query = self.db.query(Reservations).filter(
            Reservations.reservation_type == ReservationStatus.CONFIRMED,
            and_(
                Reservations.exam_start_date >= three_days_ahead,  # 3일 전 (12월 3일)부터
                Reservations.exam_start_date <= six_days_ahead      # 6일 전 (12월 6일)까지
            )
        )

        # 쿼리 실행 및 결과 가져오기
        results = query.all()  # 쿼리 결과를 한 번만 호출

        # 데이터 정제
        for reservation in results:
            reservation_info = {
                "exam_start_date": reservation.exam_start_date,
                "exam_end_date": reservation.exam_end_date,
                "exam_participants": reservation.exam_participants,
            }

            # 결과를 리스트로 변환
            yield reservation_info

        return results


