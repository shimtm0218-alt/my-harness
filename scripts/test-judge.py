#!/usr/bin/env python3
"""프로젝트 설정 변경, 판정 누락, 정책 실패를 검사하는 합성 데이터 테스트."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
rules={'status':'ready','colors':['#123456'],'radius':[8],'spacing':[8],'font_families':['Project Font'],'font_weights':[500],'pill_types':[],'allow_shadow':False,'policy_ids':['P1'],'policy_not_applicable_reason':''}
base={'screen':'collection-panel','frames':[{'id':'1','direction':'A','viewer_role':'buyer','nodes':[{'id':'n','type':'card','fills':['#123456'],'radius':8,'gap':8,'font':{'family':'Project Font','weight':500}}]}],'policy_checks':[{'id':'P1','passed':True,'evidence':'기획서 P1과 프레임 1 대조'}]}
def clone(v):return json.loads(json.dumps(v))
cases=[]
def case(name,change,expected):
    d,r=clone(base),clone(rules);change(d,r);cases.append((name,d,r,expected))
case('프로젝트 고유 값 허용',lambda d,r:None,0)
case('색 위반',lambda d,r:d['frames'][0]['nodes'][0].update(fills=['#ffffff']),1)
case('radius 위반',lambda d,r:d['frames'][0]['nodes'][0].update(radius=16),1)
case('간격 위반',lambda d,r:d['frames'][0]['nodes'][0].update(gap=12),1)
case('폰트 위반',lambda d,r:d['frames'][0]['nodes'][0]['font'].update(family='Other'),1)
case('그림자 위반',lambda d,r:d['frames'][0]['nodes'][0].update(shadow=True),1)
case('정책 실패',lambda d,r:d['policy_checks'][0].update(passed=False),1)
case('정책 근거 누락',lambda d,r:d['policy_checks'][0].update(evidence=''),2)
case('미설정',lambda d,r:r.update(status='unconfigured'),2)
case('새 화면 허용',lambda d,r:d.update(screen='store-header'),0)
case('경로 탈출 차단',lambda d,r:d.update(screen='../outside'),2)
case('정책 없음 사유 필요',lambda d,r:r.update(policy_ids=[]),2)
case('정책 적용 제외 사유',lambda d,r:r.update(policy_ids=[],policy_not_applicable_reason='시각 비교만 수행'),0)
case('필수 프레임 누락',lambda d,r:d.update(frames=[]),2)
failed=0
for name,d,r,expected in cases:
    with tempfile.TemporaryDirectory() as td:
        p=Path(td);(p/'frames.json').write_text(json.dumps(d));(p/'design.md').write_text('```harness-rules\n'+json.dumps(r)+'\n```')
        result=subprocess.run([sys.executable,str(ROOT/'scripts/judge.py'),str(p/'frames.json'),'--design',str(p/'design.md'),'--expect-directions','1'],capture_output=True,text=True)
    ok=result.returncode==expected
    print(('PASS ' if ok else 'FAIL ')+name)
    if not ok:print(result.stdout)
    failed+=not ok
print(f'{len(cases)-failed}/{len(cases)} 통과')
sys.exit(bool(failed))
