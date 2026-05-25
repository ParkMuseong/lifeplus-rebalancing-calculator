"""KRX 종목 리스트 스냅샷 생성기.

사용법:
    python scripts/refresh_krx_listing.py

repo 루트의 `data/krx_listing.csv`를 최신 KRX 데이터로 덮어쓴다.
신규 상장/상장폐지 반영이 필요할 때 로컬에서 실행 후 커밋한다.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from stock_api import load_krx_listing  # noqa: E402


def main() -> int:
    out_path = REPO_ROOT / "data" / "krx_listing.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[1/2] KRX에서 최신 종목 리스트 다운로드 중...")
    df = load_krx_listing(force_refresh=True)
    if df is None or df.empty:
        print("[ERROR] 종목 리스트가 비어있음. 네트워크 또는 FDR 응답 확인 필요.")
        return 1

    print(f"[2/2] CSV 저장: {out_path} ({len(df):,}건)")
    df.to_csv(out_path, index=False, encoding="utf-8")

    by_market = df["Market"].value_counts().to_dict()
    print("\n시장별 종목 수:")
    for market, count in by_market.items():
        print(f"  {market}: {count:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
