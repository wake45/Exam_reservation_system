from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from enums.reservation_status import ReservationStatus
from models.reservations import Reservations

class ReservationModifyService:
    def __init__(self, db: Session):
        self.db = db  # 데이터베이스 세션 저장

    def modify_reservation(self,
        id: int,
        exam_name: str, 
        exam_start_date: datetime,
        exam_end_date: datetime,
        exam_participants: int, 
    ):
        
        # 예약 존재 여부 확인
        reservation = self.db.query(Reservations).filter(Reservations.id == id).first();

        # 예약이 존재하지 않을 경우
        if not reservation:
                return {"error": "예약을 찾을 수 없습니다."}

        # 현재 시간 및 3일 후 시간 구하기
        current_time = datetime.now()
        three_days_ago = current_time + timedelta(days=3)
        
        # 예약 시간 유효성 확인
        if exam_start_date > exam_end_date:
            return {"error": "시험 시작시간이 종료 시간 보다 빠릅니다."}

        # 시험 시작 날짜 확인(3일전)
        if exam_start_date < three_days_ago:
            return {"error": "예약은 현재 시간 기준 시험시작 3일 전 부터 가능합니다."}
        
        # 응시 인원 확인 (5만명 이하)
        if exam_participants > 50000:
            return {"error": "응시인원은 5만명 이하로만 가능합니다."}

        # 같은 시간대의 확정된 예약의 응시 인원 합산
        overlapping_participants = self.db.query(
            Reservations.exam_participants
        ).filter(
            and_(
                Reservations.exam_start_date <= exam_end_date,
                Reservations.exam_end_date >= exam_start_date,
                Reservations.reservation_type == ReservationStatus.CONFIRMED
            )
        ).all()

        # 총 응시 인원 계산
        total_participants = sum(reservation.exam_participants for reservation in overlapping_participants)

        # 확정된 응시 인원이 5만 명 이상인지 확인
        if total_participants >= 50000:
            return {"error": "해당 시간대에 확정된 응시 인원이 5만 명을 초과하였습니다."}

        # 수정 예약의 응시 인원도 포함
        total_participants_add = total_participants + exam_participants

        # 수정 예약 응시 인원을 포함한 응시 인원이 5만 명 초과하는지 확인
        if total_participants_add > 50000:
            return {"error": "해당 시간대에는 " + str(50000 - total_participants) + "명으로만 수정 가능합니다."}
        
        # 예약 수정
        try:
            reservation.exam_name = exam_name
            reservation.exam_start_date = exam_start_date
            reservation.exam_end_date = exam_end_date
            reservation.exam_participants = exam_participants
            reservation.modified_date = datetime.now() # 수정 시간 설정
            
            self.db.commit()  # 변경사항 저장

            return {"message": "예약이 성공적으로 수정되었습니다."}
        except Exception as e:
            print(f'예약 등록 중 오류 발생: {e}')
            self.db.rollback()  # 오류 발생 시 롤백

            return {"error": "예약 수정 중 오류가 발생했습니다."}