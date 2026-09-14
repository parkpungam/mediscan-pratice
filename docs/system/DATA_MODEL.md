# 논리 데이터 모델

> **문서 역할:** 제품 기능에 필요한 데이터 엔터티와 주요 필드를 논리 수준에서 정의한다.  
> **이 문서가 기준인 내용:** 엔터티 책임, 주요 필드 후보, 저장 금지 데이터와 미확정 설계  
> **이 문서에 기록하지 않는 내용:** 특정 DB 제품의 DDL, 마이그레이션 코드, API 경로, 화면 상태  
> **상태:** 논리 초안 / 물리 스키마 미확정  
> **기준일:** 2026-09-11

## 1. 관련 문서

- 시스템 경계: [ARCHITECTURE](./ARCHITECTURE.md)
- 제품 요구사항: [PRD](../product/PRD.md)
- 회원가입 필드: [SIGN_UP](../product/features/SIGN_UP.md)
- 데이터·AI 규칙: [DATA_AI](../ai/DATA_AI.md)
- ROI 평가: [ROI_EVALUATION](../ai/ROI_EVALUATION.md)
- API 계약 초안: [API](./API.md)

## 2. 엔터티 초안

| 엔터티 | 주요 필드 초안 | 상태와 주의 |
| --- | --- | --- |
| `users` | `id`, `email`, `password_hash`, `email_verified_at`, `status`, `age_14_plus_confirmed_at`, `created_at` | 이메일 중복 불가, 비밀번호 원문 저장 금지, 생년월일 수집 없음 |
| `user_profiles` | `user_id`, `nickname`, `major`, `major_status`, `signup_source` | 닉네임·전공 필수, 가입 경로 선택. 학교·교육과정·학년 없음 |
| `learning_preferences` | `user_id`, `experience_level`, `selected_difficulty`, `recommended_difficulty`, `recommendation_rule_version`, `updated_at` | 최초 학습 진입에서 생성, 추천 규칙 미확정 |
| `user_consents` | `user_id`, `terms_id`, `terms_version`, `required`, `agreed`, `agreed_at` | 필수·선택 동의를 분리하고 버전 추적 |
| `email_verifications` | `user_id`, `token_hash`, `expires_at`, `used_at`, `created_at` | 토큰 원문 저장 금지, 만료·재발송 정책 미확정 |
| `dataset_sources` | `id`, `name`, `version`, `source_url`, `license`, `allowed_uses`, `deidentification_check`, `label_provenance`, `validation_level` | 의료 검수 부재와 허용 목적 기록 |
| `case_assets` | `id`, `dataset_source_id`, `storage_key`, `original_format`, `derived_format`, `width`, `height`, `checksum`, `transform_version` | 승인된 학습 자산만 영구 저장 |
| `cases` | `id`, `body_region`, `modality`, `finding_or_disease`, `asset_id`, `learning_difficulty`, `status` | 부위 네 값 확정, 나머지 분류 미확정 |
| `reference_rois` | `id`, `case_id`, `geometry_type`, `geometry`, `coordinate_space`, `label`, `source_annotation_id`, `version` | `ground truth` 대신 데이터셋 제공 기준 ROI로 명명 |
| `explanations` | `case_id`, `title`, `major_findings`, `terms`, `references`, `review_status`, `version` | 의료전문가 검수 없음과 출처 표시 |
| `evaluation_rules` | `id`, `metric`, `correct_threshold`, `partial_threshold`, `oversize_policy`, `multi_roi_policy`, `version` | 약 40%는 잠정 시작값 |
| `attempts` | `id`, `user_id`, `case_id`, `evaluation_rule_id`, `result`, `score_metrics`, `parent_attempt_id`, `submitted_at` | 재도전 연결과 판정 재현 |
| `attempt_rois` | `id`, `attempt_id`, `geometry_type`, `geometry`, `coordinate_space` | 좌표 규격 미확정 |
| `review_items` | `id`, `user_id`, `case_id`, `first_attempt_id`, `latest_attempt_id`, `status`, `updated_at` | 부분정답·오답 자동 생성, 완료 정책 미확정 |
| `ai_models` | `id`, `body_region`, `modality`, `task_type`, `model_version`, `data_version`, `supported_labels`, `status` | 구체 모델 미확정 |
| `ai_analysis_jobs` | `id`, `user_id`, `body_region`, `model_id`, `status`, `created_at`, `finished_at`, `input_deleted_at`, 제한된 결과 메타데이터 | 엔터티 보존 여부 미확정 |

## 3. 저장 경계

- 관계형 DB에 의료영상 바이너리와 사용자 원본 영상을 저장하지 않는다.
- 사용자 입력 임시 파일은 임의 키, 짧은 만료, 최소 권한과 성공·실패 공통 삭제 작업을 사용한다.
- 실제 환자 개인정보와 비식별화되지 않은 의료데이터를 저장하지 않는다.
- 키, 테이블 분리, 좌표 형식, 보존 기간과 DB 제품은 미확정이다.
