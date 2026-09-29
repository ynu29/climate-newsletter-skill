# 참고 매체 및 저널 목록

이 목록은 기존 발간 뉴스레터 분석과 사용자 피드백을 반영하여 정리한 매체/저널이다.
각 섹션에서 우선 탐색해야 할 소스의 순서가 중요하다.

---

## 국내 정책·연구

### 1순위: 정부/공공기관 보도자료
- **대한민국 정책브리핑** (korea.kr) — 최우선 소스. 기후에너지환경부(2025.10 환경부 개편), 기상청, 과기정통부, 2050탄소중립녹색성장위원회 등의 보도자료를 가장 먼저 확인
- **에어코리아** (airkorea.or.kr) — 대기환경 실시간 데이터
- **환경위성센터** — 위성 기반 대기질 자료
- **한국수자원공사(K-water)** (kwater.or.kr) — 수자원·물순환 분야 (물자원순환연구단 소관 범위). 지하수·물 재이용·가뭄 대응 등 정책·제도 이슈에 한정

### 2순위: 주요 대형 언론사
아래 목록에 해당하는 언론사의 기사를 우선 선정한다.

- **연합뉴스** (yna.co.kr) — 국내 최대 통신사 ※ fetch 차단 도메인 (하단 '차단 도메인' 참고)
- **동아사이언스** (dongascience.com) — 과학 분야 전문 매체
- **조선비즈** (biz.chosun.com) — 과학·환경 섹션
- **뉴시스** (newsis.com) — 주요 통신사
- **뉴스1** (news1.kr)
- **한겨레** (hani.co.kr)
- **경향신문** (khan.co.kr)
- **중앙일보** (joongang.co.kr)
- **헤럴드경제** (heraldcorp.com)

### 3순위: 전문지 티어
대형 언론사가 다루지 않는 전문 영역을 보완하는 매체. 각 매체의 적용 조건을 지킨다.

- **헬로디디** (hellodd.com) — 출연연·대덕특구 전문지. **출연연(KIST, KAIST, 표준연 등)의 기후·대기 분야 연구성과 보도에 한정**하여 사용. 정부출연연구기관 동향 커버리지에 강점
- **지디넷코리아** (zdnet.co.kr) — IT 전문지. **기후×기술 교차 주제(데이터센터 전력·냉각, AI 에너지 수요, 탄소관리 솔루션 등)에 한정**하여 사용. 순수 대기환경 기사 용도로는 사용하지 않음
- **전자신문** (etnews.com) — 산업기술 전문지. **에너지·산업기술이 탄소중립과 직접 연결되는 주제에 한정**하여 사용

전문지 기사도 대형 언론사가 같은 사안을 더 충실히 보도한 경우 대형 언론사 버전을 우선한다.

### 피해야 할 매체
- 지역방송 (경인방송, 지역MBC 등)
- 소규모 인터넷 언론 (한국글로벌뉴스, 한국미디어뉴스 등)
- 블로그, 개인 채널
- 같은 사안이 대형 언론사에도 보도된 경우, 반드시 대형 언론사 기사를 선택

### 검색 키워드 예시
정책브리핑 기후에너지환경부, 정책브리핑 기상청, 정책브리핑 기후, 지하수 관리 정책, 물 재이용 제도, 가뭄 대응 수자원, 기후변화 정책 연합뉴스, 미세먼지 대기질 동아사이언스, 탄소중립 온실가스, 대기환경 조선비즈, 출연연 기후 헬로디디, 데이터센터 탄소 지디넷

### 차단 도메인 목록 (fetch 불가 — 우회 경로 필수)

아래 도메인은 `web_fetch` 접근이 차단되는 것으로 확인되었다. 직접 fetch를 반복 시도하지 말고 SKILL.md의 '차단 도메인 대응 프로토콜'에 따라 우회한다. 새로 차단이 확인된 도메인은 이 목록에 추가한다.

| 도메인 | 매체/기관 | 권장 우회 경로 |
|--------|----------|---------------|
| korea.kr | 대한민국 정책브리핑 | 부처 원본 보도자료 → RSS → 사용자 본문 요청 |
| yna.co.kr | 연합뉴스 | 네이버 뉴스 미러(n.news.naver.com) → 사용자 본문 요청 |
| mcee.go.kr | 기후에너지환경부 | 정책브리핑 동일 기사 검색 → 사용자 본문 요청 |

