#!/usr/bin/env python3
"""PreToolUse 훅(judge용): Bash로는 판정 스크립트(judge.py, judge_md.py)만 실행할 수 있다. 그 밖의 명령은 종료 코드 2로 차단한다.

판정자는 읽기 전용이다. 리다이렉트·파이프·명령 연결·치환을 쓰면 파일을 쓸 수 있으므로 모두 막는다.
"""
import json
import re
import sys

ALLOWED = re.compile(r"^python3 scripts/(judge|judge_md)\.py( [A-Za-z0-9_./\-]+| --[a-z\-]+)+$")


def block(msg):
    print(f"차단: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        block("hook 입력을 읽지 못했다")
    command = ((data.get("tool_input") or {}).get("command") or "").strip()
    if not command:
        block("실행할 명령을 알 수 없다")
    if ALLOWED.match(command):
        sys.exit(0)
    block("판정자는 'python3 scripts/judge.py <frames.json> [--gate G4|G5|all] [--expect-directions N]' 만 실행할 수 있다")


if __name__ == "__main__":
    main()
