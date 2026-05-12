# ULTRA 학교지원 의사결정 지원 플랫폼

Streamlit 기반의 학교지원 우선순위·예산배분 시뮬레이션 웹서비스입니다.

## 1. 폴더 구성

```text
ULTRA_streamlit_deploy/
 ┣ app.py
 ┣ requirements.txt
 ┣ school_master_final_v2.csv
 ┣ data/
 ┃ ┗ school_master_final_v2_SAMPLE.csv
 ┣ .streamlit/
 ┃ ┗ config.toml
 ┣ .gitignore
 ┗ README.md
```

## 2. 로컬 실행 방법

터미널에서 이 폴더로 이동한 뒤 실행합니다.

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저가 자동으로 열리지 않으면 터미널에 표시되는 `Local URL` 주소로 접속합니다.

## 3. 웹 배포 방법: Streamlit Community Cloud

1. GitHub에 새 저장소를 만듭니다.
2. 이 폴더 안의 파일을 저장소 최상단에 업로드합니다.
3. Streamlit Community Cloud에서 `New app`을 선택합니다.
4. Repository, Branch, Main file path를 지정합니다.
   - Main file path: `app.py`
5. `Deploy`를 누릅니다.
6. 생성된 `*.streamlit.app` 주소를 보고서·PPT·시연 영상에 넣습니다.

## 4. 실제 데이터 연결 방법

현재 포함된 `school_master_final_v2.csv`는 시연용 샘플 데이터입니다. 실제 서비스에서는 같은 파일명으로 실제 전처리 데이터를 교체하면 됩니다.

필수 또는 권장 컬럼은 다음과 같습니다.

| 컬럼명 | 의미 |
|---|---|
| `school_name` | 학교명 |
| `region_office` | 교육청 또는 지역 |
| `school_level` | 학교급: 초등학교, 중학교, 고등학교 등 |
| `school_type` | 공립/사립 등 학교 유형 |
| `region_type` | 도시형, 도농형, 읍면형, 농산어촌 등 |
| `finance_type` | 국공립/사립 등 재정 유형 |
| `student_count` | 학생 수 |
| `has_request` | 학교 신청 여부: 1 또는 0 |
| `urgent_flag` | 긴급 지원 신호: 1 또는 0 |
| `first_choice_area` | 1순위 지원 영역 |
| `support_facility_score` | 시설 지원 점수 |
| `budget_total` | 예산 총액 |
| `desired_support_count` | 희망 지원 개수 |
| `reason_v2` | 추천 사유 문장 |

파일은 아래 둘 중 한 위치에 둘 수 있습니다.

```text
school_master_final_v2.csv
```

또는

```text
data/school_master_final_v2.csv
```

## 5. 공개 배포 전 주의사항

- 실제 학교 데이터가 포함되어 있다면 학교명, 세부 위치, 민감한 신청 사유 등은 익명화 또는 가명 처리하는 것이 안전합니다.
- GitHub 저장소를 public으로 둘 경우 CSV 파일도 공개됩니다.
- 대회 제출용이면 샘플/익명화 데이터로 시연하고, 보고서에는 실제 적용 시 교육청 내부망 또는 권한 기반 운영이 필요하다고 적는 것이 좋습니다.

## 6. 오류가 날 때 확인할 것

- `requirements.txt` 파일명이 정확한지 확인합니다.
- `app.py`가 저장소 최상단에 있는지 확인합니다.
- 실제 데이터 파일명이 `school_master_final_v2.csv`인지 확인합니다.
- CSV 인코딩은 `utf-8-sig`, `utf-8`, `cp949` 순서로 자동 시도됩니다.
