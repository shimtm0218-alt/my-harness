# 프로젝트 시안 판정 입력

`work/<화면>/design/frames.json`은 실제 Figma에서 추출한다.

- `screen`: 영문 소문자·숫자·하이픈으로 정한 화면 이름.
- `frames`: 프레임 목록. 각 항목에 `id`, `direction`, `viewer_role`, `nodes`가 필요하다.
- `nodes`: 각 노드에 `id`, `type`을 기록한다. 측정 항목은 `fills`, `strokes`, `textColor`, `radius`, `padding`, `gap`, `margin`, `font`(family·weight), `shadow`다.
- `policy_checks`: 각 항목에 `id`, `passed`(boolean), `evidence`(원본 화면·정책 대조 근거)를 기록한다. 정책 ID는 design.md 설정과 일치해야 한다.

project design.md의 harness-rules 설정이 ready여야 한다. 미설정·누락은 판정 불가(종료 코드 2), 위반은 1, 지정 검사 통과는 0이다.
G5는 사람 또는 판정자가 확인한 정책 기록을 검사한다. 실제 준수 여부를 코드만으로 증명하지 않는다.

```bash
python3 scripts/judge.py work/<화면>/design/frames.json
python3 scripts/judge.py work/<화면>/review/frames.json --expect-directions 1
```
