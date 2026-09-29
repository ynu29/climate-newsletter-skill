#!/usr/bin/env python3
"""
청정대기 이슈동향 뉴스레터 HTML + DOCX 생성기 (2024 디자인)

사용법:
    python generate_newsletter.py newsletter_data.json 뉴스레터_2026.03.25

    → 뉴스레터_2026.03.25.html  (이메일 발송용 HTML)
    → 뉴스레터_2026.03.25.docx  (검수/수정용 Word 파일 — HTML 소스코드)

입력 JSON 형식: SKILL.md Step 4 참고

v1.2 변경:
  - 모든 섹션 항목에 선택 필드 `footnotes`(문자열 배열) 지원
    → 출처 아래에 회색 12px 각주 블록(<!--각주 시작--> ~ <!--/각주 끝-->)으로 출력
  - `source`에 "출처 –"가 이미 포함돼 있으면 자동 제거 (중복 표기 방지)
  - JSON 로드 시 BOM(utf-8-sig) 허용
"""

import json
import re
import sys
import os
from docx import Document as DocxDocument
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ─── HTML 블록 템플릿 (2024 디자인) ───

DOMESTIC_ARTICLE_BLOCK = """<!-- {n}번 국내기사 시작-->
<tr>
<td>
{agency_block}<!-- 국내기사 제목 시작-->
<h4 style="margin:0px 40px 0px 40px; padding-bottom:15px; color:#414454; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:20px; font-weight:bold; letter-spacing:-0.03em; word-break:keep-all; line-height:1.4;"><a href="{link}" target="_blank" style="color:#414454; text-decoration:none;">{title}
</a></h4>
<!-- /국내기사 제목 끝-->
<!-- 국내기사 본문 시작-->
<p style="margin:0 40px 0 40px; padding:0; color:#414454; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; text-align:justify; letter-spacing:-0.035em; line-height:1.7; word-break:keep-all;">{summary}</p>
<!-- /국내기사 본문 끝-->
{note_block}{extra_link_block}<!--국내기사 출처 시작-->
<p style="margin:0 40px 0 40px; padding-top:8px; color:#414454; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; font-weight:bold; letter-spacing:-0.035em; line-height:1.7;">출처 – {source}</p>
<!--/국내기사 출처 끝-->
{footnote_block}</td>
</tr>
<!-- {n}번 국내기사 끝-->"""

DOMESTIC_AGENCY_BLOCK = """<!--행정기관명 시작-->
<h3 style="margin:0 40px 0 40px; padding:0; color:#1d7791; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; font-weight:bold; letter-spacing:-0.03em; line-height:1.4;">{agency}</h3>
<!--/행정기관명 끝-->
"""

DOMESTIC_NOTE_BLOCK = """<!--국내기사 부가설명 시작-->
<p style="margin:0 40px 0 40px; padding-top:5px; color:#1d7791; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:13px; letter-spacing:-0.035em; line-height:1.4; word-break:keep-all;">{note}</p>
<!--/국내기사 부가설명 끝-->
"""

DOMESTIC_EXTRA_LINK_BLOCK = """<!--국내기사 추가링크 시작-->
<h4 style="margin:0 40px 0 40px; padding-top:5px; color:#1d7791; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; letter-spacing:-0.035em; line-height:1.4; word-break:keep-all;"><a href="{extra_link_url}" target="_blank" style="color:#1d7791; text-decoration:none;">※ {extra_link_title}</a></h4>
<!--/국내기사 추가링크 끝-->
"""

