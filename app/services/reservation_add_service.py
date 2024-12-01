from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime

from enums.reservation_status import ReservationStatus
from models.reservations import Reservations

class ReservationAddService:
    def __init__(self, db: Session):
        self.db = db  # 데이터베이스 세션 저장

    def add_reservation(self,
        id: int,
        additional_exam_participants: int, 
    ):
        
        # 예약 ID 기준 조회
        existing_reservation = self.db.query(Reservations).filter(Reservations.id == id).first()

        # 예약이 존재하지 않을 경우
        if not existing_reservation:
            return {"error": "예약을 찾을 수 없습니다."}
        
        # 같은 시간대의 확정된 예약의 응시 인원 합산
        overlapping_participants = self.db.query(
            Reservations.exam_participants
        ).filter(
            and_(
                Reservations.exam_start_date <= existing_reservation.exam_end_date,
                Reservations.exam_end_date >= existing_reservation.exam_start_date,
                Reservations.reservation_type == ReservationStatus.CONFIRMED
            )
        ).all()

        # 총 응시 인원 계산
        total_participants = sum(reservation.exam_participants for reservation in overlapping_participants)

        # 확정된 응시 인원이 5만 명 이상인지 확인
        if total_participants >= 50000:
            return {"error": "해당 시간대에 확정된 응시 인원이 5만 명을 초과하였습니다."}
        
        # 추가 응시 인원도 포함
        total_participants_add = total_participants + additional_exam_participants

        # 추가 응시 인원을 포함한 응시 인원이 5만 명 초과하는지 확인
        if total_participants_add > 50000:
            return {"error": "해당 시간대에는 " + str(50000 - total_participants) + "명만 추가 가능합니다."}

        # 예약 수정
        try:
            existing_reservation.exam_participants = existing_reservation.exam_participants + additional_exam_participants  # 응시 인원 업데이트
            existing_reservation.modified_date = datetime.now()  # 수정 시간 설정

            self.db.commit()  # 변경사항 저장

            return {"message": "예약 인원이 성공적으로 추가되었습니다."}
        except Exception as e:
            print(f'예약 등록 중 오류 발생: {e}')
            self.db.rollback()  # 오류 발생 시 롤백
            
            return {"error": "예약 인원 추가 중 오류가 발생했습니다."}