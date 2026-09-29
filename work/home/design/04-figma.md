# 04-figma — home (S4)

## Figma 파일
- 파일: 허들링 home S4 시범 — https://www.figma.com/design/nkenzD973iXX1DupzTLGRd
- 플랜: 심태민's team (개인 starter 팀). 다른 플랜(딜리셔스_프로덕트디자인, 해커톤 게스트)은 쓰지 않음.
- 페이지: `home S4` 1개. 프레임 3개, 각 390×844 (Figma에서 읽은 크기).

| 방향 | 프레임 이름 | 프레임 ID | 노드 수(프레임 포함) |
| --- | --- | --- | --- |
| 1 | 방향1 이어서 하기 | 2:2 | 55 |
| 2 | 방향2 주제로 둘러보기 | 2:57 | 61 |
| 3 | 방향3 열어 보기 | 2:118 | 76 |

viewer_role은 세 프레임 모두 `free`(무료 회원). flow는 쓰지 않음(home은 G5 적용 화면 아님).

## 0단계 확인
- 도구: 공식 Figma MCP(use_figma, create_new_file, whoami, get_screenshot).
- Pretendard: Light / Regular / SemiBold / Bold 4개 모두 loadFontAsync 성공. 대체 폰트는 쓰지 않음.

## frames.json 추출 방식 (읽기 전용 스크립트, 값은 Figma 노드에서 읽음)
- 프레임마다 루트 노드 + `findAll` 모든 자손을 순회. 값을 손으로 옮기지 않고 스크립트가 출력한 JSON을 그대로 저장.
- 원래 한 번에 세 프레임을 뽑았으나 출력이 20kb에서 잘려서, 프레임당 한 번씩 세 번 나눠 실행. 두 실행에서 같은 스크립트 로직을 씀(첫 실행은 name 필드를 포함, 두 번째 이후는 뺐음).
- type/role: 노드 이름이 `type:role` 형식이고 type이 허용 목록(button/toggle/badge/chip/nav/input/card/text/image/section)이면 그대로. 아니면 Figma 노드 타입 소문자(프레임 루트는 `frame`).
- fills / strokes: visible SOLID만. 불투명도 <1이면 `rgba(r,g,b,a)`(이번 시안에는 해당 없음). TEXT 노드의 fill은 `textColor`.
- radius: `cornerRadius` 숫자. 모서리별로 다르면 4개 목록(이번 시안에는 해당 없음). **값이 min(width,height)/2 이상이면 `"full"`**로 기록. 이 규칙으로 `"full"`이 된 노드의 원본 값은 전부 9999였음(첫 실행에서 확인: 45개 노드 중 원본 9999 45개). 그 외 radius 값은 원본 그대로 16/24/0.
- padding: auto layout 노드의 [top,right,bottom,left] 중 0이 아닌 값 목록. 전부 0이면 필드 생략.
- gap: auto layout의 itemSpacing. **0이면 필드를 생략**(간격 없음). wrap 레이아웃(카테고리 칩 줄)은 [itemSpacing, counterAxisSpacing] 목록.
- font: TEXT 노드의 fontName.family와 style을 Light 300 / Regular 400 / SemiBold 600 / Bold 700으로 변환.
- shadow: 보이는 DROP/INNER_SHADOW가 있을 때만 true. 이번 시안에서는 어떤 노드에도 기록되지 않음(effects 없음).
- text: TEXT 노드의 characters(추가 필드).

## 읽지 못한 값
- 노드의 의미상 역할(role)은 Figma가 갖고 있지 않아 이름 규칙에서 뽑았음. 이름이 실제 역할과 맞는지는 읽은 값이 아니라 내가 붙인 것이다.
- 자동 레이아웃이 아닌 노드(사각형 이미지 자리표시자, 로고마크)의 padding/gap은 해당 없음으로 생략.
- 버튼 높이·아이콘 크기 등 padding·gap 이외의 치수(width/height, 라인하이트, 글자 크기)는 judge 입력 형식에 없어 frames.json에 넣지 않음.

## 만들면서 design.md와 충돌하거나 타협한 것
- 섹션 간격: design.md는 섹션 사이 48px(주요 구간 64px)를 말하지만, 390×844 한 화면 안에 방향별 5개 정보를 우선순위 순서대로 넣기 위해 프레임 안 섹션 간격을 방향1 24px, 방향2·3 16px로 줄임(허용 목록 값이긴 하나 design.md의 "sections separated by 48px" 서술과는 다름). 홈은 원래 스크롤 화면인데 프레임을 844로 고정한 탓이다.
- 로고마크: 실제 로고가 없어 24×24 #141414 둥근 사각형(radius 9999) 자리표시자. 이름 `image:logomark`.
- 이미지: 사진 없이 #f3f3f3 사각형(radius 16) 자리표시자. 흰 카드 안에서만 보이도록 배치.
- 콘텐츠 개수·제목·미션 제목은 더미(`자료 N개`, `콘텐츠 제목 더미` 등). 실제 서비스 데이터 아님.
- 상단 내비게이션: mobile 규칙대로 logomark + 워드마크 + CTA를 담은 pill. design.md는 "logomark + CTA"라고만 써 있어 워드마크 텍스트(허들링)를 함께 넣은 것은 내 해석.
- 방향3 미션 카드에 배지를 3개(무료 미션 / 작성 중 / 유료 미션 잠김) 나란히 둠. 무료 회원의 제출 가능 범위는 01-scope에서 미정이라, "작성 중" 표시는 가정.
- 잠김 표현은 "잠김" 텍스트 배지로만 했고 자물쇠 아이콘은 넣지 못함(아이콘 자산 없음).
- 액센트 #0066ff는 프레임마다 배지 1개(멤버 전용/멤버십)에만 씀. 버튼에는 쓰지 않음.
- 알림 진입점은 홈에 넣지 않음(01-scope 질문 8은 별도 진입점을 두라고 하나 형태 미정이라 이번 시안 범위에서 제외).

이 문서는 규칙 준수를 선언하지 않는다. 판정은 judge가 한다.
