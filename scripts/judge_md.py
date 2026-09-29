#!/usr/bin/env python3
"""마크다운 산출물의 게이트 판정. 읽기 전용: 어떤 파일도 수정하지 않는다.

사용:  python3 scripts/judge_md.py G1 work/<화면>/research/01-scope.md
사용:  python3 scripts/judge_md.py G2 work/<화면>/research/02-research.md
       python3 scripts/judge_md.py G3 work/<화면>/research/03-directions.md
       python3 scripts/judge_md.py G6 work/<화면>/review
현재 지원: G1, G2, G3, G6.
종료 코드: 0 통과 / 1 위반 있음 / 2 입력 오류(판정 불가)

G1 (gates.md): 유지 ≥1, 변경 ≥1, 근거 없는 항목 0, 질문 목록에서 답변이 빈 것 0.
근거 = 직접·해석 항목은 PRD 절 번호, 가정 항목은 질문 목록에 실제로 있고 답이 채워진 질문 번호.
참고 집계(조건 아님): 근거 유형(직접/해석/가정)별 개수, 가정으로 채운 답변 수.
"""
import json
import re
import sys
from pathlib import Path

PRD_REF = re.compile(r"(\d+-\d+|\d+절)")
KINDS = ("직접", "해석", "가정")
EMPTY_ANSWERS = {"", "(미답변)", "미답변", "-", "(없음)"}


class InputError(Exception):
    pass


def sections(text):
    """'## 제목' 기준으로 나눈 {제목: 본문}."""
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def table(body):
    """첫 표의 (헤더, 행 목록). 표가 없으면 ([], [])."""
    rows = []
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return (rows[0], rows[1:]) if rows else ([], [])


def find_section(secs, prefix):
    for k, v in secs.items():
        if k.startswith(prefix):
            return v
    raise InputError(f"'## {prefix}...' 섹션이 없다")


def col(header, name):
    for i, h in enumerate(header):
        if name in h:
            return i
    raise InputError(f"표에 '{name}' 열이 없다: {header}")


def judge_g1(path):
    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise InputError(f"파일이 없다: {path}")
    secs = sections(text)
    v, info = [], []

    def add(check, msg):
        v.append(f"FAIL G1.{check}: {msg}")

    # 질문 목록을 먼저 읽는다 (가정 항목의 근거가 실제 질문인지 확인하려면 필요하다)
    q_header, q_rows = table(find_section(secs, "질문 목록"))
    if not q_header:
        raise InputError("'질문 목록' 섹션에 표가 없다")
    c_num, c_ans = col(q_header, "#"), col(q_header, "답변")
    answered, assumed = set(), 0
    for r in q_rows:
        r = r + [""] * (len(q_header) - len(r))
        ans = r[c_ans].strip()
        if ans in EMPTY_ANSWERS:
            add("답변", f"질문 {r[c_num]}번의 답변이 비어 있다")
        else:
            answered.add(r[c_num].strip())
            if "가정" in ans:
                assumed += 1

    counts = {}
    kind_counts = {k: 0 for k in KINDS}
    for label, prefix in (("유지", "유지할 콘텐츠"), ("변경", "변경 가능한 영역")):
        header, rows = table(find_section(secs, prefix))
        if not header:
            raise InputError(f"'{prefix}' 섹션에 표가 없다")
        c_item, c_ref, c_kind = col(header, "항목"), col(header, "PRD 근거"), col(header, "근거 유형")
        counts[label] = len(rows)
        if len(rows) < 1:
            add(label, f"{label} 항목이 0개다 (1개 이상이어야 함)")
        for n, r in enumerate(rows, 1):
            r = r + [""] * (len(header) - len(r))
            kind = r[c_kind].strip("` ")
            name = r[c_item][:40]
            if kind not in KINDS:
                add("근거유형", f"{label} {n}번 항목의 근거 유형이 직접/해석/가정이 아니다: '{r[c_kind]}'")
                continue
            kind_counts[kind] += 1
            if kind == "가정":
                refs = re.findall(r"질문\s*(\d+)", r[c_ref])
                if not refs:
                    add("근거", f"{label} {n}번(가정) 항목에 질문 번호가 없다: {name}")
                elif not all(x in answered for x in refs):
                    add("근거", f"{label} {n}번(가정) 항목이 없거나 답이 비어 있는 질문을 근거로 든다: {name}")
            elif not PRD_REF.search(r[c_ref]):
                add("근거", f"{label} {n}번({kind}) 항목에 PRD 절 번호가 없다: {name}")

    info.append(f"유지 {counts['유지']}개, 변경 {counts['변경']}개, 질문 {len(q_rows)}개")
    info.append("근거 유형: " + ", ".join(f"{k} {n}" for k, n in kind_counts.items()))
    info.append(f"가정으로 채운 답변 {assumed}개 / 하이서가 확인한 답변 {len(answered) - assumed}개")
    return v, info


