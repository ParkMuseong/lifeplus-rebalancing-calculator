"""포트폴리오 — 자산 추적 · 정밀 리밸런싱

실행:
    streamlit run app.py
"""
from __future__ import annotations

import base64
import json
import math
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


@st.cache_data(show_spinner=False)
def _load_image_b64(path: str) -> str:
    try:
        return base64.b64encode(Path(path).read_bytes()).decode("ascii")
    except Exception:
        return ""


LIFEPLUS_LOGO_B64 = _load_image_b64(r"C:\Users\한화손해보험\VS CODE\이미지\LIFEPLUS_LOGO_가로.png")


@st.cache_data(show_spinner=False)
def _load_video_b64(path: str) -> str:
    try:
        return base64.b64encode(Path(path).read_bytes()).decode("ascii")
    except Exception:
        return ""


LIFEPLUS_MOTION_B64 = _load_video_b64(r"C:\Users\한화손해보험\VS CODE\이미지\LIFEPLUS_MOTION_3sec.mp4")

from stock_api import (
    get_kr_price,
    get_us_price,
    get_usd_krw_rate,
    load_krx_listing,
    search_kr_stocks,
    search_us_stocks,
)
from theme import C, CSS, style_fig


st.set_page_config(
    page_title="포트폴리오",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(CSS, unsafe_allow_html=True)


# ============================================================================
# State
# ============================================================================
if "holdings" not in st.session_state:
    st.session_state.holdings: list[dict] = []
if "last_sync" not in st.session_state:
    st.session_state.last_sync = datetime.now()


def _to_krw(price_native: float, currency: str, fx: float) -> float:
    return price_native * (fx if currency == "USD" else 1.0)


def _add_holding(market: str, code: str, name: str, price_native: float, currency: str) -> None:
    for h in st.session_state.holdings:
        if h["code"] == code and h["market"] == market:
            st.toast(f"이미 추가된 종목입니다 · {name}")
            return
    st.session_state.holdings.append({
        "market": market, "code": code, "name": name,
        "price_native": float(price_native), "currency": currency,
        "shares": 0, "target_pct": 0.0,
    })
    st.toast(f"{name} 추가됨")


def _refresh_prices() -> None:
    for h in st.session_state.holdings:
        if h["currency"] == "USD":
            p = get_us_price(h["code"])
        else:
            p = get_kr_price(h["code"])
        if p is not None:
            h["price_native"] = float(p)
    st.session_state.last_sync = datetime.now()


def _status() -> tuple[str, str, str]:
    n = len(st.session_state.holdings)
    if n == 0:
        return "준비 중", "종목을 추가해 시작하세요", C.MUTED

    total = sum(h["shares"] * _to_krw(h["price_native"], h["currency"], fx) for h in st.session_state.holdings)
    ts = sum(h["target_pct"] for h in st.session_state.holdings)

    if total <= 0 and ts == 0:
        return "입력 대기", "수량과 목표 비율을 입력하세요", C.MUTED
    if abs(ts - 100.0) >= 0.01:
        return "목표 설정 필요", f"현재 합계 {ts:.1f}%", C.WARN
    if total <= 0:
        return "수량 입력 필요", "보유 수량을 입력해 주세요", C.WARN

    drift = 0.0
    for h in st.session_state.holdings:
        cur = h["shares"] * _to_krw(h["price_native"], h["currency"], fx) / total * 100
        drift += abs(cur - h["target_pct"])
    drift /= 2.0

    if drift < 1.0:
        return "균형 유지", "재조정 불필요", C.PRIMARY
    if drift < 5.0:
        return "미세 이탈", f"이탈도 {drift:.1f}%", C.WARN
    return "조정 권장", f"이탈도 {drift:.1f}%", C.SELL


# ============================================================================
# Load data
# ============================================================================
with st.spinner("종목 데이터를 불러오는 중"):
    krx_df = load_krx_listing()
fx = get_usd_krw_rate()

total_value = sum(
    h["shares"] * _to_krw(h["price_native"], h["currency"], fx)
    for h in st.session_state.holdings
)
target_sum = sum(h["target_pct"] for h in st.session_state.holdings)
n_holdings = len(st.session_state.holdings)

total_drift = 0.0
if total_value > 0 and abs(target_sum - 100.0) < 0.01:
    for h in st.session_state.holdings:
        cur_pct = h["shares"] * _to_krw(h["price_native"], h["currency"], fx) / total_value * 100
        total_drift += abs(cur_pct - h["target_pct"])
    total_drift /= 2.0

status_label, status_sub, status_color = _status()
sync_time = st.session_state.last_sync.strftime("%H:%M")


# ============================================================================
# Top notice bar — LIFEPLUS 로고 + 안내문구 + 문의자
# ============================================================================
_logo_html = (
    f'<img src="data:image/png;base64,{LIFEPLUS_LOGO_B64}" class="topbar__logo" alt="LIFEPLUS">'
    if LIFEPLUS_LOGO_B64
    else '<div class="topbar__logo-text">LIFEPLUS</div>'
)

st.markdown(f"""
<div class="topbar">
  <div class="topbar__brand">
    {_logo_html}
    <div class="topbar__divider"></div>
  </div>
  <div class="topbar__service">
    <div class="topbar__service-label">서비스 안내</div>
    <div class="topbar__service-text">
      이 페이지는 <b>LIFEPLUS 부문 구성원</b>이 <mark>자산 리밸런싱 시 종목별 매수·매도 수량 계산을 편리하게</mark> 할 수 있도록 돕는 목적의 서비스입니다.
    </div>
  </div>
  <div class="topbar__contact">
    <div class="topbar__contact-label">문의 사항</div>
    <div class="topbar__contact-name">박무성 사원</div>
    <div class="topbar__contact-phone">010-9920-6171</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# 2-column layout: 좌측 백엔드 패널 + 우측 메인
# ============================================================================
left_col, main_col = st.columns([1, 3.5], gap="medium")

with left_col:
    st.markdown("""
    <div class="sb">
      <span class="sb__eyebrow">Behind the Scenes</span>
      <h3>백엔드 처리 흐름</h3>
      <p class="sb__subtitle"><span style="white-space:nowrap;">입력 즉시 자동으로 수행되는</span><br><b>7단계 처리 프로세스</b></p>

      <div class="sb__metrics">
        <div class="sb__metric">
          <div class="sb__metric-value">3,500+</div>
          <div class="sb__metric-label">종목</div>
        </div>
        <div class="sb__metric">
          <div class="sb__metric-value">실시간</div>
          <div class="sb__metric-label">시세</div>
        </div>
        <div class="sb__metric">
          <div class="sb__metric-value">USD·KRW</div>
          <div class="sb__metric-label">통합</div>
        </div>
      </div>

      <ol class="sb__steps">
        <li class="sb__step">
          <div class="sb__step-num">01</div>
          <div>
            <div class="sb__step-title">시장 데이터 캐싱</div>
            <div class="sb__step-desc">KOSPI·KOSDAQ·ETF 전체 종목 12시간 메모리 캐시</div>
          </div>
        </li>
        <li class="sb__step">
          <div class="sb__step-num">02</div>
          <div>
            <div class="sb__step-title">종목 자동 매칭</div>
            <div class="sb__step-desc">이름·코드 부분 일치, 시작 일치 우선 정렬</div>
          </div>
        </li>
        <li class="sb__step">
          <div class="sb__step-num">03</div>
          <div>
            <div class="sb__step-title">실시간 시세 조회</div>
            <div class="sb__step-desc">국내 FinanceDataReader · 해외 yfinance</div>
          </div>
        </li>
        <li class="sb__step">
          <div class="sb__step-num">04</div>
          <div>
            <div class="sb__step-title">USD·KRW 환산</div>
            <div class="sb__step-desc">환율 동기화 후 원화 통합 평가금액 계산</div>
          </div>
        </li>
        <li class="sb__step">
          <div class="sb__step-num">05</div>
          <div>
            <div class="sb__step-title">자산 구성 분석</div>
            <div class="sb__step-desc">종목별 비율 · 목표 대비 드리프트 산출</div>
          </div>
        </li>
        <li class="sb__step">
          <div class="sb__step-num">06</div>
          <div>
            <div class="sb__step-title">리밸런싱 알고리즘</div>
            <div class="sb__step-desc">(목표가치 − 현재가치) ÷ 종가 = 거래 주식 수</div>
          </div>
        </li>
        <li class="sb__step">
          <div class="sb__step-num">07</div>
          <div>
            <div class="sb__step-title">정밀 반올림</div>
            <div class="sb__step-desc">round·floor·ceil + 최소 거래 금액 필터</div>
          </div>
        </li>
      </ol>

    </div>
    """, unsafe_allow_html=True)

with main_col:
    # ========================================================================
    # App header
    # ========================================================================
    st.markdown(f"""
    <div class="app-header">
      <div class="app-brand">
        <span class="app-eyebrow">Dashboard</span>
        <h1 class="app-title">MY Portfolio</h1>
        <div class="app-subtitle">LIFEPLUS Rebalancing Calculator</div>
      </div>
      <div class="app-meta">
        <div class="app-meta-item">
          <div class="app-meta-label">USD / KRW</div>
          <div class="app-meta-value">₩{fx:,.2f}</div>
        </div>
        <div class="app-meta-item">
          <div class="app-meta-label">최근 동기화</div>
          <div class="app-meta-value">{sync_time}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================================
    # KPI cards
    # ========================================================================
    drift_display = f"{total_drift:.2f}<span class='unit'>%</span>" if total_drift > 0 or (total_value > 0 and abs(target_sum-100)<0.01) else "—"
    nav_display = f"₩{total_value:,.0f}" if total_value > 0 else "—"

    largest_pct, largest_name = 0.0, "—"
    if total_value > 0:
        for h in st.session_state.holdings:
            p = h["shares"] * _to_krw(h["price_native"], h["currency"], fx) / total_value * 100
            if p > largest_pct:
                largest_pct = p
                largest_name = h["name"]

    n_kr = sum(1 for h in st.session_state.holdings if h["currency"] == "KRW")
    n_us = sum(1 for h in st.session_state.holdings if h["currency"] == "USD")

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card primary">
        <div class="kpi-label">총자산</div>
        <div class="kpi-value">{nav_display}</div>
        <div class="kpi-meta">{n_holdings}개 종목 · 국내 {n_kr} · 해외 {n_us}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">최대 비중</div>
        <div class="kpi-value text">{largest_name if largest_name != '—' else '—'}</div>
        <div class="kpi-meta">{f'{largest_pct:.1f}% 차지' if largest_pct > 0 else '입력 후 표시'}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">목표 이탈도</div>
        <div class="kpi-value">{drift_display}</div>
        <div class="kpi-meta">목표 비율 대비 평균 차이</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">상태</div>
        <div class="kpi-value text" style="color: {status_color};">{status_label}</div>
        <div class="kpi-meta">{status_sub}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    has_holdings = len(st.session_state.holdings) > 0

    if not st.session_state.get("show_results", False):
        # ========================================================================
        # STEP 01 — 종목 추가
        # ========================================================================
        with st.container(border=True):
            st.markdown("""
            <div class="step-card-header">
              <div class="step-num">01</div>
              <div class="step-info">
                <h2 class="step-title">현재 포트폴리오 입력</h2>
                <p class="step-sub" style="white-space:nowrap;">탭에서 자산군을 고르고 <b>① 검색 → ② 선택 → ③ 추가</b> 순서로 보유 종목을 등록하세요. 현재가는 자동으로 조회됩니다.</p>
              </div>
            </div>
            """, unsafe_allow_html=True)

            tab_kr, tab_us, tab_cash = st.tabs([
                "국내 주식 · ETF (국장)",
                "미국 주식 (미장)",
                "현금성 자산 · 국채 / 미국채",
            ])

            with tab_kr:
                query = st.text_input(
                    "① 종목명 또는 코드 입력",
                    placeholder="삼성전자, KODEX 200, 005930 등을 입력하세요",
                    key="kr_query",
                )
                if not query:
                    st.markdown('<div class="quick-anchor"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="search-empty__label">예시 검색어 — 아래 형식 중 아무거나 입력 가능</div>', unsafe_allow_html=True)
                    kr_examples = ["삼성전자", "SK하이닉스", "KODEX 200", "TIGER 미국S&P500", "PLUS K방산"]
                    kr_chip_cols = st.columns(len(kr_examples))
                    for i, name in enumerate(kr_examples):
                        with kr_chip_cols[i]:
                            if st.button(name, key=f"kr_quick_{i}", use_container_width=True):
                                ex_hits = search_kr_stocks(name, krx_df, limit=1)
                                if not ex_hits:
                                    st.error(f"'{name}' 검색 결과 없음")
                                else:
                                    ex_s = ex_hits[0]
                                    with st.spinner("현재가 조회 중"):
                                        ex_price = get_kr_price(ex_s["Code"])
                                    if ex_price is None:
                                        st.error("현재가 조회에 실패했습니다.")
                                    else:
                                        _add_holding(ex_s["Market"], ex_s["Code"], ex_s["Name"], ex_price, "KRW")
                                        st.rerun()
                    st.markdown('<div class="search-empty__hint">입력하면 후보 종목이 자동으로 나타납니다. <b>드롭다운에서 종목을 고른 후 추가 버튼</b>을 누르세요.</div>', unsafe_allow_html=True)
                else:
                    hits = search_kr_stocks(query, krx_df, limit=30)
                    if not hits:
                        st.info("검색 결과가 없습니다. 다른 키워드로 시도해 보세요.")
                    else:
                        options = {f"{r['Name']}   ·   {r['Code']}   ·   {r['Market']}": r for r in hits}
                        sel = st.radio(
                            "② 추가할 종목 선택",
                            list(options.keys()),
                            key="kr_sel",
                            index=0,
                        )
                        if st.button("③ 포트폴리오에 추가", key="kr_add", type="primary", use_container_width=True):
                            s = options[sel]
                            with st.spinner("현재가 조회 중"):
                                price = get_kr_price(s["Code"])
                            if price is None:
                                st.error("현재가 조회에 실패했습니다.")
                            else:
                                _add_holding(s["Market"], s["Code"], s["Name"], price, "KRW")
                                st.rerun()

            with tab_us:
                us_q = st.text_input(
                    "① 티커 또는 회사명 입력",
                    placeholder="AAPL, TSLA, VOO 등을 입력하세요",
                    key="us_q",
                )
                if not us_q:
                    st.markdown('<div class="quick-anchor"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="search-empty__label">예시 검색어 — 정확한 티커(영문 약자)가 가장 정확합니다</div>', unsafe_allow_html=True)
                    us_examples = ["AAPL", "TSLA", "VOO", "QQQ", "NVDA"]
                    us_chip_cols = st.columns(len(us_examples))
                    for i, ticker in enumerate(us_examples):
                        with us_chip_cols[i]:
                            if st.button(ticker, key=f"us_quick_{i}", use_container_width=True):
                                with st.spinner("검색 중"):
                                    ex_hits = search_us_stocks(ticker, limit=1)
                                if not ex_hits:
                                    st.error(f"'{ticker}' 검색 결과 없음")
                                else:
                                    ex_s = ex_hits[0]
                                    with st.spinner("현재가 조회 중"):
                                        ex_price = get_us_price(ex_s["Code"])
                                    if ex_price is None:
                                        st.error("현재가 조회에 실패했습니다.")
                                    else:
                                        _add_holding("US", ex_s["Code"], ex_s["Name"], ex_price, "USD")
                                        st.rerun()
                    st.markdown('<div class="search-empty__hint">회사명(예: <b>Apple</b>)으로도 검색되지만, 정확한 티커가 가장 빠릅니다.</div>', unsafe_allow_html=True)
                else:
                    with st.spinner("검색 중"):
                        hits = search_us_stocks(us_q, limit=15)
                    if not hits:
                        st.info("검색 결과가 없습니다. 정확한 티커(AAPL 등)로 시도해 보세요.")
                    else:
                        options = {f"{r['Name']}   ·   {r['Code']}   ·   {r['Market']}": r for r in hits}
                        sel = st.radio(
                            "② 추가할 종목 선택",
                            list(options.keys()),
                            key="us_sel",
                            index=0,
                        )
                        if st.button("③ 포트폴리오에 추가", key="us_add", type="primary", use_container_width=True):
                            s = options[sel]
                            with st.spinner("현재가 조회 중"):
                                price = get_us_price(s["Code"])
                            if price is None:
                                st.error("현재가 조회에 실패했습니다.")
                            else:
                                _add_holding("US", s["Code"], s["Name"], price, "USD")
                                st.rerun()

            with tab_cash:
                cash_kind = st.radio(
                    "자산 종류",
                    options=["국채", "미국채", "직접 입력"],
                    horizontal=True,
                    key="cash_kind",
                    help="국채(KRW) · 미국채(USD) · 직접 입력(예금·MMF·외화 등 자유 입력)",
                )

                if cash_kind == "국채":
                    kb_q = st.text_input(
                        "① 국채 ETF 종목명 또는 코드 입력",
                        placeholder="KODEX 국고채3년, TIGER 국고채30년액티브, 114260 등",
                        key="kb_q",
                    )
                    if not kb_q:
                        st.markdown('<div class="quick-anchor"></div>', unsafe_allow_html=True)
                        st.markdown('<div class="search-empty__label">대표 국채 ETF — 클릭 대신 아래 키워드를 검색창에 입력</div>', unsafe_allow_html=True)
                        kb_examples = ["KODEX 국고채3년", "KODEX 국고채10년", "TIGER 국고채30년액티브", "KOSEF 국고채10년", "KODEX 단기채권"]
                        kb_chip_cols = st.columns(len(kb_examples))
                        for i, name in enumerate(kb_examples):
                            with kb_chip_cols[i]:
                                if st.button(name, key=f"kb_quick_{i}", use_container_width=True):
                                    ex_hits = search_kr_stocks(name, krx_df, limit=1)
                                    if not ex_hits:
                                        st.error(f"'{name}' 검색 결과 없음")
                                    else:
                                        ex_s = ex_hits[0]
                                        with st.spinner("현재가 조회 중"):
                                            ex_price = get_kr_price(ex_s["Code"])
                                        if ex_price is None:
                                            st.error("현재가 조회에 실패했습니다.")
                                        else:
                                            _add_holding(ex_s["Market"], ex_s["Code"], ex_s["Name"], ex_price, "KRW")
                                            st.rerun()
                        st.markdown('<div class="search-empty__hint">검색 결과는 <b>국고채·통안채·단기채권 ETF</b>만 필터링되어 표시됩니다. 만기·듀레이션을 확인하고 추가하세요.</div>', unsafe_allow_html=True)
                    else:
                        hits = search_kr_stocks(kb_q, krx_df, limit=80)
                        BOND_KW = ("국고채", "국채", "통안채", "단기채", "중기채", "장기채", "회사채", "크레딧채", "채권")
                        hits = [r for r in hits if any(k in str(r["Name"]) for k in BOND_KW)]
                        if not hits:
                            st.info("국채 관련 ETF가 검색되지 않습니다. 예: KODEX 국고채3년, TIGER 국고채30년액티브")
                        else:
                            options = {f"{r['Name']}   ·   {r['Code']}   ·   {r['Market']}": r for r in hits}
                            sel = st.radio("② 추가할 국채 ETF 선택", list(options.keys()), key="kb_sel", index=0)
                            if st.button("③ 포트폴리오에 추가", key="kb_add", type="primary", use_container_width=True):
                                s = options[sel]
                                with st.spinner("현재가 조회 중"):
                                    price = get_kr_price(s["Code"])
                                if price is None:
                                    st.error("현재가 조회에 실패했습니다.")
                                else:
                                    _add_holding(s["Market"], s["Code"], s["Name"], price, "KRW")
                                    st.rerun()

                elif cash_kind == "미국채":
                    ub_q = st.text_input(
                        "① 미국채 ETF 티커 또는 이름 입력",
                        placeholder="TLT, IEF, SHY, GOVT, BIL 등",
                        key="ub_q",
                    )
                    if not ub_q:
                        st.markdown('<div class="quick-anchor"></div>', unsafe_allow_html=True)
                        st.markdown('<div class="search-empty__label">대표 미국채 ETF — 만기별 분류</div>', unsafe_allow_html=True)
                        ub_examples = ["TLT", "IEF", "SHY", "GOVT", "BIL", "TLTW"]
                        ub_chip_cols = st.columns(len(ub_examples))
                        for i, ticker in enumerate(ub_examples):
                            with ub_chip_cols[i]:
                                if st.button(ticker, key=f"ub_quick_{i}", use_container_width=True):
                                    with st.spinner("검색 중"):
                                        ex_hits = search_us_stocks(ticker, limit=1)
                                    if not ex_hits:
                                        st.error(f"'{ticker}' 검색 결과 없음")
                                    else:
                                        ex_s = ex_hits[0]
                                        with st.spinner("현재가 조회 중"):
                                            ex_price = get_us_price(ex_s["Code"])
                                        if ex_price is None:
                                            st.error("현재가 조회에 실패했습니다.")
                                        else:
                                            _add_holding("US", ex_s["Code"], ex_s["Name"], ex_price, "USD")
                                            st.rerun()
                        st.markdown('<div class="search-empty__hint"><b>TLT</b> 20년+ · <b>IEF</b> 7-10년 · <b>SHY</b> 1-3년 · <b>BIL</b> 1-3개월 · <b>GOVT</b> 미국채 전체 · <b>TLTW</b> TLT 커버드콜</div>', unsafe_allow_html=True)
                    else:
                        with st.spinner("검색 중"):
                            hits = search_us_stocks(ub_q, limit=30)
                        BOND_KW = ("treasury", "bond", "t-bill", "tbill", "gov", "ultra", "maturity", "fixed income")
                        if hits:
                            filtered = [r for r in hits if any(k in str(r["Name"]).lower() for k in BOND_KW)]
                            if filtered:
                                hits = filtered
                        if not hits:
                            st.info("미국채 ETF가 검색되지 않습니다. 정확한 티커(TLT, IEF, SHY 등)로 시도해 보세요.")
                        else:
                            options = {f"{r['Name']}   ·   {r['Code']}   ·   {r['Market']}": r for r in hits}
                            sel = st.radio("② 추가할 미국채 ETF 선택", list(options.keys()), key="ub_sel", index=0)
                            if st.button("③ 포트폴리오에 추가", key="ub_add", type="primary", use_container_width=True):
                                s = options[sel]
                                with st.spinner("현재가 조회 중"):
                                    price = get_us_price(s["Code"])
                                if price is None:
                                    st.error("현재가 조회에 실패했습니다.")
                                else:
                                    _add_holding("US", s["Code"], s["Name"], price, "USD")
                                    st.rerun()

                else:  # 직접 입력
                    cur_choice = st.radio(
                        "① 통화 선택",
                        options=["원화 (KRW)", "달러 (USD)"],
                        horizontal=True,
                        key="cash_cur",
                    )
                    is_krw = cur_choice.startswith("원화")
                    currency = "KRW" if is_krw else "USD"
                    unit_label = "원" if is_krw else "USD"
                    default_name = "현금성 자산 (원화)" if is_krw else "현금성 자산 (달러)"

                    cdi1, cdi2 = st.columns([1.2, 1])
                    with cdi1:
                        cash_name = st.text_input(
                            "② 명칭 (선택)",
                            placeholder="예: MMF 통장, 외화예금, RP, 단기 예금",
                            key="cash_name_input",
                        )
                    with cdi2:
                        cash_amount = st.number_input(
                            f"③ 금액 ({unit_label})",
                            min_value=0.0,
                            value=0.0,
                            step=10_000.0 if is_krw else 100.0,
                            format="%.0f",
                            key="cash_amount_input",
                            help="실제 보유한 현금성 자산의 금액을 입력하세요",
                        )

                    if st.button(
                        "④ 포트폴리오에 추가",
                        key="cash_add",
                        type="primary",
                        use_container_width=True,
                        disabled=(cash_amount <= 0),
                    ):
                        existing = sum(
                            1 for h in st.session_state.holdings
                            if h.get("market") == "CASH" and h.get("currency") == currency
                        )
                        code = f"CASH-{currency}-{existing + 1}"
                        name = cash_name.strip() if cash_name and cash_name.strip() else default_name
                        st.session_state.holdings.append({
                            "market": "CASH",
                            "code": code,
                            "name": name,
                            "price_native": 1.0,
                            "currency": currency,
                            "shares": int(cash_amount),
                            "target_pct": 0.0,
                        })
                        st.toast(f"{name} ₩{int(cash_amount):,} 추가됨" if is_krw else f"{name} ${int(cash_amount):,} 추가됨")
                        st.rerun()

                    st.caption(
                        "직접 입력 자산은 1단위 = 1원/1달러로 처리되어 포트폴리오 평가에 반영됩니다. "
                        "동일 통화로 여러 항목을 추가하면 자동으로 번호가 매겨집니다."
                    )

        # ========================================================================
        # STEP 02 — 자산별 목표 비중 설정
        # ========================================================================
        has_holdings = len(st.session_state.holdings) > 0

        with st.container(border=True):
            st.markdown("""
            <div class="step-card-header">
              <div class="step-num">02</div>
              <div class="step-info">
                <h2 class="step-title">자산별 목표 비중 설정</h2>
                <p class="step-sub">보유 수량을 입력하고 <b>목표 비중(%)</b>을 설정하면 매수·매도 수량이 자동 계산됩니다</p>
              </div>
              <div class="step-aside">행을 삭제하면 종목이 제거됩니다</div>
            </div>
            """, unsafe_allow_html=True)

            if not has_holdings:
                st.markdown("""
                <div class="empty-state" style="padding:36px 24px;">
                  <div class="empty-title">보유 종목이 없습니다</div>
                  <div class="empty-body">위 검색창에서 종목을 추가하면 수량과 목표 비율 입력 표가 활성화됩니다.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                qa_l, _qa_r = st.columns([1, 4])
                with qa_l:
                    if st.button("균등 배분", key="eq_split", use_container_width=True, help="목표 비율을 모든 종목에 균등하게"):
                        n = len(st.session_state.holdings)
                        if n:
                            base = round(100.0 / n, 2)
                            for i, h in enumerate(st.session_state.holdings):
                                v = round(100.0 - base * (n - 1), 2) if i == n - 1 else base
                                h["target_pct"] = v
                                # number_input widget state도 같이 갱신 ── 화면 표시값과 동기화
                                st.session_state[f"_target_{h['code']}"] = v
                        st.rerun()

                def _on_shares_change(c):
                    v = st.session_state.get(f"_shares_{c}", 0)
                    for hh in st.session_state.holdings:
                        if hh["code"] == c:
                            hh["shares"] = int(v) if v is not None else 0
                            break

                def _on_target_change(c):
                    v = st.session_state.get(f"_target_{c}", 0.0)
                    for hh in st.session_state.holdings:
                        if hh["code"] == c:
                            hh["target_pct"] = float(v) if v is not None else 0.0
                            break

                for h in st.session_state.holdings:
                    code = h["code"]
                    market = h.get("market", "")
                    currency = h["currency"]
                    price_krw = _to_krw(h["price_native"], h["currency"], fx)
                    val_krw = h["shares"] * price_krw
                    cur_pct = (val_krw / total_value * 100) if total_value > 0 else 0.0
                    drift = (cur_pct - h["target_pct"]) if (h["target_pct"] > 0 or cur_pct > 0) else 0.0

                    if market == "CASH":
                        chip_label = "현금 · 원화" if currency == "KRW" else "현금 · 달러"
                        chip_class = "cash"
                    elif currency == "USD":
                        chip_label, chip_class = "미국 주식", "us"
                    else:
                        chip_label, chip_class = "국내 주식", "kr"

                    if abs(drift) < 1.0:
                        drift_class = "ok"
                    elif drift > 0:
                        drift_class = "over"
                    else:
                        drift_class = "under"

                    step_shares = 10000 if market == "CASH" else 1
                    shares_label = "보유 금액 (원)" if (market == "CASH" and currency == "KRW") else \
                                   "보유 금액 ($)" if market == "CASH" else "보유 수량 (주)"
                    price_extra = f"   ·   {currency} {h['price_native']:,.2f}" if currency != "KRW" else ""
                    market_tag = f"   ·   {market}" if (market and market not in ("CASH",)) else ""

                    with st.container(border=True):
                        # ── 1행: 종목 정보 + 삭제 버튼
                        head_l, head_r = st.columns([14, 1])
                        with head_l:
                            st.markdown(f"""
                            <div class="hc-head">
                              <div class="hc-name">{h['name']}</div>
                              <div class="hc-meta">
                                <span class="hc-chip {chip_class}">{chip_label}</span>
                                <span class="hc-code">{code}{market_tag}</span>
                                <span class="hc-price">현재가  ₩{price_krw:,.0f}{price_extra}</span>
                              </div>
                            </div>
                            """, unsafe_allow_html=True)
                        with head_r:
                            if st.button("✕", key=f"_del_{code}", help="이 종목 삭제"):
                                st.session_state.holdings = [x for x in st.session_state.holdings if x["code"] != code]
                                st.rerun()

                        # ── 2행: 보유 수량/금액 + 목표 비중
                        in1, in2 = st.columns(2)
                        with in1:
                            st.number_input(
                                shares_label,
                                value=int(h["shares"]),
                                min_value=0,
                                step=step_shares,
                                key=f"_shares_{code}",
                                on_change=_on_shares_change,
                                args=(code,),
                            )
                        with in2:
                            st.number_input(
                                "목표 비중 (%)",
                                value=float(h["target_pct"]),
                                min_value=0.0,
                                max_value=100.0,
                                step=0.5,
                                format="%.2f",
                                key=f"_target_{code}",
                                on_change=_on_target_change,
                                args=(code,),
                            )

                        # ── 3행: 통계 (평가금액 · 현재 비중 · 이탈)
                        st.markdown(f"""
                        <div class="hc-stats">
                          <div class="hc-stat">
                            <div class="hc-stat-label">평가 금액</div>
                            <div class="hc-stat-value">₩{val_krw:,.0f}</div>
                          </div>
                          <div class="hc-stat">
                            <div class="hc-stat-label">현재 비중</div>
                            <div class="hc-stat-value">{cur_pct:.2f}<span class="hc-stat-unit">%</span></div>
                          </div>
                          <div class="hc-stat">
                            <div class="hc-stat-label">목표 대비 이탈</div>
                            <div class="hc-stat-value drift-{drift_class}">{drift:+.2f}<span class="hc-stat-unit">%p</span></div>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

            # 섹션 종료 후 재계산
            target_sum = sum(h["target_pct"] for h in st.session_state.holdings)
            total_value = sum(
                h["shares"] * _to_krw(h["price_native"], h["currency"], fx)
                for h in st.session_state.holdings
            )

            if has_holdings:
                if abs(target_sum - 100.0) < 0.01:
                    pill_cls, label = "pill-primary", f"목표 합계 {target_sum:.2f}%"
                elif target_sum == 0:
                    pill_cls, label = "pill-muted", "목표 비율 미입력"
                else:
                    pill_cls, label = "pill-warn", f"목표 합계 {target_sum:.2f}% — 100% 필요"
                st.markdown(f'<div style="margin:14px 0 18px;"><span class="pill {pill_cls} pill-dot">{label}</span></div>', unsafe_allow_html=True)

    # ========================================================================
    # 자산 리밸런싱 계산 토글 ── STEP 01/02 입력 후 결과(STEP 03/04) 호출
    # ========================================================================
    if "show_results" not in st.session_state:
        st.session_state.show_results = False

    calc_disabled = (not has_holdings) or (abs(target_sum - 100.0) >= 0.01)

    if not st.session_state.show_results:
        st.markdown("""
        <div class="calc-cta">
          <div class="calc-cta__marker"></div>
          <span class="calc-cta__eyebrow">Ready to Calculate</span>
          <h3 class="calc-cta__title">자산 리밸런싱 계산</h3>
          <p class="calc-cta__sub">위 단계의 입력이 끝났다면 아래 버튼을 누르세요.</p>
          <p class="calc-cta__sub calc-cta__sub--next">종목별 <b>매수·매도 수량과 거래 금액</b>을 즉시 산출하고, <b>현 포트폴리오 구성</b>과 <b>리밸런싱 계획</b>이 함께 표시됩니다.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "자산 리밸런싱 계산   →",
            type="primary",
            use_container_width=True,
            disabled=calc_disabled,
            key="calc_run",
        ):
            st.session_state.show_results = True
            st.session_state._scroll_top = True
            st.rerun()

        if not has_holdings:
            st.caption("⚠  STEP 01에서 종목을 먼저 추가해 주세요.")
        elif abs(target_sum - 100.0) >= 0.01:
            st.caption(f"⚠  STEP 02 목표 비중 합계가 100% 여야 합니다 ── 현재 {target_sum:.2f}%")

        st.stop()

    # ── show_results == True : STEP 03, 04 표시 + 상단에 입력 수정 버튼
    # 진입 효과 ── 페이지 최상단 스크롤 + 메인 영역 안에 LIFEPLUS 모션 카드 (3초)
    if st.session_state.pop("_scroll_top", False):
        import streamlit.components.v1 as _components
        if LIFEPLUS_MOTION_B64:
            _components.html(
                f"""
                <script>
                  (function(){{
                      try {{
                          var win = window.parent || window;
                          var doc = win.document;
                          win.scrollTo({{ top: 0, behavior: 'instant' }});

                          // 기존 오버레이 정리
                          var prev = doc.getElementById('lifeplus-motion-overlay');
                          if (prev) prev.remove();

                          // 메인 영역 안 inline 오버레이 (사이드바·topbar 영향 없음)
                          var main = doc.querySelector('section[data-testid="stMain"]')
                                  || doc.querySelector('[data-testid="stMainBlockContainer"]');
                          if (!main) return;
                          if (win.getComputedStyle(main).position === 'static') {{
                              main.style.position = 'relative';
                          }}
                          var inner = main.querySelector('[data-testid="stMainBlockContainer"]') || main;

                          // 결과 페이지 콘텐츠는 일단 hidden + 살짝 아래
                          inner.style.opacity = '0';
                          inner.style.transform = 'translateY(18px) scale(0.99)';
                          inner.style.transformOrigin = 'top center';
                          inner.style.transition = 'opacity 0.7s cubic-bezier(0.22,1,0.36,1), transform 0.8s cubic-bezier(0.22,1,0.36,1)';
                          inner.style.willChange = 'opacity, transform';

                          // overlay ── 메인 영역 안 viewport-height 풀필
                          var ov = doc.createElement('div');
                          ov.id = 'lifeplus-motion-overlay';
                          ov.style.cssText = [
                              'position:absolute',
                              'top:0','left:0','right:0',
                              'height:100vh',
                              'background:radial-gradient(ellipse 80% 60% at 50% 50%, rgba(11,17,14,1) 0%, rgba(4,6,5,1) 100%)',
                              'z-index:50',
                              'display:flex','flex-direction:column','align-items:center','justify-content:center',
                              'pointer-events:auto','overflow:hidden',
                              'opacity:0','transition:opacity 0.35s ease-out'
                          ].join(';');

                          // 미세 grid texture
                          var grid = doc.createElement('div');
                          grid.style.cssText = [
                              'position:absolute','inset:0','pointer-events:none',
                              'background-image:linear-gradient(rgba(94,224,165,0.045) 1px, transparent 1px),linear-gradient(90deg, rgba(94,224,165,0.045) 1px, transparent 1px)',
                              'background-size:34px 34px',
                              '-webkit-mask-image:radial-gradient(ellipse 70% 60% at 50% 50%, #000 25%, transparent 90%)',
                              'mask-image:radial-gradient(ellipse 70% 60% at 50% 50%, #000 25%, transparent 90%)',
                              'opacity:0.7'
                          ].join(';');
                          ov.appendChild(grid);

                          // 상단 좌→우 emerald shimmer (페이지 전환 표식)
                          var topBar = doc.createElement('div');
                          topBar.style.cssText = [
                              'position:absolute','top:0','left:0','width:60%','height:1.5px',
                              'background:linear-gradient(90deg, transparent, rgba(28,158,110,0.6) 35%, #5ee0a5 50%, rgba(28,158,110,0.6) 65%, transparent)',
                              'animation:shimmer-x 2.6s ease-in-out infinite',
                              'box-shadow:0 0 14px rgba(94,224,165,0.7)',
                              'pointer-events:none'
                          ].join(';');
                          ov.appendChild(topBar);

                          // 좌측 emerald marker strip
                          var leftMarker = doc.createElement('div');
                          leftMarker.style.cssText = [
                              'position:absolute','left:0','top:18%','bottom:18%','width:2px',
                              'background:linear-gradient(180deg, #5ee0a5, #1c9e6e 50%, #0e5a3e)',
                              'box-shadow:0 0 18px rgba(28,158,110,0.7)',
                              'pointer-events:none'
                          ].join(';');
                          ov.appendChild(leftMarker);

                          // video frame card ── 둥근 카드 안에 video
                          var frame = doc.createElement('div');
                          frame.style.cssText = [
                              'position:relative',
                              'padding:0',
                              'border-radius:18px',
                              'overflow:hidden',
                              'background:#040605',
                              'border:1px solid rgba(28,158,110,0.55)',
                              'box-shadow:0 0 0 1px rgba(28,158,110,0.20), 0 0 56px -4px rgba(28,158,110,0.45), 0 0 120px 8px rgba(28,158,110,0.18), 0 24px 60px -16px rgba(0,0,0,0.65)',
                              'transform:scale(0.94)','opacity:0',
                              'transition:transform 0.55s cubic-bezier(0.22,1,0.36,1), opacity 0.55s ease-out',
                              'max-width:62%','max-height:72%','display:flex','align-items:center','justify-content:center'
                          ].join(';');

                          var vid = doc.createElement('video');
                          vid.src = 'data:video/mp4;base64,{LIFEPLUS_MOTION_B64}';
                          vid.autoplay = true;
                          vid.muted = true;
                          vid.playsInline = true;
                          vid.setAttribute('playsinline','');
                          vid.style.cssText = 'display:block;width:100%;height:auto;max-height:72vh;object-fit:contain;';
                          frame.appendChild(vid);

                          // 하단 캡션
                          var caption = doc.createElement('div');
                          caption.style.cssText = [
                              'position:absolute','bottom:6.5vh','left:50%','transform:translateX(-50%)',
                              'font-family:LIFEPLUS, sans-serif','font-size:10.5px','font-weight:800',
                              'letter-spacing:0.28em','text-transform:uppercase',
                              'color:#5ee0a5','opacity:0',
                              'transition:opacity 0.5s ease-out 0.4s',
                              'display:inline-flex','align-items:center','gap:10px',
                              'padding:6px 14px 6px 12px',
                              'background:rgba(28,158,110,0.10)','border:1px solid rgba(28,158,110,0.32)',
                              'border-radius:999px','backdrop-filter:blur(8px)'
                          ].join(';');
                          caption.innerHTML = '<span style="width:6px;height:6px;border-radius:50%;background:#5ee0a5;box-shadow:0 0 0 3px rgba(28,158,110,0.2),0 0 10px #5ee0a5;"></span>CALCULATING REBALANCE PLAN';
                          ov.appendChild(caption);

                          ov.appendChild(frame);
                          main.appendChild(ov);

                          // 페이드 인 + frame 등장
                          requestAnimationFrame(function(){{
                              ov.style.opacity = '1';
                              requestAnimationFrame(function(){{
                                  frame.style.opacity = '1';
                                  frame.style.transform = 'scale(1)';
                                  caption.style.opacity = '1';
                              }});
                          }});

                          var dismissed = false;
                          function dismiss() {{
                              if (dismissed) return;
                              dismissed = true;
                              // frame 살짝 축소 + 페이드 + overlay 페이드
                              frame.style.transform = 'scale(0.97)';
                              frame.style.opacity = '0';
                              caption.style.opacity = '0';
                              ov.style.opacity = '0';
                              // 결과 페이지 등장
                              requestAnimationFrame(function(){{
                                  inner.style.opacity = '1';
                                  inner.style.transform = 'translateY(0) scale(1)';
                              }});
                              setTimeout(function(){{
                                  if (ov.parentNode) ov.parentNode.removeChild(ov);
                                  inner.style.willChange = '';
                              }}, 650);
                          }}
                          vid.addEventListener('ended', dismiss);
                          vid.addEventListener('error', dismiss);
                          // 클릭으로 스킵
                          ov.addEventListener('click', dismiss);
                          // 안전장치 ── 최대 5초 후 강제 종료
                          setTimeout(dismiss, 5000);
                      }} catch (e) {{}}
                  }})();
                </script>
                """,
                height=0,
            )
        else:
            # mp4 로드 실패 fallback ── 스크롤만
            _components.html(
                """
                <script>
                  (function(){
                      try {
                          var win = window.parent || window;
                          win.scrollTo({ top: 0, behavior: 'smooth' });
                      } catch (e) {}
                  })();
                </script>
                """,
                height=0,
            )

    back_l, _back_r = st.columns([1, 4])
    with back_l:
        if st.button("← 입력 다시 수정", key="calc_back", use_container_width=True):
            st.session_state.show_results = False
            st.session_state._scroll_top = True
            st.rerun()

    # ========================================================================
    # STEP 03 — 현 포트폴리오 구성
    # ========================================================================
    with st.container(border=True):
        st.markdown("""
        <div class="step-card-header">
          <div class="step-num">03</div>
          <div class="step-info">
            <h2 class="step-title">현 포트폴리오 구성</h2>
            <p class="step-sub">현재 비율과 목표 비율의 차이를 한눈에 확인합니다. 국장·미장 분포와 종목별 이탈도 함께 표시됩니다.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if total_value <= 0:
            cc1, cc2 = st.columns([1, 1.3])
            with cc1:
                placeholder = go.Figure(data=[go.Pie(
                    labels=["—"], values=[1], hole=0.68, sort=False,
                    marker=dict(colors=[C.SURFACE_3], line=dict(color=C.SURFACE, width=2)),
                    textinfo="none", hoverinfo="skip",
                )])
                placeholder.add_annotation(
                    text=f"<span style='font-size:13px; color:{C.MUTED};'>비율이 여기에<br>표시됩니다</span>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(family="LIFEPLUS, sans-serif", color=C.MUTED),
                )
                placeholder.update_layout(showlegend=False)
                st.plotly_chart(style_fig(placeholder, title="현재 비율", height=400), use_container_width=True)
            with cc2:
                st.markdown("""
                <div class="empty-state" style="padding:48px 32px; min-height:340px; display:flex; flex-direction:column; justify-content:center;">
                  <div class="empty-title">시각화 미리보기</div>
                  <div class="empty-body">
                    종목을 추가하고 보유 수량을 입력하면<br>
                    도넛 차트와 목표 대비 이탈 차트가 표시됩니다.
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            alloc = []
            kr_value = 0.0
            us_value = 0.0
            kr_count = 0
            us_count = 0
            for h in st.session_state.holdings:
                v = h["shares"] * _to_krw(h["price_native"], h["currency"], fx)
                cur_pct = v / total_value * 100 if total_value > 0 else 0
                if h["currency"] == "USD":
                    us_value += v
                    if v > 0: us_count += 1
                else:
                    kr_value += v
                    if v > 0: kr_count += 1
                if v <= 0 and h["target_pct"] <= 0:
                    continue
                alloc.append({
                    "name": h["name"], "code": h["code"],
                    "value": v, "current": cur_pct, "target": h["target_pct"],
                    "drift": cur_pct - h["target_pct"],
                    "currency": h["currency"],
                })
            df_alloc = pd.DataFrame(alloc)

            # 국장 / 미장 분리 카드
            kr_pct = (kr_value / total_value * 100) if total_value > 0 else 0
            us_pct = (us_value / total_value * 100) if total_value > 0 else 0
            st.markdown(f"""
            <div class="market-split">
              <div class="market-split__card kr">
                <div class="market-split__left">
                  <div class="market-split__label">국장 · 국내 주식 · ETF</div>
                  <div class="market-split__title">KOSPI · KOSDAQ · ETF</div>
                  <div class="market-split__sub">{kr_count}개 종목</div>
                </div>
                <div class="market-split__right">
                  <div class="market-split__percent">{kr_pct:.1f}%</div>
                  <div class="market-split__amount">₩{kr_value:,.0f}</div>
                </div>
              </div>
              <div class="market-split__card us">
                <div class="market-split__left">
                  <div class="market-split__label">미장 · 미국 주식</div>
                  <div class="market-split__title">NYSE · NASDAQ</div>
                  <div class="market-split__sub">{us_count}개 종목</div>
                </div>
                <div class="market-split__right">
                  <div class="market-split__percent">{us_pct:.1f}%</div>
                  <div class="market-split__amount">₩{us_value:,.0f}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            cc1, cc2 = st.columns([1, 1.3])

            with cc1:
                donut = go.Figure(data=[go.Pie(
                    labels=df_alloc["name"],
                    values=df_alloc["value"],
                    hole=0.68,
                    sort=False,
                    marker=dict(
                        colors=["#1c9e6e", "#6ba1c8", "#c89968", "#5ee0a5", "#3d7faf",
                                "#d9b487", "#22b07e", "#8fc0e0", "#a07a4c", "#0e5a3e"],
                        line=dict(color=C.SURFACE, width=2),
                    ),
                    textfont=dict(color=C.PRIMARY_INK, size=11, family="LIFEPLUS, sans-serif"),
                    textinfo="percent",
                    textposition="inside",
                    insidetextorientation="radial",
                    hovertemplate="<b>%{label}</b><br>₩%{value:,.0f}<br>%{percent}<extra></extra>",
                )])
                donut.add_annotation(
                    text=f"<span style='font-size:11px;color:{C.MUTED};'>총자산</span><br>"
                         f"<b style='color:{C.TEXT};font-size:20px;letter-spacing:-0.02em;'>₩{total_value/1e6:,.1f}M</b><br>"
                         f"<span style='font-size:11px;color:{C.MUTED};'>{len(df_alloc)}개 종목</span>",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(family="LIFEPLUS, sans-serif", color=C.TEXT),
                )
                donut.update_layout(
                    showlegend=True,
                    legend=dict(orientation="v", x=1.02, y=0.5, yanchor="middle", font=dict(size=11)),
                )
                st.plotly_chart(style_fig(donut, title="현재 비율", height=400), use_container_width=True)

            with cc2:
                if abs(target_sum - 100.0) < 0.01:
                    df_sorted = df_alloc.sort_values("drift", ascending=True).reset_index(drop=True)

                    def _color(d):
                        if abs(d) < 1.0:
                            return "#5ee0a5"
                        if d > 0:
                            return C.SELL if abs(d) >= 5 else C.WARN
                        return C.PRIMARY if abs(d) >= 5 else C.PRIMARY_DIM
                    colors = [_color(d) for d in df_sorted["drift"]]

                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        y=df_sorted["name"],
                        x=df_sorted["drift"],
                        orientation="h",
                        marker=dict(color=colors, line=dict(color=C.SURFACE, width=1)),
                        text=df_sorted["drift"].apply(lambda d: f"{d:+.2f}%"),
                        textposition="outside",
                        textfont=dict(family="LIFEPLUS, sans-serif", color=C.TEXT, size=11),
                        hovertemplate="<b>%{y}</b><br>이탈도: %{x:+.2f}%<extra></extra>",
                    ))
                    fig.add_vline(x=0, line=dict(color=C.BORDER_STRONG, width=1, dash="dot"))
                    fig.update_layout(
                        xaxis=dict(
                            title=dict(text="← 부족   ·   초과 →", font=dict(size=11, color=C.MUTED)),
                            ticksuffix="%", zeroline=True,
                        ),
                        yaxis=dict(autorange="reversed", title=None),
                        showlegend=False,
                    )
                    st.plotly_chart(style_fig(fig, title="목표 대비 이탈", height=400), use_container_width=True)
                else:
                    bar = go.Figure()
                    bar.add_trace(go.Bar(
                        x=df_alloc["name"], y=df_alloc["current"],
                        name="현재", marker_color=C.PRIMARY_DIM,
                        text=df_alloc["current"].apply(lambda x: f"{x:.1f}%"),
                        textposition="outside",
                        textfont=dict(color=C.TEXT_2, size=10, family="LIFEPLUS, sans-serif"),
                    ))
                    bar.add_trace(go.Bar(
                        x=df_alloc["name"], y=df_alloc["target"],
                        name="목표", marker_color=C.PRIMARY_HOVER,
                        text=df_alloc["target"].apply(lambda x: f"{x:.1f}%"),
                        textposition="outside",
                        textfont=dict(color=C.PRIMARY_HOVER, size=10, family="LIFEPLUS, sans-serif"),
                    ))
                    bar.update_layout(
                        barmode="group", bargap=0.3,
                        yaxis=dict(ticksuffix="%"),
                        legend=dict(orientation="h", y=-0.18),
                    )
                    st.plotly_chart(style_fig(bar, title="현재 vs 목표 비율", height=400), use_container_width=True)

    # ========================================================================
    # STEP 04 — 리밸런싱 계획 (서비스 핵심 · primary variant)
    # ========================================================================
    with st.container(border=True, key="step_04_card"):
        st.markdown("""
        <div class="step-card-header step-card-primary">
          <div class="step-num">04</div>
          <div class="step-info">
            <h2 class="step-title">리밸런싱 수량</h2>
            <p class="step-sub">목표 비중에 맞춰 종목별 <b>매수·매도 수량</b>을 자동 산출합니다.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("거래 조건 설정 (선택)", expanded=False):
            pc1, pc2 = st.columns([1, 1])
            with pc1:
                additional_cash = st.number_input(
                    "추가 입금액 (원)",
                    min_value=0, value=0, step=10_000,
                    help="현재 자산 외에 추가로 투입할 현금이 있다면 입력하세요",
                )
            with pc2:
                min_trade = st.number_input(
                    "최소 거래 금액 (원)",
                    min_value=0, value=0, step=10_000,
                    help="이 금액 미만의 작은 거래는 자동으로 제외됩니다",
                )

            round_mode = st.radio(
                "수량 처리 방식",
                options=["round", "floor", "ceil"],
                format_func=lambda x: {"round": "반올림 (균형)", "floor": "내림 (보수적)", "ceil": "올림 (적극적)"}[x],
                horizontal=True, label_visibility="visible",
            )

        if not has_holdings:
            st.markdown("""
            <div class="empty-state">
              <div class="empty-title">계산 결과 미리보기</div>
              <div class="empty-body">
                종목을 추가하고 목표 비율을 설정하면<br>
                매수·매도 수량과 거래 금액이 종목별로 자동 계산됩니다.
              </div>
            </div>
            """, unsafe_allow_html=True)
        elif abs(target_sum - 100.0) >= 0.01:
            st.markdown(f"""
            <div class="empty-state">
              <div class="empty-title">목표 비율 설정이 필요합니다</div>
              <div class="empty-body">
                리밸런싱 계산을 시작하려면 모든 종목의 목표 비율 합계가 100%가 되어야 합니다.<br>
                현재 합계는 <b style="color:{C.WARN};">{target_sum:.2f}%</b>입니다.
                위에서 <span class="code-inline">균등 배분</span> 또는 <span class="code-inline">현재 비율로</span> 버튼으로 빠르게 설정할 수 있습니다.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            total_target = total_value + additional_cash

            plan_rows = []
            for h in st.session_state.holdings:
                price_krw = _to_krw(h["price_native"], h["currency"], fx)
                cur_v = h["shares"] * price_krw
                tgt_v = total_target * h["target_pct"] / 100.0
                diff_v = tgt_v - cur_v
                if price_krw <= 0:
                    shares_diff = 0
                else:
                    raw = diff_v / price_krw
                    if round_mode == "round":
                        shares_diff = int(round(raw))
                    elif round_mode == "floor":
                        shares_diff = int(raw) if raw >= 0 else -int(-raw)
                    else:
                        shares_diff = math.ceil(raw) if raw >= 0 else -math.ceil(-raw)

                trade_amount = abs(shares_diff) * price_krw
                if trade_amount < min_trade:
                    shares_diff = 0
                    trade_amount = 0

                if shares_diff > 0:
                    action = "매수"
                elif shares_diff < 0:
                    action = "매도"
                else:
                    action = "유지"
                plan_rows.append({
                    "name": h["name"], "code": h["code"], "market": h["market"],
                    "current": h["shares"], "target": h["shares"] + shares_diff,
                    "action": action,
                    "qty": abs(shares_diff),
                    "amount": trade_amount,
                    "cur_v": cur_v, "tgt_v": tgt_v, "diff_v": diff_v,
                })
            df_plan = pd.DataFrame(plan_rows)

            buy_total = df_plan.loc[df_plan["action"] == "매수", "amount"].sum()
            sell_total = df_plan.loc[df_plan["action"] == "매도", "amount"].sum()
            net_cash = buy_total - sell_total
            remaining = additional_cash - net_cash

            st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

            oc1, oc2 = st.columns(2)

            def _order_row(row, side):
                cls = "buy" if side == "매수" else "sell"
                side_kor = "매수" if side == "매수" else "매도"
                return f"""
                <div class="order-row {cls}">
                  <div>
                    <div>
                      <span class="order-name">{row['name']}</span>
                      <span class="order-code">{row['code']} · {row['market']}</span>
                    </div>
                    <div class="order-side {cls}">{side_kor}</div>
                  </div>
                  <div class="order-right">
                    <div class="order-qty">{int(row['qty']):,}<span class="unit">주</span></div>
                    <div class="order-amount">₩{row['amount']:,.0f}</div>
                  </div>
                </div>
                """

            with oc1:
                st.markdown(f'<div style="font-size:14px; font-weight:600; color:{C.PRIMARY_HOVER}; margin-bottom:12px;">매수 주문</div>', unsafe_allow_html=True)
                buys = df_plan[df_plan["action"] == "매수"]
                if buys.empty:
                    st.markdown('<div class="note" style="padding:18px; background:'+C.SURFACE+'; border:1px solid '+C.BORDER+'; border-radius:12px;">매수할 종목이 없습니다.</div>', unsafe_allow_html=True)
                else:
                    for _, r in buys.iterrows():
                        st.markdown(_order_row(r, "매수"), unsafe_allow_html=True)

            with oc2:
                st.markdown(f'<div style="font-size:14px; font-weight:600; color:{C.SELL}; margin-bottom:12px;">매도 주문</div>', unsafe_allow_html=True)
                sells = df_plan[df_plan["action"] == "매도"]
                if sells.empty:
                    st.markdown('<div class="note" style="padding:18px; background:'+C.SURFACE+'; border:1px solid '+C.BORDER+'; border-radius:12px;">매도할 종목이 없습니다.</div>', unsafe_allow_html=True)
                else:
                    for _, r in sells.iterrows():
                        st.markdown(_order_row(r, "매도"), unsafe_allow_html=True)

            with st.expander("상세 내역 보기", expanded=True):
                df_view = df_plan.copy().rename(columns={
                    "name": "종목명", "code": "코드", "market": "시장",
                    "action": "액션",
                    "current": "현재 수량", "target": "목표 수량",
                    "qty": "거래 수량", "amount": "거래 금액",
                    "cur_v": "현재 평가", "tgt_v": "목표 평가", "diff_v": "차액",
                })

                def _style_action(v):
                    if v == "매수":
                        return f"background-color: rgba(16,185,129,0.10); color: {C.PRIMARY_HOVER}; font-weight: 600;"
                    if v == "매도":
                        return f"background-color: rgba(248,113,113,0.10); color: {C.SELL}; font-weight: 600;"
                    return f"color: {C.MUTED};"

                st.dataframe(
                    df_view[["종목명", "코드", "시장", "액션", "현재 수량", "목표 수량", "거래 수량", "거래 금액", "현재 평가", "목표 평가", "차액"]]
                        .style.format({
                            "거래 금액": "₩{:,.0f}",
                            "현재 평가": "₩{:,.0f}",
                            "목표 평가": "₩{:,.0f}",
                            "차액": "₩{:+,.0f}",
                        })
                        .applymap(_style_action, subset=["액션"]),
                    hide_index=True,
                    use_container_width=True,
                )

            if net_cash > additional_cash:
                st.warning(f"입금 예정 금액보다 ₩{net_cash - additional_cash:,.0f} 더 필요합니다. 추가 입금을 늘리거나 목표 비율을 조정해 보세요.")
            elif net_cash < additional_cash and additional_cash > 0:
                st.info(f"리밸런싱 후 ₩{additional_cash - net_cash:,.0f}이 현금으로 남습니다. 다음 매수에 활용할 수 있습니다.")

    # ========================================================================
    # Footer
    # ========================================================================
    st.markdown(f"""
    <div class="app-footer">
      <div class="app-footer__left">
        <div class="app-footer__mark"></div>
        <div class="app-footer__brand">
          <b>한화손해보험 LIFEPLUS</b> · 포트폴리오 리밸런싱 도구
        </div>
      </div>
      <div class="app-footer__meta">
        <span>v1.0.0</span>
        <span>박무성 사원 · 010-9920-6171</span>
        <span>USD/KRW ₩{fx:,.2f}</span>
      </div>
    </div>
    <div class="app-footer__disclaimer">
      본 도구는 LIFEPLUS 부문 구성원의 개인 자산 관리 편의를 위해 제작된 내부 참고용 서비스입니다.
      시세는 종가 기준이며, 실제 매매 결과와 차이가 있을 수 있습니다. 투자 결정의 책임은 사용자 본인에게 있으며, 회사는 어떠한 손해에 대해서도 책임을 지지 않습니다.
    </div>
    """, unsafe_allow_html=True)
