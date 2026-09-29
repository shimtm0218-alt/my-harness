#!/usr/bin/env python3
"""judge_md.py(G1·G2·G3·G6)가 위반을 실제로 잡는지 확인한다. 통과 샘플을 하나씩 망가뜨려 본다."""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JUDGE = ROOT / "scripts" / "judge_md.py"

BASE = """# 01-scope — home
## 유지할 콘텐츠·정책
| 항목 | PRD 근거 | 근거 유형 |
| --- | --- | --- |
| 무료/유료 표시가 있다 | 6-1 | 직접 |
| 홈에도 무료/유료 표시를 둔다 | 6-1 | 해석 |
| 홈은 학습 흐름의 시작점이다 | 질문 1 답변(가정) | 가정 |
## 변경 가능한 영역
| 항목 | PRD 근거 | 근거 유형 |
| --- | --- | --- |
| 섹션 배치와 순서 | 5절 | 해석 |
## 질문 목록 (하이서에게)
| # | 질문 | 왜 필요한가 (PRD 근거) | 답변 |
| --- | --- | --- | --- |
| 1 | 홈의 목적은? | 16절 | 기본값(가정, 하이서 미확인): 학습 흐름의 시작점 |
| 2 | 운영자 홈은? | 16절 | 하이서: 범위 밖 |
## 남은 모호함 (질문이 아닌 가정)
- 없음
"""


def run(text, gate="G1"):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "doc.md"
        p.write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, str(JUDGE), gate, str(p)], capture_output=True, text=True)
    return r.returncode, r.stdout


ROWS = "".join(f"| {i} | 서비스{i} | https://example.com/{i} | 관찰{i} | {'가능' if i % 2 else '불가'} | 이유{i} |\n" for i in range(1, 6))
G2_BASE = f"""# 02-research — home
## 사례
| # | 사례 | 출처 URL | 관찰한 것 | 적용 | 이유 (1줄) |
| --- | --- | --- | --- | --- | --- |
{ROWS}
## 패턴·전략 분류
| 패턴 | 해당 사례 # | 전략 한 문장 |
| --- | --- | --- |
| 이어서 하기 | 1, 2 | 최근 학습을 맨 위에 둔다 |
| 잠금 미리보기 | 3 | 잠긴 콘텐츠도 보이게 한다 |
| 카테고리 진입 | 4, 5 | 주제별로 들어가게 한다 |
## 확인하지 못한 사례
- 없음
"""

G3_BASE = """# 03-directions — home
## 방향 1: 이어서 학습
- UX 전략: 진행 중인 학습을 홈 맨 위에 둔다.
- 정보 우선순위:
  1. 현재 미션·제출 상태
  2. 최근 본 자료
  3. 카테고리
- 근거: 02-research 사례 1
## 방향 2: 탐색 우선
- UX 전략: 카테고리와 무료 콘텐츠로 먼저 둘러보게 한다.
- 정보 우선순위:
  1. 카테고리 진입
  2. 무료 콘텐츠
  3. 현재 미션
- 근거: 02-research 사례 2
## 방향 3: 전환 우선
- UX 전략: 잠긴 유료 콘텐츠 미리보기로 전환을 유도한다.
- 정보 우선순위:
  1. 유료 전환 CTA
  2. 잠금 미리보기
  3. 카테고리
- 근거: 02-research 사례 3
"""


REVIEW = """# 05-review — home
## 방향별 장점·리스크·선택 근거
| 방향 | 장점 | 리스크 | 선택 근거 |
| --- | --- | --- | --- |
| 1 | a | b | c |
## 검토 의견
검토 의견 수: 2
| # | 검토자 | 의견 | 반영 여부 | 사유 |
| --- | --- | --- | --- | --- |
| 1 | 하이서 | 미션을 더 크게 | 반영 | 카드 확대 |
| 2 | 개발자 | 애니메이션 추가 | 미반영 | MVP 범위 밖 |
## 최종 방향
최종 방향: 방향 1
"""
FINAL = "# 05-final — home\n최종 화면 Figma 프레임: 2:2\n방향: 1\n"
GUIDE = "".join(f"## {n}\n내용\n" for n in ("화면 구조", "컴포넌트와 토큰", "상태", "PRD 근거", "미확정 사항"))
FRAMES = '{"screen": "home", "frames": [{"id": "2:2", "direction": 1, "viewer_role": "free", "nodes": []}]}'