def read_doc(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise InputError(f"파일이 없다: {path}")


def judge_g2(path):
    """G2 (gates.md): 사례 ≥5, 모든 사례에 출처 URL과 '적용(가능/불가) + 이유', 패턴 분류 ≥3."""
    secs = sections(read_doc(path))
    v = []

    def add(check, msg):
        v.append(f"FAIL G2.{check}: {msg}")

    header, rows = table(find_section(secs, "사례"))
    if not header:
        raise InputError("'사례' 섹션에 표가 없다")
    c_case, c_url, c_apply, c_why = col(header, "사례"), col(header, "출처"), col(header, "적용"), col(header, "이유")
    if len(rows) < 5:
        add("사례수", f"사례가 {len(rows)}개다 (5개 이상이어야 함)")
    ok_n = no_n = 0
    for n, r in enumerate(rows, 1):
        r = r + [""] * (len(header) - len(r))
        name = r[c_case][:30]
        if not re.search(r"https?://", r[c_url]):
            add("출처", f"사례 {n}번({name})에 출처 URL이 없다")
        apply = r[c_apply].strip("` ")
        if apply not in ("가능", "불가"):
            add("적용", f"사례 {n}번({name})의 적용이 가능/불가가 아니다: '{r[c_apply]}'")
        else:
            ok_n += apply == "가능"
            no_n += apply == "불가"
        if not r[c_why].strip():
            add("이유", f"사례 {n}번({name})의 이유가 비어 있다")

    p_header, p_rows = table(find_section(secs, "패턴"))
    if not p_header:
        raise InputError("'패턴·전략 분류' 섹션에 표가 없다")
    if len(p_rows) < 3:
        add("패턴수", f"패턴 분류가 {len(p_rows)}개다 (3개 이상이어야 함)")
    info = [f"사례 {len(rows)}개 (적용 가능 {ok_n}, 불가 {no_n}), 패턴 {len(p_rows)}개"]
    return v, info


def _norm(text):
    return re.sub(r"[\s`*_.,:;!?()\[\]'\"·-]+", "", text).lower()


def judge_g3(path):
    """G3 (gates.md): 방향 정확히 3, 각 방향에 정보 우선순위 목록과 UX 전략 1문장, 세 방향의 1순위가 서로 다름."""
    text = read_doc(path)
    v = []

    def add(check, msg):
        v.append(f"FAIL G3.{check}: {msg}")

    parts = re.split(r"^## 방향 ?(\d+)[^\n]*$", text, flags=re.M)
    # parts = [앞부분, 번호1, 본문1, 번호2, 본문2, ...]
    dirs = [(parts[i], parts[i + 1]) for i in range(1, len(parts) - 1, 2)]
    if len(dirs) != 3:
        add("방향수", f"방향이 {len(dirs)}개다 (정확히 3개여야 함)")

    firsts = []
    for num, body in dirs:
        strat = re.search(r"^-\s*UX 전략\s*:\s*(.+)$", body, flags=re.M)
        if not strat or not strat.group(1).strip():
            add("전략", f"방향 {num}에 'UX 전략:' 한 줄이 없다")
        elif len(re.findall(r"[.!?。]\s|[.!?。]$", strat.group(1).strip())) > 1:
            add("전략", f"방향 {num}의 UX 전략이 한 문장이 아니다")
        m = re.search(r"정보 우선순위\s*:\s*\n((?:\s+\d+\.\s+.+\n?)+)", body)
        items = re.findall(r"^\s+\d+\.\s+(.+)$", m.group(1), flags=re.M) if m else []
        if not items:
            add("우선순위", f"방향 {num}에 '정보 우선순위:' 번호 목록이 없다")
        else:
            firsts.append((num, items[0].strip()))
    seen = {}
    for num, item in firsts:
        seen.setdefault(_norm(item), []).append(num)
    for key, nums in seen.items():
        if len(nums) > 1:
            add("1순위중복", f"방향 {', '.join(nums)}의 1순위가 같다")
    info = [f"방향 {len(dirs)}개, 1순위: " + " / ".join(f"방향{n}: {i[:24]}" for n, i in firsts)]
    return v, info


DEV_GUIDE_SECTIONS = ("화면 구조", "컴포넌트와 토큰", "상태", "PRD 근거", "미확정")


def judge_g6(path):
    """G6 (gates.md): 최종 화면 1, 개발 가이드 1, 최종 방향 선택 1, 검토 의견 각각에 반영/미반영+사유(빈 것 0).
    인자는 work/<화면>/review 폴더. G4·G5는 review/frames.json으로 judge.py가 따로 판정한다."""
    d = Path(path)
    v, info = [], []

    def add(check, msg):
        v.append(f"FAIL G6.{check}: {msg}")

    for name in ("05-review.md", "05-final.md", "05-dev-guide.md", "frames.json"):
        if not (d / name).exists():
            add("파일", f"{name}이(가) 없다")
    if v:
        return v, info
    review = (d / "05-review.md").read_text(encoding="utf-8")
    final = (d / "05-final.md").read_text(encoding="utf-8")
    guide = (d / "05-dev-guide.md").read_text(encoding="utf-8")

    # 최종 방향 선택 1
    picks = re.findall(r"^최종 방향\s*:\s*방향\s*(\d+)", review, flags=re.M)
    if len(picks) != 1:
        add("최종방향", f"'최종 방향: 방향 N' 줄이 {len(picks)}개다 (정확히 1개여야 함)")

    # 최종 화면 1
    ids = sorted(set(re.findall(r"\b\d+:\d+\b", final)))
    if len(ids) != 1:
        add("최종화면", f"05-final.md의 Figma 프레임 ID가 {len(ids)}개다 (정확히 1개여야 함): {ids}")
    fdir = re.search(r"^방향\s*:\s*(\d+)", final, flags=re.M)
    if picks and fdir and fdir.group(1) != picks[0]:
        add("최종방향", f"05-final.md의 방향({fdir.group(1)})이 05-review.md의 최종 방향({picks[0]})과 다르다")
    if not fdir:
        add("최종화면", "05-final.md에 '방향: N' 줄이 없다")

    # review/frames.json이 그 최종 화면 하나만 담는지
    try:
        frames = json.loads((d / "frames.json").read_text(encoding="utf-8")).get("frames", [])
    except json.JSONDecodeError:
        raise InputError("review/frames.json이 JSON이 아니다")
    if len(frames) != 1:
        add("최종화면", f"review/frames.json의 프레임이 {len(frames)}개다 (정확히 1개여야 함)")
    elif ids and frames[0].get("id") != ids[0]:
        add("최종화면", f"review/frames.json의 프레임({frames[0].get('id')})이 05-final.md의 프레임({ids[0]})과 다르다")

    # 검토 의견
    m = re.search(r"^검토 의견 수\s*:\s*(\d+)", review, flags=re.M)
    if not m:
        add("의견", "'검토 의견 수: N' 줄이 없다")
        n_declared = None
    else:
        n_declared = int(m.group(1))
    secs = sections(review)
    body = next((b for k, b in secs.items() if k.startswith("검토 의견")), "")
    header, rows = table(body)
    if n_declared is not None and len(rows) != n_declared:
        add("의견", f"검토 의견 수({n_declared})와 표의 행 수({len(rows)})가 다르다")
    if rows:
        c_reflect, c_reason = col(header, "반영"), col(header, "사유")
        for i, r in enumerate(rows, 1):
            r = r + [""] * (len(header) - len(r))
            status = r[c_reflect].strip("` ")
            if not re.match(r"^(반영|미반영)", status):
                add("의견", f"검토 의견 {i}번의 반영 여부가 반영/미반영이 아니다: '{r[c_reflect]}'")
            elif status.startswith("미반영") and not r[c_reason].strip():
                add("의견", f"검토 의견 {i}번이 미반영인데 사유가 비어 있다")
    elif n_declared == 0:
        if not re.search(r"^사유\s*:\s*\S+", body, flags=re.M):
            add("의견", "검토 의견이 0개인데 '사유:' 줄이 없다")
    review_human = n_declared

    # 개발 가이드 1
    gsecs = sections(guide)
    for name in DEV_GUIDE_SECTIONS:
        body_g = next((b for k, b in gsecs.items() if k.startswith(name)), None)
        if body_g is None or not body_g.strip():
            add("개발가이드", f"'## {name}' 섹션이 없거나 비어 있다")

    info.append(f"최종 방향 {picks[0] if picks else '?'}, 최종 프레임 {ids[0] if ids else '?'}, 검토 의견 {review_human}개")
    if review_human == 0:
        info.append("주의: 검토 의견이 0개다. 하이서·개발자의 검토가 실제로 없었다는 뜻이다 (조건은 충족하지만 사람 검토는 0회)")
    return v, info


GATES = {"G1": ("G1 범위", judge_g1), "G2": ("G2 사례", judge_g2), "G3": ("G3 전략", judge_g3), "G6": ("G6 완료", judge_g6)}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2 or argv[0] not in GATES:
        print(f"사용: python3 scripts/judge_md.py <{'|'.join(GATES)}> <파일>")
        return 2
    label, fn = GATES[argv[0]]
    try:
        violations, info = fn(argv[1])
    except InputError as e:
        print(f"입력 오류(판정 불가): {e}")
        return 2
    for x in violations:
        print(x)
    for line in info:
        print(f"  · {line}")
    print(f"{label}: 위반 {len(violations)}건 → {'통과' if not violations else '실패'}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
