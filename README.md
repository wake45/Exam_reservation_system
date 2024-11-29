# 설명
## 프로젝트명 : Exam_reservation_system ( 시험 일정 예약 시스템 API 개발 )
## 사용기술 : python, fastAPI, PostgreSQL
## 기간 : 2024년 11/25 ~ 12/2

# 주요 고려사항
## 1. 관리자 권한 관련
### 관리자는 id를 ""로 해서 권한 기능 생략해서 개발 (id가 "" 경우 전체 조회)
## 2. 확정 취소 기능 생략
### 확정된 기능에 대해서는 취소할 수 없고 관리자만 수정이 가능하도록 개발
## 3. 신규예약시 보여주는 예약 가능 일자 기간
### 3일 전부터 신청이 가능하므로 간단하게 6일전 ~ 3일전 까지 일자 만 보여주도록 개발
## 4. 시험을 동 시간대 여러시험이 예약 또는 확정이 가능하도록 개발?
### 테스트1 12:00 ~ 14:00(3만명) / 테스트2 13:00 ~ 15:00(3만명) 일 경우
### 다른 시간대를 제외하고 13:00 ~ 14:00 만 5만명이 초과되는데 이 부분에 대한 로직을 개발 불가능(시간....)
### 때문에 동 시간대 하나의 시험만 가능하도록 우선적으로 개발 예정(추후 변경)
### (예약하려는 시간대이미 예약 확정 된 시험이 있을 경우 오류) 
### - 신규 예약시 예약 되어있는 시간대를 노출하여 고객 입장에서 시간대 파악할 수 있도록 개발
### - 가능한 응시인원 노출은 5만명 고정...

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