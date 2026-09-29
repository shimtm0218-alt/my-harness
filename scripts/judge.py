#!/usr/bin/env python3
"""G4(design.md 위반)·G5(story-service.md 금지 규칙 위반) 판정. 읽기 전용: 어떤 파일도 수정하지 않는다.

사용:  python3 scripts/judge.py work/<화면>/design/frames.json [--gate G4|G5|all] [--expect-directions N]
종료 코드: 0 통과 / 1 위반 있음 / 2 입력 오류(판정 불가)

허용 목록은 design.md에서 읽는다(복사본 없음). 입력 형식은 scripts/README-judge.md 참조.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
G5_SCREENS = {"my-assets", "asset-detail", "admin-review", "submission"}
PILL_TYPES = {"button", "toggle", "badge", "chip", "nav"}
CONFIRM_KEYWORDS = ("개인정보", "고객정보", "회사기밀", "저작권")
CONFIRM_FLOWS = {"asset-register", "sale-request"}
VISIBILITY_FLOWS = {"asset-register"}
SCREENS = {"home", "free-learning", "paid-library", "skill-library", "mission-detail",
           "submission", "my-learning", "my-assets", "asset-detail", "admin-review"}


class InputError(Exception):
    pass


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def load_rules(design_path):
    """design.md에서 허용 목록을 읽는다. 읽지 못하면 판정 불가."""
    s = design_path.read_text(encoding="utf-8")
    colors = {m.group(1): m.group(2).lower()
              for m in re.finditer(r"\(`\{colors\.([a-z0-9-]+)\}` — (#[0-9a-fA-F]{6})\)", s)}
    radius = {int(n) for n in re.findall(r"^\| `\{rounded\.[a-z]+\}`\s*\|\s*(\d+)px", s, re.M)}
    spacing = {int(n) for n in re.findall(r"`\{spacing\.[a-z-]+\}` (\d+)px", s)}
    weights = {int(n) for n in re.findall(r"(?:Light|Regular|SemiBold|Bold) (\d{3})", s)}
    overlay = re.search(r"badge-overlay`\*\* — translucent gray pill \((rgba\([^)]*\))\)", s)
    rules = {
        "colors": colors,
        "hex": set(colors.values()),
        "accent": colors.get("accent"),
        "radius": radius,
        "spacing": spacing,
        "weights": weights,
        "family": "pretendard",
        "overlay": overlay.group(1).replace(" ", "").lower() if overlay else None,
    }
    for key in ("hex", "accent", "radius", "spacing", "weights", "overlay"):
        if not rules[key]:
            raise InputError(f"design.md에서 '{key}' 규칙을 읽지 못했다")
    return rules


def load_frames(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise InputError(f"파일이 없다: {path}")
    except json.JSONDecodeError as e:
        raise InputError(f"JSON이 아니다: {e}")
    if not isinstance(data, dict) or data.get("screen") not in SCREENS:
        raise InputError(f"screen은 {sorted(SCREENS)} 중 하나여야 한다")
    frames = data.get("frames")
    if not isinstance(frames, list) or not frames:
        raise InputError("frames가 비어 있다")
    for i, f in enumerate(frames):
        for k in ("id", "direction", "viewer_role", "nodes"):
            if k not in f:
                raise InputError(f"frames[{i}]에 '{k}'가 없다")
        if not isinstance(f["nodes"], list):
            raise InputError(f"frames[{i}].nodes가 목록이 아니다")
        for j, n in enumerate(f["nodes"]):
            if "id" not in n or "type" not in n:
                raise InputError(f"frames[{i}].nodes[{j}]에 id 또는 type이 없다")
    return data


def norm_color(c):
    return str(c).strip().lower().replace(" ", "")


def colors_of(node):
    out = []
    for field in ("fills", "strokes", "textColor"):
        out += [norm_color(c) for c in as_list(node.get(field))]
    return out


def norm_radius(v):
    return 9999 if v == "full" else v


# ---------------------------------------------------------------- G4
def judge_g4(data, rules, expect_directions):
    v = []

    def add(check, frame, node, msg):
        v.append({"gate": "G4", "check": check, "frame": frame, "node": node, "msg": msg})

    directions = {f["direction"] for f in data["frames"]}
    if len(directions) != expect_directions:
        add("frames", "-", "-", f"시안 방향이 {len(directions)}개다 (기대 {expect_directions}개)")

    for f in data["frames"]:
        fid = f["id"]
        accent_nodes = 0
        segmented_shadow = 0
        for n in f["nodes"]:
            nid, role, ntype = n["id"], n.get("role"), n["type"]
            cs = colors_of(n)

            # 색
            for c in cs:
                if c in rules["hex"]:
                    continue
                if role == "badge-overlay" and c == rules["overlay"]:
                    continue
                add("color", fid, nid, f"허용 밖 색 {c}")

            # 액센트
            if rules["accent"] in cs:
                accent_nodes += 1
                if ntype == "button":
                    add("accent", fid, nid, "액센트를 CTA(버튼)에 사용")

            # radius
            rs = [norm_radius(r) for r in as_list(n.get("radius"))]
            for r in rs:
                if role == "app-icon-squircle" and r == "30%":
                    continue
                if isinstance(r, bool) or not isinstance(r, (int, float)) or r not in rules["radius"]:
                    add("radius", fid, nid, f"허용 밖 radius {r}")

            # pill
            if ntype in PILL_TYPES:
                if not rs or not all(r == 9999 for r in rs):
                    add("pill", fid, nid, f"{ntype}이(가) pill(9999)이 아님: {rs or 'radius 없음'}")

            # spacing (간격이 없는 0은 제외)
            for field in ("padding", "gap", "margin"):
                for val in as_list(n.get(field)):
                    if isinstance(val, bool) or not isinstance(val, (int, float)):
                        add("spacing", fid, nid, f"{field}이(가) 숫자가 아님: {val}")
                    elif val != 0 and val not in rules["spacing"]:
                        add("spacing", fid, nid, f"허용 밖 {field} {val}")

            # 폰트
            font = n.get("font")
            if font:
                family = str(font.get("family", "")).lower()
                if not family.startswith(rules["family"]):
                    add("font", fid, nid, f"허용 밖 폰트 {font.get('family')}")
                if "weight" in font and font["weight"] not in rules["weights"]:
                    add("font", fid, nid, f"허용 밖 weight {font['weight']}")

            # 그림자
            if n.get("shadow"):
                if role == "segmented-control-active":
                    segmented_shadow += 1
                else:
                    add("shadow", fid, nid, "drop shadow 사용")

        if accent_nodes > 2:
            add("accent", fid, "-", f"액센트 사용 요소가 {accent_nodes}개다 (최대 2개)")
        if segmented_shadow > 1:
            add("shadow", fid, "-", f"segmented control 그림자 예외가 {segmented_shadow}곳이다 (최대 1곳)")
    return v


# ---------------------------------------------------------------- G5
def judge_g5(data):
    """(위반 목록, 메모 목록). 적용 화면이 아니면 (None, 메모)."""
    if data["screen"] not in G5_SCREENS:
        return None, [f"{data['screen']}은(는) G5 적용 화면이 아님 → 해당 없음"]

    v, notes = [], []

    def add(check, frame, node, msg):
        v.append({"gate": "G5", "check": check, "frame": frame, "node": node, "msg": msg})

    checked = 0
    for f in data["frames"]:
        fid, nodes = f["id"], f["nodes"]
        flow = f.get("flow")

        # 금지 규칙 1: 자산 등록·판매 신청 화면에 개인정보·기밀·저작권 확인 항목
        if flow in CONFIRM_FLOWS:
            checked += 1
            text = " ".join(str(n.get("text", "")) for n in nodes if n.get("role") == "confirm-item")
            missing = [k for k in CONFIRM_KEYWORDS if k not in text]
            if missing:
                add("confirm", fid, "-", f"확인 항목에 없음: {', '.join(missing)}")

        # 금지 규칙 2: 공개 범위 기본값은 비공개
        if flow in VISIBILITY_FLOWS:
            groups = [n for n in nodes if n.get("group") == "visibility"]
            if not groups:
                add("visibility", fid, "-", "공개 범위 선택이 없다")
            for g in groups:
                if g.get("default") != "비공개":
                    add("visibility", fid, g["id"], f"공개 범위 기본값이 '{g.get('default')}'이다 (비공개여야 함)")

        # 금지 규칙 2: 판매 신청 옵션은 판매 승인 회원 화면에만
        for n in nodes:
            is_option = n.get("role") == "sale-request-option" or (
                n["type"] == "option" and "판매 신청" in str(n.get("text", "")))
            if is_option and f["viewer_role"] != "seller":
                add("sale-option", fid, n["id"], f"판매 신청 옵션이 {f['viewer_role']} 화면에 보인다")

    if checked == 0:
        notes.append("경고: flow가 asset-register/sale-request인 프레임이 0개라 금지 규칙 1·2를 검사하지 못했다")
    return v, notes


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("frames", help="work/<화면>/design/frames.json")
    ap.add_argument("--gate", choices=["G4", "G5", "all"], default="all")
    ap.add_argument("--expect-directions", type=int, default=3, help="S4=3(기본), S5 최종 화면=1")
    ap.add_argument("--design", default=str(ROOT / "design.md"))
    args = ap.parse_args(argv)

    try:
        rules = load_rules(Path(args.design))
        data = load_frames(args.frames)
    except InputError as e:
        print(f"입력 오류(판정 불가): {e}")
        return 2

    violations, lines = [], []
    if args.gate in ("G4", "all"):
        g4 = judge_g4(data, rules, args.expect_directions)
        violations += g4
        lines.append(f"G4 design.md 위반: {len(g4)}건 → {'통과' if not g4 else '실패'}")
    if args.gate in ("G5", "all"):
        g5, notes = judge_g5(data)
        if g5 is None:
            lines.append("G5 금지 규칙 위반: 해당 없음 → 통과")
        else:
            violations += g5
            lines.append(f"G5 금지 규칙 위반: {len(g5)}건 → {'통과' if not g5 else '실패'}")
        lines += [f"  · {n}" for n in notes]

    for x in violations:
        print(f"FAIL {x['gate']}.{x['check']} frame={x['frame']} node={x['node']}: {x['msg']}")
    print(f"화면 {data['screen']}, 프레임 {len(data['frames'])}개")
    print("\n".join(lines))
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
