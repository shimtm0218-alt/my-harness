# roles.md

출처: story-work.md(넘김 3곳), pipeline.md, artifacts.md, gates.md
이 문서는 역할과 권한의 규칙을 정의한다. 구현은 `.claude/agents/`(에이전트 정의 4개)와 `scripts/guard-path.py`, `scripts/guard-judge.py`(쓰기 차단 훅), `scripts/state.py`(state.json 관리)다.
에이전트 정의는 세션을 시작할 때 읽히므로, 만든 뒤에는 새 세션에서만 인식된다.

## 역할 (작업 에이전트 3 + 판정자 1 + 오케스트레이터)

| 역할 | 맡는 단계 | 쓰기 허용 (편집 폴더 1개) | 쓰기 금지 | 쓰는 도구 |
| --- | --- | --- | --- | --- |
| researcher | S1~S3 | work/<화면>/research/ | 그 밖의 전부 | 파일 읽기·쓰기, 웹 조사 |
| designer | S4 | work/<화면>/design/, Figma 파일 | 그 밖의 전부 | 파일 읽기·쓰기, Figma 쓰기 |
| reviewer | S5 | work/<화면>/review/ | 그 밖의 전부 | 파일 읽기·쓰기, Figma 조회 |
| judge (판정자) | 모든 게이트 | 없음 (읽기 전용) | 전부 | 파일 읽기, 판정 스크립트 실행, Figma 조회 |
| 오케스트레이터 | 전체 진행 | state.json, attempt-N/ 이동 | 각 에이전트 폴더의 내용 작성 | 파일 읽기·쓰기, 에이전트 호출 |

- 하이서와 개발자는 에이전트가 아니다. 하이서 답변 대기(S1)와 검토 공유(S5)는 오케스트레이터가 멈추고 사람의 입력을 받는다.
- 사람 승인 지점 1곳은 S3 끝이다(gates.md). 승인은 프로덕트 디자이너가 하고 오케스트레이터가 state.json에 기록한다.

## 판정자

- 게이트 G1~G6의 조건을 세는 스크립트를 실행하고 결과를 읽는다. 산출물을 수정하지 않는다.
- Figma는 조회만 한다.
- 결과는 화면에 출력한다. state.json에 기록하는 것은 오케스트레이터다.
- G4·G5는 `python3 scripts/judge.py <frames.json>`, G1·G2·G3·G6은 `python3 scripts/judge_md.py <게이트> <파일>`로 판정한다.
- 판정 입력(frames.json)은 designer(S4)와 reviewer(S5)가 자기 폴더에 쓴다. judge는 읽기만 한다.

## 화면 이름 → 폴더 이름

| 화면 | 폴더 |
| --- | --- |
| 홈 | home |
| 무료 학습자료 | free-learning |
| 유료 멤버 자료실 | paid-library |
| 스킬 라이브러리 | skill-library |
| 미션 상세 | mission-detail |
| 제출 화면 | submission |
| 내 학습 | my-learning |
| 내 자산 | my-assets |
| 자산 상세 | asset-detail |
| 운영자 검수 화면 | admin-review |

## 자연어 트리거 (4개)

| 말 | 하는 일 |
| --- | --- |
| "<화면 이름> 시안 작업 시작해줘" | 화면 이름을 폴더 이름으로 바꿔 work/<화면>/ 을 만들고 S1부터 시작 |
| "이어서 진행해줘" | state.json을 읽고 멈춘 단계부터 재개 |
| "방향 3개 승인" | S3의 사람 승인을 기록하고 S4로 진행 (G3 통과 상태일 때만) |
| "<단계> 판정해줘" | 해당 단계의 게이트만 judge로 실행해 결과 출력 (예: "S4 판정해줘") |