def run_g6(review=REVIEW, final=FINAL, guide=GUIDE, frames=FRAMES, skip=()):
    with tempfile.TemporaryDirectory() as d:
        for name, text in (("05-review.md", review), ("05-final.md", final), ("05-dev-guide.md", guide), ("frames.json", frames)):
            if name not in skip:
                (Path(d) / name).write_text(text, encoding="utf-8")
        r = subprocess.run([sys.executable, str(JUDGE), "G6", d], capture_output=True, text=True)
    return r.returncode, r.stdout


g6_cases = [
    ("G6 통과 샘플은 통과", {}, 0, "위반 0건"),
    ("G6 파일이 없음", {"skip": ("05-final.md",)}, 1, "G6.파일"),
    ("G6 최종 방향 줄이 없음", {"review": REVIEW.replace("최종 방향: 방향 1\n", "")}, 1, "G6.최종방향"),
    ("G6 최종 방향이 2개", {"review": REVIEW + "최종 방향: 방향 2\n"}, 1, "G6.최종방향"),
    ("G6 final의 방향이 다름", {"final": FINAL.replace("방향: 1", "방향: 2")}, 1, "G6.최종방향"),
    ("G6 프레임 ID가 2개", {"final": FINAL + "대안: 2:57\n"}, 1, "G6.최종화면"),
    ("G6 frames.json의 프레임이 final과 다름", {"frames": FRAMES.replace("2:2", "9:9")}, 1, "G6.최종화면"),
    ("G6 frames.json에 프레임이 2개", {"frames": FRAMES.replace("}]}", '}, {"id": "2:57", "direction": 2, "viewer_role": "free", "nodes": []}]}')}, 1, "G6.최종화면"),
    ("G6 검토 의견 수와 행 수가 다름", {"review": REVIEW.replace("검토 의견 수: 2", "검토 의견 수: 3")}, 1, "G6.의견"),
    ("G6 반영 여부가 애매함", {"review": REVIEW.replace("| 반영 | 카드 확대 |", "| 검토중 | 카드 확대 |")}, 1, "G6.의견"),
    ("G6 미반영인데 사유가 없음", {"review": REVIEW.replace("| 미반영 | MVP 범위 밖 |", "| 미반영 |  |")}, 1, "G6.의견"),
    ("G6 의견 0개는 사유가 있으면 통과(주의 표시)",
     {"review": REVIEW[:REVIEW.index("검토 의견 수")] + "검토 의견 수: 0\n사유: 시범 실행이라 검토자가 없었다\n## 최종 방향\n최종 방향: 방향 1\n"}, 0, "주의"),
    ("G6 의견 0개인데 사유가 없음",
     {"review": REVIEW[:REVIEW.index("검토 의견 수")] + "검토 의견 수: 0\n## 최종 방향\n최종 방향: 방향 1\n"}, 1, "G6.의견"),
    ("G6 개발 가이드 섹션이 비어 있음", {"guide": GUIDE.replace("## 상태\n내용\n", "## 상태\n")}, 1, "G6.개발가이드"),
    ("G6 개발 가이드 섹션이 없음", {"guide": GUIDE.replace("## PRD 근거\n내용\n", "")}, 1, "G6.개발가이드"),
]


cases = [
    ("통과 샘플은 통과", BASE, 0, "위반 0건"),
    ("답변이 (미답변)", BASE.replace("하이서: 범위 밖", "(미답변)"), 1, "G1.답변"),
    ("답변이 비어 있음", BASE.replace("하이서: 범위 밖", ""), 1, "G1.답변"),
    ("직접 항목에 PRD 절 번호 없음", BASE.replace("| 6-1 | 직접 |", "| 없음 | 직접 |"), 1, "G1.근거"),
    ("해석 항목에 PRD 절 번호 없음", BASE.replace("| 5절 | 해석 |", "| 그냥 | 해석 |"), 1, "G1.근거"),
    ("가정 항목에 질문 번호 없음", BASE.replace("질문 1 답변(가정)", "가정임"), 1, "G1.근거"),
    ("가정 항목이 없는 질문을 근거로 듦", BASE.replace("질문 1 답변(가정)", "질문 9 답변(가정)"), 1, "G1.근거"),
    ("가정 항목이 답이 빈 질문을 근거로 듦",
     BASE.replace("하이서: 범위 밖", "(미답변)").replace("질문 1 답변(가정)", "질문 2 답변(가정)"), 1, "G1.근거"),
    ("근거 유형이 이상함", BASE.replace("| 6-1 | 직접 |", "| 6-1 | 확실 |"), 1, "G1.근거유형"),
    ("유지 항목이 0개",
     BASE.replace("| 무료/유료 표시가 있다 | 6-1 | 직접 |\n", "").replace("| 홈에도 무료/유료 표시를 둔다 | 6-1 | 해석 |\n", "")
         .replace("| 홈은 학습 흐름의 시작점이다 | 질문 1 답변(가정) | 가정 |\n", ""), 1, "G1.유지"),
    ("변경 항목이 0개", BASE.replace("| 섹션 배치와 순서 | 5절 | 해석 |\n", ""), 1, "G1.변경"),
    ("근거 유형 열이 없는 옛 형식은 판정 불가", BASE.replace(" | 근거 유형 |", " |").replace(" | 직접 |", " |").replace(" | 해석 |", " |").replace(" | 가정 |", " |")
        .replace("| --- | --- | --- |\n| 무료", "| --- | --- |\n| 무료"), 2, "입력 오류"),
    ("질문 목록 섹션이 없음", BASE[:BASE.index("## 질문 목록")], 2, "입력 오류"),
]

