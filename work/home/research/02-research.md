# 02-research — home

> 조사 범위 메모: WebFetch로 확인한 페이지는 대부분 로그인 전(비회원) 화면이다. 로그인 후 홈(진행 중 학습, 잠긴 콘텐츠, 내 자산이 한 화면에 있는 상태)을 직접 확인한 사례는 #2의 2016년 블로그 글뿐이고, 그것도 글의 텍스트 설명만 확인했다. 아래 "관찰한 것"은 페이지 요약 응답에 나온 내용만 적었고 화면 스크린샷·픽셀 수준 배치는 확인하지 못했다. 01-scope의 답변 1~9는 하이서 미확인 가정이므로, 아래 적용 판단도 그 가정 위에 있다.

## 사례
| # | 사례 | 출처 URL | 관찰한 것 | 적용 | 이유 (1줄) |
| --- | --- | --- | --- | --- | --- |
| 1 | Coursera 홈 (비회원 상태) | https://www.coursera.org/ | 상단에 개인/기업/대학/정부 링크와 Log In, Join for Free 버튼. 히어로 뒤에 "Most popular", "Hot new releases", "Trending AI courses" 등 탐색 섹션, 그 뒤에 Coursera Plus 구독 프로모션(7일 무료 체험 안내), 이어서 Business, Data Science 등 카테고리 목록과 FAQ가 나온다. 유료 전환 안내가 탐색 섹션 뒤의 본문 중간 블록으로 놓여 있다. | 가능 | 무료 회원용 유료 전환 CTA를 탐색 섹션 뒤 독립 블록으로 두는 위치 선택지가 되고, 결제 화면 자체는 가져오지 않는다. |
| 2 | Coursera 학습자 대시보드 (2016 블로그 글) | https://blog.coursera.org/whats-new-on-coursera-dashboard-and-course-home/ | 글은 일부 학습자 대상 파일럿으로 대시보드와 코스 홈에 진행률 바, 주차별 계획 안내, 다음 영상·과제 링크를 넣었다고 설명한다. 이유로 "진행 추적과 계획 기능이 더 필요하다"는 학습자 의견을 든다. 글은 요소의 화면 순서는 밝히지 않는다. 2016년 글이라 현재 화면은 확인하지 못했다. | 가능 | 현재 미션의 진행 상태와 다음 할 일 링크를 홈 상단 정보로 두는 근거가 되며, 6-4(현재 미션·제출 상태)의 `작성 중`/`제출 완료` 두 상태만으로 표현할 수 있다. |
| 3 | Codecademy 홈 (비회원 상태) | https://www.codecademy.com/ | 상단에 로고·검색·가입/로그인, 히어로에 AI·데이터·코딩 등 주제 탐색 유도. 중간에 "Top subjects" 주제 그리드(20여 개, "Load more" 버튼)와 전체 카탈로그 링크가 있고, 페이지 끝에 무료 가입 CTA가 있다. | 가능 | 카테고리 6개를 홈에서 그리드 진입점으로 드러내는 방식의 근거이고, 6개뿐이라 "Load more"는 필요 없다. |
| 4 | Codecademy 요금제 페이지 | https://www.codecademy.com/pricing | 무료 Basic, 유료 Plus/Pro/All Access를 월 요금과 함께 나열하고, 요금제별 포함 기능 목록을 비교한다. CTA는 "Sign up for free", "Try Plus for free", "Try Pro for free", "Get all access". | 불가 | 요금·체험 결제로 이어지는 요금제 비교 구조는 결제·구매 범위 제외 (PRD 5절, 6-6, 9절 범위 결정 1)에 해당한다. |
| 5 | Notion 템플릿 마켓 | https://www.notion.com/templates | 상단 nav 아래 Templates/Agents/Consultants/Connections 탭. 카테고리 행마다 템플릿 개수(예: Study Planner 5,520)를 표시한다. 추천 템플릿 카드에는 작성자 이름과 "Free" 표시가 붙는다. 하단에 "Become a creator" 블록이 있다. | 가능 | 카드에 무료/유료 표시를 유지하고(6-1) 카테고리별 자료 개수를 보여 주는 방식은 가져올 수 있으며, "Become a creator" 성격의 판매 진입은 seller에게만 노출하는 해석(01-scope)과 맞춰야 한다. |
| 6 | Framer 템플릿 마켓 | https://www.framer.com/marketplace/templates/ | 상단에 Trending/Best/Recent 탭과 Price·Style 정렬. 카드 그리드에 템플릿 이름, 작성자, 가격(Free 또는 $49, $129 등)이 표시되고, 무료는 복제 링크, 유료는 구매 링크가 붙는다. 하단에 50여 개 카테고리 메뉴가 나열된다. 저장/즐겨찾기와 제작자 제출 진입점은 응답에서 보이지 않았다. | 불가 | 카드마다 가격과 구매 링크가 붙는 구조는 구매자 흐름 제외 (PRD 5절, 6-6, 9절 범위 결정 1)에 걸린다. |
| 7 | Patreon 홈 (비회원 상태) | https://www.patreon.com/ | 상단 nav에 Creators/Features/Pricing/Resources와 "Find a Creator" 검색, Log in/Get Started. 본문은 크리에이터 스포트라이트 카드와 프로필 캐러셀, 기능 소개, 하단 "Get started" CTA. 응답은 이 화면이 비회원 전환용이라고 요약했고 멤버십 잠금 표시나 내 콘텐츠 영역은 보이지 않았다. | 불가 | 크리에이터 탐색·전환에 맞춘 비회원 홈이라 학습 진행과 잠긴 콘텐츠를 한 화면에서 푸는 이 화면의 문제에는 참고할 구조가 확인되지 않았다. |

