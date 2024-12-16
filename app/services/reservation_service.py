from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from enums.reservation_status import ReservationStatus
from models.reservations import Reservations


# 신규 예약 등록
class ReservationNewService:
    def __init__(self, db: Session):
        self.db = db

    def create_reservation(self,
        exam_name: str, 
        exam_start_date: datetime,
        exam_end_date: datetime,
        exam_participants: int, 
        user_id: int
    ):
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

        # 기존 예약의 응시 인원도 포함
        total_participants_add = total_participants + exam_participants

        # 신규 예약 응시 인원을 포함한 응시 인원이 5만 명 초과하는지 확인
        if total_participants_add > 50000:
            return {"error": "해당 시간대에는 " + str(50000 - total_participants) + "명만 예약 가능합니다."}

        # 예약 객체 생성
        new_reservation = Reservations(
            reservation_type=ReservationStatus.WAITING,
            exam_name=exam_name,
            exam_start_date=exam_start_date,
            exam_end_date=exam_end_date,
            exam_participants=exam_participants,
            user_id=user_id
        )

        # 예약 추가
        try:
            self.db.add(new_reservation)  # 새로운 예약 객체를 세션에 추가
            self.db.commit()  # 변경사항 저장

            return {"message": "예약이 성공적으로 등록되었습니다."}
        except Exception as e:
            print(f'예약 등록 중 오류 발생: {e}')
            self.db.rollback()  # 오류 발생 시 롤백

            return {"error": "예약 등록 중 오류가 발생했습니다."}
        

# 예약되어있는 리스트 조회
class ReservationAvailableService:
    def __init__(self, db: Session):
        self.db = db  # 데이터베이스 세션 저장

    def select_available_reservation(self):
        
        # 오늘 날짜 기준으로 10일 전과 3일 전 계산
        today = datetime.now()
        ten_days_ahead = today + timedelta(days=10)
        three_days_ahead = today + timedelta(days=3)

        # 오늘 날짜 기준으로 10일전 부터 3일전 확정된 데이터만 조회
        query = self.db.query(Reservations).filter(
            Reservations.reservation_type == ReservationStatus.CONFIRMED,
            and_(
                Reservations.exam_start_date >= three_days_ahead,
                Reservations.exam_start_date <= ten_days_ahead
            )
        )

        # 쿼리 실행 및 결과 가져오기
        results = query.order_by(Reservations.exam_start_date).all()

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

# 예약 목록 조회
class ReservationListService:
    def __init__(self, db: Session):
        self.db = db

    def select_reservationList(self, user_id: int):

        # 관리자일 경우 전체 조회 아닐 경우 해당 사용자 ID 기준 조회
        if user_id != 999 :
            query = self.db.query(Reservations).filter(Reservations.user_id == user_id)
        else :
            query = self.db.query(Reservations)
        
        # 쿼리 실행 및 결과 가져오기
        results = query.order_by(Reservations.exam_start_date).all()  # 쿼리 결과를 한 번만 호출
        
        # 데이터 정제
        for reservation in results:
            if reservation.reservation_type == ReservationStatus.WAITING:
                reservation.reservation_type = 'WAITING'
            elif reservation.reservation_type == ReservationStatus.CONFIRMED:
                reservation.reservation_type = 'CONFIRMED'
            elif reservation.reservation_type == ReservationStatus.CANCELED:
                reservation.reservation_type = 'CANCELED'

        return results


# 예약 내역 수정
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
        

# 예약 삭제
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
        

# 예약 확정
class ReservationConfirmService:
    def __init__(self, db: Session):
        self.db = db

    def confirm_reservation(self,
        id: int
    ):
        
        # 예약 ID 기준 조회
        existing_reservation = self.db.query(Reservations).filter(Reservations.id == id).first()

        # 예약이 존재 하지 않을 경우
        if not existing_reservation:
            return {"error": "예약을 찾을 수 없습니다."}

        # 같은 시간대의 확정된 예약의 응시 인원 합산
        overlapping_participants = self.db.query(
            Reservations.exam_participants
        ).filter(
            and_(
                Reservations.exam_start_date <= existing_reservation.exam_start_date,
                Reservations.exam_end_date >= existing_reservation.exam_end_date,
                Reservations.reservation_type == ReservationStatus.CONFIRMED
            )
        ).all()

        # 총 응시 인원 계산
        total_participants = sum(reservation.exam_participants for reservation in overlapping_participants)

        # 확정된 응시 인원이 5만 명 초과하는지 확인
        if total_participants > 50000:
            return {"error": "해당 시간대에 확정된 응시 인원이 5만 명을 초과하였습니다."}

        # 기존 예약의 응시 인원도 포함
        total_participants_add = total_participants + existing_reservation.exam_participants

        # 수정 예약 응시 인원을 포함한 응시 인원이 5만 명 초과하는지 확인
        if total_participants_add > 50000:
            return {"error": "해당 시간대에는 " + str(50000 - total_participants) + "명만 확정 가능합니다."}
        
        # 예약 확정
        try:
            existing_reservation.reservation_type = ReservationStatus.CONFIRMED
            existing_reservation.modified_date = datetime.now() # 수정 시간 설정

            self.db.commit()  # 변경사항 저장

            return {"message": "예약이 성공적으로 확정되었습니다."}
        except Exception as e:
            print(f'예약 삭제 중 오류 발생: {e}')
            self.db.rollback()  # 오류 발생 시 롤백
            
            return {"error": "예약 삭제 중 오류가 발생했습니다."}
        

# 예약 인원 추가
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