INTERNATIONAL_ARTICLE_BLOCK = """<!-- {n}번 해외기사 시작-->
<tr>
<td>
<!-- 해외기사 제목 시작-->
<h4 style="margin:0px 40px 0px 40px; padding-bottom:15px; color:#414454; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:20px; font-weight:bold; letter-spacing:-0.03em; word-break:keep-all; line-height:1.4;"><a href="{link}" target="_blank" style="color:#414454; text-decoration:none;">{title}
</a></h4>
<!-- /해외기사 제목 끝-->
<!-- 해외기사 본문 시작-->
<p style="margin:0 40px 0 40px; padding:0; color:#414454; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; text-align:justify; letter-spacing:-0.035em; line-height:1.7; word-break:keep-all;">{summary}</p>
<!-- /해외기사 본문 끝-->
{ref_block}<!--해외기사 출처 시작-->
<p style="margin:0 40px 0 40px; padding-top:8px; color:#414454; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; font-weight:bold; letter-spacing:-0.035em; line-height:1.7;">출처 – {source}</p>
<!--/해외기사 출처 끝-->
{footnote_block}</td>
</tr>
<!-- {n}번 해외기사 끝-->"""

INTERNATIONAL_REF_BLOCK = """<!--추가링크 시작-->
<h4 style="margin:0 40px 0 40px; padding-top:5px; color:#3d6df8; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; letter-spacing:-0.035em; line-height:1.4; word-break:keep-all;"><a href="{ref_url}" target="_blank" style="color:#3d6df8; text-decoration:none;">※ {ref_title}</a></h4>
<!--/추가링크 끝-->
"""

JOURNAL_ARTICLE_BLOCK = """<!-- {n}번 최신논문 시작-->
<tr>
<td>
<!-- 최신논문기사 제목 시작-->
<h4 style="margin:0px 40px 0px 40px; padding-bottom:15px; color:#414454; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:20px; font-weight:bold; letter-spacing:-0.03em; word-break:keep-all; line-height:1.4;"><a href="{link}" target="_blank" style="color:#414454; text-decoration:none;">{title}
</a></h4>
<!-- /최신논문기사 제목 끝-->
<!-- 최신논문기사 본문 시작-->
<p style="margin:0 40px 0 40px; padding:0; color:#414454; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; text-align:justify; letter-spacing:-0.035em; line-height:1.7; word-break:keep-all;">{summary}</p>
<!-- /최신논문기사 본문 끝-->
<!--최신논문기사 출처 시작-->
<p style="margin:0 40px 0 40px; padding-top:8px; color:#414454; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; font-weight:bold; letter-spacing:-0.035em; line-height:1.7;">출처 – {source}</p>
<!--/최신논문기사 출처 끝-->
{footnote_block}</td>
</tr>
<!-- {n}번 최신논문 끝-->"""

FOOTNOTE_BLOCK = """<!--각주 시작-->
<p style="margin:0 40px 0 40px; padding-top:6px; color:#8a8d99; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:12px; letter-spacing:-0.035em; line-height:1.6; word-break:keep-all;">{lines}</p>
<!--/각주 끝-->
"""

SPACER = """<tr>
<td height="30" style="font-size:0; line-height:0;">&nbsp;</td>
</tr>
"""

