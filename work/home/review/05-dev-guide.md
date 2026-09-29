# 05-dev-guide — home (방향 1 이어서 하기)

기준: `design/frames.json`의 방향 1 프레임(390×844, 뷰어 역할 free)과 04-figma 기록. 값은 frames.json에 있는 것만 적었다. 글자 크기·줄 높이·요소 너비/높이는 frames.json에 없어서 적지 않았다(미확정 사항 참조).

## 화면 구조
프레임 루트: 배경 colors.canvas #ffffff, 좌우·상하 패딩 spacing.md(16), 섹션 사이 gap spacing.lg(24). 위→아래 순서:
1. 상단 내비게이션(top-nav): 로고마크 자리표시자 + 워드마크 "허들링" + 버튼 "멤버십 보기". 알림 진입점은 없다.
2. 미션 상태 카드(mission-status): 배지 "작성 중", 캡션 "이번 달 무료 미션 (더미)", 제목 "미션 제목 더미 텍스트", 본문 "제출 상태: 작성 중 · 제출 전", 버튼 "이어서 작성하기".
3. 최근 본 · 저장한 자료(recent): 제목 + 카드 2개(이미지 자리표시자 + 자료 제목).
4. 내 학습·내 자산(my-locked): 잠긴 타일 2개, 각각 제목과 "잠김" 배지.
5. 카테고리(categories): 제목 + 칩 6개(AI 실무, Figma + AI, 바이브코딩, 자동화, 콘텐츠 제작, 1인 사업가 운영), 줄바꿈되는 배치.
6. 유료 전환 카드(upgrade-cta): 제목 "멤버십으로 전체 열기", 배지 "멤버 전용", 버튼 "유료 전환하기".

우선순위 순서(03-directions)와 위 배치 순서는 일치한다. 미션·자료 제목과 카드 내용은 더미 텍스트다.

## 컴포넌트와 토큰
| 컴포넌트 (frames.json role) | 사용된 값 → design.md 이름 |
| --- | --- |
| 프레임 루트 | fill #ffffff colors.canvas, radius 0, padding 16 spacing.md, gap 24 spacing.lg |
| top-nav | fill #f3f3f3 colors.canvas-soft, rounded.full, padding 위·오른쪽·아래 8 spacing.xs / 왼쪽 16 spacing.md, gap 8 spacing.xs |
| logomark (image) | fill #141414 colors.ink, rounded.full (실제 로고 없음, 자리표시자) |
| wordmark | 글자색 #141414 colors.ink, Pretendard 700 |
| button-primary (3곳: 멤버십 보기, 이어서 작성하기, 유료 전환하기) | fill #141414 colors.primary, rounded.full, padding 8/16 (spacing.xs, spacing.md), 라벨 #ffffff colors.on-primary, Pretendard 600 (typography.link 후보) |
| mission-status 카드 | fill #ffffff colors.canvas, 테두리 #f0f0f0 colors.hairline-soft, rounded.md(24), padding 16 spacing.md, gap 8 spacing.xs |
| badge-status "작성 중" | fill #f3f3f3 colors.canvas-soft, rounded.full, padding 4/12 (spacing.xxs, spacing.sm), 라벨 #262626 colors.ink-soft, Pretendard 600 (typography.label 후보) |
| caption / body-sm (미션 카드) | 글자색 #707070 colors.text-muted, Pretendard 400 |
| heading 4개 (미션 제목 2:13, 섹션 제목 2곳 2:18 "최근 본 · 저장한 자료"·2:36 "카테고리", CTA 제목 2:52). "내 학습·내 자산" 타일 묶음(2:26)에는 별도 섹션 제목이 없다 | 글자색 #141414 colors.ink, Pretendard 700 |
| recent-item 카드 (2개) | fill #ffffff, 테두리 #f0f0f0 colors.hairline-soft, rounded.sm(16), padding 12 spacing.sm, gap 8 spacing.xs. 이미지 자리표시자 fill #f3f3f3 colors.canvas-soft, rounded.sm(16). 제목 body-sm 후보, #141414, 400 |
| locked-tile (2개) | fill #f3f3f3 colors.canvas-soft, rounded.sm(16), padding 12 spacing.sm, gap 8 spacing.xs. 제목 #141414 colors.ink, Pretendard 600 (typography.title 후보) |
| badge-locked "잠김" | fill #ffffff colors.canvas, rounded.full, padding 4/12, 라벨 #707070 colors.text-muted, Pretendard 600 |
| chip category (6개) | fill #f3f3f3 colors.canvas-soft, rounded.full, padding 8/16 (spacing.xs, spacing.md), 라벨 #141414 colors.ink, Pretendard 400. 칩 줄 gap 가로 8·세로 8 spacing.xs |
| upgrade-cta 카드 | fill #f3f3f3 colors.canvas-soft, rounded.md(24), padding 16 spacing.md, gap 12 spacing.sm |
| badge-popular "멤버 전용" | fill #0066ff colors.accent, rounded.full, padding 4/12, 라벨 #ffffff colors.on-primary, Pretendard 600. 액센트는 화면에서 이 1곳뿐이고 버튼에는 쓰지 않는다 |

