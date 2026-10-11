# 프로젝트 디자인 기준

이 파일은 프로젝트가 실제 사용하는 디자인 시스템을 입력하는 양식이다.
특정 서비스의 색상, 버튼 형태, 폰트, 모바일 크기를 기본값으로 강제하지 않는다.
실행 전 상태를 `ready`로 바꾸고, 근거와 기준을 작성한다.

## 기준과 근거

- 프로젝트명:
- 디자인 시스템 / Figma 라이브러리 링크:
- 기준 화면 크기와 반응형 조건:
- 토큰·컴포넌트와 예외:
- 상태별 표현과 접근성 기준:

## 기계 판정 설정

아래 `harness-rules` JSON을 프로젝트 기준에 맞게 채운다.
색은 hex, radius·spacing은 숫자(px), 폰트는 실제 family 이름을 쓴다.
빈 허용 목록은 해당 항목을 자동 검사하지 않는다는 의미다. 미검사 항목은 사람이 확인한다.
`pill_types`에 적힌 요소만 pill 형태를 검사한다. `allow_shadow`는 그림자 허용 여부다.
`policy_ids`에는 이번 화면에서 확인할 정책 ID를 적는다. 상세 내용과 적용 이유는 기획서 및 범위 문서에 기록한다.
정책이 없으면 `policy_not_applicable_reason`에 이유를 적는다.

```harness-rules
{
  "status": "unconfigured",
  "colors": [],
  "radius": [],
  "spacing": [],
  "font_families": [],
  "font_weights": [],
  "pill_types": [],
  "allow_shadow": null,
  "policy_ids": [],
  "policy_not_applicable_reason": ""
}
```

미설정이거나 자동 검사 항목이 전부 비어 있으면 판정 불가다.
자동 판정은 지정된 값과 정책 검토 기록의 형식만 확인한다. 화면 사용성과 정책 준수의 사실 여부는 원본 화면과 근거를 직접 대조한다.