FULL_TEMPLATE = """<table cellpadding="0" cellspacing="0" border="0" align="center" class="newsletter_wrap" style="width:100%; max-width:800px; margin:40px; auto; border-collapse: collapse;">
<tbody>
<tr>
<td><img src="https://www.pixfactory.co.kr/mail/kist/images/2024_top_01_01.jpg" width="100%" alt="" style="display: block; margin: 0;"/></td>
</tr>
<!-- 일자 시작-->
<tr>
<td bgcolor="#aff1f6" style="font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:20px; font-weight:bold; text-align:center;">{date}</td>
</tr>
<!-- 일자 끝-->
<tr>
<td><img src="https://www.pixfactory.co.kr/mail/kist/images/2024_top_01_02.jpg" width="100%" alt="" style="display: block; margin: 0;"/></td>
</tr>
<tr>
<td><img src="https://www.pixfactory.co.kr/mail/kist/images/2024_title_01.jpg" width="100%" alt="" style="display: block; margin: 0;"/></td>
</tr>
<tr>
<td>
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="border:#22a5cb solid 6px; border-collapse: collapse;">
<tbody>
<tr>
<td height="30" style="font-size:0; line-height:0;">&nbsp;</td>
</tr>
<!-- 국내 정책 연구 시작-->
{domestic_articles}<!--/국내 정책 연구 끝-->
</tbody>
</table>
</td>
</tr>
<tr>
<td>
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="border:#2f6ec5 solid 6px; border-collapse: collapse;">
<tbody>
<!-- 해외 정책 연구 시작-->
<tr>
<td><img src="https://www.pixfactory.co.kr/mail/kist/images/2024_title_02.jpg" width="100%" alt="" style="display: block; margin: 0;"/></td>
</tr>
<tr>
<td height="30" style="font-size:0; line-height:0;">&nbsp;</td>
</tr>
{international_articles}<!--/해외 정책 연구 끝-->
</tbody>
</table>
</td>
</tr>
<tr>
<td>
<table width="100%" border="0" cellspacing="0" cellpadding="0" style="border:#5ac99a solid 6px; border-collapse: collapse;">
<tbody>
<!--최신논문 시작-->
<tr>
<td><img src="https://www.pixfactory.co.kr/mail/kist/images/2024_title_03.jpg" width="100%" alt="" style="display: block; margin: 0;"/></td>
</tr>
<tr>
<td height="30" style="font-size:0; line-height:0;">&nbsp;</td>
</tr>
{journal_articles}<!--/최신논문 끝-->
</tbody>
</table>
</td>
</tr>
<tr>
<!--담당자정보 시작-->
<td height="50" bgcolor="#5ac99a" style="color:#fff; font-family:'Noto Sans CJK KR', Dotum,'돋움',sans-serif; font-size:14px; text-align:center"><b>문의</b>&nbsp;&nbsp;청정대기센터&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Tel&nbsp;&nbsp;02-958-7315&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;E-mail&nbsp;&nbsp;<a href="mailto:cleanair@kist.re.kr" target="_blank" style="color:#fff; text-decoration:none;">cleanair@kist.re.kr</a></td>
<!--담당자정보 끝-->
</tr>
</tbody>
</table>"""


# ─── 공통 헬퍼 ───

_SOURCE_PREFIX = re.compile(r"^\s*출처\s*[–\-—:]\s*")


def clean_source(source):
    """source 필드에 '출처 –'가 들어와도 한 번만 출력되도록 접두어 제거."""
    return _SOURCE_PREFIX.sub("", source or "").strip()


def build_footnote_block(art):
    """footnotes: ["* 용어 설명", ...] (문자열 1개도 허용). 없으면 빈 문자열."""
    notes = art.get("footnotes") or []
    if isinstance(notes, str):
        notes = [notes]
    notes = [n.strip() for n in notes if n and n.strip()]
    if not notes:
        return ""
    lines = [n if n[0] in "*※¹²³⁴⁵⁶⁷⁸⁹" else "* " + n for n in notes]
    return FOOTNOTE_BLOCK.format(lines="<br/>\n".join(lines))


# ─── 섹션 빌더 ───

def build_domestic_articles(articles):
    blocks = []
    for i, art in enumerate(articles, 1):
        agency_block = ""
        if art.get("agency"):
            agency_block = DOMESTIC_AGENCY_BLOCK.format(agency=art["agency"])
        note_block = ""
        if art.get("note"):
            note_block = DOMESTIC_NOTE_BLOCK.format(note=art["note"])
        extra_link_block = ""
        if art.get("extra_link_title") and art.get("extra_link_url"):
            extra_link_block = DOMESTIC_EXTRA_LINK_BLOCK.format(
                extra_link_title=art["extra_link_title"],
                extra_link_url=art["extra_link_url"]
            )
        block = DOMESTIC_ARTICLE_BLOCK.format(
            n=i, agency_block=agency_block, title=art["title"],
            link=art["link"], summary=art["summary"], source=clean_source(art["source"]),
            note_block=note_block, extra_link_block=extra_link_block,
            footnote_block=build_footnote_block(art)
        )
        blocks.append(block)
    return SPACER.join(blocks) + SPACER


