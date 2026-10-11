#!/usr/bin/env python3
"""work/<화면>/state.json 관리. 오케스트레이터만 쓴다. 단계 순서와 승인·실패 규칙을 여기서 강제한다.

명령:
  init <화면>                      state.json 만들기 (이미 있으면 거부)
  start <단계>                     단계 시작 (앞 단계가 통과했고, S4는 S3 승인이 있어야 함)
  wait <단계> --for "<누구를>"     사람의 입력을 기다리는 상태로 기록
  pass <단계>                      게이트 통과
  fail <단계> --to <복귀 단계> --reason "<이유>"   게이트 실패. 같은 단계 3회 실패면 halted
  approve S3                       사람 승인 기록 (S3가 통과한 상태에서만)
  show                             현재 상태 출력
공통 옵션: --screen <화면> --work-dir <경로>
종료 코드: 0 성공 / 1 규칙 위반 / 3 halted(사람을 불러야 함)
"""
import argparse
import re
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGES = ["S1", "S2", "S3", "S4", "S5"]
MAX_FAILURES = 3


class Rule(Exception):
    pass


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def state_path(work_dir, screen):
    return Path(work_dir) / screen / "state.json"


def load(work_dir, screen):
    p = state_path(work_dir, screen)
    if not p.exists():
        raise Rule(f"{p} 이(가) 없다. 먼저 init 하세요")
    return json.loads(p.read_text(encoding="utf-8"))


def save(work_dir, screen, st):
    p = state_path(work_dir, screen)
    p.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def log(st, event):
    st["log"].append({"time": now(), "event": event})


def check_stage(stage):
    if stage not in STAGES:
        raise Rule(f"단계는 {STAGES} 중 하나여야 한다")


def cmd_init(a):
    p = state_path(a.work_dir, a.screen)
    if p.exists():
        raise Rule(f"{p} 이(가) 이미 있다")
    p.parent.mkdir(parents=True, exist_ok=True)
    st = {"screen": a.screen, "current_stage": "S1", "waiting_for": None, "s3_approved": False,
          "stages": {s: {"status": "pending", "failures": 0} for s in STAGES}, "log": []}
    log(st, "init")
    save(a.work_dir, a.screen, st)


def cmd_start(a, st):
    s = a.stage
    i = STAGES.index(s)
    if st["stages"][s]["status"] == "halted":
        raise Rule(f"{s}은(는) {MAX_FAILURES}회 실패로 halted 상태다. 사람이 원인을 정리한 뒤에 다시 시작할 수 있다")
    if st["stages"][s]["status"] == "running":
        raise Rule(f"{s}은(는) 이미 running이다")
    if i > 0 and st["stages"][STAGES[i - 1]]["status"] != "passed":
        raise Rule(f"{STAGES[i - 1]}이(가) passed가 아니다 ({st['stages'][STAGES[i - 1]]['status']}). {s}을(를) 시작할 수 없다")
    if s == "S4" and not st["s3_approved"]:
        raise Rule("S3 사람 승인이 없다. 'approve S3' 후에 S4를 시작할 수 있다")
    st["stages"][s]["status"] = "running"
    st["current_stage"], st["waiting_for"] = s, None
    log(st, f"start {s}")


def cmd_wait(a, st):
    if st["stages"][a.stage]["status"] != "running":
        raise Rule(f"{a.stage}이(가) running이 아니라 wait로 바꿀 수 없다")
    st["stages"][a.stage]["status"] = "waiting_human"
    st["waiting_for"] = a.for_
    log(st, f"wait {a.stage}: {a.for_}")


def cmd_pass(a, st):
    s = a.stage
    if st["stages"][s]["status"] not in ("running", "waiting_human"):
        raise Rule(f"{s}은(는) {st['stages'][s]['status']} 상태라 pass할 수 없다")
    st["stages"][s]["status"] = "passed"
    i = STAGES.index(s)
    st["current_stage"] = STAGES[min(i + 1, len(STAGES) - 1)]
    st["waiting_for"] = "S3 승인" if s == "S3" else None
    log(st, f"pass {s}")


def cmd_fail(a, st):
    s, to = a.stage, a.to
    check_stage(to)
    if STAGES.index(to) > STAGES.index(s):
        raise Rule("복귀 단계는 실패한 단계보다 뒤일 수 없다")
    if st["stages"][s]["status"] not in ("running", "waiting_human"):
        raise Rule(f"{s}은(는) {st['stages'][s]['status']} 상태라 fail할 수 없다")
    st["stages"][s]["failures"] += 1
    halted = st["stages"][s]["failures"] >= MAX_FAILURES
    st["stages"][s]["status"] = "halted" if halted else "failed"
    for later in STAGES[STAGES.index(to):]:
        if later != s:
            st["stages"][later]["status"] = "pending"
    if STAGES.index(to) <= STAGES.index("S3"):
        st["s3_approved"] = False
    if to != s and not halted:
        st["stages"][to]["status"] = "pending"
    st["current_stage"] = to
    st["waiting_for"] = "사람 호출 (3회 실패)" if halted else None
    log(st, f"fail {s} -> {to}: {a.reason}" + (" [halted]" if halted else ""))
    return 3 if halted else 0


def cmd_approve(a, st):
    if a.stage != "S3":
        raise Rule("사람 승인 지점은 S3 하나다")
    if st["stages"]["S3"]["status"] != "passed":
        raise Rule("S3가 passed가 아니다. G3를 통과한 뒤에만 승인할 수 있다")
    st["s3_approved"], st["waiting_for"] = True, None
    log(st, "approve S3" + (f": {a.reason}" if a.reason else ""))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["init", "start", "wait", "pass", "fail", "approve", "show"])
    ap.add_argument("target", nargs="?", help="init은 화면, 나머지는 단계")
    ap.add_argument("--screen")
    ap.add_argument("--work-dir", default=str(ROOT / "work"))
    ap.add_argument("--for", dest="for_")
    ap.add_argument("--to")
    ap.add_argument("--reason", default="")
    a = ap.parse_args(argv)
    try:
        if a.command == "init":
            a.screen = a.target
            if not a.screen or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a.screen):
                raise Rule("화면 이름은 영문 소문자·숫자·하이픈으로 작성한다")
            cmd_init(a)
            print(f"init {a.screen}")
            return 0
        if not a.screen or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a.screen):
            raise Rule("유효한 --screen 이 필요하다")
        st = load(a.work_dir, a.screen)
        if a.command == "show":
            print(json.dumps(st, ensure_ascii=False, indent=2))
            return 0
        a.stage = a.target
        check_stage(a.stage)
        if a.command == "wait" and not a.for_:
            raise Rule("--for 가 필요하다")
        if a.command == "fail" and not a.to:
            raise Rule("--to 가 필요하다")
        code = {"start": cmd_start, "wait": cmd_wait, "pass": cmd_pass, "fail": cmd_fail, "approve": cmd_approve}[a.command](a, st) or 0
        save(a.work_dir, a.screen, st)
        print(f"{a.command} {a.stage}: {st['stages'][a.stage]['status']}"
              + (f" (대기: {st['waiting_for']})" if st["waiting_for"] else ""))
        return code
    except Rule as e:
        print(f"규칙 위반: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