cases = [(n, t, c, e, "G1") for n, t, c, e in cases]
cases += [
    ("G2 통과 샘플은 통과", G2_BASE, 0, "위반 0건", "G2"),
    ("G2 사례가 4개", G2_BASE.replace("| 5 | 서비스5 | https://example.com/5 | 관찰5 | 가능 | 이유5 |\n", ""), 1, "G2.사례수", "G2"),
    ("G2 출처 URL 없음", G2_BASE.replace("https://example.com/2", "기억"), 1, "G2.출처", "G2"),
    ("G2 적용이 애매함", G2_BASE.replace("| 불가 | 이유2 |", "| 아마 | 이유2 |"), 1, "G2.적용", "G2"),
    ("G2 이유가 비어 있음", G2_BASE.replace("| 불가 | 이유2 |", "| 불가 |  |"), 1, "G2.이유", "G2"),
    ("G2 패턴이 2개", G2_BASE.replace("| 카테고리 진입 | 4, 5 | 주제별로 들어가게 한다 |\n", ""), 1, "G2.패턴수", "G2"),
    ("G2 사례 섹션 없음", G2_BASE.replace("## 사례", "## 다른 것"), 2, "입력 오류", "G2"),
    ("G3 통과 샘플은 통과", G3_BASE, 0, "위반 0건", "G3"),
    ("G3 방향이 2개", G3_BASE[:G3_BASE.index("## 방향 3")], 1, "G3.방향수", "G3"),
    ("G3 방향이 4개", G3_BASE + "## 방향 4: 추가\n- UX 전략: 하나 더.\n- 정보 우선순위:\n  1. 알림\n", 1, "G3.방향수", "G3"),
    ("G3 UX 전략 없음", G3_BASE.replace("- UX 전략: 진행 중인 학습을 홈 맨 위에 둔다.\n", ""), 1, "G3.전략", "G3"),
    ("G3 UX 전략이 두 문장", G3_BASE.replace("맨 위에 둔다.", "맨 위에 둔다. 그리고 알린다."), 1, "G3.전략", "G3"),
    ("G3 정보 우선순위 없음", G3_BASE.replace("  1. 현재 미션·제출 상태\n  2. 최근 본 자료\n  3. 카테고리\n", ""), 1, "G3.우선순위", "G3"),
    ("G3 1순위가 같음", G3_BASE.replace("1. 카테고리 진입", "1. 현재 미션·제출 상태"), 1, "G3.1순위중복", "G3"),
    ("G3 1순위가 표기만 다르면 같은 것으로 본다", G3_BASE.replace("1. 카테고리 진입", "1. 현재 미션 · 제출 상태."), 1, "G3.1순위중복", "G3"),
]

fails = 0
for name, text, code, expect, gate in cases:
    rc, out = run(text, gate)
    ok = rc == code and expect in out
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  (종료 코드 {rc}, 기대 {code}, 기대 문자열 {expect!r})\n{out}"))
    fails += 0 if ok else 1
total = len(cases)
for name, kwargs, code, expect in g6_cases:
    rc, out = run_g6(**kwargs)
    ok = rc == code and expect in out
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  (종료 코드 {rc}, 기대 {code}, 기대 문자열 {expect!r})\n{out}"))
    fails += 0 if ok else 1
    total += 1
print(f"\n{total - fails}/{total} 통과")
sys.exit(1 if fails else 0)
