# 설명
## 프로젝트명 : Exam_reservation_system ( 시험 일정 예약 시스템 API 개발 )
## 사용기술 : python, fastAPI, PostgreSQL
## 기간 : 2024년 11/25 ~ 12/2

# 주요 고려사항
## 1. 관리자 권한 관련
### 관리자는 id를 "999"로 해서 권한 기능 생략해서 개발 (id가 "999" 경우 전체 조회)
## 2. 확정 취소 기능 생략
### 확정된 기능에 대해서는 취소할 수 없고 관리자만 수정,삭제가 가능하도록 개발
## 3. 신규예약시 보여주는 예약 가능 일자 기간 최대 10일후 예약까지 보여주도록 개발
### 3일 전부터 신청이 가능하므로 기준을 3일후~10일후 까지 예약 정보만 보여주도록 개발

# History
## 11월 28일 
### Git Repository 생성
### ERD 생성
### DB 및 테이블 생성
### DB 수정 및 VIEW파일 생성
### root 화면 연결 및 VIEW파일 수정

## 11월 29일
### routes 생성
### services 생성
### models 생성
### 신규 예약 등록 기능 추가
### 테스트 데이터 생성 기능 추가
### 예약 내역 목록 조회 기능 추가

## 11월 30일
### 수정 삭제 확정 추가 기능 추가
### 신규 예약에 확정 인원 체크 로직 추가
### 확정 기능에 확정 인원 체크 로직 추가
### 신규 예약시 현재 예약되어 있는 시간대 및 응시인원 확인 가능하도록 로직 추가

## 12월 1일
### 기능테스트 후 결함 로직 수정
### 디자인 수정
### 주석 정리
### API 문서 및 설계서 제작