## 패턴·전략 분류
| 패턴 | 해당 사례 # | 전략 한 문장 |
| --- | --- | --- |
| 탐색 뒤 전환 CTA (전환 안내를 탐색 섹션 뒤 독립 블록으로 배치) | 1, 3, 7 | 무료 회원의 유료 전환 CTA를 상단 고정이 아니라 카테고리·콘텐츠 탐색 뒤 블록으로 두어, 본 콘텐츠를 보여 준 다음 전환을 제안한다. |
| 진행 상태 우선 (진행률·다음 할 일을 학습 홈의 앞 정보로 배치) | 2 | 로그인한 사용자에게는 현재 미션 상태와 다음 행동 링크를 카테고리 탐색보다 앞에 둔다. |
| 카테고리 그리드 진입 (주제 목록을 홈에서 직접 진입점으로 노출) | 1, 3, 5, 6 | 카테고리 6개를 고정 그리드나 행으로 홈에 두고, 사례의 "더 보기"·50여 개 나열 같은 확장은 쓰지 않는다. |
| 무료/유료 라벨과 개수 표시 (카드·카테고리에 접근 조건과 수량 명시) | 5, 6 | 콘텐츠 카드에 무료/유료 표시를 붙이고 카테고리에 자료 개수를 함께 보여 준다. |
| 가격·구매 결합 (탐색 화면에 요금·구매 링크를 결합) — 적용 제외 패턴 | 4, 6 | 요금 비교와 구매 링크는 MVP 범위 밖이므로 홈 시안에서 제외한다. |

## 확인하지 못한 사례
| 사례 | URL | 이유 |
| --- | --- | --- |
| Figma Community | https://www.figma.com/community | HTTP 403 Forbidden. |
| Skillshare | https://www.skillshare.com/ | HTTP 403 Forbidden. |
| Udemy | https://www.udemy.com/ | HTTP 403 Forbidden. |
| Patreon 도움말 (잠긴 게시물, 혜택 접근) | https://support.patreon.com/hc/en-us/articles/360026984152-Why-can-t-I-access-posts, https://support.patreon.com/hc/en-us/articles/204606265-Access-my-benefits | 두 페이지 모두 HTTP 403. WebSearch 결과 요약에 잠금 표시와 티어 안내가 언급되지만 페이지를 열어 확인하지 못해 사례에 넣지 않았다. |
| Gumroad Discover | https://gumroad.com/discover | 응답에 페이지 제목/설명만 있고 화면 구성이 없었다. |
| Duolingo (홈, 스트릭 도움말) | https://www.duolingo.com/, https://www.duolingo.com/help/what-is-a-streak | 응답에 사이트 이름만 있고 본문이 없었다. WebSearch 요약의 잠금·스트릭 설명은 페이지를 열어 확인하지 못했다. |
| Khan Academy | https://www.khanacademy.org/ | 응답에 사이트 이름만 있고 본문이 없었다. |
| freeCodeCamp Learn | https://www.freecodecamp.org/learn | 응답에 본문이 비어 있었다. |
| 로그인 후 홈/대시보드 전반 (Coursera, Codecademy, Patreon 등) | - | 로그인이 필요해 접근하지 못했다. 위 사례 중 로그인 후 화면을 확인한 것은 #2(2016년 글의 텍스트 설명)뿐이다. |