**우회 경로 요약:**
1. 네이버 뉴스 미러: `"기사 제목" 네이버 뉴스` 검색 → `n.news.naver.com` 링크 fetch (출처 표기는 원 매체로)
2. 부처 원본: 기상청(kma.go.kr), 과기정통부(msit.go.kr) 등 부처 보도자료 페이지 검색 후 fetch (기후에너지환경부 mcee.go.kr은 원본도 차단 → 네이버 뉴스 미러 우선)
3. RSS: 정책브리핑·기상청 RSS(XML) 엔드포인트로 제목·발행일 검증
4. 최후 수단: `⚠️ 원문 미확인` 표시 후 사용자에게 본문 제공 요청 (스니펫만으로 요약 작성 금지)

---

## 해외 정책·연구

### 1순위: 국제기구/정부기관 공식 발표
이 기관들의 보고서 발간 소식, 연구결과 발표, 정책 성명을 최우선으로 검색한다.

- **WMO** (wmo.int) — 세계기상기구. 기후·기상 관련 주요 발표
- **IEA** (iea.org) — 국제에너지기구. 에너지·배출 관련 보고서
- **UNFCCC** (unfccc.int) — 유엔기후변화협약. COP 관련 소식
- **NASA** (nasa.gov, climate.nasa.gov) — 기후 위성 데이터, 기후 연구
- **NOAA** (climate.gov, noaa.gov) — 미국 해양대기청
- **UNEP** (unep.org) — 유엔환경계획. Emissions Gap Report 등
- **IPCC** (ipcc.ch) — 기후변화에 관한 정부간 패널
- **GCF** (greenclimate.fund) — 녹색기후기금
- **ESA** (esa.int) — 유럽우주국. 지구 관측/기후 관련

### 2순위: 기후 전문 매체
- **Carbon Brief** (carbonbrief.org) — 가장 권위 있는 기후 전문 매체. 데이터 기반 심층 분석
- **The Guardian** (theguardian.com) — 환경 섹션 강점
- **Reuters** — 기후·에너지 보도
- **Euronews** (euronews.com) — 유럽 환경·기후 정책

### 3순위: 연구기관/NGO 보고서
- **Oxfam** — 기후 불평등 관련
- **World Resources Institute (WRI)** — 환경·기후 정책 연구
- **Climate Action Tracker** — 국가별 기후 목표 추적

### 이 섹션에서 다루지 않는 것
- Nature, Science 등 학술저널의 논문 발간 뉴스/논문 소개 기사 → '최신 연구 동향' 섹션으로 분류
- 학술지 사이트의 뉴스 섹션에서 다루는 연구 결과 소개 → '최신 연구 동향' 섹션으로 분류

### 검색 키워드 예시
WMO climate report 2026, IEA energy report, UNFCCC climate policy, NASA climate, NOAA atmospheric, UNEP emissions gap, Carbon Brief analysis, climate policy news

---

## 최신 연구 동향 (학술 논문)

### 1순위: Nature 계열
- **Nature** (nature.com)
- **Nature Climate Change** — 기후변화 전문
- **Nature Geoscience** — 지구과학
- **Nature Communications** — 학제간 연구
- **Communications Earth & Environment** — 환경과학

### 2순위: Science 계열
- **Science** (science.org)
- **Science Advances** — 다학제 연구

### 3순위: 기타 고영향력 저널
- **PNAS** (Proceedings of the National Academy of Sciences) — 반드시 포함하여 검색
- **Atmospheric Research** — 대기과학 전문
- **Atmospheric Chemistry and Physics (ACP)**
- **Environmental Science & Technology (ES&T)**
- **Journal of Geophysical Research: Atmospheres**
- **Geophysical Research Letters**

### 논문 링크 규칙
- 반드시 **해당 논문의 고유 페이지 URL** 사용
- Nature 계열: `https://www.nature.com/articles/s41558-xxx-xxxxx-x` 형식
- Science 계열: `https://www.science.org/doi/10.1126/science.xxxxx` 형식
- PNAS: `https://www.pnas.org/doi/10.1073/pnas.xxxxxxxxxx` 형식
- DOI 기반 URL 권장: `https://doi.org/10.xxxx/xxxxx`
- **절대 사용하지 말 것**: 저널 목록 페이지, 검색결과 페이지, 카테고리 페이지 URL

### 검색 키워드 예시
climate change Nature 2026, atmospheric Science 2026, air quality PNAS, greenhouse gas Nature Climate Change, aerosol research paper, PM2.5 study Nature Communications
