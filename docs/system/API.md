# API 목록과 계약 초안

> **문서 역할:** 프론트엔드와 백엔드 사이에 필요한 API와 보호 조건을 관리한다.  
> **이 문서가 기준인 내용:** 경로 후보, 목적, 인증·검증 조건, MVP 제외 API  
> **이 문서에 기록하지 않는 내용:** 구현 코드, DB 테이블, 화면 배치, 모델 학습 방식  
> **상태:** 권장 초안 / 기술 스택 승인 후 확정  
> **기준일:** 2026-09-11

## 1. 공통 원칙

- 경로와 HTTP 방식은 후보이며 기술 스택 승인 후 OpenAPI 계약으로 확정한다.
- 보호 API는 세션 인증과 이메일 인증 완료 상태를 함께 검사한다.
- 미인증이면 일관된 `EMAIL_VERIFICATION_REQUIRED` 오류를 반환한다.
- 공개 응답에 원본 파일 경로, 스토리지 키, 내부 예외와 개인정보 가능 로그를 노출하지 않는다.

## 2. 계정

| API | 목적 | 상태 |
| --- | --- | --- |
| `GET /v1/auth/email-availability?email=` | 이메일 중복 확인 | 실제 인증 연결 시 필요 |
| `GET /v1/users/nickname-availability?nickname=` | 닉네임 중복 확인 | 실제 인증 연결 시 필요 |
| `POST /v1/auth/register` | 계정·기본 정보·동의 저장과 인증 메일 요청 | 이번 주 미연결 |
| `POST /v1/auth/verify-email` | 이메일 인증 완료 | 토큰 방식 미확정 |
| `POST /v1/auth/resend-verification` | 인증 메일 재발송 | 만료·횟수·대기 미확정 |
| `PATCH /v1/auth/pending-email` | 미인증 계정 이메일 변경과 재발송 | 토큰 폐기 규칙 미확정 |
| `POST /v1/auth/login` | 로그인과 세션 시작 | 미인증 로그인 허용, 핵심 기능 제한 |
| `POST /v1/auth/logout` | 세션 종료 | 인증 방식 미확정 |
| `GET /v1/users/me` | 현재 사용자와 최소 프로필 조회 | 로그인 채택 시 필요 |
| `GET /v1/users/me/learning-preferences` | 학습 경험·선택·추천 난이도 조회 | 최초 학습 진입 |
| `PUT /v1/users/me/learning-preferences` | 학습 경험과 직접 선택 난이도 저장 | 허용 값과 권한 검증 |

비밀번호 찾기, 설정, 상세 마이페이지와 토큰 갱신 API는 MVP 이후 또는 인증 방식 결정 후 검토한다.

## 3. 케이스와 학습

| API | 목적 | 필수 보호 조건 |
| --- | --- | --- |
| `GET /v1/capabilities` | 지원 부위·영상 종류·질환·입력 형식 조회 | 실제 활성 범위만 반환 |
| `GET /v1/cases?body_region=&modality=&difficulty=` | 케이스 목록 조회 | 정답 라벨·기준 ROI 제외 |
| `GET /v1/cases/{case_id}` | 문제용 케이스와 영상 접근 정보 | 제출 전 병명·기준 ROI·해설 제외 |
| `POST /v1/cases/{case_id}/attempts` | 사용자 ROI 제출과 평가 | 좌표·권한·규칙 버전 검증 |
| `GET /v1/attempts/{attempt_id}/result` | 판정·기준 ROI·해설·비교 조회 | 시도 소유권 확인 |

## 4. 오답노트와 재학습

| API | 목적 | 상태 |
| --- | --- | --- |
| `GET /v1/review-items` | 부분정답·오답 목록 | 필수 |
| `GET /v1/review-items/{id}` | 이전 시도와 케이스 요약 | 필수 |
| `POST /v1/review-items/{id}/attempts` | 동일 케이스 재도전 제출 | 일반 시도 API 재사용 가능 |
| `PATCH /v1/review-items/{id}` | 완료·보류 상태 변경 | 완료 정책 결정 후 확정 |

## 5. 사용자 영상 AI 분석

| API | 목적 | 상태 |
| --- | --- | --- |
| `POST /v1/ai/analyses` | 부위·영상 종류·관심 ROI·파일/캡처 분석 요청 | 동기/비동기 미확정 |
| `GET /v1/ai/analyses/{id}` | 비동기 상태와 결과 조회 | 비동기 채택 시 필요 |
| `DELETE /v1/ai/analyses/{id}/input` | 사용자 명시 삭제 요청 | 서버 자동 삭제의 보조 수단 후보 |

사용자 원본 영상을 다시 내려받거나 영구 보관하는 API와 관리자용 데이터 업로드 API는 MVP에 두지 않는다.

## 6. 운영

- `GET /health` 또는 동등한 상태 확인 경로
- 내부용 모델 준비 상태와 지원 범위 확인 경로
- 인증·권한, 오류 코드, 요청·응답 스키마는 기술 스택 승인 후 보완
