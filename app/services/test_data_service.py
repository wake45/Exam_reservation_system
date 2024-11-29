from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from models.reservations import Reservations
from models.users import Users

class TestDataService:
    def __init__(self, db: Session):
        self.db = db

    def create_test_data(self, user_name: str):

        test_data_form = Users(user_name=user_name)
        self.db.add(test_data_form)

        try:
            self.db.commit()  # 변경 사항 저장
            return {"message": "테스트 데이터 생성 완료", "user_name" : user_name}
        except IntegrityError:
            self.db.rollback()  # 오류 발생 시 롤백
            return {"error": "테스트 데이터 생성 중 오류 발생"}