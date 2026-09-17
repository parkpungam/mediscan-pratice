# 메디스캔노트 프로젝트 작업 규칙

이 파일은 저장소 전체에 적용되는 현재 작업 규칙이다. 상세 기획과 설계는 복사하지 않고 문서 안내(`C:\Users\user\Desktop\setting\medinote\README.md`)에 연결한다.

> **문서 위치 변경(2026-09-15):** 제품·시스템·AI·프로젝트 관리·테스트 문서는 더 이상 이 저장소의 `docs/`에 있지 않다. Claude·Codex 공통 협업 저장소인 `C:\Users\user\Desktop\setting\medinote\`로 이동했으며 내부 폴더 구조와 문서 간 상대 링크는 그대로다. `references/`와 `frontend/`는 이 저장소에 그대로 있다.

## 1. 작업 전 확인 순서

1. 제품 범위는 PRD(`C:\Users\user\Desktop\setting\medinote\product\PRD.md`)를 확인한다.
2. 화면 이동은 USER_FLOW(`C:\Users\user\Desktop\setting\medinote\product\USER_FLOW.md`)를 확인한다.
3. 회원가입 상세는 SIGN_UP(`C:\Users\user\Desktop\setting\medinote\product\features\SIGN_UP.md`)을 확인한다.
4. 기술 경계는 ARCHITECTURE(`C:\Users\user\Desktop\setting\medinote\system\ARCHITECTURE.md`)를 확인한다.
5. 확정·미확정·충돌 상태는 DECISIONS(`C:\Users\user\Desktop\setting\medinote\project\DECISIONS.md`)를 확인한다.
6. 구현 순서와 완료 조건은 IMPLEMENTATION_PLAN(`C:\Users\user\Desktop\setting\medinote\project\IMPLEMENTATION_PLAN.md`)을 따른다.

## 2. 문서 및 결정 규칙

- 노션 Markdown은 `내부기획서`, PDF는 `산출물 기획서`라고 부른다.
- 제품 기획과 개발 판단은 내부기획서를 우선 근거로 한다.
- 원본 자료 또는 기준 문서가 다르면 임의로 선택하지 말고 `DECISIONS.md`에 충돌로 기록한다.
- 미확정 사항을 코드, API 또는 데이터 구조로 임의 확정하지 않는다.
- 같은 상세 내용을 여러 문서에 반복하지 않고 담당 기준 문서로 연결한다.
- 사용자의 명시적인 승인 전에는 새 기능 범위나 기술을 추가하지 않는다.

## 3. 확정된 기술 경계

- Vue 3
- JavaScript
- Vue CLI
- Vue Router
- Options API
- 기본 CSS
- npm

프론트엔드는 루트의 `frontend/`에 둔다. 팀장 저장소는 기술 사용 방식을 이해하기 위한 참고자료이며 코드를 복사하거나 해당 저장소에 직접 작업하지 않는다.

- 백엔드 런타임은 Node.js이며 루트의 `backend/`에 둔다.
- 관계형 데이터베이스는 PostgreSQL이다.
- 백엔드 프레임워크·ORM, 호스팅·스토리지, AI 모델·프레임워크는 아직 확정하지 않는다.

## 4. 현재 구현 범위

- 첫 산출물은 2단계 회원가입 프론트엔드 화면과 인증메일 발송 안내 상태다.
- 실제 계정·동의 저장, 이메일·닉네임 중복 조회, 인증메일 발송과 인증 완료는 이번 화면 작업에 포함하지 않는다.
- 데모 동작을 실제 서버 동작처럼 표현하지 않는다.
- 구체적인 입력값·검증·문구는 `SIGN_UP.md`만 기준으로 삼는다.

## 5. 의료데이터 및 개인정보

- 서비스와 AI를 확정적 의료 진단·처방·진료 지시로 표현하지 않는다.
- 실제 환자 개인정보가 포함되거나 비식별화되지 않은 의료데이터를 개발·테스트·데모에 사용하지 않는다.
- 이메일, 닉네임, 전공, 가입 경로, 동의·접속·학습 이력은 개인정보로 취급한다.
- 데이터셋은 출처, 라이선스, 재배포 조건, 비식별화 상태와 라벨 출처를 확인한다.
- 사용자 영상, 원본 데이터셋, 모델 가중치와 비밀키를 Git에 커밋하지 않는다.
- 의료전문가 추가 검수 인력이 없으므로 공개 데이터셋 라벨을 임상적으로 검증된 절대 정답이라고 표현하지 않는다.

## 6. 변경 및 검증

- 기존 사용자 변경과 원본 자료를 보존한다.
- 기능을 구현하면 관련 테스트와 빌드를 실행하고 결과를 보고한다.
- 패키지 설치, 애플리케이션 생성과 기능 구현은 사용자가 승인한 단계 안에서만 수행한다.
- 패키지 설치, 애플리케이션 생성과 기능 구현은 사용자의 명시적 착수 승인 후에만 수행한다.
