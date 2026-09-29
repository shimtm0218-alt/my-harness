#!/usr/bin/env python3
"""쓰기 차단 훅(guard-path, guard-judge)과 state.py가 규칙대로 동작하는지 확인한다."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def hook(script, args, payload, raw=None):
    stdin = raw if raw is not None else json.dumps(payload, ensure_ascii=False)
    r = subprocess.run([PY, str(ROOT / "scripts" / script), *args], input=stdin, capture_output=True, text=True,
                       env={"CLAUDE_PROJECT_DIR": str(ROOT), "PATH": "/usr/bin:/bin"})
    return r.returncode


def write_to(path):
    return {"tool_name": "Write", "tool_input": {"file_path": str(path)}, "cwd": str(ROOT)}


# ---- guard-path
W = ROOT / "work"
check("research가 research/ 안에 쓰기 허용", hook("guard-path.py", ["research"], write_to(W / "home/research/01-scope.md")) == 0)
check("research가 attempt-1/ 안에 쓰기 허용", hook("guard-path.py", ["research"], write_to(W / "home/research/attempt-1/x.md")) == 0)
check("research가 design/ 에 쓰기 차단", hook("guard-path.py", ["research"], write_to(W / "home/design/04-figma.md")) == 2)
check("research가 다른 화면의 research/ 도 화면 이름이 맞으면 허용", hook("guard-path.py", ["research"], write_to(W / "my-assets/research/x.md")) == 0)
check("research가 없는 화면 폴더에 쓰기 차단", hook("guard-path.py", ["research"], write_to(W / "nowhere/research/x.md")) == 2)
check("research가 state.json에 쓰기 차단", hook("guard-path.py", ["research"], write_to(W / "home/state.json")) == 2)
check("research가 design.md에 쓰기 차단", hook("guard-path.py", ["research"], write_to(ROOT / "design.md")) == 2)
check("research가 scripts/에 쓰기 차단", hook("guard-path.py", ["research"], write_to(ROOT / "scripts/judge.py")) == 2)
check("designer가 design/ 안에 쓰기 허용", hook("guard-path.py", ["design"], write_to(W / "home/design/frames.json")) == 0)
check("designer가 research/ 에 쓰기 차단", hook("guard-path.py", ["design"], write_to(W / "home/research/01-scope.md")) == 2)
check("reviewer가 review/ 안에 쓰기 허용", hook("guard-path.py", ["review"], write_to(W / "home/review/05-final.md")) == 0)
check("reviewer가 design/ 에 쓰기 차단", hook("guard-path.py", ["review"], write_to(W / "home/design/frames.json")) == 2)
check("..로 우회 시도 차단", hook("guard-path.py", ["research"], write_to(W / "home/research/../design/04-figma.md")) == 2)
check("상대 경로도 판정한다(cwd 기준)",
      hook("guard-path.py", ["research"], {"tool_input": {"file_path": "work/home/research/01-scope.md"}, "cwd": str(ROOT)}) == 0)
check("상대 경로 우회도 차단",
      hook("guard-path.py", ["research"], {"tool_input": {"file_path": "work/home/design/x.md"}, "cwd": str(ROOT)}) == 2)
check("경로가 없으면 차단(fail closed)", hook("guard-path.py", ["research"], {"tool_input": {}}) == 2)
check("JSON이 아니면 차단(fail closed)", hook("guard-path.py", ["research"], None, raw="이건 json이 아님") == 2)
check("폴더 인자가 잘못되면 차단", hook("guard-path.py", ["hack"], write_to(W / "home/research/x.md")) == 2)

with tempfile.TemporaryDirectory() as d:
    (Path(d) / "work/home/research").mkdir(parents=True)
    (Path(d) / "work/home/design").mkdir(parents=True)
    link = Path(d) / "work/home/research/link"
    try:
        link.symlink_to(ROOT / "design.md")
        r = hook("guard-path.py", ["research"], write_to(link))
        check("research/ 안의 심볼릭 링크로 밖에 쓰는 것 차단", r == 2, f"종료 코드 {r}")
    except OSError:
        pass

# ---- guard-judge
def bash(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


check("judge가 judge.py 실행 허용", hook("guard-judge.py", [], bash("python3 scripts/judge.py work/home/design/frames.json")) == 0)
check("judge가 옵션 붙여 실행 허용",
      hook("guard-judge.py", [], bash("python3 scripts/judge.py work/home/review/frames.json --gate G4 --expect-directions 1")) == 0)
for label, cmd in [("rm", "rm -rf work"), ("리다이렉트", "python3 scripts/judge.py x.json > out.txt"),
                   ("명령 연결", "python3 scripts/judge.py x.json; rm -rf work"), ("파이프", "python3 scripts/judge.py x.json | tee y"),
                   ("명령 치환", "python3 scripts/judge.py $(rm x)"), ("다른 스크립트", "python3 scripts/state.py pass S1 --screen home"),
                   ("cat", "cat design.md"), ("빈 명령", "")]:
    check(f"judge의 {label} 차단", hook("guard-judge.py", [], bash(cmd)) == 2)

# ---- state.py
def st(*args, work):
    r = subprocess.run([PY, str(ROOT / "scripts/state.py"), *args, "--work-dir", work], capture_output=True, text=True)
    return r.returncode, r.stdout


with tempfile.TemporaryDirectory() as w:
    S = lambda *a: st(*a, "--screen", "home", work=w)
    check("init 성공", st("init", "home", work=w)[0] == 0)
    check("init 중복 거부", st("init", "home", work=w)[0] == 1)
    check("잘못된 화면 이름 거부", st("init", "nowhere", work=w)[0] == 1)
    check("S2를 S1 전에 시작하면 거부", S("start", "S2")[0] == 1)
    check("S1 시작", S("start", "S1")[0] == 0)
    check("S1을 running에서 다시 시작하면 거부", S("start", "S1")[0] == 1)
    check("S1 하이서 답변 대기", S("wait", "S1", "--for", "하이서 답변")[0] == 0)
    check("대기 중에는 S2 시작 거부", S("start", "S2")[0] == 1)
    check("S1 통과", S("pass", "S1")[0] == 0)
    check("S2 시작·통과", S("start", "S2")[0] == 0 and S("pass", "S2")[0] == 0)
    check("S3 시작·통과", S("start", "S3")[0] == 0 and S("pass", "S3")[0] == 0)
    check("승인 전에는 S4 시작 거부", S("start", "S4")[0] == 1)
    check("S3 승인", S("approve", "S3")[0] == 0)
    check("승인 후 S4 시작", S("start", "S4")[0] == 0)
    for i in range(1, 4):
        rc, _ = S("fail", "S4", "--to", "S4", "--reason", f"G4 위반 {i}")
        if i < 3:
            check(f"S4 {i}회 실패는 계속 가능", rc == 0)
            S("start", "S4")
        else:
            check("S4 3회 실패는 halted(종료 코드 3)", rc == 3)
    check("halted 단계는 시작 거부", S("start", "S4")[0] == 1)
    state = json.loads(S("show")[1])
    check("halted 상태가 기록됨", state["stages"]["S4"]["status"] == "halted" and state["stages"]["S4"]["failures"] == 3)

with tempfile.TemporaryDirectory() as w:
    S = lambda *a: st(*a, "--screen", "home", work=w)
    st("init", "home", work=w)
    for s in ("S1", "S2", "S3"):
        S("start", s)
        S("pass", s)
    S("approve", "S3")
    S("start", "S4")
    rc, _ = S("fail", "S4", "--to", "S3", "--reason", "방향 부적합")
    state = json.loads(S("show")[1])
    check("S3로 복귀하면 S3 승인이 취소된다", rc == 0 and state["s3_approved"] is False and state["stages"]["S3"]["status"] == "pending")
    check("복귀 후 승인 없이 S4 거부", S("start", "S4")[0] == 1)
    check("복귀 단계가 실패 단계보다 뒤면 거부", S("fail", "S3", "--to", "S4", "--reason", "x")[0] == 1)

fails = 0
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  ({detail})"))
    fails += 0 if ok else 1
print(f"\n{len(results) - fails}/{len(results)} 통과")
sys.exit(1 if fails else 0)
