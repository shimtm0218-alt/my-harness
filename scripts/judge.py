#!/usr/bin/env python3
"""프로젝트별 디자인 설정과 정책 검토 기록을 검사한다. 0 통과 / 1 위반 / 2 판정 불가."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
class InputError(Exception):
    pass

def valid_screen(value):
    return isinstance(value, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value)

def as_list(value):
    return value if isinstance(value, list) else [value] if value is not None else []

def load_rules(path):
    match = re.search(r'```harness-rules\s*\n(.*?)\n```', Path(path).read_text(), re.S)
    if not match:
        raise InputError('design.md에 harness-rules 설정이 없다')
    rules = json.loads(match.group(1))
    if not isinstance(rules, dict) or rules.get('status') != 'ready':
        raise InputError('프로젝트 디자인 기준이 미설정이다')
    for key in ('colors', 'radius', 'spacing', 'font_families', 'font_weights', 'pill_types', 'policy_ids'):
        if not isinstance(rules.get(key), list):
            raise InputError(f'{key}는 목록이어야 한다')
        values = rules[key]
        numeric = key in ('radius', 'spacing', 'font_weights')
        if any((isinstance(v, bool) or not isinstance(v, (int, float)) or v < 0) if numeric else (not isinstance(v, str) or not v.strip()) for v in values):
            raise InputError(f'{key} 값 형식이 잘못됐다')
        if len(values) != len(set(values)):
            raise InputError(f'{key}에 중복 값이 있다')
    if any(not re.fullmatch(r'#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?', c) for c in rules['colors']):
        raise InputError('colors는 hex 색상이어야 한다')
    if rules.get('allow_shadow') is not None and not isinstance(rules['allow_shadow'], bool):
        raise InputError('allow_shadow는 boolean 또는 null이어야 한다')
    if not isinstance(rules.get('policy_not_applicable_reason'), str):
        raise InputError('정책 적용 제외 사유는 문자열이어야 한다')
    return rules

def load_frames(path):
    data = json.loads(Path(path).read_text())
    if not isinstance(data, dict) or not valid_screen(data.get('screen')):
        raise InputError('screen 이름이 잘못됐다')
    if not isinstance(data.get('frames'), list) or not data['frames']:
        raise InputError('frames가 비어 있다')
    for frame in data['frames']:
        if not isinstance(frame, dict) or any(not frame.get(k) for k in ('id','direction','viewer_role','nodes')):
            raise InputError('프레임 필수 값이 누락됐다')
        if not isinstance(frame['nodes'], list):
            raise InputError('nodes는 목록이어야 한다')
        for node in frame['nodes']:
            if not isinstance(node, dict) or not node.get('id') or not node.get('type'):
                raise InputError('노드 id/type 누락')
    return data

def judge_g4(data, rules, expected):
    keys = ('colors','radius','spacing','font_families','font_weights','pill_types')
    if not any(rules[k] for k in keys) and rules.get('allow_shadow') is None:
        raise InputError('G4 검사 기준이 전부 비어 있다')
    violations = []
    if len({f['direction'] for f in data['frames']}) != expected:
        violations.append('G4.frames: 방향 수 불일치')
    for f in data['frames']:
        for n in f['nodes']:
            def add(kind):
                violations.append(f"G4.{kind}: frame={f['id']} node={n['id']}")
            cs = [c for k in ('fills','strokes','textColor') for c in as_list(n.get(k))]
            if rules['colors'] and any(str(c).lower() not in {v.lower() for v in rules['colors']} for c in cs):
                add('color')
            radius = as_list(n.get('radius'))
            radius = [9999 if v == 'full' else v for v in radius]
            if rules['radius'] and any(isinstance(v,bool) or v not in rules['radius'] for v in radius):
                add('radius')
            if n['type'] in rules['pill_types'] and (not radius or any(v != 9999 for v in radius)):
                add('pill')
            if rules['spacing'] and any(isinstance(v,bool) or v not in [0,*rules['spacing']] for k in ('padding','gap','margin') for v in as_list(n.get(k))):
                add('spacing')
            font = n.get('font')
            if font is not None:
                if not isinstance(font, dict):
                    raise InputError('font는 객체여야 한다')
                if rules['font_families'] and str(font.get('family','')).lower() not in {v.lower() for v in rules['font_families']}:
                    add('font')
                if rules['font_weights'] and font.get('weight') not in rules['font_weights']:
                    add('font')
            if rules.get('allow_shadow') is False and n.get('shadow'):
                add('shadow')
    notes = ['G4 미검사 항목: '+', '.join(k for k in keys if not rules[k])]
    if rules.get('allow_shadow') is None:
        notes.append('G4 그림자 미검사')
    return violations, notes

def judge_g5(data, rules):
    ids = rules['policy_ids']
    if not ids:
        reason = rules['policy_not_applicable_reason'].strip()
        if not reason:
            raise InputError('G5 정책 또는 적용 제외 사유가 필요하다')
        return [], ['G5 적용 제외: '+reason]
    checks = data.get('policy_checks')
    if not isinstance(checks,list):
        raise InputError('policy_checks가 필요하다')
    mapped = {}
    for c in checks:
        if not isinstance(c,dict) or not isinstance(c.get('id'),str) or c['id'] in mapped:
            raise InputError('정책 ID 누락 또는 중복')
        mapped[c['id']] = c
    violations = []
    for pid in ids:
        c = mapped.get(pid)
        if not c or not isinstance(c.get('passed'),bool) or not isinstance(c.get('evidence'),str) or not c['evidence'].strip():
            raise InputError(f'정책 {pid}의 검토 기록 또는 근거 누락')
        if not c['passed']:
            violations.append('G5.policy: '+pid)
    return violations, ['G5는 정책 검토 기록을 검사한다. 실제 화면 준수 여부는 근거 대조가 필요하다.']

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('frames')
    ap.add_argument('--gate',choices=['G4','G5','all'],default='all')
    ap.add_argument('--expect-directions',type=int,default=3)
    ap.add_argument('--design',default=str(ROOT/'design.md'))
    a = ap.parse_args()
    try:
        if a.expect_directions < 1:
            raise InputError('기대 방향 수는 1 이상이어야 한다')
        rules, data = load_rules(a.design), load_frames(a.frames)
        failures = []
        for name, fn in [('G4',lambda:judge_g4(data,rules,a.expect_directions)),('G5',lambda:judge_g5(data,rules))]:
            if a.gate not in (name,'all'):
                continue
            v, notes = fn()
            failures.extend(v)
            print(f'{name} 지정 검사: {len(v)}건 위반')
            for line in v+notes:
                print(line)
        return 1 if failures else 0
    except (InputError, OSError, ValueError, TypeError, KeyError) as e:
        print('입력 오류(판정 불가): '+str(e))
        return 2
if __name__ == '__main__':
    sys.exit(main())
