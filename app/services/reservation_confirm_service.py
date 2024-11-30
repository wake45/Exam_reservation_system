from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime

from enums.reservation_status import ReservationStatus
from models.reservations import Reservations

class ReservationConfirmService:
    def __init__(self, db: Session):
        self.db = db  # 데이터베이스 세션 저장

    def confirm_reservation(self,
        id: int
    ):
        existing_reservation = self.db.query(Reservations).filter(Reservations.id == id).first()

        if not existing_reservation:
            return {"error": "예약을 찾을 수 없습니다."}

        # 예약의 시작 및 종료 시간
        start_time = existing_reservation.exam_start_date
        end_time = existing_reservation.exam_end_date

        # 같은 시간대의 확정된 예약의 응시 인원 합산
        overlapping_participants = self.db.query(
            Reservations.exam_participants
        ).filter(
            and_(
                Reservations.exam_start_date < end_time,
                Reservations.exam_end_date > start_time,
                Reservations.reservation_type == ReservationStatus.CONFIRMED
            )
        ).all()

        # 총 응시 인원 계산
        total_participants = sum(reservation.exam_participants for reservation in overlapping_participants)

        # 기존 예약의 응시 인원도 포함
        total_participants += existing_reservation.exam_participants

        # 응시 인원이 5만 명 초과하는지 확인
        if total_participants > 50000:
            return {"error": "해당 시간대에 응시 인원이 5만 명을 초과하였습니다."}
        
        # 예약 확정
        try:
            existing_reservation.reservation_type = ReservationStatus.CONFIRMED
            existing_reservation.modified_date = datetime.now()

            self.db.commit()  # 데이터베이스에 커밋

            return {"message": "예약이 성공적으로 확정되었습니다."}
        except Exception as e:
            print(f'예약 삭제 중 오류 발생: {e}')
            self.db.rollback()  # 오류 발생 시 롤백
            
            return {"error": "예약 삭제 중 오류가 발생했습니다."}