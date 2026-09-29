#!/usr/bin/env python3
"""PreToolUse 훅: 에이전트가 자기 편집 폴더 밖에 쓰지 못하게 막는다.

사용 (에이전트 정의의 hooks에서):  python3 scripts/guard-path.py <research|design|review>
허용: <프로젝트>/work/<화면 10개 중 하나>/<폴더>/ 아래. 그 밖은 종료 코드 2로 차단한다.
입력을 읽지 못하거나 경로를 알 수 없으면 차단한다(통과가 기본이 아니다).
"""
import json
import os
import sys
from pathlib import Path

SCREENS = {"home", "free-learning", "paid-library", "skill-library", "mission-detail",
           "submission", "my-learning", "my-assets", "asset-detail", "admin-review"}
FOLDERS = {"research", "design", "review"}


def block(msg):
    print(f"차단: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in FOLDERS:
        block("guard 설정 오류: 폴더 이름은 research/design/review 중 하나여야 한다")
    folder = sys.argv[1]
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parent.parent).resolve()

    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        block("hook 입력을 읽지 못했다")

    tool_input = data.get("tool_input") or {}
    raw = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not raw:
        block("쓰려는 경로를 알 수 없다")

    target = Path(raw)
    if not target.is_absolute():
        target = Path(data.get("cwd") or root) / target
    target = Path(os.path.realpath(target))  # 심볼릭 링크·.. 를 풀어서 본다

    try:
        parts = target.relative_to((root / "work").resolve()).parts
    except ValueError:
        block(f"{target} 은(는) work/ 밖이다. 이 에이전트는 work/<화면>/{folder}/ 에만 쓸 수 있다")

    if len(parts) >= 3 and parts[0] in SCREENS and parts[1] == folder:
        sys.exit(0)
    block(f"{'/'.join(parts)} 은(는) 허용 밖이다. 이 에이전트는 work/<화면>/{folder}/ 에만 쓸 수 있다")


if __name__ == "__main__":
    main()
