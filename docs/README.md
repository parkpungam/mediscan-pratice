# 메디스캔노트 문서 안내

> **문서 역할:** `docs/` 전체의 목차이자 정보 위치 안내서다.  
> **이 문서가 기준인 내용:** 문서 구조, 문서별 책임, 읽는 순서, 작성·분리 규칙  
> **이 문서에 기록하지 않는 내용:** 제품 요구사항, 기술 설계, 개별 결정의 상세 내용  
> **상태:** 문서 구조 기준  
> **기준일:** 2026-09-11

## 1. 처음 문서를 보는 사람의 읽는 순서

1. [PROJECT_BRIEF](./product/PROJECT_BRIEF.md)에서 프로젝트를 만드는 이유와 사용자를 이해한다.
2. [PRD](./product/PRD.md)에서 MVP에 포함되는 기능과 제외 범위를 확인한다.
3. [USER_FLOW](./product/USER_FLOW.md)에서 사용자가 화면을 이용하는 순서를 확인한다.
4. 필요한 기능의 상세 문서와 시스템·AI 문서를 찾아본다.
5. 구현 전에는 [DECISIONS](./project/DECISIONS.md)에서 확정·미확정 상태를 확인한다.
6. 작업 순서와 완료 조건은 [IMPLEMENTATION_PLAN](./project/IMPLEMENTATION_PLAN.md)을 따른다.

## 2. 전체 문서 구조

```text
docs/
├─ README.md                         # 지금 보고 있는 전체 안내서
├─ product/
│  ├─ PROJECT_BRIEF.md               # 배경·문제·목표·사용자
│  ├─ PRD.md                         # MVP 범위와 제품 요구사항
│  ├─ USER_FLOW.md                   # 사용자 여정과 화면 전이
│  └─ features/
│     └─ SIGN_UP.md                  # 회원가입 상세 규칙
├─ system/
│  ├─ ARCHITECTURE.md                # 시스템 구성과 영역별 책임
│  ├─ API.md                         # API 목록과 보호 조건
│  └─ DATA_MODEL.md                  # 논리 데이터 모델
├─ ai/
│  ├─ DATA_AI.md                     # 데이터셋·AI 역할·모델 평가
│  └─ ROI_EVALUATION.md              # 기준 ROI와 위치 평가 규칙
├─ project/
│  ├─ DECISIONS.md                   # 결정·미확정·충돌 기록
│  ├─ IMPLEMENTATION_PLAN.md          # 구현 단계와 완료 조건
│  ├─ IMPLEMENTATION_PHASES.md        # 단계별 작업·완료 조건 상세
│  └─ RISKS.md                       # 의료데이터·개인정보·AI 위험
├─ testing/
│  └─ TEST_PLAN.md                   # 전체 테스트 기준
├─ mockups/                          # 검토용 화면·로고 이미지
└─ archive/
   └─ AGENTS_LEGACY.md               # 더 이상 적용되지 않는 과거 규칙
```

## 3. 어떤 내용을 어디에 기록하는가

