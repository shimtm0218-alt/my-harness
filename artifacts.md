# artifacts.md

출처: pipeline.md, harness-goal.md

## 작업 폴더

`my-harness/work/<화면 영문 이름>/` 화면 1개당 폴더 1개.

화면 영문 이름 (10개 고정, PRD 16절):
home, free-learning, paid-library, skill-library, mission-detail,
submission, my-learning, my-assets, asset-detail, admin-review

## 단계별 파일

| 단계 | 파일 (work/<화면>/ 기준) | 담는 것 | 쓰는 에이전트 |
| --- | --- | --- | --- |
| S1 | research/01-scope.md | 유지·변경 영역, 질문 목록, 하이서 답변 | researcher |
| S2 | research/02-research.md | 사례 조사, 패턴·전략 분류 | researcher |
| S3 | research/03-directions.md | 시안 방향 3개 (정보 우선순위, UX 전략) | researcher |
| S4 | design/04-figma.md | 방향별 Figma 파일 URL과 프레임 ID | designer |
| S4 | design/frames.json | 시안의 색·radius·간격·폰트 등 판정용 값 (G4·G5 입력) | designer |
| S5 | review/05-review.md | 장점·리스크·선택 근거, 검토 의견, 최종 방향 선택 | reviewer |
| S5 | review/05-final.md | 최종 화면의 Figma 프레임, 최종 방향 | reviewer |
| S5 | review/05-dev-guide.md | 개발 가이드 | reviewer |
| S5 | review/frames.json | 최종 화면의 판정용 값 (G5 입력, 방향 1개) | reviewer |
| 공통 | state.json | 현재 단계, 완료한 단계, 시도 횟수, 하이서 답변 대기 여부, S3 승인 여부 | 오케스트레이터 |

Figma 시안은 Figma 파일 안에 있고, md에는 URL과 프레임 ID만 기록한다.

## 규칙 SSOT

- 시각 규칙의 단일 기준은 design.md 하나다.
- 판정 스크립트는 design.md에서 허용 색·radius·spacing을 직접 읽는다.
  rules.json 같은 복사본은 만들지 않는다.
- 어기면 안 되는 것(story-service.md)은 gates.md의 G5 조건으로 쓴다.

## 재개

- 중간에 멈췄다가 이어서 할 수 있다.
- 어디까지 했는지는 state.json과 각 단계 파일의 존재로 판단한다.
- S1에서 하이서 답변을 기다리는 중이면 state.json에 대기 상태를 기록하고,
  답변이 오면 S1부터 이어간다.

## 되돌아갈 때

- 기존 산출물은 덮어쓰지 않고 각 에이전트 폴더 안의 attempt-1/, attempt-2/로 옮겨 보관한 뒤 새로 만든다. (옮기는 것은 오케스트레이터가 한다.)
- 같은 단계의 시도 횟수는 state.json에 기록한다. 같은 단계에서 3회 실패하면 멈춘다(gates.md).