- 그림자: frames.json에 기록된 것 없음(04-figma 기록상 effects 없음). 폰트는 Pretendard 300/400/600/700 중 400·600·700만 쓰였다.
- 섹션 내부(mission-meta, recent, my-locked, categories 등)의 gap은 8(spacing.xs)이다. 섹션 사이 gap은 루트의 24이다.

## 상태
Figma에 그려진 것은 무료 회원(free) 기준 한 가지 상태뿐이다. 나머지는 01-scope의 가정이며 프레임에 없다.
- 무료 회원(그려짐): 미션 카드는 "작성 중" 상태. 내 학습·내 자산은 "잠김" 배지가 붙은 타일. 유료 전환 카드와 "멤버십 보기" 버튼이 보인다.
- 잠금: 잠금 표현은 "잠김" 텍스트 배지뿐이다. 자물쇠 아이콘은 없다. 잠긴 타일을 눌렀을 때의 동작은 정해지지 않았다.
- 제출 상태: PRD 6-4의 값은 작성 중 / 제출 완료 둘이다. 프레임에는 "작성 중"만 그려졌다. "제출 완료"일 때의 미션 카드(배지, 본문, 버튼 라벨)는 그려지지 않았다.
- 비회원: 01-scope 질문 9 가정은 미션·최근 본 영역을 숨기고 가입 CTA로 대체하는 것이다. 프레임에 없다.
- 유료 회원: 내 학습·내 자산이 열린 상태와 유료 전환 카드의 처리는 프레임에 없다.
- 판매 승인 회원: 홈의 판매 신청 진입은 그려지지 않았다(01-scope는 seller가 아니면 노출하지 않는다고 해석했고 seller의 노출 여부·형태는 미정).
- 운영자: 이 화면 범위 밖(01-scope 질문 3 가정).
- 비어 있는 상태(미션 없음, 최근 본/저장 없음)와 로딩·오류 상태는 그려지지 않았다.

## PRD 근거
- 6-4 (미션과 학습 관리): 현재 미션 보기·제출 상태(작성 중 / 제출 완료). 미션 카드의 근거.
- 6-2 (유료 멤버 자료실): 최근 본/저장한 자료. 최근 본 · 저장한 자료 섹션의 근거(홈 노출 자체는 PRD가 말하지 않는다. 01-scope 질문 5 가정).
- 6-1 (무료 학습자료): 카테고리 6개, 유료 전환 CTA. 카테고리 칩과 유료 전환 카드의 근거.
- 7-1·7-2 (권한 구조): 비회원 가입 CTA, 무료 회원의 미션 일부 참여와 유료 자료 미리보기. 무료 회원 기준 화면의 근거.
- 5절, 9절: 앱 섹션 목록과 MVP 범위(내 학습·내 자산 포함, 허들링 픽 제외).
- 6-8 (알림): 알림은 필수 기능이나 홈 본문에는 두지 않는다는 것은 01-scope 질문 5·8 가정이다.
- 6-5, 7-4: 판매 신청은 판매 승인 회원만 선택 가능.
- 14절, 15절: design.md 규칙 준수, 학습 흐름의 완성도, 디자인 완성도.
- 16절: 핵심 화면 목록에 "홈"이 있다(홈의 구성은 PRD에 없다).

