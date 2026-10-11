#!/usr/bin/env python3
"""공통 실행 문서·역할·프로젝트 입력 연결을 확인한다. 프로젝트 내용의 진실성은 검사하지 않는다."""
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DOCS = ['design.md','story-service.md','story-work.md','harness-goal.md','pipeline.md','artifacts.md','gates.md','roles.md','CLAUDE.md','verification.md']
checks = []
def check(name,ok):
    checks.append(ok)
    print(('PASS ' if ok else 'FAIL ')+name)
def read(p):
    return (ROOT/p).read_text() if (ROOT/p).exists() else ''
check('공통 문서 존재',all((ROOT/p).exists() for p in DOCS))
check('프로젝트 디자인 설정 양식 존재','```harness-rules' in read('design.md'))
check('단계 S1~S5 연결',set(re.findall(r'^\| (S\d) ',read('pipeline.md'),re.M)) == {f'S{i}' for i in range(1,6)})
check('게이트 G1~G6 연결',set(re.findall(r'^\| (G\d) ',read('gates.md'),re.M)) == {f'G{i}' for i in range(1,7)})
m=re.search(r'^## 어기면 안 되는 것\n(.*?)(?=^## |\Z)',read('story-service.md'),re.M|re.S)
check('공통 금지 규칙 2개',bool(m) and len(re.findall(r'^\d+\. ',m[1],re.M))==2)
refs=set(re.findall(r'\b([a-z-]+\.md)\b',read('CLAUDE.md')))-{'prd.md','CLAUDE.md'}
check('실행 문서 참조 존재',all((ROOT/p).exists() for p in refs))
for folder in ['research','design','review']:
    check(folder+' 편집 경계 명시',f'work/<화면>/{folder}/' in read('roles.md'))
check('화면 고정 목록 대신 이름 형식 검사',all('SCREENS =' not in read(p) for p in ['scripts/judge.py','scripts/state.py','scripts/guard-path.py']))
print(f'{sum(checks)}/{len(checks)} 통과')
sys.exit(0 if all(checks) else 1)
