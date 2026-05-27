"""주식 데이터 조회 모듈

한국 주식: FinanceDataReader (KOSPI/KOSDAQ 종목 검색 + 시세)
미국 주식: yfinance (티커 검색 + 시세)
환율: yfinance USDKRW=X
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st


_KRX_CSV_PATH = Path(__file__).parent / "data" / "krx_listing.csv"


# ---------------------------------------------------------------------------
# 한국 주식
# ---------------------------------------------------------------------------

def _pick_col(df: pd.DataFrame, candidates: tuple[str, ...], fallback_idx: int = 0) -> str:
    for c in candidates:
        if c in df.columns:
            return c
    return df.columns[fallback_idx]


@st.cache_data(ttl=60 * 60 * 12, show_spinner=False)
def load_krx_listing(force_refresh: bool = False) -> pd.DataFrame:
    """KOSPI + KOSDAQ + ETF 전체 종목 리스트를 반환한다.

    force_refresh=False이고 번들된 CSV(`data/krx_listing.csv`)가 존재하면
    CSV에서 즉시 로드한다. CSV가 없거나 손상되었거나, 사용자가 강제 갱신을
    요청하면 FinanceDataReader에서 새로 다운로드한다.
    """
    if not force_refresh and _KRX_CSV_PATH.exists():
        try:
            df = pd.read_csv(_KRX_CSV_PATH, dtype={"Code": str})
            df["Code"] = df["Code"].astype(str).str.zfill(6)
            df["Name"] = df["Name"].astype(str)
            df["Market"] = df["Market"].astype(str)
            if not df.empty:
                return df.reset_index(drop=True)
        except Exception:
            pass

    import FinanceDataReader as fdr

    frames: list[pd.DataFrame] = []

    # 1) 일반 주식: KOSPI / KOSDAQ
    for market in ("KOSPI", "KOSDAQ"):
        try:
            df = fdr.StockListing(market)
        except Exception:
            continue
        df = df.rename(columns={c: c.strip() for c in df.columns})
        code_col = _pick_col(df, ("Code", "Symbol"), 0)
        name_col = _pick_col(df, ("Name",), 1)
        frames.append(pd.DataFrame({
            "Code": df[code_col].astype(str).str.zfill(6),
            "Name": df[name_col].astype(str),
            "Market": market,
        }))

    # 2) ETF (KODEX, TIGER, PLUS, ACE, RISE, SOL, KOSEF, ...)
    etf_loaded = False
    for key in ("ETF/KR", "KRX-ETF"):
        try:
            etf = fdr.StockListing(key)
            etf = etf.rename(columns={c: c.strip() for c in etf.columns})
            code_col = _pick_col(etf, ("Symbol", "Code"), 0)
            name_col = _pick_col(etf, ("Name",), 1)
            frames.append(pd.DataFrame({
                "Code": etf[code_col].astype(str).str.zfill(6),
                "Name": etf[name_col].astype(str),
                "Market": "ETF",
            }))
            etf_loaded = True
            break
        except Exception:
            continue

    # 3) ETF 로드가 실패했으면 KRX 전체 리스트에서 보충 (ETF/ETN/리츠 등 포함)
    if not etf_loaded:
        try:
            krx = fdr.StockListing("KRX")
            krx = krx.rename(columns={c: c.strip() for c in krx.columns})
            code_col = _pick_col(krx, ("Code", "Symbol"), 0)
            name_col = _pick_col(krx, ("Name",), 1)
            # 기존 KOSPI/KOSDAQ 코드 제외 (남은 게 ETF/ETN/리츠 등)
            existing_codes = set()
            for f in frames:
                existing_codes.update(f["Code"].tolist())
            extra = pd.DataFrame({
                "Code": krx[code_col].astype(str).str.zfill(6),
                "Name": krx[name_col].astype(str),
                "Market": "ETF/기타",
            })
            extra = extra[~extra["Code"].isin(existing_codes)]
            frames.append(extra)
        except Exception:
            pass

    if not frames:
        return pd.DataFrame(columns=["Code", "Name", "Market"])

    merged = pd.concat(frames, ignore_index=True)
    # 동일 코드가 여러 시장으로 중복될 경우 최초 등장만 유지 (KOSPI 우선)
    merged = merged.drop_duplicates(subset=["Code"], keep="first").reset_index(drop=True)

    # 강제 갱신으로 새로 받은 결과는 번들 CSV에 덮어써서, 이후 기본 호출
    # (force_refresh=False) 도 동일한 최신 데이터를 보도록 한다.
    if force_refresh:
        try:
            _KRX_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
            merged.to_csv(_KRX_CSV_PATH, index=False, encoding="utf-8-sig")
        except Exception:
            pass

    return merged


def search_kr_stocks(query: str, listing: pd.DataFrame, limit: int = 30) -> list[dict]:
    """이름 또는 코드 일부로 한국 종목 검색 (주식 + ETF)."""
    if not query:
        return []
    q = query.strip()
    name_mask = listing["Name"].str.contains(q, case=False, na=False, regex=False)
    code_mask = listing["Code"].str.contains(q, na=False, regex=False)
    hits = listing[name_mask | code_mask]
    # 이름이 검색어로 시작하는 항목을 우선 노출
    starts = hits["Name"].str.lower().str.startswith(q.lower(), na=False)
    hits = pd.concat([hits[starts], hits[~starts]], ignore_index=True)
    return hits.head(limit).to_dict("records")


_MARKET_SUFFIX = {"KOSPI": ".KS", "KOSDAQ": ".KQ"}


@st.cache_data(ttl=60, show_spinner=False)
def get_kr_price(code: str, market: str = "") -> Optional[float]:
    """한국 종목 최근 종가.

    Streamlit Cloud 환경에서 FinanceDataReader가 KRX/Naver 접근에 실패하는 경우가
    있어 yfinance(.KS/.KQ 접미사)를 먼저 시도하고, 실패 시 FDR로 폴백한다.
    """
    import yfinance as yf

    suffix = _MARKET_SUFFIX.get(market.upper())
    tickers = [f"{code}{suffix}"] if suffix else [f"{code}.KS", f"{code}.KQ"]

    for ticker in tickers:
        try:
            hist = yf.Ticker(ticker).history(period="5d")
            if hist is not None and not hist.empty:
                return float(hist["Close"].iloc[-1])
        except Exception:
            continue

    try:
        import FinanceDataReader as fdr

        end = _dt.date.today()
        start = end - _dt.timedelta(days=14)
        df = fdr.DataReader(code, start=start, end=end)
        if df is not None and not df.empty:
            return float(df["Close"].iloc[-1])
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# 미국 주식
# ---------------------------------------------------------------------------

@st.cache_data(ttl=60, show_spinner=False)
def get_us_price(ticker: str) -> Optional[float]:
    """미국 종목 최근 종가 (USD)."""
    import yfinance as yf

    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="5d")
        if hist is not None and not hist.empty:
            return float(hist["Close"].iloc[-1])
        info = getattr(t, "fast_info", None)
        if info is not None:
            for key in ("last_price", "lastPrice", "regular_market_price"):
                v = getattr(info, key, None) if not isinstance(info, dict) else info.get(key)
                if v:
                    return float(v)
    except Exception:
        return None
    return None


@st.cache_data(ttl=60 * 30, show_spinner=False)
def search_us_stocks(query: str, limit: int = 10) -> list[dict]:
    """미국 종목 검색. yfinance.Search가 있으면 사용, 없으면 티커 직접 조회로 폴백."""
    if not query:
        return []
    q = query.strip().upper()
    results: list[dict] = []

    # 1) yfinance Search API (신버전)
    try:
        import yfinance as yf
        if hasattr(yf, "Search"):
            s = yf.Search(query, max_results=limit, news_count=0)
            for quote in (s.quotes or []):
                sym = quote.get("symbol")
                if not sym:
                    continue
                name = quote.get("longname") or quote.get("shortname") or sym
                exch = quote.get("exchange") or quote.get("exchDisp") or "US"
                # ETF 또는 EQUITY만 (미국 시장 우선)
                qt = (quote.get("quoteType") or "").upper()
                if qt and qt not in ("EQUITY", "ETF"):
                    continue
                results.append({"Code": sym, "Name": name, "Market": exch})
            if results:
                return results[:limit]
    except Exception:
        pass

    # 2) 폴백: 입력 자체를 티커로 검증
    price = get_us_price(q)
    if price is not None:
        try:
            import yfinance as yf
            info = yf.Ticker(q).info or {}
            name = info.get("longName") or info.get("shortName") or q
        except Exception:
            name = q
        results.append({"Code": q, "Name": name, "Market": "US"})

    return results


# ---------------------------------------------------------------------------
# 환율
# ---------------------------------------------------------------------------

@st.cache_data(ttl=60 * 60, show_spinner=False)
def get_usd_krw_rate() -> float:
    """USD/KRW 환율. 실패 시 기본값 1350."""
    import yfinance as yf

    try:
        hist = yf.Ticker("USDKRW=X").history(period="5d")
        if hist is not None and not hist.empty:
            return float(hist["Close"].iloc[-1])
    except Exception:
        pass
    return 1350.0
