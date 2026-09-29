#!/usr/bin/env python3
"""judge.py가 위반을 실제로 잡는지 확인한다. 통과 샘플을 하나씩 망가뜨려 기대한 검사가 실패하는지 본다."""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JUDGE = ROOT / "scripts" / "judge.py"
BASE = json.loads((ROOT / "tests" / "fixtures" / "pass-my-assets.json").read_text(encoding="utf-8"))


def run(data, extra=()):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "frames.json"
        p.write_text(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, str(JUDGE), str(p), *extra], capture_output=True, text=True)
    return r.returncode, r.stdout


def node(d, frame_idx, suffix):
    return next(n for n in d["frames"][frame_idx]["nodes"] if n["id"].endswith(suffix))


def mutate(fn):
    d = copy.deepcopy(BASE)
    fn(d)
    return d


cases = []  # (이름, 입력, 추가 인자, 기대 종료 코드, 출력에 있어야 하는 문자열)


def case(name, data, code, expect=None, extra=()):
    cases.append((name, data, extra, code, expect))


case("통과 샘플은 통과", BASE, 0)

# G4
case("허용 밖 색 #ff0000", mutate(lambda d: node(d, 0, "-card")["fills"].append("#ff0000")), 1, "G4.color")
case("badge-overlay의 rgba는 허용",
     mutate(lambda d: d["frames"][0]["nodes"].append(
         {"id": "ov", "type": "badge", "role": "badge-overlay", "fills": ["rgba(115, 115, 115, 0.56)"], "radius": "full"})), 0)
case("badge-overlay 아닌데 rgba", mutate(lambda d: node(d, 0, "-card")["fills"].append("rgba(115,115,115,0.56)")), 1, "G4.color")
case("액센트를 버튼에 사용", mutate(lambda d: node(d, 0, "-cta").update({"fills": ["#0066ff"]})), 1, "G4.accent")
case("액센트 요소 3개", mutate(lambda d: d["frames"][0]["nodes"].extend(
    [{"id": f"b{i}", "type": "badge", "fills": ["#0066ff"], "radius": "full"} for i in range(2)])), 1, "최대 2개")
case("허용 밖 radius 10", mutate(lambda d: node(d, 0, "-card").update({"radius": 10})), 1, "G4.radius")
case("app-icon-squircle 30%는 허용",
     mutate(lambda d: d["frames"][0]["nodes"].append({"id": "ic", "type": "image", "role": "app-icon-squircle", "radius": "30%"})), 0)
case("일반 노드의 30%는 위반", mutate(lambda d: node(d, 0, "-card").update({"radius": "30%"})), 1, "G4.radius")
case("버튼이 pill이 아님", mutate(lambda d: node(d, 0, "-cta").update({"radius": 16})), 1, "G4.pill")
case("버튼에 radius 없음", mutate(lambda d: node(d, 0, "-cta").pop("radius")), 1, "G4.pill")
case("허용 밖 padding 10", mutate(lambda d: node(d, 0, "-input").update({"padding": [10, 16]})), 1, "G4.spacing")
case("허용 밖 gap 20", mutate(lambda d: node(d, 0, "-card").update({"gap": 20})), 1, "G4.spacing")
case("0 간격은 검사 제외", mutate(lambda d: node(d, 0, "-card").update({"margin": 0})), 0)
case("Pretendard 밖 폰트", mutate(lambda d: node(d, 0, "-input").update({"font": {"family": "Arial", "weight": 400}})), 1, "G4.font")
case("허용 밖 weight 500", mutate(lambda d: node(d, 0, "-input").update({"font": {"family": "Pretendard", "weight": 500}})), 1, "G4.font")
case("그림자 사용", mutate(lambda d: node(d, 0, "-card").update({"shadow": True})), 1, "G4.shadow")
case("segmented 활성 그림자 1곳은 허용",
     mutate(lambda d: d["frames"][0]["nodes"].append({"id": "seg", "type": "toggle", "role": "segmented-control-active",
                                                       "shadow": True, "radius": "full"})), 0)
case("segmented 활성 그림자 2곳은 위반",
     mutate(lambda d: d["frames"][0]["nodes"].extend(
         [{"id": f"seg{i}", "type": "toggle", "role": "segmented-control-active", "shadow": True, "radius": "full"}
          for i in range(2)])), 1, "G4.shadow")
case("방향이 2개뿐", mutate(lambda d: d.update({"frames": d["frames"][:2]})), 1, "G4.frames")
case("S5는 방향 1개를 기대",
     mutate(lambda d: d.update({"frames": d["frames"][:1]})), 0, None, ("--expect-directions", "1"))

# G5
case("확인 항목에 저작권 없음",
     mutate(lambda d: node(d, 0, "-c2").update({"text": "회사기밀이 포함되어 있지 않습니다"})), 1, "G5.confirm")
case("확인 항목이 아예 없음",
     mutate(lambda d: d["frames"][0].update({"nodes": [n for n in d["frames"][0]["nodes"] if n.get("role") != "confirm-item"]})),
     1, "G5.confirm")
case("공개 범위 기본값이 멤버 공개", mutate(lambda d: node(d, 0, "-vis").update({"default": "멤버 공개"})), 1, "G5.visibility")
case("공개 범위 선택이 없음",
     mutate(lambda d: d["frames"][0].update({"nodes": [n for n in d["frames"][0]["nodes"] if n.get("group") != "visibility"]})),
     1, "G5.visibility")
case("paid 화면에 판매 신청 옵션", mutate(lambda d: d["frames"][0].update({"viewer_role": "paid"})), 1, "G5.sale-option")
case("role 태그 없이 텍스트로 노출된 판매 신청 옵션",
     mutate(lambda d: (d["frames"][0].update({"viewer_role": "paid"}), node(d, 0, "-sale").pop("role"))), 1, "G5.sale-option")
case("G5 적용 화면이 아니면 해당 없음",
     mutate(lambda d: (d.update({"screen": "home"}), node(d, 0, "-vis").update({"default": "공개"}))), 0, "해당 없음")
case("G5 대상 프레임이 0개면 경고",
     mutate(lambda d: [f.pop("flow") for f in d["frames"]]), 0, "경고")

# 입력 오류는 통과로 치지 않는다
case("JSON이 아님", "이건 json이 아님", 2, "입력 오류")
case("screen이 잘못됨", mutate(lambda d: d.update({"screen": "nowhere"})), 2, "입력 오류")
case("frames가 비어 있음", mutate(lambda d: d.update({"frames": []})), 2, "입력 오류")

fails = 0
for name, data, extra, code, expect in cases:
    rc, out = run(data, extra)
    ok = rc == code and (expect is None or expect in out)
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  (종료 코드 {rc}, 기대 {code}, 기대 문자열 {expect!r})\n{out}"))
    fails += 0 if ok else 1
print(f"\n{len(cases) - fails}/{len(cases)} 통과")
sys.exit(1 if fails else 0)
