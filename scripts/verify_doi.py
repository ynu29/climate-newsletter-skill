#!/usr/bin/env python3
"""
verify_doi.py — Crossref API 기반 논문 서지정보 검증 스크립트

사용법:
    python3 verify_doi.py <DOI1> [DOI2] [DOI3] ...

예시:
    python3 verify_doi.py 10.1038/s41558-024-01234-5 10.1073/pnas.2301234120

기능:
    각 DOI에 대해 Crossref API(api.crossref.org)를 조회하여
    제목 / 저자 / 게재일 / 저널명을 출력한다.
    후보 목록의 서지정보와 대조하여 불일치 시 Crossref 데이터를 기준으로 수정한다.

네트워크 차단 시:
    실행 환경의 네트워크 정책이 api.crossref.org 접근을 차단하면,
    이 스크립트는 안내 메시지를 출력하고 종료한다.
    그 경우 web_fetch 도구로 아래 URL을 직접 조회하여 동일한 검증을 수행한다:
        https://api.crossref.org/works/<DOI>

종료 코드:
    0 = 모든 DOI 조회 성공
    1 = 일부/전체 DOI 조회 실패 (DOI 오류 또는 네트워크 차단)
"""

import json
import sys
import urllib.error
import urllib.request

API_BASE = "https://api.crossref.org/works/"
TIMEOUT = 15
# Crossref 권장: 연락처를 포함한 User-Agent (polite pool)
USER_AGENT = "KIST-CleanAir-Newsletter-Skill/1.0 (mailto:newsletter@example.org)"


def format_date(parts):
    """Crossref date-parts [[YYYY, MM, DD]] → 'YYYY.MM.DD.' 문자열."""
    if not parts:
        return "(날짜 정보 없음)"
    p = parts[0]
    if len(p) >= 3:
        return f"{p[0]}.{p[1]:02d}.{p[2]:02d}."
    if len(p) == 2:
        return f"{p[0]}.{p[1]:02d}."
    return f"{p[0]}."


def fetch_doi(doi: str) -> dict:
    url = API_BASE + urllib.request.quote(doi, safe="/")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def print_record(doi: str, msg: dict) -> None:
    title = "; ".join(msg.get("title", [])) or "(제목 없음)"
    journal = "; ".join(msg.get("container-title", [])) or "(저널명 없음)"
    authors = msg.get("author", [])
    author_str = ", ".join(
        f"{a.get('given', '')} {a.get('family', '')}".strip() for a in authors[:5]
    )
    if len(authors) > 5:
        author_str += f" 외 {len(authors) - 5}명"
    pub = (
        msg.get("published-print")
        or msg.get("published-online")
        or msg.get("published")
        or msg.get("created")
        or {}
    )
    date_str = format_date(pub.get("date-parts"))

    print(f"✅ DOI: {doi}")
    print(f"   제목   : {title}")
    print(f"   저자   : {author_str or '(저자 정보 없음)'}")
    print(f"   게재일 : {date_str}")
    print(f"   저널   : {journal}")
    print(f"   링크   : https://doi.org/{doi}")
    print()


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1

    dois = [d.strip().replace("https://doi.org/", "") for d in argv[1:]]
    failures = 0

    for doi in dois:
        try:
            data = fetch_doi(doi)
            print_record(doi, data.get("message", {}))
        except urllib.error.HTTPError as e:
            failures += 1
            if e.code == 404:
                print(f"❌ DOI: {doi} — Crossref에서 조회되지 않음 (404).")
                print("   → DOI 오기 가능성. 원문 페이지에서 DOI를 재확인하고,")
                print("     재확인 후에도 조회되지 않으면 해당 논문은 후보에서 제외한다.\n")
            else:
                # 403 등은 실행 환경의 egress proxy 차단일 가능성이 높음
                print(f"⚠️  DOI: {doi} — HTTP 오류 {e.code} (네트워크 정책에 의한 차단 가능성)")
                print("   → 실행 환경에서 api.crossref.org가 차단된 것으로 보인다.")
                print("   → 대신 web_fetch 도구로 아래 URL을 조회하여 동일한 검증을 수행할 것:")
                print(f"      https://api.crossref.org/works/{doi}\n")
        except (urllib.error.URLError, OSError, TimeoutError) as e:
            failures += 1
            print(f"⚠️  DOI: {doi} — 네트워크 접근 실패: {e}")
            print("   → 실행 환경에서 api.crossref.org가 차단된 것으로 보인다.")
            print("   → 대신 web_fetch 도구로 아래 URL을 조회하여 동일한 검증을 수행할 것:")
            print(f"      https://api.crossref.org/works/{doi}\n")

    if failures:
        print(f"검증 실패 {failures}건 / 전체 {len(dois)}건")
        return 1
    print(f"전체 {len(dois)}건 검증 완료")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