| 작성하려는 내용 | 기록할 문서 | 다른 문서의 처리 |
| --- | --- | --- |
| 프로젝트 배경·문제·목표·타깃 사용자 | [PROJECT_BRIEF](./product/PROJECT_BRIEF.md) | 다른 문서에서는 한 문장 요약 후 링크 |
| MVP 포함·제외 범위와 제품 요구사항 | [PRD](./product/PRD.md) | 상세 화면 규칙은 기능 문서로 연결 |
| 사용자 행동 순서·화면 전이·예외 흐름 | [USER_FLOW](./product/USER_FLOW.md) | 입력 필드 규칙을 반복하지 않음 |
| 회원가입 필드·검증·상태·시안 | [SIGN_UP](./product/features/SIGN_UP.md) | PRD와 흐름 문서는 요약과 링크만 유지 |
| 프론트·백엔드·DB·스토리지·AI 경계 | [ARCHITECTURE](./system/ARCHITECTURE.md) | 실제 필드와 경로는 전용 문서로 연결 |
| API 경로·목적·권한·상태 | [API](./system/API.md) | 구현 계획에 API 표를 복사하지 않음 |
| 엔터티·필드·관계·보존 주의 | [DATA_MODEL](./system/DATA_MODEL.md) | 아키텍처에는 데이터 책임만 유지 |
| 데이터셋·AI 입력/출력·모델 평가 | [DATA_AI](./ai/DATA_AI.md) | ROI 계산 세부는 ROI 문서로 연결 |
| 기준 ROI·채점·임계값·다중 병변 | [ROI_EVALUATION](./ai/ROI_EVALUATION.md) | PRD에는 요구사항 수준만 유지 |
| 결정·제안·미확정·자료 충돌 | [DECISIONS](./project/DECISIONS.md) | 결정 결과는 담당 기준 문서에도 반영 |
| 전체 구현 순서·폴더 구조·단계 요약 | [IMPLEMENTATION_PLAN](./project/IMPLEMENTATION_PLAN.md) | 단계별 상세 작업을 반복하지 않음 |
| 단계별 작업·완료 조건 | [IMPLEMENTATION_PHASES](./project/IMPLEMENTATION_PHASES.md) | 계획의 큰 틀과 폴더 구조를 반복하지 않음 |
| 위험·영향·통제·남은 결정 | [RISKS](./project/RISKS.md) | 각 설계 문서는 필요한 위험 링크만 제공 |
| 단위·통합·데이터·보안·종단 테스트 | [TEST_PLAN](./testing/TEST_PLAN.md) | 구현 단계에는 통과해야 할 테스트 묶음만 명시 |

## 4. 문서 작성 규칙

1. 하나의 사실은 한 기준 문서에서만 상세하게 설명한다.
2. 다른 문서에서는 필요한 만큼만 요약하고 정확한 문서 또는 제목으로 연결한다.
3. 모든 문서 상단에 `문서 역할`, `이 문서가 기준인 내용`, `이 문서에 기록하지 않는 내용`, `상태`, `기준일`을 표시한다.
4. 상태는 `확정`, `제안`, `미확정`, `충돌`, `폐기/대체`로 구분한다.
5. 250줄을 넘으면 분리 가능성을 검토하고, 300줄을 넘으면 원칙적으로 책임별로 분리한다.
6. 줄 수를 맞추기 위해 의미가 같은 문서를 지나치게 잘게 나누지 않는다.
7. 제목이나 파일 위치를 바꾸면 연결된 상대 링크를 함께 수정하고 링크 검사를 수행한다.
8. 원본 자료가 바뀌면 먼저 DECISIONS에 변경·충돌을 기록한 뒤 담당 기준 문서를 갱신한다.
9. 확정되지 않은 내용을 구현 규칙처럼 단정하지 않는다.
10. 삭제하는 대신 다른 문서로 이동한 내용은 새 위치를 명확히 남긴다.

## 5. 원본 자료와 시안

- `references/`는 내부기획서, 산출물 기획서, 화면 흐름도와 시퀀스 다이어그램의 원본 보관 위치다.
- 원본 파일은 그 자체로 개발 기준이 되지 않는다. 확인된 내용은 담당 기준 문서와 DECISIONS에 반영한다.
- `docs/mockups/`는 검토용 화면·로고 이미지다. 확정된 제품 규칙은 이미지가 아니라 PRD와 기능 문서를 따른다.
- `docs/archive/`는 더 이상 적용되지 않지만 이력을 위해 보존하는 문서다.

## 6. 변경 전 확인 목록

- 이 내용을 책임지는 기존 문서가 있는가?
- 이미 다른 문서에 같은 설명이 있는가?
- 확정·제안·미확정 중 어떤 상태인가?
- 원본과 결정 근거를 연결했는가?
- 다른 문서의 링크와 제목을 함께 수정해야 하는가?
- 변경 후 각 Markdown 파일이 300줄 이하인가?
