# judge.py 입력 형식 (frames.json)

`work/<화면>/design/frames.json` — designer가 Figma 시안에서 뽑아 쓴다. judge는 읽기만 한다.
아직 Figma에서 이 JSON을 자동으로 뽑는 도구는 없다.

```json
{
  "screen": "my-assets",
  "frames": [
    {
      "id": "1:23",
      "direction": 1,
      "viewer_role": "seller",
      "flow": "asset-register",
      "nodes": [
        {"id": "1:30", "type": "button", "role": "button-primary",
         "fills": ["#141414"], "textColor": "#ffffff", "radius": "full",
         "padding": [0, 16], "font": {"family": "Pretendard", "weight": 600}}
      ]
    }
  ]
}
```

## 프레임

| 필드 | 뜻 |
| --- | --- |
| id | Figma 프레임 ID |
| direction | 시안 방향 번호 (S4는 1~3, S5 최종은 1개) |
| viewer_role | 이 화면을 보는 사람: guest / free / paid / seller / admin |
| flow | 선택. G5 검사 대상이면 `asset-register` 또는 `sale-request` |

## 노드 (필드는 있는 것만 적는다)

| 필드 | 뜻 |
| --- | --- |
| type | button / toggle / badge / chip / nav / input / card / text / option / option-group 등. **button·toggle·badge·chip·nav는 pill(radius 9999)이어야 한다** |
| role | 선택. 예외와 G5 검사에 쓴다: `badge-overlay`, `app-icon-squircle`, `segmented-control-active`, `confirm-item`, `sale-request-option` |
| fills, strokes, textColor | `#rrggbb` (목록 가능). badge-overlay만 `rgba(115,115,115,0.56)` 허용 |
| radius | px 숫자, `"full"`, 또는 app-icon-squircle의 `"30%"`. 모서리별이면 목록 |
| padding, gap, margin | px 숫자 (목록 가능). 간격이 없는 0은 검사에서 제외 |
| font | `{"family": "...", "weight": 400}` |
| shadow | drop shadow가 있으면 true |
| text | 화면에 보이는 글자 (G5의 확인 항목·판매 신청 옵션 검사에 쓴다) |
| group, default | 공개 범위 선택이면 `"group": "visibility"`, `"default": "비공개"` |

## 실행

```
python3 scripts/judge.py work/my-assets/design/frames.json
python3 scripts/judge.py work/my-assets/review/frames.json --expect-directions 1   # S5 최종 화면
python3 scripts/judge.py work/home/design/frames.json --gate G4
```

종료 코드: 0 통과 / 1 위반 있음 / 2 입력 오류(판정 불가, 통과로 치지 않는다)