## 미확정 사항
01-scope의 가정(하이서 미확인, 오케스트레이터가 기본값으로 채움). 하이서가 확인하면 바뀔 수 있다.
- 홈은 학습 흐름의 시작점이다(질문 1). 이 방향 1 선택의 전제이기도 하다.
- 홈 하나가 권한에 따라 일부 잠기는 방식이다. 역할별 홈은 따로 설계하지 않는다(질문 2).
- 운영자 홈은 범위 밖이다(질문 3).
- 무료 회원에게 내 학습·내 자산이 잠금 상태로 보인다(질문 4).
- 미션·제출 상태와 최근 본/저장을 노출하고 미션이 우선이다. 알림은 홈 본문에 없다(질문 5).
- 카테고리는 PRD 6-1의 6개만 쓴다(질문 6).
- 무료 미션이 있으면 노출하고 유료 미션은 잠금이다(질문 7).
- 알림 확인은 별도 진입점이다(질문 8).
- 비회원은 미션·최근 본 영역 대신 가입 CTA다(질문 9).

01-scope의 남은 모호함 중 개발에 영향을 주는 것.
- 무료 회원의 미션 참여 범위: 무료 미션이 실제로 존재하는지, 열람만인지 제출까지인지 PRD에 없다. 카드의 "작성 중" 표시와 "이어서 작성하기" 버튼은 이 가정 위에 있다.
- 비회원 홈이 앱에 존재하는지(공개 웹인지) 정해지지 않았다.
- 알림 진입점의 형태와 위치가 정해지지 않았고 현재 프레임에는 없다.
- 최근 본/저장 자료의 범위: 6-2는 유료 멤버 자료실의 기능으로 적는다. 무료 회원이 무엇을 저장·조회하는지, 이 영역이 어떤 자료를 담는지 PRD에 없다.
- 판매 승인 회원의 홈 진입 형태가 정해지지 않았다.

S4 judge가 짚은 한계와 시안 제작 시 타협한 것(04-figma 기록).
- 대비: #707070 글자를 #f3f3f3 위에 쓰면 대비가 약 4.46:1로 4.5:1에 조금 못 미친다(S4 judge). 이 조합은 design.md가 정한 색 조합에서 생길 수 있는 일반 위험이며, 방향 1(2:2)의 노드에는 해당 조합이 없다(frames.json 확인: #707070 글자 2:12·2:14·2:30·2:34는 모두 #ffffff 바탕 위). 방향 2·3에서 나타난다.
- 섹션 간격: 프레임의 섹션 간격은 24px이고 섹션 내부는 8px이다. design.md는 섹션 사이 48px(주요 구간 64px)를 서술한다. 스크롤 화면인 홈을 844px 프레임에 맞추려고 줄인 것이다(04-figma). 구현 시 24와 48 중 무엇을 따를지 정해야 한다.
- 하단 여백: Figma get_metadata 측정으로 마지막 카드 2:50이 y=765에서 끝나고 프레임 높이가 844라 아래 남는 공간은 79px(프레임 하단 패딩 16 포함)이다. 홈은 스크롤 화면이라 실제 하단 처리(탭 바 유무 등)는 정해지지 않았다.
- 내비게이션 워드마크: design.md는 모바일 nav를 logomark + CTA로만 적는다. 워드마크 "허들링"을 함께 넣은 것은 제작 시의 해석이다(04-figma). 로고마크도 실제 로고가 아닌 자리표시자다.
- 자물쇠 아이콘 없음: 잠김은 텍스트 배지로만 표현했다. 아이콘 자산이 없었다(04-figma).
- 더미 값: 미션 제목, 자료 제목, 캡션은 더미 텍스트이며 이미지는 자리표시자다.
- 글자 크기·줄 높이·요소 너비/높이: frames.json에 없어 이 가이드에 적지 않았다. design.md 타이포 토큰과의 대응은 weight 기준의 후보일 뿐 크기는 확인하지 못했다.
