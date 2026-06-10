# climate-newsletter-skill

Claude Code skill: KIST 청정대기센터 주간 **청정대기 이슈동향** 뉴스레터 자동 생성 (기사/논문 수집 + 요약 + HTML/DOCX 출력)

---


## 개요

기후변화 및 대기환경 관련 국내외 정책·연구·최신 논문을 매주 수집·요약하여  
KIST 청정대기센터 주간 뉴스레터 형식의 **HTML 이메일 파일**과 **DOCX 검수 파일**을 자동 생성하는 Claude Code 스킬입니다.


## 주요 기능

- **3개 섹션 자동 구성**: 국내 정책·연구 / 해외 정책·연구 / 최신 연구 동향
- **웹 검색 자동 수집**: 지난 1주일 기사·논문을 섹션별 5~6건씩 탐색
- **3대 필수 검증**: 발행일 확인 / 해외 섹션 Nature 뉴스 제외 / 주제 적합성 검토
- **사용자 선택 후 요약**: 후보 목록 제시 → 사용자 선택 → 격식체 한국어 요약 작성
- **이중 출력**: `.html` (이메일 발송용) + `.docx` (검수·수정용) 동시 생성


## 파일 구조

```
climate-newsletter/
├── SKILL.md                        # 스킬 정의 (워크플로우 전체 명세)
├── assets/
│   └── template_raw.html           # 원본 HTML 이메일 템플릿 (참고용)
├── references/
│   ├── sources.md                  # 참고 매체·저널 목록 및 검색 키워드
│   └── style-guide.md              # 요약 작성 스타일 상세 지침
└── scripts/
    └── generate_newsletter.py      # HTML + DOCX 생성 스크립트
```


## 사용법

Claude Code 또는 Claude.ai에서 다음과 같이 요청합니다:

```
이번 주 뉴스레터 만들어줘
```

```
이번 주 청정대기 이슈동향 작성해줘 (6월 1~5일)
```

```
# URL 직접 제공
https://www.korea.kr/briefing/...
https://www.nature.com/articles/...
위 URL들로 뉴스레터 만들어줘
```


## 워크플로우

```
Step 1  웹 검색으로 후보 수집 (섹션별 5~6건)
   ↓
Step 1-1  3대 필수 검증 (발행일 / 섹션 적합성 / 주제 관련성)
   ↓
Step 2  후보 목록 제시 → 사용자 선택
   ↓
Step 3  격식체 한국어 요약 작성 (국내·해외 500~700자 / 논문 600~800자)
   ↓
Step 4  JSON 데이터 구성
   ↓
Step 5  generate_newsletter.py 실행 → .html + .docx 생성
   ↓
Step 6  출력 파일 전달
```


## 출력 형식

| 파일 | 용도 |
|------|------|
| `뉴스레터_YYYY.MM.DD.html` | 이메일 발송용 HTML (인라인 CSS 포함) |
| `뉴스레터_YYYY.MM.DD.docx` | 검수·수정용 Word 파일 |


## JSON 데이터 구조

`generate_newsletter.py`에 전달하는 JSON의 필수/선택 필드:

```json
{
  "date": "2026.06.09.",
  "domestic": [
    {
      "agency": "기후에너지환경부",          // 행정기관명 (필수)
      "title": "기사 제목 (원문 그대로)",    // 필수
      "link": "https://...",               // 필수
      "summary": "500~700자 요약",          // 필수
      "source": "대한민국 정책브리핑, 2026.03.23.",  // 필수
      "note": "부가 설명 (선택)",           // 선택
      "extra_link_title": "관련 자료명",    // 선택 — note 아래 추가 링크 제목
      "extra_link_url": "https://..."      // 선택 — extra_link_title과 함께 사용
    }
  ],
  "international": [
    {
      "title": "Article Title",            // 필수 (영어 원문 그대로)
      "link": "https://...",               // 필수
      "summary": "500~700자 요약",          // 필수
      "source": "WMO, 2026.03.23.",        // 필수
      "ref_title": "Full Report 명칭",     // 선택 — 원문 보고서 링크 제목 (※ 형식으로 표시)
      "ref_url": "https://..."             // 선택 — ref_title과 함께 사용
    }
  ],
  "journals": [
    {
      "title": "논문 제목 (영어 원문 그대로)",  // 필수
      "link": "https://doi.org/10.xxxx/...",  // 필수 — 반드시 DOI 페이지
      "summary": "600~800자 요약",             // 필수
      "source": "Nature Communications, 2026.03.19."  // 필수
    }
  ]
}
```


## 소스 우선순위

**국내 정책·연구**
- 대한민국 정책브리핑(korea.kr) — 기후에너지환경부, 환경부, 기상청, 과기정통부 보도자료 최우선
- 연합뉴스, 조선비즈, 동아사이언스, 한겨레, 중앙일보 등 주요 언론사

**해외 정책·연구**
- WMO, IEA, UNEP, UNFCCC, NASA, NOAA 등 국제기구 공식 발표 최우선
- Carbon Brief, The Guardian 등 전문 기후 매체 심층 보도

**최신 연구 동향**
- Nature, Nature Climate Change, Nature Geoscience 등 Nature 계열 저널 우선
- Science, PNAS, Atmospheric Chemistry and Physics 등 주요 학술지


## 요약 스타일

- **격식체(합쇼체)** 일관 사용: "~하였다", "~밝혔다", "~것으로 나타났다"
- 구체적 수치·데이터 적극 포함
- 전문용어 첫 등장 시 영문 병기
- 마지막 1~2문장은 전문가 인용 또는 시사점으로 마무리
- 기사 제목은 반드시 원문 그대로 사용 (임의 변형 금지)


## 의존성

- Python 3.8+
- `python-docx` (`pip install python-docx`) — DOCX 생성에 사용
- Claude 모델 접근 (claude.ai 또는 Claude Code)

> **이미지 호스팅**: HTML 템플릿의 섹션 헤더 이미지는 `pixfactory.co.kr` 외부 서버에서 불러옵니다. 해당 서버 접근이 불가한 환경에서는 이미지가 표시되지 않을 수 있습니다.


## 라이선스

내부 사용 전용 — KIST 청정대기센터
