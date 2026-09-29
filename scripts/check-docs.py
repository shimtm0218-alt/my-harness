#!/usr/bin/env python3
"""하네스 문서끼리 서로 맞는지 세는 검사. 실패가 있으면 종료 코드 1."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ["prd.md", "design.md", "story-service.md", "story-work.md", "harness-goal.md",
        "pipeline.md", "artifacts.md", "gates.md", "roles.md", "CLAUDE.md", "verification.md"]
SCREENS = ["home", "free-learning", "paid-library", "skill-library", "mission-detail",
           "submission", "my-learning", "my-assets", "asset-detail", "admin-review"]

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def read(name):
    p = ROOT / name
    return p.read_text(encoding="utf-8") if p.exists() else ""


# 1. 문서가 모두 있다
missing = [d for d in DOCS if not (ROOT / d).exists()]
check("문서 11개가 모두 있다", not missing, f"없음: {missing}" if missing else "")

design, gates, artifacts, roles = read("design.md"), read("gates.md"), read("artifacts.md"), read("roles.md")
pipeline, claude, service = read("pipeline.md"), read("CLAUDE.md"), read("story-service.md")

# 2. design.md가 참조하는 토큰은 전부 정의돼 있다
used = set(re.findall(r"\{((?:colors|typography|spacing|rounded)\.[a-z0-9-]+)\}", design))
defined = set(re.findall(r"\(`\{(colors\.[a-z0-9-]+)\}` — #", design))
defined |= set(re.findall(r"^\| `\{(typography\.[a-z0-9-]+)\}`", design, re.M))
defined |= set(re.findall(r"`\{(spacing\.[a-z0-9-]+)\}` \d", design))
defined |= set(re.findall(r"^\| `\{(rounded\.[a-z0-9-]+)\}`", design, re.M))
undefined = sorted(used - defined)
check("design.md: 정의 없는 토큰이 0개", not undefined, f"{undefined}" if undefined else "")

# 3. gates.md의 허용 hex == design.md에 정의된 색
design_hex = {h.lower() for h in re.findall(r"\(`\{colors\.[a-z0-9-]+\}` — (#[0-9a-fA-F]{6})\)", design)}
gate_line = next((l for l in gates.splitlines() if l.startswith("| 색 |")), "")
gate_hex = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}", gate_line)}
diff = sorted(design_hex ^ gate_hex)
check("gates.md 허용 색 == design.md 정의 색", design_hex == gate_hex and bool(gate_hex), f"차이: {diff}" if diff else "")

# 4. gates.md의 radius·spacing 허용 목록이 design.md와 같다
radius_design = set(re.findall(r"^\| `\{rounded\.[a-z]+\}`\s*\|\s*(\d+)px", design, re.M))
radius_design |= {"9999"} if "9999px" in design else set()
radius_gate_line = next((l for l in gates.splitlines() if l.startswith("| radius |")), "")
radius_gate = set(re.findall(r"\b(0|16|24|9999)\b", radius_gate_line))
check("radius 허용 {0,16,24,9999}이 design.md와 같다",
      {"0", "16", "24", "9999"} == radius_gate and {"0", "16", "24", "9999"} <= (radius_design | {"0"}),
      f"design={sorted(radius_design)} gates={sorted(radius_gate)}")

spacing_design = {int(n) for n in re.findall(r"`\{spacing\.[a-z-]+\}` (\d+)px", design)}
spacing_gate_line = next((l for l in gates.splitlines() if l.startswith("| spacing |")), "")
spacing_gate = {int(n) for n in re.findall(r"\d+", spacing_gate_line.split("|")[2])}
check("spacing 허용 목록이 design.md와 같다", spacing_design == spacing_gate,
      f"design={sorted(spacing_design)} gates={sorted(spacing_gate)}")

# 5. 게이트 6개, 단계 5개, 금지 규칙 2개
gate_ids = set(re.findall(r"^\| (G\d) ", gates, re.M))
check("gates.md: 게이트 G1~G6", gate_ids == {f"G{i}" for i in range(1, 7)}, f"{sorted(gate_ids)}")
stage_ids = set(re.findall(r"^\| (S\d) ", pipeline, re.M))
check("pipeline.md: 단계 S1~S5", stage_ids == {f"S{i}" for i in range(1, 6)}, f"{sorted(stage_ids)}")
rules = re.findall(r"^\d+\. ", service.split("## 이 서비스에서 어기면 안 되는 것")[-1], re.M)
check("story-service.md: 어기면 안 되는 것 1~2개", 1 <= len(rules) <= 2, f"{len(rules)}개")
check("G5가 금지 규칙 1과 2를 모두 참조한다", "금지 규칙 1" in gates and "금지 규칙 2" in gates)

# 6. 화면 이름 10개가 artifacts.md와 roles.md에서 같다
art_missing = [s for s in SCREENS if s not in artifacts]
role_missing = [s for s in SCREENS if s not in roles]
check("화면 폴더 10개가 artifacts.md와 roles.md에 모두 있다", not art_missing and not role_missing,
      f"artifacts 없음={art_missing} roles 없음={role_missing}")

# 7. 산출물 파일 7개가 artifacts.md에 있고, 담당 에이전트 폴더와 roles.md가 맞는다
files = ["research/01-scope.md", "research/02-research.md", "research/03-directions.md",
         "design/04-figma.md", "design/frames.json", "review/05-review.md", "review/05-final.md",
         "review/05-dev-guide.md", "review/frames.json"]
check("artifacts.md에 단계 파일 9개", all(f in artifacts for f in files),
      f"없음: {[f for f in files if f not in artifacts]}")
folders_ok = all(f"work/<화면>/{d}/" in roles for d in ("research", "design", "review"))
check("roles.md의 편집 폴더가 research/design/review", folders_ok)

# 8. CLAUDE.md가 참조하는 문서가 실제로 있다
refs = set(re.findall(r"\b([a-z-]+\.md)\b", claude)) - {"CLAUDE.md"}
missing_refs = sorted(r for r in refs if not (ROOT / r).exists())
check("CLAUDE.md가 참조하는 md가 모두 존재", not missing_refs, f"없음: {missing_refs}" if missing_refs else "")

# 9. 예전 이름·낡은 문장이 남아 있지 않다
stale = [d for d in DOCS if "workflow-service" in read(d)]
check("옛 파일명 workflow-service가 남아 있지 않다", not stale, f"{stale}" if stale else "")
stale2 = [d for d in DOCS if "R5에서 정한다" in read(d)]
check("'R5에서 정한다' 같은 미결 문장이 남아 있지 않다", not stale2, f"{stale2}" if stale2 else "")

# 결과
fails = 0
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail and not ok else ""))
    fails += 0 if ok else 1
print(f"\n{len(results) - fails}/{len(results)} 통과")
sys.exit(1 if fails else 0)
