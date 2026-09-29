# DESIGN.md

SEED Design(당근 디자인 시스템) 기반 디자인 규칙. AI 에이전트가 UI 코드를 생성·수정할 때 참조한다.

- 출처: https://seed-design.io (각 섹션 `llms.txt`), 수집일 2026-09-29
- 표기: 토큰은 SEED 표기(`$color.fg.neutral` 등)를 그대로 쓴다. 코드에 옮길 때의 변수명은 프로젝트 토큰 CSS를 따른다.
- 이 문서에 없는 값은 **추측하지 말고** "확인 필요"로 남기거나 아래 [조회 경로](#조회-경로)에서 가져온다.

## 0. 개요

흰색과 옅은 회색 면(`bg.layer-*`) 위에 짙은 회색 텍스트(`fg.neutral`)를 얹는 중립적인 화면이다. 브랜드색(Carrot 주황)은 사용자 간 연결이 일어나는 핵심 액션에만 아껴 쓰고, 나머지 CTA는 뉴트럴(검정 계열)로 처리한다. 깊이는 그림자가 아니라 레이어 색으로 표현하고, 모서리는 8~12px 정도로 부드럽게 둥글린다. 모든 색은 라이트/다크 두 테마를 토큰이 알아서 처리한다.

## 1. 절대 규칙

1. 색상·간격·타이포·radius·shadow는 **토큰만** 쓴다. raw hex, `rgb()`/`hsl()`, raw px, Tailwind arbitrary value(`w-[..]`, `text-[..]`)는 금지.
2. 색상은 palette(`gray-100`, `carrot-500` 등)가 아니라 **semantic role**(`fg` / `bg` / `stroke`)로 참조한다. palette 직접 참조는 role에 맞는 토큰이 없을 때만 허용한다.
3. 새 값이 필요하면 값을 만들지 말고 가장 가까운 토큰을 쓴 뒤 사용자에게 알린다.
4. 컴포넌트는 SEED에 있으면 재사용한다. 비슷한 것을 새로 만들지 않는다.
5. Deprecated 컴포넌트는 신규 사용 금지: Action Chip, Action Sheet, Control Chip, Error State, Extended Action Sheet, Extended FAB, FAB, Inline Banner, Link Content.

## 2. 색상

### 2.1 Role 토큰

**Foreground (`$color.fg.*`)**

| 토큰 | 용도 |
| --- | --- |
| `neutral` | 기본 콘텐츠 텍스트·아이콘 |
| `neutral-muted` | 보조 텍스트 (강조 낮음) |
| `neutral-subtle` | 가장 약한 텍스트 |
| `neutral-inverted` | 어두운 배경 위 텍스트 |
| `brand`, `brand-contrast` | 브랜드 요소 |
| `positive`, `positive-contrast` | 성공·확인 |
| `warning`, `warning-contrast` | 주의 |
| `critical`, `critical-contrast` | 오류·심각 |
| `informative`, `informative-contrast` | 정보·상태 |
| `disabled` | 비활성 |
| `placeholder` | 입력 placeholder |

**Background (`$color.bg.*`)**

| 그룹 | 토큰 |
| --- | --- |
| Brand | `brand-solid`, `brand-solid-pressed`, `brand-weak`, `brand-weak-pressed` |
| Neutral | `neutral-solid`, `neutral-weak`, `neutral-inverted`, `neutral-inverted-pressed`, `neutral-weak-alpha`, `neutral-weak-alpha-pressed` |
| Positive / Warning / Critical / Informative | 각각 `*-solid`, `*-solid-pressed`, `*-weak`, `*-weak-pressed` |
| Layer | `layer-basement`(최하단), `layer-default`, `layer-default-pressed`, `layer-fill`, `layer-floating`, `layer-floating-pressed` |
| Functional | `disabled`, `overlay`, `overlay-muted`, `transparent`, `transparent-pressed`, `transparent-selected`, `transparent-selected-pressed`, `magic-weak` |

**Stroke (`$color.stroke.*`)**

| 그룹 | 토큰 |
| --- | --- |
| Neutral | `neutral-solid`, `neutral-contrast`, `neutral-muted`, `neutral-subtle`, `neutral-weak` |
| Brand / Positive / Warning / Critical / Informative | 각각 `*-solid`, `*-weak` |
| Functional | `focus-ring` (키보드 포커스 표시) |

### 2.2 사용 규칙

- `solid`는 높은 강조(주요 버튼 등), `weak`는 낮은 강조(배경 틴트)에 쓴다.
- 인터랙션 요소의 눌림 상태는 대응하는 `*-pressed` 토큰을 쓴다. opacity나 임의 색으로 대체하지 않는다.
- 화면 깊이는 `bg.layer-*`로 표현한다: `basement` < `default` < `floating`.
- 시맨틱 색(`positive`/`warning`/`critical`/`informative`)은 의미가 맞을 때만 쓴다. 장식용으로 쓰지 않는다.
- 다크 모드는 토큰이 자동으로 대응한다. 테마별 분기용 raw 색을 만들지 않는다.

### 2.3 Role → 값 매핑 (light / dark)

토큰 이름 → palette 참조. 코드에서는 항상 **왼쪽 role 이름**을 쓴다. 실제 hex는 2.4 palette 표에서 찾는다. `*-alpha-N`은 static black/white의 alpha 단계다.

**fg**

| 토큰 | light / dark |
| --- | --- |
| `fg.neutral` | gray-1000 / gray-1000 |
| `fg.neutral-muted` | gray-800 / gray-800 |
| `fg.neutral-subtle` | gray-700 / gray-700 |
| `fg.neutral-inverted` | gray-00 / gray-100 |
| `fg.placeholder` | gray-600 / gray-600 |
| `fg.disabled` | gray-500 / gray-500 |
| `fg.brand` | carrot-600 / carrot-700 |
| `fg.brand-contrast` | carrot-700 / carrot-700 |
| `fg.positive` · `-contrast` | green-700 · green-900 (양 테마 동일) |
| `fg.warning` · `-contrast` | yellow-700 · yellow-900 (양 테마 동일) |
| `fg.critical` · `-contrast` | red-700 · red-900 (양 테마 동일) |
| `fg.informative` · `-contrast` | blue-700 · blue-900 (양 테마 동일) |

**bg**

| 토큰 | light / dark |
| --- | --- |
| `bg.layer-basement` | gray-200 / gray-00 |
| `bg.layer-default` (`-pressed`) | gray-00 (gray-100) / gray-100 (gray-300) |
| `bg.layer-fill` | gray-100 / gray-200 |
| `bg.layer-floating` (`-pressed`) | gray-00 (gray-100) / gray-200 (gray-300) |
| `bg.neutral-solid` | gray-1000 / gray-300 |
| `bg.neutral-weak` (`-pressed`) | gray-200 (gray-300) / gray-300 (gray-400) |
| `bg.neutral-inverted` (`-pressed`) | gray-900 (gray-800) / gray-1000 (gray-800) |
| `bg.neutral-weak-alpha` (`-pressed`) | static-black-alpha-200 (300) / static-white-alpha-200 (300) |
| `bg.brand-solid` (`-pressed`) | carrot-600 (carrot-700) / carrot-700 (carrot-800) |
| `bg.brand-weak` (`-pressed`) | carrot-100 (carrot-200) / carrot-100 (carrot-200) |
| `bg.positive-solid` (`-pressed`) | green-700 (green-800) / green-500 (green-600) |
| `bg.warning-solid` (`-pressed`) | yellow-300 (yellow-400) / yellow-800 (yellow-900) |
| `bg.critical-solid` (`-pressed`) | red-700 (red-800) / red-600 (red-700) |
| `bg.informative-solid` (`-pressed`) | blue-700 (blue-800) / blue-600 (blue-700) |
| `bg.positive-weak` · `warning-weak` · `critical-weak` · `informative-weak` | 각 색-100 (`-pressed`는 색-200), 양 테마 동일 |
| `bg.disabled` | gray-200 / gray-300 |
| `bg.overlay` · `bg.overlay-muted` | static-black-alpha-700 · 500 (양 테마 동일) |
| `bg.transparent` | 완전 투명 |
| `bg.transparent-pressed` | static-black-alpha-100 / static-white-alpha-50 |
| `bg.transparent-selected` (`-pressed`) | static-black-alpha-200 (300) / static-white-alpha-100 (200) |
| `bg.magic-weak` | #f9f2ee / #201f1f |

**stroke**

| 토큰 | light / dark |
| --- | --- |
| `stroke.neutral-weak` | gray-400 / gray-400 |
| `stroke.neutral-muted` | static-black-alpha-300 / static-white-alpha-100 |
| `stroke.neutral-subtle` | static-black-alpha-200 / static-white-alpha-50 |
| `stroke.neutral-solid` | gray-800 / gray-800 |
| `stroke.neutral-contrast` | gray-1000 / gray-1000 |
| `stroke.brand-solid` · `brand-weak` | carrot-700 · carrot-300 |
| `stroke.positive-solid` · `-weak` | green-700 · green-300 |
| `stroke.warning-solid` · `-weak` | yellow-700 · yellow-300 |
| `stroke.critical-solid` · `-weak` | red-700 · red-300 |
| `stroke.informative-solid` · `-weak` | blue-700 · blue-300 |
| `stroke.focus-ring` | blue-600 / blue-600 |

### 2.4 Palette (role에 맞는 토큰이 없을 때만)

값은 참조용이다. 코드에 hex를 직접 쓰지 말고 토큰 이름으로 참조한다. 표기: light / dark.

| 단계 | gray | carrot | blue |
| --- | --- | --- | --- |
| 00 | #ffffff / #000000 | | |
| 100 | #f7f8f9 / #16171b | #fff2ec / #31241f | #eff6ff / #202742 |
| 200 | #f3f4f5 / #1d2025 | #ffe8db / #4b291c | #e2edfc / #1e3352 |
| 300 | #eeeff1 / #2b2e35 | #ffd5c0 / #6b311c | #cbdffa / #1a4275 |
| 400 | #dcdee3 / #393d46 | #ffb999 / #923600 | #aacefd / #0f559e |
| 500 | #d1d3d8 / #5b606a | #ff9364 / #bd4201 | #85b8fd / #1964d8 |
| 600 | #b0b3ba / #868b94 | #ff6600 / #e65200 | #5e98fe / #1e82eb |
| 700 | #868b94 / #b0b3ba | #e14d00 / #ff6600 | #217cf9 / #41a2f9 |
| 800 | #555d6d / #dcdee3 | #b93901 / #ff9e65 | #135fcd / #83bcf9 |
| 900 | #2a3038 / #e9eaec | #862b00 / #eecebc | #0b4596 / #b9d7fb |
| 1000 | #1a1c20 / #f3f4f5 | #471601 / #f4eeea | #032451 / #e5f0fe |

| 단계 | red | green | yellow | purple |
| --- | --- | --- | --- | --- |
| 100 | #fdf0f0 / #322323 | #edfaf6 / #202926 | #fff7de / #302819 | #f5f3fe / #28213b |
| 200 | #fde7e7 / #4f2624 | #d9f6e9 / #20362e | #fdefb9 / #413218 | #efeafe / #3b2873 |
| 300 | #fed4d2 / #742826 | #b9e9d2 / #20493b | #fbdc65 / #543e15 | #e1d8ff / #443081 |
| 400 | #feb7b3 / #a12621 | #7ddcb3 / #19604c | #e9c647 / #714e15 | #d0c0ff / #5a3bb1 |
| 500 | #fe928d / #ca2319 | #42c593 / #117956 | #d4ab28 / #91601b | #b8a1ff / #764fd9 |
| 600 | #fc6a66 / #f73526 | #10ab7d / #1b946d | #c49725 / #b6720d | #9f84fb / #8e6bee |
| 700 | #fa342c / #ff6e60 | #079171 / #22b27f | #9b7821 / #ca901c | #8969ea / #a78df0 |
| 800 | #ca1d13 / #ffa299 | #00745f / #35ce9a | #755b22 / #dab156 | #6d50cb / #beadf2 |
| 900 | #921708 / #f8c5c3 | #075445 / #93e5c0 | #4f3e1f / #e5d49b | #50379b / #d9cefa |
| 1000 | #4a1209 / #fdf2f2 | #0a2b24 / #d4f6ef | #2c2512 / #f7f0cd | #29175d / #f0edfc |

- `static-black` `#000000`, `static-white` `#ffffff` (라이트·다크 동일). Black alpha 100~1000(`#00000007`~`#000000e3`), White alpha 50~1000(`#ffffff0d`~`#fffffff4`).
**Manner-temp** (bg / text, light → dark)

| 레벨 | light bg / text | dark bg / text |
| --- | --- | --- |
| l1 | #f1f2f3 / #757b85 | #292929 / #b8b8b9 |
| l2 | #f8f4ec / #ab863f | #332605 / #f5db97 |
| l3 | #fff5e5 / #e08a00 | #372b01 / #fdda65 |
| l4 | #fff3e5 / #f57e00 | #372301 / #fbbe55 |
| l5 | #fff1e5 / #ff7300 | #371f01 / #faac4b |
| l6 | #fff0e5 / #ff6600 | #351b03 / #fc9855 |
| l7 | #ffefe5 / #ff5100 | #371701 / #f97a25 |
| l8 | #ffeee5 / #ff3300 | #380f00 / #fe6a34 |
| l9 | #fdeded / #e82c45 | #380500 / #fe6a5d |
| l10 | #ffebee / #cb0123 | #34040a / #fb6f82 |

**Banner** (light / dark): blue #e1f7ff / #0d2a3a · cool-gray #ebf1f5 / #242c33 · green #f0fbe5 / #1e361c · orange #fff2e1 / #42230a · pink #ffebf1 / #3b172c · purple #f5ecff / #2e1e45 · red #ffecee / #3a0f15 · teal #e6faf6 / #143633 · warm-gray #f2f0ee / #2f2b27 · yellow #fffae1 / #3e2b00

## 3. 타이포그래피

- 폰트 패밀리: **Pretendard**. SEED 토큰은 size/weight/line-height만 제공하고 패밀리는 정의하지 않으므로, 패밀리는 이 프로젝트에서 Pretendard로 지정한다. 다른 폰트로 대체하지 않는다.
- 스타일 이름은 `t{N}{Weight}` 형식이다. 예: `t5Regular`, `t1Bold`.
- Weight: `regular`(400), `medium`(500), `bold`(700). 이 외의 weight 금지.
- 크기는 rem 같은 상대 단위를 쓴다.

| Scale | font-size | line-height |
| --- | --- | --- |
| t1 | 0.6875rem (11px) | 0.9375rem (15px) |
| t2 | 0.75rem (12px) | 1rem (16px) |
| t3 | 0.8125rem (13px) | 1.125rem (18px) |
| t4 | 0.875rem (14px) | 1.1875rem (19px) |
| t5 | 1rem (16px) | 1.375rem (22px) |
| t6 | 1.125rem (18px) | 1.5rem (24px) |
| t7 | 1.25rem (20px) | 1.6875rem (27px) |
| t8 | 1.375rem (22px) | 1.875rem (30px) |
| t9 | 1.5rem (24px) | 2rem (32px) |
| t10 | 1.625rem (26px) | 2.1875rem (35px) |
| t11 | 1.75rem (28px) | 2.375rem (38px) |
| t12 | 2rem (32px) | 2.625rem (42px) |
| t13 | 2.5rem (40px) | 3.25rem (52px) |
| t14 | 3rem (48px) | 3.75rem (60px) |

- 역할 기반 semantic text style(`screenTitle`, `articleBody` 등)이 있으면 scale 스타일보다 우선한다. 전체 매핑은 **확인 필요** (문서에 미공개, 컴포넌트 스펙 JSON `/rootage/components/typography.json`).
- 제목과 본문은 크기·weight로 위계를 분명히 구분한다.

## 4. Spacing

Base scale (`$dimension.*`)

| 토큰 | 값 | 토큰 | 값 |
| --- | --- | --- | --- |
| `x0_5` | 2px | `x5` | 20px |
| `x1` | 4px | `x6` | 24px |
| `x1_5` | 6px | `x7` | 28px |
| `x2` | 8px | `x8` | 32px |
| `x2_5` | 10px | `x9` | 36px |
| `x3` | 12px | `x10` | 40px |
| `x3_5` | 14px | `x12` | 48px |
| `x4` | 16px | `x13` | 52px |
| `x4_5` | 18px | `x14` | 56px |
| | | `x16` | 64px |

`$dimension.*`는 간격뿐 아니라 컴포넌트의 높이·패딩·아이콘 크기에도 쓴다.

Composite (의미가 정해진 간격은 이쪽을 우선 사용)

| 토큰 | 값 | 용도 |
| --- | --- | --- |
| `spacing-x.global-gutter` | 16px | 화면 좌우 여백 |
| `spacing-x.between-chips` | 8px | 칩 사이 가로 간격 |
| `spacing-y.component-default` | 12px | 컴포넌트 간 기본 세로 간격 |
| `spacing-y.nav-to-title` | 20px | 내비게이션과 페이지 타이틀 사이 |
| `spacing-y.between-text` | 6px | 텍스트 줄/블록 사이 |
| `spacing-y.screen-bottom` | 56px | 화면 하단 여백 |

- 화면 여백은 safe area 경계 기준으로 잰다. 화면 가장자리 기준이 아니다.
- 위 표에 없는 간격(예: 5px, 14px)은 만들지 않는다.

## 5. Radius

| 토큰 | 값 | 토큰 | 값 |
| --- | --- | --- | --- |
| `r0_5` | 2px | `r3` | 12px |
| `r1` | 4px | `r3_5` | 14px |
| `r1_5` | 6px | `r4` | 16px |
| `r2` | 8px | `r5` | 20px |
| `r2_5` | 10px | `r6` | 24px |
| | | `full` | 9999px |

- 컴포넌트별 기본 radius는 해당 컴포넌트 문서를 따른다.

## 6. Elevation (Shadow)

| 토큰 | Light | Dark |
| --- | --- | --- |
| `$shadow.s1` | `#00000014`, 0 / 1px / 4px blur | `#00000080` |
| `$shadow.s2` | `#0000001a`, 0 / 2px / 10px blur | `#000000ad` |
| `$shadow.s3` | `#0000001f`, 0 / 4px / 16px blur | `#000000cc` |

- 다크 모드에서 shadow가 잘 보이지 않는다. 화면에서 주목도가 높은 **소수의 요소에만** 쓴다.
- 일반적인 깊이 구분은 shadow가 아니라 `bg.layer-*`로 한다.

## 7. Motion · Feedback

Duration: `d1` 50ms · `d2` 100ms · `d3` 150ms · `d4` 200ms · `d5` 250ms · `d6` 300ms

| Timing | cubic-bezier | 용도 |
| --- | --- | --- |
| `linear` | (0, 0, 1, 1) | |
| `easing` | (0.35, 0, 0.35, 1) | 버튼 클릭·입력창 포커스 등 기능적 마이크로 모션, 눌림 상태의 색·scale 전환(`d3`) |
| `enter` | (0, 0, 0.15, 1) | 다이얼로그·시트 등장 |
| `exit` | (0.35, 0, 1, 1) | 다이얼로그·시트 퇴장 |
| `enter-expressive` | (0.03, 0.4, 0.1, 1) | 강조가 필요한 등장 |
| `exit-expressive` | (0.35, 0, 0.95, 0.55) | 강조가 필요한 퇴장 |
| `pressed-scale` | (0, 0, 0.15, 1) | 눌림 scale |

- 눌림 피드백 scale: `s95`, `s97`, `s98`. 눌림 색상은 `*-pressed` 토큰을 쓴다.
- 임의의 `transition: 200ms`나 raw cubic-bezier 금지.
- `s95`/`s97`/`s98`을 요소별로 어떻게 나눠 쓰는지는 **확인 필요** (`feedback/scale.txt`).

## 7-1. Layout

| Breakpoint | 범위 | Gutter | Margin |
| --- | --- | --- | --- |
| base | 0–479px | 16px | 12px |
| sm | 480–767px | 16px | 12px |
| md | 768–1279px | 32px | 24px |
| lg | 1280–1439px | 32px | 24px |
| xl | 1440px+ | 32px | 24px |

- 콘텐츠 레이아웃 기본은 12-column, 중앙 정렬. max-width는 1040px(기본) 또는 1280px(커머스·검색 결과).
- Dashboard 밀도: Low(8 columns, 최대 720px), Middle(12 columns, 최대 1040px, 기본), High(fluid, 최소 1040px). 공통으로 gutter 24px, margin 32px.
- 위 breakpoint 외의 값으로 media query를 쓰지 않는다.

## 8. 컴포넌트 목록 (재사용 우선)

**Action**: Action Button, Floating Action Button, Contextual Floating Button, Reaction Button, Input Button
**Input**: Text Input & Textarea, Field, Select, Select Box, Checkbox, Radio, Switch, Slider, Segmented Control, Quantity Picker, Attachment Input, Date Picker, Time Picker, Wheel Picker
**Navigation**: Top Navigation, Bottom Navigation, Side Navigation, Tabs, Pagination, Table Pagination
**Overlay**: Dialog, Alert Dialog, Bottom Sheet, Menu Sheet, Menu, Side Panel, Help Bubble, Snackbar
**Display**: List, Avatar, Image Frame, Badge, Notification Badge, Chip, Tag Group, Divider, Accordion, Manner Temp
**Feedback / Status**: Callout, Page Banner, Skeleton, Content Placeholder, Identity Placeholder, Progress Circle, Result Section, Scroll Fog
**기타**: Footer

컴포넌트별 anatomy·properties·가이드는 `https://seed-design.io/llms/components/{kebab-case-name}.txt`, 수치 스펙은 `https://seed-design.io/rootage/components/{kebab-case-name}.json`.

### 8.1 Action Button (버튼)

SEED에는 Card 컴포넌트가 없다. 카드형 영역은 `bg.layer-*` + radius 토큰으로 구성하고 별도 규격은 만들지 않는다(**확인 필요**).

**Size** — label은 항상 `bold`

| size | min-height | radius | padding X / Y | gap | 아이콘 | label |
| --- | --- | --- | --- | --- | --- | --- |
| xsmall | `x8` (32) | `full` | `x3_5` / `x1_5` | `x1` | `x3_5` | t3 |
| small | `x9` (36) | `r2` | `x3_5` / `x2` | `x1` | `x3_5` | t4 |
| medium | `x10` (40) | `r2` | `x4` / `x2_5` | `x1_5` | `x4` | t4 |
| large | `x13` (52) | `r3` | `x5` / `x3_5` | `x2` | 22px | t6 |

- Icon only: min-width는 min-height와 같고, padding은 X=Y(xsmall `x1_5`, small `x2`, medium `x2_5`, large `x3_5`). 아이콘은 xsmall `x3_5`, small `x4`, medium 18px, large 22px.
- 22px, 18px은 스펙 원문이 raw 값이다. 토큰이 없으므로 코드에서는 가장 가까운 dimension 토큰을 쓰고 사용자에게 알린다.
- Large는 CTA용. Small/Medium은 화면 중간의 일반 액션용. xsmall은 좁은 공간용 pill.

**Variant** (enabled / pressed)

| variant | 배경 | label·아이콘 | pressed 배경 | 용도 |
| --- | --- | --- | --- | --- |
| brandSolid | `bg.brand-solid` | static-white | `bg.brand-solid-pressed` | 사용자 간 연결이 일어나는 핵심 기능. 화면당 1개 권장 |
| neutralSolid | `bg.neutral-inverted` | `fg.neutral-inverted` | `bg.neutral-inverted-pressed` | 대부분 화면의 CTA. 화면당 1개 권장 |
| neutralWeak | `bg.neutral-weak` | `fg.neutral` | `bg.neutral-weak-pressed` | CTA 외 대부분의 액션 |
| criticalSolid | `bg.critical-solid` | static-white | `bg.critical-solid-pressed` | 삭제·초기화 등 되돌릴 수 없는 작업 |
| neutralOutline | `bg.transparent` + stroke `stroke.neutral-muted` 1px | `fg.neutral` | `bg.transparent-pressed` | brandOutline과 짝으로 사용 |
| brandOutline | `bg.transparent` + stroke `stroke.neutral-muted` 1px | `fg.brand` | `bg.transparent-pressed` | neutralOutline과 짝으로 사용 |
| ghost | 투명 | `fg.neutral` | `bg.transparent-pressed` | 낮은 강조 |

- Disabled: 배경 `bg.disabled`(outline·ghost는 투명), label·아이콘 `fg.disabled`. Loading: 배경은 해당 variant의 pressed 색.
- 색 전환은 `easing` timing. 눌림 시 버튼 자체가 scale 축소된다.
- 라벨 앞과 뒤에 아이콘을 동시에 두지 않는다. 한 줄에 버튼 4개 이상 금지. 아이콘만 있는 버튼은 꼭 필요할 때만.
- Outline 두 variant는 solid 계열과 함께 쓸 수 없다. neutralWeak과 주 액션을 나란히 놓을 때는 너비 비율 3:7.

### 8.2 Text Input (입력창)

| variant | size | min-height | radius | padding | gap | 텍스트 | 아이콘 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| outline | large | `x13` (52) | `r3` | X `x4` | `x2_5` | t5 | `x5` |
| outline | medium | `x10` (40) | `r2` | X `x3_5` | `x2` | t4 | `x4` |
| underline | large | `x10` (40) | 없음 | Y `x2` | `x2_5` | t6 | `x6` |
| underline | medium | 34px (raw) | 없음 | Y `x1_5` | `x2` | t5 | `x5` |

- Textarea(multiline) min-height: large 94px, medium 82px (스펙 원문이 raw 값). padding Y는 large `x3_5`, medium `x3`.
- 색: 값 `fg.neutral`(regular), placeholder `fg.placeholder`, prefix/suffix 텍스트 `fg.neutral-subtle`, prefix/suffix 아이콘 `fg.neutral-muted`.
- 테두리: enabled `stroke.neutral-weak` 1px → focused `stroke.neutral-contrast` 2px → invalid `stroke.critical-solid` 2px. underline은 하단선만 같은 규칙. 전환은 0.1s `easing`.
- Disabled: 모든 텍스트·아이콘 `fg.disabled`, outline은 배경 `bg.disabled`. Read only(outline)도 배경 `bg.disabled`.
- 화면에 입력창이 하나뿐이면 underline. 전화번호처럼 형식이 있는 값은 필드를 쪼개지 말고 한 필드에서 자동 포맷한다.

### 8.3 Chip

| size | height | padding X | label | prefix 아이콘 | suffix 아이콘 | prefix 아바타 | min-width (텍스트 / 아이콘만) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| small | 32px (raw) | `x1_5` | t4 | `x3_5` | `x3_5` | `x5` | 44px (raw) / `x8` |
| medium | 36px (raw) | `x2` | t4 | `x4` | `x3_5` | `x6` | `x12` / `x9` |
| large | 40px (raw) | `x2_5` | t4 | `x4` | `x4` | `x7` | `x13` / `x10` |

- 공통: radius `full`, label `medium` weight + padding X `x1_5`, prefix 아이콘 왼쪽 padding·suffix 아이콘 오른쪽 padding `x1_5`. 눌림 시 chip 자체가 scale 축소, 색 전환은 `easing`.
- height는 스펙 원문이 raw px다. 코드에서는 가장 가까운 dimension 토큰(`x8` / `x9` / `x10`)을 쓰고 사용자에게 알린다.

| variant | enabled | pressed | selected (pressed) | disabled |
| --- | --- | --- | --- | --- |
| solid | 배경 `bg.neutral-weak-alpha`, 텍스트·아이콘 `fg.neutral` | `bg.neutral-weak-alpha-pressed` | 배경 `bg.neutral-inverted`(`-pressed`), 텍스트·아이콘 `fg.neutral-inverted` | opacity 0.5 |
| outlineStrong | 배경 `bg.transparent`, stroke `stroke.neutral-muted` 1px, 텍스트·아이콘 `fg.neutral` | `bg.transparent-pressed` | 배경 `bg.neutral-inverted`(`-pressed`), 텍스트·아이콘 `fg.neutral-inverted` | opacity 0.5 |
| outlineWeak | outlineStrong과 동일 | `bg.transparent-pressed` | stroke `stroke.neutral-contrast`, 배경 `bg.neutral-weak`(`-pressed`) | opacity 0.5 |

- 다중 선택 값에는 outlineWeak 권장. 사용자가 입력한 값은 suffix에 삭제 버튼을 둔다.
- Chip 목록(tablist 형태): 좌우 padding `x4`, chip 사이 gap 8px(=`spacing-x.between-chips`).

### 8.4 List Item

| 항목 | 값 |
| --- | --- |
| padding | Y `x3`, X `spacing-x.global-gutter` |
| body | gap `x0_5`, 오른쪽 padding `x2_5` |
| prefix | 오른쪽 padding `x3`, 아이콘 22px(raw) `fg.neutral` |
| suffix | gap `x1`, 텍스트 t5 `fg.neutral-subtle`, 아이콘 18px(raw) `fg.neutral-subtle` |
| title | t5 regular, `fg.neutral` |
| detail | t3 regular, `fg.neutral-subtle` |
| 배경 | 기본 `bg.transparent` |
| pressed | 배경 `bg.transparent-pressed`, 좌우 margin `x1_5`, radius `x2_5`, 콘텐츠가 scale 축소 |
| highlighted | 배경 `bg.brand-weak` (pressed: `bg.brand-weak-pressed`) |
| disabled | title·detail·아이콘 `fg.disabled` |

- 항목당 인터랙티브 요소 4개 초과 금지. 컨테이너 radius에서 내부 padding을 뺀 값을 안쪽 요소 radius로 쓴다(concentric).

### 8.5 Checkbox

| size | 영역 min-height | 박스 크기 | 박스 radius | label | 체크 아이콘 (square / ghost) |
| --- | --- | --- | --- | --- | --- |
| medium | `x8` | `x5` | `r1` | t4 | 12px / 14px (raw) |
| large | `x9` | `x6` | `r1` | t5 | 14px / 18px (raw) |

- 박스와 label 사이 gap `x2`. label 색 `fg.neutral`, disabled는 `fg.disabled`. label weight는 regular 또는 bold.
- **Square**: 미선택 stroke `stroke.neutral-weak` 1px. 선택 시 stroke 없이 배경 채움 — brand는 `bg.brand-solid`(pressed `-pressed`) + static-white 아이콘, neutral은 `bg.neutral-inverted`(pressed `-pressed`) + `fg.neutral-inverted` 아이콘. disabled는 배경 `bg.disabled`, stroke `stroke.neutral-muted`, 아이콘 `fg.disabled`. pressed 배경 `bg.transparent-pressed`.
- **Ghost**: 박스 없이 아이콘만. 미선택 `fg.placeholder`, 선택 시 brand `fg.brand` / neutral `fg.neutral`, disabled `fg.disabled`. pressed 배경 `bg.transparent-pressed`.
- 선택 사항이 3개 이하면 Ghost, 필수 동의처럼 명시적 확인이 필요하면 Square. 즉시 적용되는 설정은 Switch, 저장이 필요한 선택은 Checkbox. label을 포함한 영역 전체가 터치 타깃.

### 8.6 Tabs

**Line 탭** (tablist + tab)

| size | tablist 높이 | tab min-height | tab padding | label |
| --- | --- | --- | --- | --- |
| small | 40px (raw) | 40px (raw) | X·Y `x2_5` | t4 bold |
| medium | 44px (raw) | 44px (raw) | X·Y `x2_5` | t5 bold |

- tablist: 배경 `bg.layer-default`, 하단선 `stroke.neutral-muted` 1px. indicator 높이 2px, 색 `fg.neutral`, 이동 `d4` + `easing`.
- tab label 색: 기본 `fg.neutral-subtle`, 선택 `fg.neutral`, 비활성 `fg.disabled`. 눌림 시 scale 축소.
- Layout: hug는 tablist 좌우 padding `spacing-x.global-gutter`, indicator inset 0. fill은 tablist padding 0, indicator inset X `spacing-x.global-gutter`. 탭이 6개 이상이거나 라벨이 길면 hug.
- 높이 40/44px는 스펙 원문이 raw px다. 가장 가까운 dimension 토큰(`x10` / `x12`)을 쓰고 사용자에게 알린다.

**Chip 탭**: 좌우 padding `x4`, chip 사이 gap 8px, 개별 chip 규격은 8.3을 따른다. 화면 전체 전환은 Solid, 부분 전환은 Outline.

### 8.7 Top Navigation

| 항목 | 값 |
| --- | --- |
| 높이 | iOS 44px / Android 56px (raw) |
| 좌우 padding | `x1_5` (Android는 main 왼쪽 `x1_5`) |
| tone=layer | 배경 `bg.layer-default`, title `fg.neutral`, subtitle `fg.neutral-muted` |
| tone=transparent | title·subtitle static-white. gradient=true면 위→아래 검정 35%→투명 그라데이션, 아래로 `x5` 번짐 |
| title만 있을 때 | t6 bold |
| subtitle이 있을 때 | title t5 bold, subtitle t2 regular |
| 글꼴 배율 | 최소 1, 최대 1.2 |

- Root(최상위 탭용)와 Standard(2-depth 이상). 우측 아이콘 버튼은 최대 3개(권장 2개), 텍스트 버튼은 1개. title은 한 줄, 넘치면 말줄임.

### 8.8 Dialog

| 항목 | 값 |
| --- | --- |
| content | 배경 `bg.layer-floating`, radius `r5`, 너비 화면의 90%, 최대 높이 화면의 80%, 좌우 margin `x5` |
| size | medium 최대 480px / large 최대 800px (raw) |
| header | padding X `x6`, 위 `x6`, 아래 `x4`, gap `x1_5` |
| body | padding X `x6`, 아래 `x12` |
| footer | padding X `x6`, 위 `x4`, 아래 `x6` |
| title | t8 bold `fg.neutral` |
| description | t5 regular `fg.neutral-muted` |
| 닫기 버튼 | 위 `x7`, 오른쪽 `x6` |
| 스크롤 시 | body 상단에 `stroke.neutral-muted` 1px 구분선 |
| backdrop | `bg.overlay` |
| 모션 | backdrop 등장 `d2` `enter` / 퇴장 `d2` `exit`. content 등장 `d4` `enter-expressive`, scale 1.3에서 시작 / 퇴장 `d2` `exit` |

- md(768px) 미만에서는 Bottom Sheet로 전환한다. 헤더 닫기 버튼과 푸터 취소 버튼을 동시에 두지 않는다.

### 8.9 Bottom Sheet

| 항목 | 값 |
| --- | --- |
| content | 배경 `bg.layer-floating`, 최대 너비 480px (raw), 위쪽 모서리 radius `r6` |
| header | 위 `x6`, 아래 `x4`, gap `x2` |
| body | padding X `spacing-x.global-gutter` |
| footer | padding X `spacing-x.global-gutter`, 위 `x3`, 아래 `x4` |
| title | t8 bold `fg.neutral` |
| description | t5 regular `fg.neutral-muted`, padding X `spacing-x.global-gutter` |
| 닫기 버튼 | 위 `x6`, 오른쪽 `x4` |
| title 좌우 padding | left 정렬: 닫기 버튼 있으면 오른쪽 56px(raw), 왼쪽 `global-gutter`. center 정렬 + 닫기 버튼: 좌우 56px(raw). 그 외 `global-gutter` |
| backdrop | `bg.overlay` |
| 모션 | backdrop 등장 `d6` `enter` / 퇴장 `d4` `exit`. content 등장 `d6` `enter-expressive` / 퇴장 `d4` `exit` |

- 최대 높이는 화면의 90%. 헤더를 쓰면 title 필수. snap point는 최소 2개(있으면 핸들 필수). 닫기 버튼 터치 타깃 40×40.

## 8-1. Do / Don't

**Do**
- 색은 `fg` / `bg` / `stroke` role 토큰으로, 간격·크기는 `$dimension.*`, 모서리는 `$radius.*`로 쓴다.
- 브랜드 버튼(brandSolid)은 화면당 하나, 사용자 간 연결이 일어나는 핵심 기능에만 쓴다. 일반 CTA는 neutralSolid.
- 눌림·비활성 상태는 `*-pressed`, `bg.disabled`, `fg.disabled` 토큰으로 표현한다.
- 깊이는 `bg.layer-basement` → `layer-default` → `layer-floating`으로 구분하고, shadow는 주목도가 높은 소수 요소에만 쓴다.
- SEED에 있는 컴포넌트는 그대로 재사용하고, 값이 부족하면 조회 경로에서 확인한다.

**Don't**
- raw hex, rgb(), raw px, Tailwind arbitrary value(`w-[..]`)를 쓰지 않는다.
- palette(`gray-100` 등)를 role 토큰이 있는데도 직접 참조하지 않는다.
- 브랜드색을 여러 곳에 남발하지 않는다. 한 줄에 버튼 4개 이상을 놓지 않는다.
- 토큰 표에 없는 간격·radius·font-size·weight(400/500/700 외)를 만들지 않는다.
- Deprecated 컴포넌트(FAB, Action Chip 등)를 새로 쓰지 않는다.

## 9. 조회 경로

값이 필요한데 이 문서에 없으면 아래에서 조회한다.

| 필요한 것 | 경로 |
| --- | --- |
| 토큰 전체 목록 | https://seed-design.io/llms/foundations/design-token/reference.txt |
| 색상 palette | https://seed-design.io/llms/foundations/color/palette.txt |
| 색상 role | https://seed-design.io/llms/foundations/color/color-role.txt |
| 타이포그래피 | https://seed-design.io/llms/foundations/typography.txt |
| 레이아웃·breakpoint | https://seed-design.io/llms/foundations/layout.txt |
| 모션 | https://seed-design.io/llms/foundations/motion.txt |
| 컴포넌트 | https://seed-design.io/components/llms.txt |
| React 구현 | https://seed-design.io/react/llms.txt |

## 10. 이 문서의 한계

- 아이콘, 접근성(Inclusive Design), Voice and Tone·Writing, Patterns, Gradient는 수록하지 않았다.
- 컴포넌트 수치는 Action Button, Text Input, Chip, List Item, Checkbox, Tabs, Top Navigation, Dialog, Bottom Sheet만 수록했다. 나머지 컴포넌트는 `rootage/components/*.json`에서 조회해야 한다.
- semantic text style 매핑은 SEED 문서에 없어 비워 두었다.
- 값의 출처: 색상·dimension은 `daangn/seed-design` 저장소 `packages/rootage/__generated__`(color.json 기준 2026-06-15 갱신), 컴포넌트는 `seed-design.io/rootage/components`.
- SEED MCP(`@seed-design/mcp`)를 연결하면 최신 값을 도구로 조회할 수 있다. 이 문서는 공개 문서 스냅샷이므로 SEED 업데이트 시 갱신이 필요하다.