def build_international_articles(articles):
    blocks = []
    for i, art in enumerate(articles, 1):
        ref_block = ""
        if art.get("ref_title") and art.get("ref_url"):
            ref_block = INTERNATIONAL_REF_BLOCK.format(
                ref_title=art["ref_title"], ref_url=art["ref_url"]
            )
        block = INTERNATIONAL_ARTICLE_BLOCK.format(
            n=i, title=art["title"], link=art["link"],
            summary=art["summary"], source=clean_source(art["source"]), ref_block=ref_block,
            footnote_block=build_footnote_block(art)
        )
        blocks.append(block)
    return SPACER.join(blocks) + SPACER


def build_journal_articles(articles):
    blocks = []
    for i, art in enumerate(articles, 1):
        block = JOURNAL_ARTICLE_BLOCK.format(
            n=i, title=art["title"], link=art["link"],
            summary=art["summary"], source=clean_source(art["source"]),
            footnote_block=build_footnote_block(art)
        )
        blocks.append(block)
    return SPACER.join(blocks) + SPACER


def generate_html(data):
    return FULL_TEMPLATE.format(
        date=data["date"],
        domestic_articles=build_domestic_articles(data["domestic"]),
        international_articles=build_international_articles(data["international"]),
        journal_articles=build_journal_articles(data["journals"])
    )


# ─── DOCX 생성 (HTML 소스코드를 Word 문서로) ───

def generate_docx(html_content, output_path):
    """
    생성된 HTML 소스코드를 원본 템플릿과 동일한 형식의 Word 문서로 변환.
    사용자가 Word에서 직접 검수/수정할 수 있도록 HTML 코드를 텍스트로 담는다.
    원본 템플릿: 맑은 고딕 폰트, 각 HTML 줄이 하나의 문단.
    """
    doc = DocxDocument()

    # 기본 스타일 설정 (원본 템플릿과 동일하게 맑은 고딕)
    style = doc.styles['Normal']
    font = style.font
    font.name = '맑은 고딕'
    font.size = Pt(10)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    # HTML을 줄 단위로 분할하여 각 줄을 문단으로 추가
    lines = html_content.split('\n')
    for line in lines:
        para = doc.add_paragraph(line)
        para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    doc.save(output_path)


# ─── 메인 ───

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_newsletter.py <input.json> <output_basename>")
        print("  → <output_basename>.html + <output_basename>.docx")
        sys.exit(1)

    input_path = sys.argv[1]
    output_basename = sys.argv[2]

    # .html/.docx 확장자가 이미 붙어있으면 제거
    for ext in ['.html', '.docx', '.json']:
        if output_basename.endswith(ext):
            output_basename = output_basename[:-len(ext)]

    html_path = output_basename + '.html'
    docx_path = output_basename + '.docx'

    # utf-8-sig: BOM이 붙은 JSON도 허용. JSON은 반드시
    # json.dump(data, f, ensure_ascii=False, indent=2) 로 작성할 것 (SKILL.md Step 4)
    try:
        with open(input_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"[오류] JSON 로드 실패: {e}")
        print("  → JSON을 문자열로 직접 조립하지 말고 Python json.dump(..., ensure_ascii=False)로 다시 저장하세요.")
        print("  → 요약문 안의 큰따옴표(\")·줄바꿈이 이스케이프되지 않은 경우가 가장 흔한 원인입니다.")
        sys.exit(1)

    # 1) HTML 생성
    html = generate_html(data)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 2) DOCX 생성 (HTML 소스코드를 Word 문서로)
    generate_docx(html, docx_path)

    # 통계
    n_domestic = len(data["domestic"])
    n_international = len(data["international"])
    n_journals = len(data["journals"])
    n_footnotes = sum(1 for sec in ("domestic", "international", "journals")
                      for a in data[sec] if a.get("footnotes"))
    print(f"뉴스레터 생성 완료!")
    print(f"  HTML: {html_path}")
    print(f"  DOCX: {docx_path}")
    print(f"  국내 정책·연구: {n_domestic}건")
    print(f"  해외 정책·연구: {n_international}건")
    print(f"  최신 연구 동향: {n_journals}건")
    if n_footnotes:
        print(f"  각주 포함 항목: {n_footnotes}건")


if __name__ == "__main__":
    main()
