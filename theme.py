"""디자인 시스템 — Sovereign Forest

Stripe · Linear · Mercury · Wealthfront 류의 정제된 다크 emerald.
색감 철학: 95% 카본 그레이 · 5% sovereign green 액센트.
타이포: LIFEPLUS OTF (Bold / Medium / Light) — 위계별 weight 매핑.
"""
from __future__ import annotations

import base64
from pathlib import Path

import plotly.graph_objects as go


# ============================================================================
# Font loader — LIFEPLUS OTF (Bold / Medium / Light)
# 위계 매핑: Bold(700) = 타이틀·강조 / Medium(500) = 본문·라벨 / Light(300) = 부제
# ============================================================================
_FONT_DIR = Path(__file__).parent / "assets" / "fonts"
_FONT_FILES = {
    300: "LIFEPLUS OTF Light.otf",
    500: "LIFEPLUS OTF Medium.otf",
    700: "LIFEPLUS OTF Bold.otf",
}


def _load_font_b64(filename: str) -> str:
    try:
        return base64.b64encode((_FONT_DIR / filename).read_bytes()).decode("ascii")
    except Exception:
        return ""


def _font_face_block() -> str:
    blocks = []
    for weight, fname in _FONT_FILES.items():
        b64 = _load_font_b64(fname)
        if not b64:
            continue
        blocks.append(
            f"@font-face {{"
            f" font-family: 'LIFEPLUS';"
            f" src: url(data:font/otf;base64,{b64}) format('opentype');"
            f" font-weight: {weight};"
            f" font-style: normal;"
            f" font-display: block;"
            f" }}"
        )
    return "\n".join(blocks)


# 폰트 스택: LIFEPLUS 전용. 로드 실패 시에만 generic sans-serif 로 폴백.
FONT_SANS = "'LIFEPLUS', sans-serif"
FONT_NUMERIC = "'LIFEPLUS', sans-serif"


class C:
    """Design Tokens — Sovereign Forest financial design system.

    Color philosophy
        70% neutral · 25% primary surface · 5% accent
        Green chosen for trust/stability; bronze used <5% as premium signal.
    """

    # === Surface — 8-tier neutral scale (true carbon greys with hint of warmth) ===
    BG = "#04060500"            # transparent (used with body radial gradient)
    BG_BASE = "#040605"         # 1000 — page background (deepest)
    BG_2 = "#070b09"            # 950 — recessed
    SURFACE = "#0b110e"         # 900 — card surface
    SURFACE_2 = "#101713"       # 800 — elevated card
    SURFACE_3 = "#161e19"       # 700 — highlighted card
    SURFACE_4 = "#1d2721"       # 600 — interactive state
    SURFACE_5 = "#26302a"       # 500 — focus / active

    # === Borders — 3-tier divider system ===
    BORDER = "#161f1b"          # default divider
    BORDER_STRONG = "#202c26"   # card edge / hover
    BORDER_STRONGER = "#33403a" # active / focused
    BORDER_PRIMARY = "rgba(28, 158, 110, 0.32)"
    BORDER_PRIMARY_STRONG = "rgba(34, 176, 126, 0.52)"

    # === PRIMARY — Sovereign Forest (refined) ===
    # HSL(157°, 70%, 25%) — saturated, deep, trust-coded
    PRIMARY = "#136f4d"             # 메인 브랜드
    PRIMARY_HOVER = "#1c9e6e"       # interactive hover
    PRIMARY_DIM = "#0e5a3e"         # darker variant
    PRIMARY_DEEP = "#03241a"        # ultra-dark bg tint
    PRIMARY_DARKER = "#011a12"      # deepest emerald shadow
    PRIMARY_INK = "#f0f6f3"         # text on primary surfaces
    PRIMARY_SOFT = "rgba(28, 158, 110, 0.08)"
    PRIMARY_SOFTER = "rgba(28, 158, 110, 0.04)"
    PRIMARY_GLOW = "rgba(28, 158, 110, 0.22)"
    PRIMARY_BRIGHT = "#22b07e"      # highlight on dark surface
    PRIMARY_GLINT = "#5ee0a5"       # premium highlight (sparingly)

    # === BRONZE — premium accent (보색, <5% usage) ===
    BRONZE = "#c89968"              # warm bronze
    BRONZE_DIM = "#a07a4c"          # darker variant
    BRONZE_SOFT = "rgba(200, 153, 104, 0.08)"
    BRONZE_GLOW = "rgba(200, 153, 104, 0.22)"

    # === Text — 4-tier scale ===
    TEXT = "#f3f7f4"                # primary
    TEXT_2 = "#cad6cf"              # secondary
    MUTED = "#869691"               # tertiary / labels
    MUTED_DEEP = "#566460"          # quaternary / metadata
    MUTED_DEEPER = "#3a4540"        # ghosted / placeholder

    # === Status — refined sophistication ===
    BUY = "#1c9e6e"
    SELL = "#c25462"                # refined red (less saturation)
    HOLD = "#869691"
    WARN = "#c89968"                # uses bronze (intentional unification)
    INFO = "#4082c4"

    # === Market secondary (US) — sophisticated slate ===
    US_PRIMARY = "#3d7faf"
    US_BRIGHT = "#6ba1c8"
    US_SOFT = "rgba(107, 161, 200, 0.10)"


PLOTLY_PALETTE = [
    "#136f4d", "#1c9e6e", "#22b07e", "#42c294", "#65d1aa",
    "#0e5a3e", "#0a4830", "#26876c", "#3a957a", "#558e7b",
]


def style_fig(fig: go.Figure, *, title: str | None = None, height: int | None = None) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=C.TEXT, family="LIFEPLUS, sans-serif", size=12),
        colorway=PLOTLY_PALETTE,
        margin=dict(l=24, r=24, t=64 if title else 24, b=28),
        legend=dict(
            font=dict(color=C.TEXT_2, size=11.5),
            bgcolor="rgba(0,0,0,0)",
            bordercolor=C.BORDER,
            borderwidth=0,
        ),
        xaxis=dict(
            gridcolor=C.BORDER, zerolinecolor=C.BORDER_STRONG,
            color=C.MUTED, linecolor=C.BORDER,
            tickfont=dict(size=11, color=C.MUTED),
        ),
        yaxis=dict(
            gridcolor=C.BORDER, zerolinecolor=C.BORDER_STRONG,
            color=C.MUTED, linecolor=C.BORDER,
            tickfont=dict(size=11, color=C.MUTED),
        ),
        hoverlabel=dict(
            bgcolor=C.SURFACE_3,
            bordercolor=C.BORDER_STRONGER,
            font=dict(color=C.TEXT, family="LIFEPLUS, sans-serif", size=12),
        ),
    )
    if title:
        fig.update_layout(title=dict(
            text=(
                f"<span style='color:{C.MUTED};font-size:10px;font-weight:700;"
                f"letter-spacing:0.18em;text-transform:uppercase;'>"
                f"&#9642;&nbsp;&nbsp;{title}</span>"
            ),
            x=0.0, xanchor="left", y=0.97,
            font=dict(color=C.MUTED, size=11, family="LIFEPLUS, sans-serif"),
        ))
    if height:
        fig.update_layout(height=height)
    return fig


# ============================================================================
# CSS — Sovereign Forest design system
# Naming convention: kebab-case BEM-ish. Tokens are interpolated via {C.X}.
# ============================================================================
CSS = f"""
<style>
{_font_face_block()}

:root {{
    --font-sans: {FONT_SANS};
    --font-numeric: {FONT_NUMERIC};
    --fw-light: 300;
    --fw-medium: 500;
    --fw-bold: 700;
    --bg: {C.BG_BASE};
    --bg-2: {C.BG_2};
    --surface: {C.SURFACE};
    --surface-2: {C.SURFACE_2};
    --surface-3: {C.SURFACE_3};
    --surface-4: {C.SURFACE_4};
    --border: {C.BORDER};
    --border-strong: {C.BORDER_STRONG};
    --border-stronger: {C.BORDER_STRONGER};
    --primary: {C.PRIMARY};
    --primary-hover: {C.PRIMARY_HOVER};
    --primary-bright: {C.PRIMARY_BRIGHT};
    --primary-glint: {C.PRIMARY_GLINT};
    --text: {C.TEXT};
    --text-2: {C.TEXT_2};
    --muted: {C.MUTED};
    --muted-deep: {C.MUTED_DEEP};
    --ease: cubic-bezier(0.22, 1, 0.36, 1);

    --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
    --shadow-md: 0 6px 16px -4px rgba(0,0,0,0.4), 0 1px 3px rgba(0,0,0,0.3);
    --shadow-lg: 0 16px 40px -12px rgba(0,0,0,0.55), 0 2px 8px rgba(0,0,0,0.35);
    --shadow-primary: 0 12px 32px -10px rgba(19,111,77,0.32);

    --inset-line: inset 0 1px 0 rgba(255,255,255,0.025);
    --inset-primary: inset 0 1px 0 rgba(28,158,110,0.16);

    --radius-sm: 8px;
    --radius-md: 10px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    --radius-2xl: 20px;
}}

html, body {{
    font-family: var(--font-sans);
    font-feature-settings: 'tnum' on, 'cv11' on, 'ss01' on, 'calt' on;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    word-break: keep-all;
    overflow-wrap: break-word;
}}

/* ============================================================================
   Page background — true carbon black + emerald glow + film grain
============================================================================ */
.stApp {{
    background:
        radial-gradient(1200px 700px at 92% -10%, rgba(28,158,110,0.12) 0%, transparent 55%),
        radial-gradient(1400px 800px at -8% 10%, rgba(19,111,77,0.08) 0%, transparent 50%),
        radial-gradient(1000px 700px at 50% 110%, rgba(34,176,126,0.05) 0%, transparent 55%),
        linear-gradient(180deg, {C.BG_BASE} 0%, #030605 55%, {C.BG_BASE} 100%);
    color: {C.TEXT};
    font-family: var(--font-sans);
    position: relative;
}}
/* 미세 grid + dot texture ── tradingdesk 분위기, 매우 약하게 */
.stApp::before {{
    content: '';
    position: fixed; inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(94,224,165,0.020) 1px, transparent 1px),
        linear-gradient(90deg, rgba(94,224,165,0.020) 1px, transparent 1px),
        radial-gradient(rgba(28,158,110,0.018) 1px, transparent 1px);
    background-size: 56px 56px, 56px 56px, 4px 4px;
    opacity: 0.5;
    mix-blend-mode: overlay;
}}
/* 상단 좌→우 scan line ── 매우 미세 한 줄, 디지털 hint */
.stApp::after {{
    content: '';
    position: fixed; left: 0; right: 0; top: 0;
    height: 1px;
    pointer-events: none;
    z-index: 0;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(28,158,110,0.45) 35%,
        rgba(94,224,165,0.85) 50%,
        rgba(28,158,110,0.45) 65%,
        transparent 100%);
    opacity: 0.55;
}}
.stApp > * {{ position: relative; z-index: 1; }}

.block-container {{
    padding-top: 2.4rem !important;
    padding-bottom: 5rem !important;
    max-width: 1280px !important;
}}

/* Hide Streamlit chrome */
#MainMenu, header[data-testid="stHeader"], footer {{
    visibility: hidden !important;
    height: 0 !important;
}}
.stDeployButton, [data-testid="stToolbar"], [data-testid="manage-app-button"] {{ display: none !important; }}

/* Streamlit container ergonomics */
[data-testid="stVerticalBlock"] {{ gap: 0.85rem !important; }}

/* ============================================================================
   Selection / focus / scrollbar
============================================================================ */
::selection {{
    background: {C.PRIMARY_GLOW};
    color: {C.TEXT};
}}
::-webkit-scrollbar {{ width: 9px; height: 9px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: linear-gradient(180deg, {C.SURFACE_4}, {C.SURFACE_3});
    border-radius: 5px;
    border: 2px solid transparent;
    background-clip: padding-box;
}}
::-webkit-scrollbar-thumb:hover {{
    background: linear-gradient(180deg, {C.PRIMARY_DIM}, {C.SURFACE_4});
    background-clip: padding-box;
}}

/* ============================================================================
   Top service bar — LIFEPLUS brand + contact (luxury financial heading)
============================================================================ */
.topbar {{
    background:
        radial-gradient(circle at 92% -20%, rgba(28,158,110,0.10) 0%, transparent 55%),
        linear-gradient(180deg, {C.SURFACE_2} 0%, {C.SURFACE} 100%);
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-xl);
    padding: 20px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 28px;
    margin-bottom: 28px;
    flex-wrap: wrap;
    position: relative;
    overflow: hidden;
    box-shadow: var(--inset-line), var(--shadow-md);
    isolation: isolate;
}}
.topbar::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        {C.BORDER_STRONG} 12%,
        {C.PRIMARY_HOVER} 35%,
        {C.PRIMARY_GLINT} 50%,
        {C.PRIMARY_HOVER} 65%,
        {C.BORDER_STRONG} 88%,
        transparent 100%);
    opacity: 0.65;
}}
.topbar::after {{
    content: '';
    position: absolute;
    top: -40%;
    right: -10%;
    width: 360px;
    height: 280px;
    background: radial-gradient(closest-side, rgba(28,158,110,0.18), transparent 70%);
    pointer-events: none;
    z-index: -1;
    filter: blur(14px);
    animation: float-orb-a 12s ease-in-out infinite;
}}
.topbar__brand {{
    display: flex;
    align-items: center;
    gap: 18px;
    flex-shrink: 0;
}}
.topbar__logo {{
    height: 46px;
    width: auto;
    display: block;
    filter: brightness(0) invert(1);
    opacity: 0.97;
}}
.topbar__logo-text {{
    font-size: 26px;
    font-weight: 800;
    color: {C.TEXT};
    letter-spacing: -0.025em;
    font-family: var(--font-sans);
}}
.topbar__divider {{
    width: 1px;
    height: 50px;
    background: linear-gradient(180deg, transparent 0%, {C.BORDER_STRONG} 30%, {C.BORDER_STRONG} 70%, transparent 100%);
}}
.topbar__service {{
    flex: 1; min-width: 320px;
}}
.topbar__service-label {{
    font-size: 10px;
    color: {C.MUTED};
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 7px;
    display: inline-flex; align-items: center; gap: 8px;
}}
.topbar__service-label::before {{
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: {C.PRIMARY_HOVER};
    box-shadow: 0 0 0 3px rgba(28,158,110,0.18), 0 0 14px rgba(28,158,110,0.8);
    animation: pulse 2.4s ease-in-out infinite;
}}
@keyframes pulse {{
    0%, 100% {{ box-shadow: 0 0 0 3px rgba(28,158,110,0.18), 0 0 14px rgba(28,158,110,0.7); }}
    50%      {{ box-shadow: 0 0 0 5px rgba(28,158,110,0.08), 0 0 22px rgba(28,158,110,1.0); }}
}}

/* ========================================================================
   Motion primitives — green light system
   - rotate-glow: 박스 테두리를 도는 conic gradient 빛
   - shimmer-x: 가로로 흘러가는 빛 스캔 (좌→우 반복)
   - float-orb: 박스 안에서 부유하는 그린 구체
   - hl-sweep: 형광펜 강조 텍스트의 빛 스윕
======================================================================== */
@keyframes rotate-glow {{
    0%   {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}
@keyframes shimmer-x {{
    0%   {{ transform: translateX(-120%); opacity: 0; }}
    25%  {{ opacity: 1; }}
    75%  {{ opacity: 1; }}
    100% {{ transform: translateX(120%); opacity: 0; }}
}}
@keyframes float-orb-a {{
    0%, 100% {{ transform: translate(0%, 0%) scale(1); opacity: 0.6; }}
    50%      {{ transform: translate(40%, -25%) scale(1.15); opacity: 0.85; }}
}}
@keyframes float-orb-b {{
    0%, 100% {{ transform: translate(0%, 0%) scale(1); opacity: 0.5; }}
    50%      {{ transform: translate(-35%, 30%) scale(1.2); opacity: 0.75; }}
}}
@keyframes hl-sweep {{
    0%   {{ background-position: -120% 100%, 0 100%; }}
    100% {{ background-position: 220% 100%, 0 100%; }}
}}
@keyframes underline-grow {{
    0%   {{ background-size: 0% 38%; }}
    60%  {{ background-size: 100% 38%; }}
    100% {{ background-size: 100% 38%; }}
}}
@keyframes ticker-blink {{
    0%, 100% {{ opacity: 0.6; }}
    50%      {{ opacity: 1.0; }}
}}
.topbar__service-text {{
    font-size: 13.5px;
    color: {C.TEXT_2};
    line-height: 1.55;
    letter-spacing: -0.005em;
}}
.topbar__service-text b {{
    color: {C.TEXT};
    font-weight: 700;
    background: linear-gradient(180deg, {C.PRIMARY_GLINT} 0%, {C.PRIMARY_BRIGHT} 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}}
/* 강조 ─ 볼드 + 흰색 (군더더기 없는 텍스트 강조) */
.topbar__service-text mark {{
    background: transparent;
    background-color: transparent;
    color: #ffffff;
    font-weight: 700;
    padding: 0;
    text-decoration: none;
    text-shadow: none;
    animation: none;
}}
.topbar__contact {{
    display: flex; flex-direction: column;
    align-items: flex-end;
    gap: 2px;
    padding-left: 28px;
    border-left: 1px solid {C.BORDER};
    min-width: 170px;
}}
.topbar__contact-label {{
    font-size: 9.5px;
    color: {C.MUTED_DEEP};
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 3px;
}}
.topbar__contact-name {{
    color: {C.TEXT};
    font-weight: 700;
    font-size: 14px;
    letter-spacing: -0.015em;
}}
.topbar__contact-phone {{
    color: {C.PRIMARY_HOVER};
    font-weight: 700;
    font-size: 13px;
    font-variant-numeric: tabular-nums;
    letter-spacing: 0.01em;
    margin-top: 2px;
}}
@media (max-width: 760px) {{
    .topbar__contact {{
        padding-left: 0;
        border-left: none;
        border-top: 1px solid {C.BORDER};
        padding-top: 14px;
        align-items: flex-start;
        width: 100%;
    }}
}}

/* ============================================================================
   App header — editorial dashboard hero
============================================================================ */
.app-header {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 36px;
    margin-bottom: 40px;
    padding: 8px 0 32px;
    border-bottom: 1px solid {C.BORDER};
    flex-wrap: wrap;
    position: relative;
}}
.app-header::after {{
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 64px; height: 1px;
    background: linear-gradient(90deg, {C.PRIMARY_HOVER}, transparent);
}}
.app-brand {{
    display: flex; flex-direction: column; gap: 0;
}}
.app-eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 11px;
    font-size: 10.5px;
    font-weight: 700;
    color: {C.MUTED};
    letter-spacing: 0.28em;
    text-transform: uppercase;
    margin-bottom: 16px;
    font-family: var(--font-sans);
}}
.app-eyebrow::before {{
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: {C.PRIMARY_HOVER};
    box-shadow: 0 0 0 3px rgba(28,158,110,0.16), 0 0 10px {C.PRIMARY_HOVER};
    animation: pulse 2.4s ease-in-out infinite;
    flex-shrink: 0;
}}
.app-title {{
    font-size: 52px;
    font-weight: 800;
    color: {C.TEXT};
    letter-spacing: -0.04em;
    line-height: 1.0;
    margin: 0;
    font-family: var(--font-sans);
    text-shadow: 0 0 38px rgba(28,158,110,0.10);
}}
.app-title .accent {{
    color: {C.PRIMARY_HOVER};
    font-weight: 800;
}}
.app-subtitle {{
    display: inline-block;
    margin-top: 14px;
    padding: 0;
    background: transparent;
    border: none;
    border-radius: 0;
    font-size: 12.5px;
    font-weight: 500;
    color: {C.MUTED};
    letter-spacing: 0.01em;
    line-height: 1.4;
    text-transform: none;
    font-family: var(--font-sans);
}}
.app-meta {{
    display: inline-flex;
    align-items: stretch;
    gap: 0;
    flex-wrap: nowrap;
    background:
        linear-gradient(180deg, rgba(255,255,255,0.012) 0%, transparent 100%),
        {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--inset-line), var(--shadow-sm);
    position: relative;
    isolation: isolate;
}}
.app-meta::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(105deg,
        transparent 0%,
        transparent 35%,
        rgba(94,224,165,0.07) 48%,
        rgba(255,255,255,0.10) 50%,
        rgba(94,224,165,0.07) 52%,
        transparent 65%,
        transparent 100%);
    pointer-events: none;
    animation: shimmer-x 7s var(--ease) 2.5s infinite;
    z-index: 0;
    mix-blend-mode: screen;
}}
.app-meta > * {{ position: relative; z-index: 1; }}
.app-meta-item {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 4px;
    padding: 12px 22px;
    min-width: 140px;
    background: transparent;
    border: none;
    border-radius: 0;
    box-shadow: none;
    transition: none;
}}
.app-meta-item + .app-meta-item {{
    border-left: 1px solid {C.BORDER};
}}
.app-meta-item:hover {{
    transform: none;
    box-shadow: none;
}}
.app-meta-label {{
    font-size: 9.5px;
    color: {C.MUTED};
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-family: var(--font-sans);
}}
.app-meta-value {{
    color: {C.TEXT};
    font-weight: 700;
    font-size: 16.5px;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.022em;
    line-height: 1.15;
    margin-top: 3px;
    font-family: var(--font-sans);
}}

/* ============================================================================
   App header — container 기반 레이아웃 (st.container(key="app_header"))
   좌측: 브랜드 / 우측: 동기화 버튼 위, 메타 카드 아래 세로 스택
============================================================================ */
[class*="st-key-app_header"] {{
    margin-bottom: 40px;
    padding: 8px 0 0;
    position: relative;
}}
[class*="st-key-app_header"]::after {{
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 96px; height: 1px;
    background: linear-gradient(90deg,
        {C.PRIMARY_GLINT} 0%,
        {C.PRIMARY_HOVER} 35%,
        rgba(28,158,110,0.5) 70%,
        transparent 100%);
    animation: accent-glow 3.4s ease-in-out infinite;
}}
@keyframes accent-glow {{
    0%, 100% {{ box-shadow: 0 0 6px rgba(28,158,110,0.5); opacity: 0.72; }}
    50%      {{ box-shadow: 0 0 14px rgba(94,224,165,0.85); opacity: 1; }}
}}
[class*="st-key-app_header_right"] .app-meta-item:last-child .app-meta-value {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
}}
[class*="st-key-app_header_right"] .app-meta-item:last-child .app-meta-value::before {{
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: {C.PRIMARY_GLINT};
    box-shadow: 0 0 8px {C.PRIMARY_HOVER};
    animation: ticker-blink 1.6s ease-in-out infinite;
    flex-shrink: 0;
}}
[class*="st-key-app_header"] > [data-testid="stHorizontalBlock"] {{
    align-items: flex-start;
}}
/* 우측 컬럼 stack ─ 버튼(위) + 메타 박스(아래), 둘 다 컬럼 너비 100% 채워 가로 크기 통일
   padding-top: eyebrow("DASHBOARD") 높이 + margin-bottom 만큼 내려 버튼 상단을 .app-title 상단과 정렬 */
[class*="st-key-app_header_right"] {{
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 12px !important;
    padding-top: 32px !important;
}}
[class*="st-key-app_header_right"] .app-meta {{
    margin: 0;
    display: flex;
    width: 100%;
}}
[class*="st-key-app_header_right"] .app-meta-item {{
    flex: 1 1 0;
    min-width: 0;
}}

/* ============================================================================
   환율·현재가 동기화 버튼 ─ app-meta-item 결의 인터랙티브 카드
   - 톤: SURFACE 표면 + BORDER + 작은 대문자 라벨 + tabular numerics
   - 아이콘: 좌측 refresh-cw SVG (emerald), 호버 시 180° 회전 + glow
   - 호버: 살짝 lift, primary border, primary glow
============================================================================ */
[class*="st-key-sync_prices_fx"] {{
    width: 100% !important;
    flex: 1 1 auto !important;
}}
[class*="st-key-sync_prices_fx"] button {{
    background:
        linear-gradient(180deg, rgba(255,255,255,0.012) 0%, transparent 100%),
        {C.SURFACE} !important;
    border: 1px solid {C.BORDER} !important;
    border-radius: var(--radius-lg) !important;
    padding: 10px 18px 10px 14px !important;
    min-height: 0 !important;
    height: auto !important;
    width: 100% !important;
    font-size: 10.5px !important;
    font-weight: 700 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: {C.MUTED} !important;
    font-family: var(--font-sans) !important;
    box-shadow: var(--inset-line), var(--shadow-sm) !important;
    transition:
        border-color 0.22s var(--ease),
        color 0.22s var(--ease),
        background 0.22s var(--ease),
        transform 0.22s var(--ease),
        box-shadow 0.22s var(--ease) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0 !important;
}}
[class*="st-key-sync_prices_fx"] button::before {{
    content: '';
    width: 13px;
    height: 13px;
    margin-right: 10px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2322b07e' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8'/><path d='M3 3v5h5'/><path d='M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16'/><path d='M16 16h5v5'/></svg>");
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
    display: inline-block;
    flex-shrink: 0;
    transition: transform 0.5s var(--ease), filter 0.22s var(--ease);
}}
[class*="st-key-sync_prices_fx"] button:hover {{
    border-color: {C.BORDER_PRIMARY} !important;
    color: {C.PRIMARY_HOVER} !important;
    background:
        linear-gradient(180deg, rgba(28,158,110,0.05) 0%, transparent 100%),
        {C.SURFACE} !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--inset-primary), var(--shadow-md) !important;
}}
[class*="st-key-sync_prices_fx"] button:hover::before {{
    transform: rotate(180deg);
    filter: drop-shadow(0 0 8px rgba(94,224,165,0.55));
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%235ee0a5' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8'/><path d='M3 3v5h5'/><path d='M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16'/><path d='M16 16h5v5'/></svg>");
}}
[class*="st-key-sync_prices_fx"] button:active {{
    transform: translateY(0) !important;
    box-shadow: var(--inset-line), var(--shadow-sm) !important;
}}
[class*="st-key-sync_prices_fx"] button:focus-visible {{
    outline: none !important;
    border-color: {C.PRIMARY_HOVER} !important;
    box-shadow: var(--inset-primary), 0 0 0 3px {C.PRIMARY_GLOW} !important;
}}

/* ============================================================================
   KPI cards — premium dashboard tiles
============================================================================ */
.kpi-grid {{
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr 1fr;
    gap: 12px;
    margin-bottom: 56px;
}}
@media (max-width: 1200px) {{
    .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}
.kpi-card {{
    background:
        linear-gradient(180deg, rgba(255,255,255,0.014) 0%, transparent 50%),
        {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-xl);
    padding: 22px 26px 28px;
    transition: border-color 0.22s var(--ease), transform 0.22s var(--ease), box-shadow 0.22s var(--ease);
    box-shadow: var(--inset-line), var(--shadow-sm);
    position: relative;
    min-height: 122px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
}}
.kpi-card::after {{
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    pointer-events: none;
    background: linear-gradient(135deg, rgba(255,255,255,0.025) 0%, transparent 30%);
    opacity: 0.7;
}}
.kpi-card:hover {{
    border-color: {C.BORDER_STRONG};
    transform: translateY(-2px);
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.04),
        0 12px 28px -8px rgba(0,0,0,0.5);
}}
.kpi-card.primary {{
    background:
        radial-gradient(ellipse 700px 220px at 100% 0%, rgba(28,158,110,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 400px 200px at 0% 100%, rgba(19,111,77,0.08) 0%, transparent 60%),
        linear-gradient(180deg, {C.SURFACE_2} 0%, {C.SURFACE} 100%);
    border-color: {C.BORDER_PRIMARY};
    box-shadow:
        var(--inset-primary),
        0 12px 32px -10px rgba(19,111,77,0.28),
        var(--shadow-sm);
    isolation: isolate;
}}
.kpi-card.primary::before {{
    content: '';
    position: absolute;
    left: 0; top: 16px; bottom: 16px;
    width: 2px;
    background: linear-gradient(180deg, {C.PRIMARY_GLINT}, {C.PRIMARY_HOVER} 35%, {C.PRIMARY_DIM});
    border-radius: 0 2px 2px 0;
    box-shadow: 0 0 18px {C.PRIMARY_GLOW};
    z-index: 1;
}}
/* 빛이 흘러가는 스캔 라인 (좌→우 반복) */
.kpi-card.primary::after {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 50%; height: 100%;
    background: linear-gradient(105deg,
        transparent 0%,
        transparent 35%,
        rgba(94,224,165,0.10) 48%,
        rgba(255,255,255,0.16) 50%,
        rgba(94,224,165,0.10) 52%,
        transparent 65%,
        transparent 100%);
    pointer-events: none;
    animation: shimmer-x 5.5s var(--ease) 1.2s infinite;
    z-index: 0;
    opacity: 0.85;
    mix-blend-mode: screen;
}}
.kpi-card.primary .kpi-label {{
    color: {C.PRIMARY_HOVER};
    font-weight: 700;
}}
.kpi-label {{
    font-size: 10.5px;
    color: {C.MUTED};
    margin-bottom: 0;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-family: var(--font-sans);
    display: inline-flex; align-items: center; gap: 8px;
}}
.kpi-label::after {{
    content: '';
    flex: 0 0 18px;
    height: 1px;
    background: {C.BORDER_STRONG};
}}
.kpi-card.primary .kpi-label::after {{ background: {C.BORDER_PRIMARY}; }}
.kpi-value {{
    font-size: 28px;
    font-weight: 800;
    color: {C.TEXT};
    letter-spacing: -0.032em;
    line-height: 1.05;
    font-variant-numeric: tabular-nums;
    margin-top: 10px;
    font-family: var(--font-sans);
}}
.kpi-card.primary .kpi-value {{
    font-size: 28px;
    color: {C.TEXT};
    font-weight: 800;
    background: linear-gradient(180deg, {C.TEXT} 0%, #d0dcd5 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.kpi-value .unit {{
    font-size: 14px;
    font-weight: 600;
    color: {C.MUTED};
    margin-left: 5px;
    letter-spacing: 0;
    -webkit-text-fill-color: {C.MUTED};
}}
.kpi-value.text {{
    font-size: 19px;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin-top: 11px;
}}
.kpi-meta {{
    font-size: 12px;
    color: {C.MUTED_DEEP};
    margin-top: 8px;
    font-weight: 500;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.005em;
}}

/* ============================================================================
   Section header — refined editorial style (used inside step cards)
============================================================================ */
.section-header {{
    margin: 32px 0 18px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
    padding-bottom: 16px;
    border-bottom: 1px solid {C.BORDER};
}}
.section-title {{
    font-size: 20px;
    font-weight: 700;
    color: {C.TEXT};
    letter-spacing: -0.028em;
    margin: 0;
    line-height: 1.25;
    position: relative;
    display: inline-flex;
    align-items: center;
    gap: 12px;
}}
.section-title::before {{
    content: '';
    width: 4px; height: 16px;
    background: linear-gradient(180deg, {C.PRIMARY_GLINT}, {C.PRIMARY_HOVER});
    border-radius: 2px;
    box-shadow: 0 0 12px {C.PRIMARY_GLOW};
    flex-shrink: 0;
}}
.section-sub {{
    font-size: 13.5px;
    color: {C.MUTED};
    margin-top: 8px;
    margin-left: 16px;
    font-weight: 400;
    line-height: 1.55;
    letter-spacing: -0.005em;
    max-width: 640px;
}}
.section-aside {{
    font-size: 11px;
    color: {C.MUTED_DEEP};
    font-weight: 600;
    letter-spacing: 0.04em;
    font-family: var(--font-sans);
}}

/* ============================================================================
   Form inputs (text, number, selectbox)
   - Text input 은 검색용으로만 사용되므로 돋보기 아이콘을 좌측에 임베드.
============================================================================ */
.stTextInput input, .stNumberInput input {{
    background: {C.SURFACE} !important;
    color: {C.TEXT} !important;
    border: 1px solid {C.BORDER} !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-sans) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    height: 52px !important;
    padding: 0 16px !important;
    transition: border-color 0.18s var(--ease), box-shadow 0.18s var(--ease), background 0.18s var(--ease);
    font-variant-numeric: tabular-nums;
    box-shadow: var(--inset-line);
}}

/* Text input ── 검색창 ── 메인 기능이므로 크고 두드러지게 강조 (좌측 돋보기 SVG)
   주의: 부모 step-card가 overflow:hidden 이라 outset glow / 우측 칩 사용 금지 — 잘림 발생함. */
.stTextInput {{
    position: relative;
    margin-bottom: 28px;            /* 다음 요소(예: ② 추가할 종목 선택 selectbox) 라벨과의 시각적 호흡 */
}}

/* BaseWeb wrapper(input 부모)도 동일 height로 ── 입력창 하단 잘림 방지 */
.stTextInput [data-baseweb="base-input"] {{
    height: 56px !important;
    min-height: 56px !important;
    background: transparent !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0 !important;
    overflow: visible !important;
}}
.stTextInput [data-baseweb="input"] {{
    border-radius: var(--radius-md) !important;
    overflow: visible !important;
}}

.stTextInput input {{
    height: 56px !important;
    min-height: 56px !important;
    line-height: 1.3 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    color: {C.TEXT} !important;
    border: 1.5px solid {C.BORDER_STRONG} !important;
    border-radius: var(--radius-md) !important;
    padding: 0 18px 0 50px !important;
    box-sizing: border-box !important;
    background-image:
        url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%2322b07e' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><circle cx='10.5' cy='10.5' r='6.5'/><path d='m20 20-4.35-4.35'/></svg>") !important;
    background-position: 18px center !important;
    background-repeat: no-repeat !important;
    background-color: {C.SURFACE_2} !important;
    background-size: 18px 18px !important;
    box-shadow: var(--inset-line) !important;
    vertical-align: middle !important;
}}
/* stTextInput 컨테이너 자체에도 overflow visible 강제 ── 부모 클립 방어 */
.stTextInput, [data-testid="stTextInput"], [data-testid="stTextInputRootElement"] {{
    overflow: visible !important;
}}
/* 우측 SEARCH 칩 제거 ── overflow:hidden 부모로 인해 잘림 발생 */
.stTextInput::after {{ display: none !important; }}

/* Streamlit 기본 'Press Enter to apply' 인스트럭션 텍스트 숨김 ── 한글 환경에서 글자 깨져 보임 */
[data-testid="InputInstructions"],
[data-testid="stWidgetInstructions"],
.stTextInput div[data-baseweb="base-input"] ~ div small,
.stTextInput [data-baseweb="base-input"] + div {{
    display: none !important;
}}
.stTextInput input:hover, .stNumberInput input:hover {{
    border-color: {C.BORDER_STRONG} !important;
    background-color: {C.SURFACE_2} !important;
}}
.stTextInput input::placeholder {{
    color: {C.MUTED} !important;
    font-weight: 500;
    letter-spacing: -0.005em;
    opacity: 0.85;
}}
.stTextInput input:focus, .stNumberInput input:focus {{
    border-color: {C.PRIMARY_HOVER} !important;
    background-color: {C.SURFACE} !important;
    box-shadow: var(--inset-line), inset 0 0 0 1px {C.PRIMARY_HOVER} !important;
    outline: none !important;
}}
/* focus 시 돋보기 아이콘만 살짝 더 밝게 (잘림 유발 없는 inset 처리) */
.stTextInput input:focus {{
    background-image:
        url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%235ee0a5' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><circle cx='10.5' cy='10.5' r='6.5'/><path d='m20 20-4.35-4.35'/></svg>") !important;
}}

[data-testid="stNumberInput"] button {{
    background: {C.SURFACE_2} !important;
    border: 1px solid {C.BORDER} !important;
    color: {C.MUTED} !important;
    transition: all 0.15s var(--ease);
}}
[data-testid="stNumberInput"] button:hover {{
    color: {C.PRIMARY_BRIGHT} !important;
    background: {C.PRIMARY_SOFT} !important;
    border-color: {C.BORDER_PRIMARY} !important;
}}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] > div {{
    background: {C.SURFACE} !important;
    border: 1px solid {C.BORDER} !important;
    color: {C.TEXT} !important;
    font-family: var(--font-sans) !important;
    min-height: 48px;
    border-radius: var(--radius-md) !important;
    font-size: 14px;
    font-weight: 500;
    transition: border-color 0.18s var(--ease), box-shadow 0.18s var(--ease);
    box-shadow: var(--inset-line);
}}
.stSelectbox div[data-baseweb="select"]:hover > div {{
    border-color: {C.BORDER_STRONG} !important;
}}
.stSelectbox div[data-baseweb="select"]:focus-within > div {{
    border-color: {C.PRIMARY_HOVER} !important;
    box-shadow: 0 0 0 3px {C.PRIMARY_GLOW} !important;
}}

[data-baseweb="popover"] ul {{
    background: {C.SURFACE_3} !important;
    border: 1px solid {C.BORDER_STRONG} !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: 0 20px 50px -10px rgba(0,0,0,0.7), 0 0 0 1px {C.BORDER} !important;
    padding: 5px !important;
    backdrop-filter: blur(16px);
}}
[data-baseweb="popover"] li {{
    color: {C.TEXT} !important;
    font-family: var(--font-sans) !important;
    font-size: 13.5px !important;
    padding: 10px 13px !important;
    border-radius: 7px !important;
    margin: 1px 0 !important;
    transition: background 0.12s var(--ease);
}}
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"] {{
    background: {C.PRIMARY_SOFT} !important;
    color: {C.PRIMARY_HOVER} !important;
}}

/* Labels */
label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stRadio label > div {{
    color: {C.TEXT_2} !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: -0.005em;
    font-family: var(--font-sans) !important;
    text-transform: none !important;
    margin-bottom: 7px !important;
}}

/* ============================================================================
   Buttons
============================================================================ */
.stButton button, .stDownloadButton button {{
    background:
        linear-gradient(180deg, rgba(255,255,255,0.025) 0%, transparent 100%),
        {C.SURFACE_2};
    color: {C.TEXT_2};
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-md);
    font-weight: 600;
    font-family: var(--font-sans);
    transition: all 0.18s var(--ease);
    padding: 11px 20px;
    font-size: 13.5px;
    letter-spacing: -0.005em;
    min-height: 46px;
    text-transform: none;
    box-shadow: var(--inset-line);
    position: relative;
    overflow: hidden;
}}
.stButton button:hover, .stDownloadButton button:hover {{
    background: {C.SURFACE_3};
    border-color: {C.BORDER_STRONG};
    color: {C.TEXT};
    transform: translateY(-1px);
    box-shadow: var(--inset-line), var(--shadow-sm);
}}
.stButton button:active {{ transform: translateY(0); }}

.stButton button[kind="primary"],
.stButton button[data-testid="baseButton-primary"] {{
    background:
        linear-gradient(180deg, {C.PRIMARY_HOVER} 0%, {C.PRIMARY} 60%, {C.PRIMARY_DIM} 100%) !important;
    color: {C.PRIMARY_INK} !important;
    border: 1px solid {C.PRIMARY_HOVER} !important;
    font-weight: 700 !important;
    letter-spacing: -0.005em !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.22),
        inset 0 -1px 0 rgba(0,0,0,0.22),
        0 4px 14px -2px rgba(19,111,77,0.42) !important;
}}
.stButton button[kind="primary"]::before {{
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: linear-gradient(180deg, rgba(255,255,255,0.08) 0%, transparent 50%);
    pointer-events: none;
}}
.stButton button[kind="primary"]:hover {{
    background:
        linear-gradient(180deg, {C.PRIMARY_BRIGHT} 0%, {C.PRIMARY_HOVER} 70%, {C.PRIMARY} 100%) !important;
    border-color: {C.PRIMARY_BRIGHT} !important;
    transform: translateY(-1px);
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.24),
        inset 0 -1px 0 rgba(0,0,0,0.22),
        0 8px 24px -6px rgba(34,176,126,0.6) !important;
}}

/* ============================================================================
   Tabs — minimal editorial
============================================================================ */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent;
    border-bottom: 1px solid {C.BORDER};
    gap: 0;
    padding: 0;
    margin-bottom: 26px;
}}
.stTabs [data-baseweb="tab"] {{
    color: {C.MUTED};
    padding: 14px 0;
    margin-right: 32px;
    font-weight: 600;
    font-size: 14px;
    background: transparent;
    border-radius: 0;
    letter-spacing: -0.005em;
    transition: color 0.18s var(--ease);
    position: relative;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {C.TEXT_2};
}}
.stTabs [aria-selected="true"] {{
    color: {C.TEXT} !important;
    background: transparent !important;
    font-weight: 700;
}}
.stTabs [aria-selected="true"]::after {{
    content: '';
    position: absolute;
    bottom: -1px; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, {C.PRIMARY_HOVER}, {C.PRIMARY_GLINT});
    border-radius: 2px;
    box-shadow: 0 0 12px {C.PRIMARY_GLOW};
}}
.stTabs [data-baseweb="tab-panel"] {{
    padding: 0;
}}

/* ============================================================================
   DataFrame / DataEditor
============================================================================ */
[data-testid="stDataFrame"], [data-testid="stDataEditor"] {{
    border: 1px solid {C.BORDER} !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
    background: {C.SURFACE} !important;
    box-shadow: var(--inset-line), var(--shadow-sm);
}}
.glideDataEditor, [data-testid="stDataEditorResizable"] {{
    --gdg-bg-cell: {C.SURFACE};
    --gdg-bg-cell-medium: {C.SURFACE_2};
    --gdg-bg-header: {C.SURFACE_2};
    --gdg-bg-header-hovered: {C.SURFACE_3};
    --gdg-bg-header-has-focus: {C.PRIMARY_DEEP};
    --gdg-text-dark: {C.TEXT};
    --gdg-text-medium: {C.TEXT_2};
    --gdg-text-light: {C.MUTED};
    --gdg-text-header: {C.MUTED};
    --gdg-text-header-selected: {C.TEXT};
    --gdg-border-color: {C.BORDER};
    --gdg-accent-color: {C.PRIMARY};
    --gdg-accent-fg: {C.PRIMARY_INK};
    --gdg-accent-light: rgba(28,158,110,0.18);
    --gdg-cell-horizontal-padding: 16px;
    --gdg-cell-vertical-padding: 11px;
    --gdg-header-bg: {C.SURFACE_2};
    --gdg-horizontal-border-color: {C.BORDER};
    --gdg-vertical-border-color: {C.BORDER};
    --gdg-font-family: var(--font-sans);
    --gdg-base-font-style: 500 13px;
    --gdg-header-font-style: 600 11.5px;
    --gdg-editor-font-size: 13.5px;
}}

/* ============================================================================
   Metrics
============================================================================ */
[data-testid="stMetric"] {{
    background:
        linear-gradient(180deg, rgba(255,255,255,0.014) 0%, transparent 100%),
        {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-lg);
    padding: 18px 22px;
    transition: border-color 0.22s var(--ease), transform 0.22s var(--ease), box-shadow 0.22s var(--ease);
    box-shadow: var(--inset-line);
}}
[data-testid="stMetric"]:hover {{
    border-color: {C.BORDER_STRONG};
    transform: translateY(-1px);
    box-shadow: var(--inset-line), var(--shadow-sm);
}}
[data-testid="stMetricValue"] {{
    font-family: var(--font-sans) !important;
    color: {C.TEXT} !important;
    font-weight: 800 !important;
    font-size: 24px !important;
    letter-spacing: -0.03em !important;
    line-height: 1.2 !important;
    font-variant-numeric: tabular-nums;
}}
[data-testid="stMetricLabel"] {{
    color: {C.MUTED} !important;
    font-size: 10.5px !important;
    font-weight: 700 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    font-family: var(--font-sans) !important;
    margin-bottom: 8px !important;
}}
[data-testid="stMetricDelta"] {{
    font-size: 11.5px !important;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.005em;
}}

/* ============================================================================
   Alerts
============================================================================ */
[data-testid="stAlert"] {{
    background: {C.SURFACE} !important;
    border: 1px solid {C.BORDER} !important;
    border-radius: var(--radius-lg) !important;
    color: {C.TEXT_2} !important;
    font-family: var(--font-sans) !important;
    font-size: 13.5px !important;
    padding: 14px 18px !important;
    line-height: 1.55;
    box-shadow: var(--inset-line);
}}
[data-testid="stAlert"][kind="success"] {{ border-left: 3px solid {C.PRIMARY_HOVER} !important; }}
[data-testid="stAlert"][kind="warning"] {{ border-left: 3px solid {C.WARN} !important; }}
[data-testid="stAlert"][kind="error"]   {{ border-left: 3px solid {C.SELL} !important; }}
[data-testid="stAlert"][kind="info"]    {{ border-left: 3px solid {C.INFO} !important; }}

/* ============================================================================
   Captions / Radio / Toast
============================================================================ */
[data-testid="stCaptionContainer"] {{
    color: {C.MUTED} !important;
    font-family: var(--font-sans) !important;
    font-size: 12.5px !important;
    line-height: 1.55;
}}

.stRadio [role="radiogroup"] {{ gap: 14px; flex-wrap: wrap; }}
.stRadio label {{
    font-family: var(--font-sans) !important;
    color: {C.TEXT_2} !important;
    font-size: 13.5px !important;
}}

/* 종목 매칭 radio ── card-list 디자인 (kr_sel / us_sel / kb_sel / ub_sel) */
[class*="st-key-kr_sel"] [role="radiogroup"],
[class*="st-key-us_sel"] [role="radiogroup"],
[class*="st-key-kb_sel"] [role="radiogroup"],
[class*="st-key-ub_sel"] [role="radiogroup"] {{
    gap: 8px !important;
    flex-direction: column !important;
    flex-wrap: nowrap !important;
    margin-top: 4px;
}}
[class*="st-key-kr_sel"] [role="radiogroup"] label,
[class*="st-key-us_sel"] [role="radiogroup"] label,
[class*="st-key-kb_sel"] [role="radiogroup"] label,
[class*="st-key-ub_sel"] [role="radiogroup"] label {{
    background:
        linear-gradient(180deg, rgba(255,255,255,0.014) 0%, transparent 100%),
        {C.SURFACE_2} !important;
    border: 1px solid {C.BORDER} !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    margin: 0 !important;
    cursor: pointer;
    transition: all 0.16s var(--ease);
    font-size: 13.5px !important;
    font-weight: 600 !important;
    color: {C.TEXT_2} !important;
    display: flex !important;
    align-items: center;
    gap: 10px;
    position: relative;
    box-shadow: var(--inset-line);
}}
[class*="st-key-kr_sel"] [role="radiogroup"] label:hover,
[class*="st-key-us_sel"] [role="radiogroup"] label:hover,
[class*="st-key-kb_sel"] [role="radiogroup"] label:hover,
[class*="st-key-ub_sel"] [role="radiogroup"] label:hover {{
    border-color: {C.BORDER_PRIMARY} !important;
    color: {C.TEXT} !important;
    background:
        linear-gradient(180deg, rgba(28,158,110,0.045) 0%, transparent 100%),
        {C.SURFACE_2} !important;
}}
/* 선택 상태 — checked radio button is first-child input[type=radio]:checked. 부모 label에 style 적용 어렵지만 currentColor 변화로 시각화 */
[class*="st-key-kr_sel"] [role="radiogroup"] label:has(input:checked),
[class*="st-key-us_sel"] [role="radiogroup"] label:has(input:checked),
[class*="st-key-kb_sel"] [role="radiogroup"] label:has(input:checked),
[class*="st-key-ub_sel"] [role="radiogroup"] label:has(input:checked) {{
    border-color: {C.BORDER_PRIMARY_STRONG} !important;
    background:
        linear-gradient(180deg, rgba(28,158,110,0.12) 0%, rgba(28,158,110,0.02) 100%),
        {C.SURFACE_2} !important;
    color: {C.PRIMARY_GLINT} !important;
    box-shadow:
        inset 2px 0 0 {C.PRIMARY_GLINT},
        inset 6px 0 14px -4px rgba(94,224,165,0.30),
        0 0 0 1px rgba(28,158,110,0.18),
        0 4px 14px -6px rgba(28,158,110,0.22) !important;
}}

[data-testid="stToast"] {{
    background: {C.SURFACE_3} !important;
    border: 1px solid {C.BORDER_STRONG} !important;
    border-left: 3px solid {C.PRIMARY_HOVER} !important;
    color: {C.TEXT} !important;
    font-family: var(--font-sans) !important;
    border-radius: var(--radius-md) !important;
    font-size: 13.5px !important;
    padding: 13px 17px !important;
    box-shadow: var(--shadow-lg);
}}

/* ============================================================================
   Pills
============================================================================ */
.pill {{
    display: inline-flex; align-items: center; gap: 7px;
    padding: 6px 13px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 600;
    border: 1px solid transparent;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.005em;
}}
.pill-primary {{
    background: {C.PRIMARY_SOFT};
    color: {C.PRIMARY_HOVER};
    border-color: {C.BORDER_PRIMARY};
    box-shadow: inset 0 0 0 1px rgba(28,158,110,0.06);
}}
.pill-warn {{
    background: rgba(200,153,104,0.08);
    color: {C.WARN};
    border-color: rgba(200,153,104,0.25);
}}
.pill-muted {{
    background: {C.SURFACE_2};
    color: {C.MUTED};
    border-color: {C.BORDER};
}}
.pill-danger {{
    background: rgba(196,84,98,0.08);
    color: {C.SELL};
    border-color: rgba(196,84,98,0.25);
}}
.pill-dot::before {{
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    box-shadow: 0 0 8px currentColor;
}}

/* ============================================================================
   Order row — trading desk premium card
============================================================================ */
.order-row {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 22px;
    background:
        linear-gradient(180deg, rgba(255,255,255,0.014) 0%, transparent 100%),
        {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-lg);
    margin-bottom: 10px;
    transition: all 0.22s var(--ease);
    gap: 16px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--inset-line), var(--shadow-sm);
}}
.order-row::before {{
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    transition: width 0.22s var(--ease);
}}
.order-row:hover {{
    border-color: {C.BORDER_STRONG};
    transform: translateY(-2px);
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.035),
        0 12px 28px -8px rgba(0,0,0,0.45);
}}
.order-row:hover::before {{ width: 4px; }}
.order-row.buy {{
    background:
        linear-gradient(90deg, rgba(28,158,110,0.06) 0%, {C.SURFACE} 55%),
        {C.SURFACE};
}}
.order-row.buy::before {{
    background: linear-gradient(180deg, {C.PRIMARY_GLINT}, {C.PRIMARY_HOVER} 50%, {C.PRIMARY});
    box-shadow: 0 0 18px {C.PRIMARY_GLOW};
}}
.order-row.buy:hover {{
    background:
        linear-gradient(90deg, rgba(28,158,110,0.1) 0%, {C.SURFACE} 55%),
        {C.SURFACE};
}}
.order-row.sell {{
    background:
        linear-gradient(90deg, rgba(196,84,98,0.06) 0%, {C.SURFACE} 55%),
        {C.SURFACE};
}}
.order-row.sell::before {{
    background: linear-gradient(180deg, #d77580, {C.SELL} 50%, #9a3a42);
    box-shadow: 0 0 14px rgba(196,84,98,0.4);
}}
.order-row.sell:hover {{
    background:
        linear-gradient(90deg, rgba(196,84,98,0.1) 0%, {C.SURFACE} 55%),
        {C.SURFACE};
}}
.order-name {{
    font-size: 15.5px;
    font-weight: 700;
    color: {C.TEXT};
    letter-spacing: -0.022em;
    line-height: 1.25;
}}
.order-code {{
    color: {C.MUTED};
    font-size: 12px;
    margin-left: 11px;
    font-weight: 600;
    letter-spacing: 0.04em;
    font-family: var(--font-numeric);
    text-transform: uppercase;
}}
.order-side {{
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-top: 8px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--font-sans);
}}
.order-side::before {{
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: currentColor;
    box-shadow: 0 0 6px currentColor;
}}
.order-side.buy {{ color: {C.PRIMARY_HOVER}; }}
.order-side.sell {{ color: {C.SELL}; }}
.order-right {{ text-align: right; }}
.order-qty {{
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
    color: {C.TEXT};
    line-height: 1.1;
    font-family: var(--font-sans);
}}
.order-qty .unit {{
    font-size: 12.5px;
    font-weight: 600;
    color: {C.MUTED};
    margin-left: 5px;
}}
.order-amount {{
    color: {C.MUTED};
    font-size: 12.5px;
    margin-top: 4px;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.005em;
}}

/* ============================================================================
   Empty state
============================================================================ */
.empty-state {{
    text-align: center;
    padding: 60px 32px;
    background:
        radial-gradient(ellipse at 50% 0%, rgba(28,158,110,0.05) 0%, transparent 60%),
        {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-xl);
    position: relative;
    overflow: hidden;
}}
.empty-state::before {{
    content: '';
    position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 140px; height: 1px;
    background: linear-gradient(90deg, transparent, {C.PRIMARY_HOVER}, transparent);
    opacity: 0.7;
}}
.empty-title {{
    font-size: 17px;
    font-weight: 700;
    color: {C.TEXT};
    margin-bottom: 12px;
    letter-spacing: -0.025em;
}}
.empty-body {{
    font-size: 14px;
    color: {C.MUTED};
    line-height: 1.75;
    max-width: 480px;
    margin: 0 auto;
    letter-spacing: -0.005em;
    font-weight: 300;
}}

/* ============================================================================
   Spinner
============================================================================ */
.stSpinner > div {{
    border-color: {C.PRIMARY_HOVER} {C.BORDER} {C.BORDER} {C.BORDER} !important;
}}

/* ============================================================================
   File uploader
============================================================================ */
[data-testid="stFileUploader"] section {{
    background: {C.SURFACE} !important;
    border: 1px dashed {C.BORDER_STRONG} !important;
    border-radius: var(--radius-lg) !important;
    padding: 18px !important;
    transition: all 0.18s var(--ease);
}}
[data-testid="stFileUploader"] section:hover {{
    border-color: {C.PRIMARY_HOVER} !important;
    background: {C.SURFACE_2} !important;
    box-shadow: 0 0 0 4px {C.PRIMARY_SOFT};
}}
[data-testid="stFileUploader"] small {{
    color: {C.MUTED} !important;
    font-family: var(--font-sans) !important;
}}

/* ============================================================================
   Sidebar (backend & stack)
============================================================================ */
[data-testid="stSidebar"] {{
    background: {C.BG_2} !important;
    border-right: 1px solid {C.BORDER} !important;
}}
[data-testid="stSidebar"] > div {{
    padding: 0 !important;
    background: transparent !important;
}}

.sb {{
    background:
        linear-gradient(180deg, rgba(255,255,255,0.014) 0%, transparent 40%),
        {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-xl);
    padding: 22px 20px;
    position: sticky;
    top: 24px;
    overflow: hidden;
    box-shadow: var(--inset-line), var(--shadow-sm);
}}

/* sticky 동작 ── 좌측 column이 자기 콘텐츠 height만 차지하도록 align top.
   main/block-container의 overflow는 절대 건드리지 않음(페이지 스크롤 보존). */
[data-testid="stHorizontalBlock"]:has(.sb) {{
    align-items: flex-start !important;
}}
[data-testid="stColumn"]:has(.sb) {{
    align-self: flex-start !important;
}}
.sb::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg,
        transparent,
        {C.PRIMARY_DIM} 25%,
        {C.PRIMARY_HOVER} 50%,
        {C.PRIMARY_DIM} 75%,
        transparent);
    opacity: 0.7;
}}
.sb::after {{
    content: '';
    position: absolute;
    top: -30%; right: -10%;
    width: 220px; height: 200px;
    background: radial-gradient(closest-side, rgba(28,158,110,0.08), transparent 70%);
    pointer-events: none;
}}
.sb__eyebrow {{
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 9.5px; font-weight: 800;
    color: {C.PRIMARY_HOVER};
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-family: var(--font-sans);
}}
.sb__eyebrow::before {{
    content: ''; width: 6px; height: 6px;
    border-radius: 50%;
    background: {C.PRIMARY_HOVER};
    box-shadow: 0 0 0 3px rgba(28,158,110,0.16), 0 0 10px {C.PRIMARY_HOVER};
    animation: pulse 2.4s ease-in-out infinite;
}}
.sb h3 {{
    font-size: 16px; font-weight: 800;
    color: {C.TEXT};
    letter-spacing: -0.028em;
    margin: 0 0 5px;
    line-height: 1.25;
    font-family: var(--font-sans);
}}
.sb__subtitle {{
    font-size: 12px;
    color: {C.MUTED};
    margin: 0 0 18px;
    line-height: 1.55;
    word-break: keep-all;
    overflow-wrap: break-word;
}}
.sb__subtitle b {{ color: {C.TEXT_2}; font-weight: 700; }}

.sb__metrics {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    padding: 14px 0 16px;
    border-bottom: 1px solid {C.BORDER};
    margin-bottom: 18px;
    position: relative;
}}
.sb__metric {{
    text-align: center;
    padding: 6px 4px;
    border-radius: 8px;
    transition: background 0.2s var(--ease);
}}
.sb__metric:hover {{ background: {C.SURFACE_2}; }}
.sb__metric-value {{
    font-size: 15px;
    font-weight: 800;
    color: {C.PRIMARY_HOVER};
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
    font-family: var(--font-sans);
}}
.sb__metric-label {{
    font-size: 9px;
    font-weight: 700;
    color: {C.MUTED};
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 5px;
}}

.sb__steps {{
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 0;
}}
.sb__step {{
    display: grid;
    grid-template-columns: 26px 1fr;
    gap: 12px;
    padding: 9px 0;
    position: relative;
}}
.sb__step:not(:last-child)::after {{
    content: '';
    position: absolute;
    left: 12px; top: 32px; bottom: -5px;
    width: 2px;
    background: linear-gradient(180deg, {C.PRIMARY_DIM} 0%, {C.PRIMARY_DEEP} 50%, transparent 100%);
}}
.sb__step-num {{
    width: 26px; height: 26px;
    border-radius: 999px;
    background:
        linear-gradient(180deg, rgba(255,255,255,0.18) 0%, transparent 60%),
        linear-gradient(135deg, {C.PRIMARY_HOVER}, {C.PRIMARY_DIM});
    color: {C.PRIMARY_INK};
    font-size: 10.5px;
    font-weight: 800;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.16),
        0 2px 8px rgba(19, 111, 77, 0.4);
    font-variant-numeric: tabular-nums;
    position: relative;
    z-index: 1;
    letter-spacing: -0.02em;
    font-family: var(--font-sans);
}}
.sb__step-title {{
    font-size: 12.5px;
    font-weight: 700;
    color: {C.TEXT};
    letter-spacing: -0.015em;
    line-height: 1.4;
    padding-top: 4px;
}}
.sb__step-desc {{
    font-size: 11px;
    color: {C.MUTED};
    line-height: 1.55;
    margin-top: 3px;
    letter-spacing: -0.005em;
}}

.sb__stack {{
    margin-top: 18px;
    padding-top: 16px;
    border-top: 1px dashed {C.BORDER};
}}
.sb__stack-label {{
    font-size: 9.5px;
    font-weight: 800;
    color: {C.MUTED};
    text-transform: uppercase;
    letter-spacing: 0.18em;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: var(--font-sans);
}}
.sb__stack-label::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, {C.BORDER}, transparent);
}}
.sb__stack-list {{
    display: grid;
    gap: 5px;
}}
.sb__stack-item {{
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 8px 11px;
    border-radius: 8px;
    background: {C.SURFACE_2};
    border: 1px solid {C.BORDER};
    transition: all 0.18s var(--ease);
}}
.sb__stack-item:hover {{
    background: {C.SURFACE_3};
    border-color: {C.BORDER_STRONG};
    transform: translateX(2px);
}}
.sb__stack-bar {{
    width: 3px;
    height: 14px;
    border-radius: 2px;
    flex-shrink: 0;
    box-shadow: 0 0 8px currentColor;
    opacity: 0.9;
}}
.sb__stack-name {{
    font-size: 11.5px;
    font-weight: 700;
    color: {C.TEXT};
    font-family: var(--font-numeric);
    letter-spacing: -0.005em;
}}
.sb__stack-role {{
    font-size: 9.5px;
    color: {C.MUTED};
    margin-left: auto;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-family: var(--font-sans);
}}

/* ============================================================================
   Market split (국장 / 미장)
============================================================================ */
.market-split {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 20px;
}}
.market-split__card {{
    background:
        linear-gradient(180deg, rgba(255,255,255,0.014) 0%, transparent 100%),
        {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-xl);
    padding: 20px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.22s var(--ease);
    position: relative;
    overflow: hidden;
    box-shadow: var(--inset-line), var(--shadow-sm);
}}
.market-split__card:hover {{
    border-color: {C.BORDER_STRONG};
    transform: translateY(-2px);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 10px 24px rgba(0,0,0,0.32);
}}
.market-split__card::before {{
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
}}
.market-split__card.kr::before {{
    background: linear-gradient(180deg, {C.PRIMARY_GLINT}, {C.PRIMARY_HOVER}, {C.PRIMARY_DIM});
    box-shadow: 0 0 14px {C.PRIMARY_GLOW};
}}
.market-split__card.kr {{
    background:
        radial-gradient(ellipse at 0% 50%, rgba(28,158,110,0.08) 0%, transparent 65%),
        {C.SURFACE};
    isolation: isolate;
}}
.market-split__card.kr::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(105deg,
        transparent 30%,
        rgba(94,224,165,0.07) 48%,
        rgba(255,255,255,0.09) 50%,
        rgba(94,224,165,0.07) 52%,
        transparent 70%);
    transform: translateX(-100%);
    pointer-events: none;
    z-index: 0;
    opacity: 0;
    transition: opacity 0.3s var(--ease);
}}
.market-split__card.kr:hover::after {{
    opacity: 1;
    animation: shimmer-x 1.6s var(--ease) forwards;
}}
.market-split__card.us::before {{
    background: linear-gradient(180deg, #8fc0e0, {C.US_BRIGHT}, #2c5a7f);
    box-shadow: 0 0 14px rgba(107,161,200,0.32);
}}
.market-split__card.us {{
    background:
        radial-gradient(ellipse at 0% 50%, rgba(61,127,175,0.08) 0%, transparent 65%),
        {C.SURFACE};
}}
.market-split__left {{ display: flex; flex-direction: column; gap: 3px; }}
.market-split__label {{
    font-size: 10px;
    font-weight: 700;
    color: {C.MUTED};
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-family: var(--font-sans);
}}
.market-split__title {{
    font-size: 16px;
    font-weight: 800;
    color: {C.TEXT};
    letter-spacing: -0.025em;
    margin-top: 5px;
    font-family: var(--font-sans);
}}
.market-split__sub {{
    font-size: 11.5px;
    color: {C.MUTED};
    font-variant-numeric: tabular-nums;
    margin-top: 4px;
}}
.market-split__right {{ text-align: right; }}
.market-split__percent {{
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.035em;
    font-variant-numeric: tabular-nums;
    line-height: 1.0;
    font-family: var(--font-sans);
}}
.market-split__card.kr .market-split__percent {{
    background: linear-gradient(180deg, {C.PRIMARY_GLINT} 0%, {C.PRIMARY_HOVER} 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.market-split__card.us .market-split__percent {{
    background: linear-gradient(180deg, #8fc0e0 0%, {C.US_BRIGHT} 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.market-split__amount {{
    font-size: 12px;
    color: {C.MUTED};
    font-variant-numeric: tabular-nums;
    margin-top: 6px;
    letter-spacing: -0.005em;
}}

/* ============================================================================
   Step Card — major workflow boxes (1/2/3/4 steps)
============================================================================ */
[data-testid="stVerticalBlockBorderWrapper"]:has(.step-card-header) {{
    background:
        linear-gradient(180deg, rgba(255,255,255,0.012) 0%, transparent 25%),
        {C.SURFACE} !important;
    border: 1px solid {C.BORDER} !important;
    border-radius: var(--radius-2xl) !important;
    padding: 32px 36px 40px !important;
    margin-bottom: 32px !important;
    box-shadow: var(--inset-line), var(--shadow-sm) !important;
    transition: border-color 0.22s var(--ease), box-shadow 0.22s var(--ease);
    position: relative;
    overflow: hidden;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.step-card-header):hover {{
    border-color: {C.BORDER_STRONG} !important;
    box-shadow: var(--inset-line), var(--shadow-md) !important;
}}

/* Primary variant — STEP 04 리밸런싱 계획 (서비스 최종 결론)
   톤: calc-cta와 동일한 emerald 강조 + 보더를 도는 회전 빛띠 + 외부 큰 halo */
[class*="st-key-step_04_card"] {{
    border: 1px solid {C.BORDER_PRIMARY_STRONG} !important;
    background-color: {C.SURFACE} !important;
    background-image:
        radial-gradient(ellipse 800px 240px at 100% 0%, rgba(28,158,110,0.14) 0%, transparent 60%),
        radial-gradient(ellipse 460px 220px at 0% 100%, rgba(19,111,77,0.08) 0%, transparent 65%),
        linear-gradient(180deg, {C.SURFACE_2} 0%, {C.SURFACE} 100%) !important;
    background-repeat: no-repeat, no-repeat, no-repeat !important;
    background-position: top right, bottom left, center !important;
    padding: 34px 38px 40px !important;
    margin-top: 32px !important;
    margin-bottom: 32px !important;
    position: relative;
    isolation: isolate;
    overflow: visible !important;
    animation: primary-pulse 5s ease-in-out infinite;
}}

@keyframes primary-pulse {{
    0%, 100% {{
        box-shadow:
            inset 2px 0 0 0 {C.PRIMARY_HOVER},
            inset 8px 0 14px -4px rgba(28,158,110,0.20),
            inset 0 1px 0 rgba(28,158,110,0.16),
            0 0 0 1px rgba(28,158,110,0.10),
            0 0 28px -4px rgba(28,158,110,0.18),
            0 18px 50px -16px rgba(19,111,77,0.34);
    }}
    50% {{
        box-shadow:
            inset 2px 0 0 0 {C.PRIMARY_GLINT},
            inset 10px 0 18px -3px rgba(28,158,110,0.28),
            inset 0 1px 0 rgba(28,158,110,0.22),
            0 0 0 1px rgba(28,158,110,0.18),
            0 0 40px -2px rgba(28,158,110,0.28),
            0 22px 60px -16px rgba(28,158,110,0.30);
    }}
}}

/* 상단 좌→우 흐르는 은은한 emerald shimmer (calc-cta와 동일 결) */
[class*="st-key-step_04_card"]::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 65%; height: 1.5px;
    background: linear-gradient(90deg,
        transparent,
        rgba(28,158,110,0.50) 35%,
        {C.PRIMARY_GLINT} 55%,
        rgba(28,158,110,0.50) 70%,
        transparent);
    animation: shimmer-x 5.5s var(--ease) infinite;
    opacity: 0.85;
    z-index: 2;
    pointer-events: none;
    box-shadow: 0 0 10px rgba(94,224,165,0.45);
}}

/* 상단 emerald scan-line 제거 */
[class*="st-key-step_04_card"]::after {{ display: none !important; content: none !important; }}

/* 카드 내부 콘텐츠가 회전 빛띠 위로 올라오도록 stacking */
[class*="st-key-step_04_card"] > * {{
    position: relative;
    z-index: 2;
}}
/* 떠다니는 그린 오브 2개 — 깊이감 부여 */
[class*="st-key-step_04_card"]::after {{
    content: '';
    position: absolute;
    top: -10%; right: -8%;
    width: 360px; height: 280px;
    background:
        radial-gradient(closest-side, rgba(34,176,126,0.22), transparent 70%);
    pointer-events: none;
    z-index: -1;
    filter: blur(18px);
    animation: float-orb-a 9s ease-in-out infinite;
}}
[class*="st-key-step_04_card"] > div:first-child::before {{
    content: '';
    position: absolute;
    bottom: -8%; left: -8%;
    width: 320px; height: 260px;
    background:
        radial-gradient(closest-side, rgba(28,158,110,0.18), transparent 70%);
    pointer-events: none;
    z-index: -1;
    filter: blur(22px);
    animation: float-orb-b 11s ease-in-out infinite;
}}
/* 상단 빛 스캔 라인 제거 */
[class*="st-key-step_04_card"] > div:first-child::after {{ display: none !important; content: none !important; }}

/* Step header (inside container) */
.step-card-header {{
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 28px;
    padding-bottom: 22px;
    border-bottom: 1px solid {C.BORDER};
}}
.step-card-header .step-info {{
    padding: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 0;
}}
.step-card-primary .step-info {{
    min-height: 0;
}}
.step-card-primary {{
    border-bottom-color: {C.BORDER_PRIMARY};
}}
/* step-num ── 흰색 텍스트만, 박스/glow 없음 */
.step-num {{
    flex-shrink: 0;
    position: relative;
    width: auto;
    height: auto;
    min-width: 36px;
    background: transparent;
    border: none;
    box-shadow: none;
    color: {C.TEXT};
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
    line-height: 1;
    font-family: var(--font-sans);
    text-shadow: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    overflow: visible;
}}
.step-num::before, .step-num::after {{ display: none !important; content: none !important; }}
.step-num::after {{
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    background: linear-gradient(135deg, rgba(94,224,165,0.32), transparent 50%);
    z-index: -1;
    opacity: 0.6;
}}
.step-card-primary .step-num {{
    font-size: 26px;
    color: {C.TEXT};
    text-shadow: none;
    background: transparent;
    border: none;
    box-shadow: none;
}}
/* 회전하는 헤일로 (Step 04 번호 주위 빛) */
.step-card-primary .step-num::before {{
    content: '';
    position: absolute;
    inset: -6px;
    border-radius: 20px;
    background: conic-gradient(
        from 0deg,
        transparent 0deg,
        rgba(94,224,165,0.55) 60deg,
        rgba(34,176,126,0.85) 90deg,
        rgba(94,224,165,0.55) 120deg,
        transparent 180deg,
        transparent 360deg
    );
    filter: blur(6px);
    opacity: 0.7;
    animation: rotate-glow 4.5s linear infinite;
    z-index: -1;
}}
.step-info {{
    flex: 1;
    min-width: 0;
}}
.step-title {{
    font-size: 18px;
    font-weight: 800;
    color: {C.TEXT};
    letter-spacing: -0.025em;
    margin: 0;
    line-height: 1.3;
    font-family: var(--font-sans);
}}
.step-card-primary .step-title {{
    font-size: 36px;
    font-weight: 800;
    color: {C.TEXT};
    letter-spacing: -0.04em;
    background: none;
    -webkit-text-fill-color: {C.TEXT};
    line-height: 1.15;
}}
.step-sub {{
    font-size: 13.5px;
    color: {C.MUTED};
    margin: 7px 0 0 0;
    line-height: 1.6;
    letter-spacing: -0.005em;
    max-width: 720px;
    font-weight: 300;
}}
.step-card-primary .step-sub {{
    font-size: 14px;
    color: {C.TEXT_2};
    max-width: 780px;
    font-weight: 300;
}}
.step-sub b {{
    color: {C.PRIMARY_HOVER};
    font-weight: 700;
}}
.step-aside {{
    font-size: 10.5px;
    color: {C.MUTED_DEEP};
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-left: auto;
    flex-shrink: 0;
    padding-left: 18px;
    align-self: center;
    font-family: var(--font-sans);
}}
.step-card-primary .step-aside {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: {C.PRIMARY_HOVER};
    font-weight: 700;
    letter-spacing: 0.18em;
    font-size: 10px;
    padding: 6px 12px;
    background: {C.PRIMARY_SOFT};
    border: 1px solid {C.BORDER_PRIMARY};
    border-radius: 999px;
}}
.step-card-primary .step-aside::before {{
    content: '';
    width: 5px; height: 5px; border-radius: 50%;
    background: {C.PRIMARY_HOVER};
    box-shadow: 0 0 8px {C.PRIMARY_HOVER};
}}

/* Step card 사이 section-header 마진 조정 */
[data-testid="stVerticalBlockBorderWrapper"]:has(.step-card-header) .section-header {{
    margin-top: 32px !important;
    margin-bottom: 18px !important;
    padding-bottom: 14px !important;
}}

/* ============================================================================
   STEP 04 ── 서비스의 최종 결론. 내부 메트릭/오더/상세를 더 강하게 강조
============================================================================ */
/* STEP 04 안 거래 조건 expander ── 카드 톤에 녹아들도록 약하게 */
[class*="st-key-step_04_card"] [data-testid="stExpander"] {{
    background: transparent !important;
    border: 1px solid {C.BORDER} !important;
    border-radius: var(--radius-md) !important;
    margin: 12px 0 22px !important;
}}
[class*="st-key-step_04_card"] [data-testid="stExpander"] summary {{
    color: {C.MUTED} !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
    padding: 12px 16px !important;
}}
[class*="st-key-step_04_card"] [data-testid="stExpander"]:hover summary {{
    color: {C.TEXT_2} !important;
}}

/* STEP 04 매수/매도 주문 행 ── 더 큼직하고 또렷이 */
[class*="st-key-step_04_card"] .order-row {{
    padding: 22px 26px !important;
    margin-bottom: 12px !important;
    border-radius: var(--radius-lg) !important;
}}
[class*="st-key-step_04_card"] .order-row.buy {{
    border-color: {C.BORDER_PRIMARY} !important;
    box-shadow: var(--inset-primary), 0 8px 22px -12px rgba(28,158,110,0.34) !important;
}}
[class*="st-key-step_04_card"] .order-row.sell {{
    border-color: rgba(196,84,98,0.32) !important;
    box-shadow: inset 0 1px 0 rgba(196,84,98,0.12), 0 8px 22px -12px rgba(196,84,98,0.30) !important;
}}
[class*="st-key-step_04_card"] .order-row::before {{
    width: 4px !important;
}}
[class*="st-key-step_04_card"] .order-name {{
    font-size: 17px !important;
}}
[class*="st-key-step_04_card"] .order-qty {{
    font-size: 26px !important;
    letter-spacing: -0.03em;
}}
[class*="st-key-step_04_card"] .order-amount {{
    font-size: 13px !important;
    margin-top: 6px;
}}
/* "매수 주문" / "매도 주문" 헤더 라벨 */
[class*="st-key-step_04_card"] .stMarkdown div[style*="매수 주문"],
[class*="st-key-step_04_card"] .stMarkdown div[style*="매도 주문"] {{
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: 0.26em !important;
    text-transform: uppercase;
    margin-bottom: 14px !important;
}}

/* "매수 주문" / "매도 주문" 헤더 라벨 ── 더 또렷이 */
[class*="st-key-step_04_card"] .stMarkdown div[style*="매수 주문"],
[class*="st-key-step_04_card"] .stMarkdown div[style*="매도 주문"] {{
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: 0.24em !important;
    text-transform: uppercase;
}}

/* "서비스 핵심" badge 강화 */
.step-card-primary .step-aside {{
    padding: 8px 14px !important;
    font-size: 10.5px !important;
    letter-spacing: 0.22em !important;
    box-shadow: 0 0 18px rgba(28,158,110,0.20);
}}

/* primary 카드 안 wide alerts (warning/info) ── emerald 톤 일관 */
[class*="st-key-step_04_card"] [data-testid="stAlert"] {{
    border-radius: var(--radius-xl) !important;
    padding: 16px 22px !important;
    font-size: 14px !important;
}}

/* ============================================================================
   Search empty state — onboarding hint
============================================================================ */
/* 예시 검색어 박스 ── 검색창보다는 약하되 또렷이 보이도록 (보조 가이드) */
.search-empty {{
    margin-top: 12px;
    padding: 14px 18px;
    background:
        linear-gradient(180deg, rgba(255,255,255,0.012) 0%, transparent 100%),
        {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: var(--radius-md);
    position: relative;
    overflow: hidden;
    transition: border-color 0.18s var(--ease);
}}
.search-empty:hover {{ border-color: {C.BORDER_STRONG}; }}
.search-empty::before {{ display: none; }}
.search-empty__label {{
    font-size: 9.5px;
    font-weight: 700;
    color: {C.MUTED};
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 11px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-sans);
}}
.search-empty__label::before {{
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: {C.PRIMARY_HOVER};
    box-shadow: 0 0 0 3px rgba(28,158,110,0.14);
    flex-shrink: 0;
}}
.search-empty__examples {{
    display: flex;
    gap: 7px;
    flex-wrap: wrap;
}}
.search-empty__chip {{
    padding: 6px 11px;
    border-radius: 6px;
    background: {C.SURFACE_2};
    border: 1px solid {C.BORDER_STRONG};
    font-size: 12px;
    color: {C.TEXT_2};
    font-weight: 600;
    font-family: var(--font-numeric);
    letter-spacing: -0.005em;
    transition: all 0.18s var(--ease);
    line-height: 1.2;
}}
.search-empty__chip:hover {{
    border-color: {C.BORDER_PRIMARY};
    color: {C.PRIMARY_HOVER};
    background: {C.PRIMARY_SOFT};
}}
.search-empty__hint {{
    margin-top: 12px;
    margin-bottom: 20px;
    padding-top: 11px;
    border-top: 1px dashed {C.BORDER};
    font-size: 11.5px;
    color: {C.MUTED};
    line-height: 1.6;
    font-weight: 400;
}}
.search-empty__hint b {{ color: {C.PRIMARY_HOVER}; font-weight: 700; }}

/* ============================================================================
   Quick chips ── 검색창 아래 예시 버튼(클릭 시 즉시 포트폴리오 추가)
============================================================================ */
.quick-chips__label {{
    font-size: 10.5px;
    font-weight: 800;
    color: {C.PRIMARY_HOVER};
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin: 14px 0 10px;
    display: flex;
    align-items: center;
    gap: 9px;
    font-family: var(--font-sans);
}}
.quick-chips__label::before {{
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: {C.PRIMARY_HOVER};
    box-shadow: 0 0 0 3px rgba(28,158,110,0.16), 0 0 10px {C.PRIMARY_HOVER};
    animation: pulse 2.4s ease-in-out infinite;
    flex-shrink: 0;
}}
.quick-chips__hint {{
    font-size: 11px;
    color: {C.MUTED};
    margin: 12px 0 0;
    line-height: 1.6;
    letter-spacing: 0.01em;
}}
.quick-chips__hint b {{
    color: {C.PRIMARY_HOVER};
    font-weight: 700;
}}
/* 균등 배분 버튼 ── 중요도 낮음, neutral secondary 톤 */
[class*="st-key-eq_split"] .stButton button {{
    min-height: 40px !important;
    height: 40px !important;
    padding: 0 16px !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: -0.005em !important;
    text-transform: none !important;
    color: {C.TEXT_2} !important;
    background: {C.SURFACE_2} !important;
    border: 1px solid {C.BORDER} !important;
    box-shadow: var(--inset-line) !important;
    transition: all 0.18s var(--ease) !important;
}}
[class*="st-key-eq_split"] .stButton button:hover {{
    background: {C.SURFACE_3} !important;
    border-color: {C.BORDER_STRONG} !important;
    color: {C.TEXT} !important;
    transform: none !important;
    box-shadow: var(--inset-line) !important;
}}

/* chip-as-button ── kr_quick_*, us_quick_*, kb_quick_*, ub_quick_*
   pill 형태 + 좌측 emerald dot indicator + 호버 시 emerald glow */
[class*="st-key-kr_quick_"] .stButton button,
[class*="st-key-us_quick_"] .stButton button,
[class*="st-key-kb_quick_"] .stButton button,
[class*="st-key-ub_quick_"] .stButton button {{
    position: relative !important;
    min-height: 32px !important;
    height: 32px !important;
    padding: 0 14px 0 22px !important;       /* 좌측에 dot 자리 */
    border-radius: 999px !important;          /* pill 형태 */
    font-size: 11.5px !important;
    font-weight: 500 !important;              /* LIFEPLUS Medium */
    background:
        linear-gradient(180deg, rgba(255,255,255,0.020) 0%, transparent 100%),
        {C.SURFACE_2} !important;
    border: 1px solid {C.BORDER_STRONG} !important;
    color: {C.TEXT_2} !important;
    box-shadow: var(--inset-line) !important;
    text-transform: none !important;
    letter-spacing: -0.005em !important;
    font-family: 'LIFEPLUS', sans-serif !important;
    transition: all 0.22s var(--ease) !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    background-image:
        radial-gradient(circle at 12px center, {C.MUTED_DEEP} 1.6px, transparent 1.8px),
        linear-gradient(180deg, rgba(255,255,255,0.020) 0%, transparent 100%) !important;
    background-repeat: no-repeat, no-repeat !important;
    background-color: {C.SURFACE_2} !important;
}}
[class*="st-key-kr_quick_"] .stButton button:hover,
[class*="st-key-us_quick_"] .stButton button:hover,
[class*="st-key-kb_quick_"] .stButton button:hover,
[class*="st-key-ub_quick_"] .stButton button:hover {{
    background:
        radial-gradient(circle at 12px center, {C.PRIMARY_GLINT} 1.8px, transparent 2.4px),
        linear-gradient(180deg, rgba(28,158,110,0.10) 0%, transparent 100%) !important;
    background-color: {C.SURFACE_3} !important;
    background-repeat: no-repeat, no-repeat !important;
    border-color: {C.PRIMARY_HOVER} !important;
    color: {C.TEXT} !important;
    transform: translateY(-1px) !important;
    box-shadow:
        var(--inset-line),
        0 4px 14px -6px rgba(28,158,110,0.40),
        0 0 0 3px rgba(28,158,110,0.10) !important;
}}
[class*="st-key-kr_quick_"] .stButton button:active,
[class*="st-key-us_quick_"] .stButton button:active,
[class*="st-key-kb_quick_"] .stButton button:active,
[class*="st-key-ub_quick_"] .stButton button:active {{
    transform: translateY(0) !important;
}}

/* anchor marker 자체는 0 height (CSS 식별용, 시각적 표시 없음) */
.quick-anchor {{ height: 0; margin: 0; padding: 0; }}
[data-testid="stElementContainer"]:has(.quick-anchor) {{
    margin: 0 !important;
    height: 0 !important;
    overflow: hidden;
}}
/* 박스 wrap 없는 inline 레이아웃 ── 위쪽 검색창과 호흡, label/chips/hint 간격만 정돈 */
[data-testid="stElementContainer"]:has(.quick-anchor) + [data-testid="stElementContainer"] .search-empty__label {{
    margin-top: 22px !important;
}}
[data-testid="stElementContainer"]:has(.quick-anchor) ~ [data-testid="stElementContainer"] [data-testid="stHorizontalBlock"] {{
    gap: 7px !important;
    margin: 4px 0 !important;
}}

/* ============================================================================
   Footer — subtle trust signal
============================================================================ */
.app-footer {{
    margin-top: 88px;
    padding: 32px 0 16px;
    border-top: 1px solid {C.BORDER};
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
    position: relative;
}}
.app-footer::before {{
    content: '';
    position: absolute;
    top: -1px; left: 0;
    width: 64px; height: 1px;
    background: linear-gradient(90deg, {C.PRIMARY_HOVER}, transparent);
}}
.app-footer__left {{
    display: flex;
    align-items: center;
    gap: 14px;
}}
.app-footer__mark {{
    width: 3px;
    height: 18px;
    background: linear-gradient(180deg, {C.BRONZE}, {C.BRONZE_DIM});
    border-radius: 2px;
    box-shadow: 0 0 10px {C.BRONZE_GLOW};
}}
.app-footer__brand {{
    font-size: 13px;
    color: {C.TEXT_2};
    font-weight: 600;
    letter-spacing: -0.005em;
}}
.app-footer__brand b {{ color: {C.TEXT}; font-weight: 800; }}
.app-footer__meta {{
    display: flex;
    gap: 18px;
    font-size: 11.5px;
    color: {C.MUTED};
    font-variant-numeric: tabular-nums;
    font-family: var(--font-sans);
}}
.app-footer__meta span {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}
.app-footer__meta span:not(:last-child)::after {{
    content: '';
    margin-left: 18px;
    width: 1px;
    height: 11px;
    background: {C.BORDER_STRONG};
}}
.app-footer__disclaimer {{
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px dashed {C.BORDER};
    font-size: 11.5px;
    font-weight: 300;
    color: {C.MUTED_DEEP};
    line-height: 1.7;
    max-width: 760px;
    letter-spacing: -0.002em;
}}

/* ============================================================================
   Ticker tape — 자산 헤드라인 스트립 (heading area)
============================================================================ */
.ticker {{
    display: flex;
    align-items: center;
    gap: 0;
    margin: 0 0 28px 0;
    padding: 0;
    background:
        linear-gradient(90deg, {C.BG_2} 0%, transparent 8%, transparent 92%, {C.BG_2} 100%),
        {C.SURFACE};
    border: 1px solid {C.BORDER};
    border-radius: 999px;
    overflow: hidden;
    position: relative;
    box-shadow: var(--inset-line), var(--shadow-sm);
}}
.ticker__label {{
    flex-shrink: 0;
    padding: 11px 18px;
    background: linear-gradient(180deg, {C.PRIMARY_HOVER}, {C.PRIMARY});
    color: {C.PRIMARY_INK};
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    display: inline-flex; align-items: center; gap: 8px;
    font-family: var(--font-sans);
    box-shadow: inset 0 -1px 0 rgba(0,0,0,0.2);
}}
.ticker__label::before {{
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: {C.PRIMARY_GLINT};
    box-shadow: 0 0 0 3px rgba(255,255,255,0.14), 0 0 10px white;
    animation: pulse 2s ease-in-out infinite;
}}
.ticker__items {{
    flex: 1;
    display: flex;
    gap: 32px;
    padding: 0 20px;
    overflow: hidden;
    font-family: var(--font-sans);
    white-space: nowrap;
    align-items: center;
}}
.ticker__item {{
    display: inline-flex;
    align-items: baseline;
    gap: 8px;
    font-size: 12.5px;
    font-variant-numeric: tabular-nums;
}}
.ticker__name {{
    color: {C.MUTED};
    font-weight: 700;
    letter-spacing: 0.04em;
    font-size: 10.5px;
    text-transform: uppercase;
}}
.ticker__value {{
    color: {C.TEXT};
    font-weight: 700;
    letter-spacing: -0.01em;
}}
.ticker__delta.up {{ color: {C.PRIMARY_BRIGHT}; font-weight: 700; }}
.ticker__delta.down {{ color: {C.SELL}; font-weight: 700; }}
.ticker__delta.flat {{ color: {C.MUTED}; font-weight: 600; }}
.ticker__sep {{
    width: 1px;
    height: 12px;
    background: {C.BORDER_STRONG};
    flex-shrink: 0;
}}

/* ============================================================================
   Helper utilities
============================================================================ */
.note {{
    font-size: 13px;
    color: {C.MUTED};
    line-height: 1.6;
    letter-spacing: -0.005em;
}}
.code-inline {{
    font-family: var(--font-numeric);
    font-size: 12.5px;
    color: {C.TEXT_2};
    background: {C.SURFACE_2};
    padding: 3px 8px;
    border-radius: 6px;
    border: 1px solid {C.BORDER};
    letter-spacing: 0;
    font-weight: 600;
}}

hr {{ border: none; border-top: 1px solid {C.BORDER}; margin: 1.75rem 0 !important; }}

/* Expander */
[data-testid="stExpander"] {{
    background: {C.SURFACE} !important;
    border: 1px solid {C.BORDER} !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--inset-line);
    transition: border-color 0.18s var(--ease);
}}
[data-testid="stExpander"]:hover {{ border-color: {C.BORDER_STRONG} !important; }}
[data-testid="stExpander"] summary {{
    font-family: var(--font-sans) !important;
    color: {C.TEXT_2} !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 14px 18px !important;
}}
[data-testid="stExpander"] summary:hover {{ color: {C.TEXT} !important; }}

/* ============================================================================
   Calc CTA ── STEP 02 → STEP 03/04 사이의 "자산 리밸런싱 계산" 패널
   톤: 디지털 그리드 + 짙은 그린·블랙, 좌측 emerald marker + shimmer scan line
============================================================================ */
.calc-cta {{
    margin: 36px 0 18px;
    padding: 34px 38px 38px;
    background:
        radial-gradient(ellipse 900px 260px at 100% 0%, rgba(28,158,110,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 500px 240px at 0% 110%, rgba(19,111,77,0.12) 0%, transparent 65%),
        linear-gradient(180deg, {C.SURFACE_2} 0%, {C.SURFACE} 55%, {C.BG_2} 100%);
    border: 1px solid {C.BORDER_PRIMARY_STRONG};
    border-radius: 18px;
    position: relative;
    overflow: hidden;
    box-shadow:
        inset 0 1px 0 rgba(28,158,110,0.24),
        0 0 0 1px rgba(28,158,110,0.10),
        0 0 36px -8px rgba(28,158,110,0.22),
        0 16px 38px -14px rgba(0,0,0,0.55);
    isolation: isolate;
}}
/* 디지털 grid texture ── 데이터/AI 분위기 */
.calc-cta::before {{
    content: '';
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background-image:
        linear-gradient(rgba(94,224,165,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(94,224,165,0.045) 1px, transparent 1px);
    background-size: 32px 32px, 32px 32px;
    -webkit-mask-image: radial-gradient(ellipse 75% 60% at 50% 50%, #000 35%, transparent 100%);
            mask-image: radial-gradient(ellipse 75% 60% at 50% 50%, #000 35%, transparent 100%);
    opacity: 0.85;
}}
/* 상단 좌→우 emerald shimmer ── 한 줄 광선 */
.calc-cta::after {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 65%; height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(28,158,110,0.5) 35%,
        {C.PRIMARY_GLINT} 55%,
        rgba(28,158,110,0.5) 70%,
        transparent);
    animation: shimmer-x 5.5s var(--ease) infinite;
    opacity: 0.85;
    z-index: 1;
}}
.calc-cta > * {{ position: relative; z-index: 2; }}

/* 좌측 emerald marker ── 카드 종목 동일 strip */
.calc-cta__marker {{
    position: absolute;
    left: 0; top: 22px; bottom: 22px;
    width: 2px;
    background: linear-gradient(180deg, {C.PRIMARY_GLINT}, {C.PRIMARY_HOVER} 50%, {C.PRIMARY_DIM});
    border-radius: 0 2px 2px 0;
    box-shadow: 0 0 18px {C.PRIMARY_GLOW};
    z-index: 2;
}}

.calc-cta__eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 10px;
    font-weight: 800;
    color: {C.PRIMARY_HOVER};
    letter-spacing: 0.28em;
    text-transform: uppercase;
    font-family: var(--font-sans);
    background: {C.PRIMARY_SOFT};
    border: 1px solid {C.BORDER_PRIMARY};
    padding: 6px 14px 6px 12px;
    border-radius: 999px;
    line-height: 1;
}}
.calc-cta__eyebrow::before {{
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: {C.PRIMARY_GLINT};
    box-shadow: 0 0 0 3px rgba(28,158,110,0.20), 0 0 10px {C.PRIMARY_GLINT};
    animation: pulse 2.4s ease-in-out infinite;
    flex-shrink: 0;
}}

.calc-cta__title {{
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.035em;
    margin: 16px 0 12px;
    line-height: 1.1;
    background: linear-gradient(180deg, #ffffff 0%, #c2d3cc 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: var(--font-sans);
}}

.calc-cta__sub {{
    font-size: 14px;
    color: {C.TEXT_2};
    line-height: 1.7;
    max-width: 760px;
    margin: 0 0 4px;
    font-weight: 400;
    letter-spacing: -0.003em;
}}
.calc-cta__sub--next {{
    margin-top: 14px;
}}
.calc-cta__sub b {{
    color: {C.PRIMARY_GLINT};
    font-weight: 700;
}}

/* 자산 리밸런싱 계산 버튼 (key=calc_run) ── CTA 카드와 톤 일치하는 큰 액션 박스 */
.st-key-calc_run .stButton button,
[data-testid="stElementContainer"].st-key-calc_run .stButton button {{
    position: relative !important;
    min-height: 82px !important;
    height: 82px !important;
    font-size: 16px !important;
    letter-spacing: 0.08em !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    color: {C.PRIMARY_INK} !important;
    border-radius: 16px !important;
    border: 1px solid {C.BORDER_PRIMARY_STRONG} !important;
    background-color: {C.SURFACE} !important;
    background-image:
        linear-gradient(rgba(94,224,165,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(94,224,165,0.05) 1px, transparent 1px),
        radial-gradient(ellipse 800px 260px at 100% 50%, rgba(94,224,165,0.22) 0%, transparent 60%),
        radial-gradient(ellipse 500px 240px at 0% 50%, rgba(28,158,110,0.20) 0%, transparent 65%),
        linear-gradient(180deg, {C.PRIMARY_HOVER} 0%, {C.PRIMARY} 60%, {C.PRIMARY_DIM} 100%) !important;
    background-size: 32px 32px, 32px 32px, auto, auto, auto !important;
    background-repeat: repeat, repeat, no-repeat, no-repeat, no-repeat !important;
    background-position: 0 0, 0 0, right center, left center, center !important;
    box-shadow:
        inset 2px 0 0 {C.PRIMARY_GLINT},
        inset 6px 0 14px -2px rgba(94,224,165,0.50),
        inset 0 1px 0 rgba(255,255,255,0.20),
        inset 0 -1px 0 rgba(0,0,0,0.24),
        0 0 0 1px rgba(28,158,110,0.20),
        0 0 36px -6px rgba(28,158,110,0.32),
        0 12px 30px -10px rgba(19,111,77,0.45) !important;
    overflow: hidden !important;
    transition: all 0.25s var(--ease) !important;
}}
/* 상단 좌→우 shimmer scan line (calc-cta와 동일) */
.st-key-calc_run .stButton button::before,
[data-testid="stElementContainer"].st-key-calc_run .stButton button::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 60%; height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(255,255,255,0.6) 40%,
        rgba(94,224,165,1) 55%,
        rgba(255,255,255,0.6) 70%,
        transparent);
    animation: shimmer-x 4.5s var(--ease) infinite;
    pointer-events: none;
}}
.st-key-calc_run .stButton button:hover,
[data-testid="stElementContainer"].st-key-calc_run .stButton button:hover {{
    transform: translateY(-1px) !important;
    border-color: {C.PRIMARY_GLINT} !important;
    box-shadow:
        inset 2px 0 0 {C.PRIMARY_GLINT},
        inset 6px 0 18px -2px rgba(94,224,165,0.65),
        inset 0 1px 0 rgba(255,255,255,0.22),
        inset 0 -1px 0 rgba(0,0,0,0.24),
        0 0 0 1px rgba(94,224,165,0.32),
        0 0 56px -4px rgba(28,158,110,0.50),
        0 18px 40px -10px rgba(28,158,110,0.55) !important;
}}
.st-key-calc_run .stButton button:disabled,
[data-testid="stElementContainer"].st-key-calc_run .stButton button:disabled {{
    opacity: 0.55 !important;
    cursor: not-allowed !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.06),
        inset 0 -1px 0 rgba(0,0,0,0.24),
        0 0 0 1px {C.BORDER} !important;
    background-image:
        linear-gradient(rgba(94,224,165,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(94,224,165,0.025) 1px, transparent 1px),
        linear-gradient(180deg, {C.SURFACE_3} 0%, {C.SURFACE_2} 100%) !important;
    border-color: {C.BORDER_STRONG} !important;
}}

/* ============================================================================
   Holdings stack card — 자산별 목표 비중 설정
   톤: 미래/디지털/AI/금속 — cool graphite + steel-cyan accent, scanline 텍스처
   구조: ① 헤더(이름+메타+✕ absolute) ② 입력 2-col ③ 통계 3-grid w/ vertical dividers
============================================================================ */
@keyframes hc-scan {{
    0%   {{ transform: translateX(-100%); opacity: 0; }}
    50%  {{ opacity: 0.7; }}
    100% {{ transform: translateX(100%); opacity: 0; }}
}}

/* nested container 식별 ── step-card 안에 .hc-head 포함된 wrapper만 holding-card.
   톤: KPI primary 카드 동일 (좌측 emerald marker, radial top-right glow, shimmer scan line) */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) {{
    position: relative !important;
    background:
        radial-gradient(ellipse 700px 200px at 100% 0%, rgba(28,158,110,0.16) 0%, transparent 60%),
        radial-gradient(ellipse 380px 180px at 0% 100%, rgba(19,111,77,0.07) 0%, transparent 65%),
        linear-gradient(180deg, {C.SURFACE_2} 0%, {C.SURFACE} 100%) !important;
    border: 1px solid {C.BORDER_PRIMARY} !important;
    border-radius: var(--radius-xl) !important;
    padding: 24px 28px 26px 28px !important;
    margin: 0 0 22px 0 !important;
    box-shadow:
        var(--inset-primary),
        0 12px 32px -10px rgba(19,111,77,0.28),
        var(--shadow-sm) !important;
    transition: border-color 0.25s var(--ease), box-shadow 0.25s var(--ease) !important;
    overflow: hidden !important;
    isolation: isolate;
}}
/* 좌측 emerald primary marker ── KPI primary 와 동일 */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head)::before {{
    content: '';
    position: absolute;
    left: 0; top: 16px; bottom: 16px;
    width: 2px;
    background: linear-gradient(180deg, {C.PRIMARY_GLINT}, {C.PRIMARY_HOVER} 35%, {C.PRIMARY_DIM});
    border-radius: 0 2px 2px 0;
    box-shadow: 0 0 18px {C.PRIMARY_GLOW};
    z-index: 2;
}}
/* 우상단으로 흐르는 shimmer scan line ── KPI primary 와 동일 */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head)::after {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 50%; height: 100%;
    background: linear-gradient(105deg,
        transparent 0%,
        transparent 35%,
        rgba(94,224,165,0.09) 48%,
        rgba(255,255,255,0.14) 50%,
        rgba(94,224,165,0.09) 52%,
        transparent 65%,
        transparent 100%);
    pointer-events: none;
    animation: shimmer-x 6.5s var(--ease) infinite;
    z-index: 0;
    opacity: 0.75;
    mix-blend-mode: screen;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head):hover {{
    border-color: {C.BORDER_PRIMARY_STRONG} !important;
    box-shadow:
        var(--inset-primary),
        0 16px 42px -12px rgba(28,158,110,0.36),
        var(--shadow-sm) !important;
}}
/* shimmer / glow가 카드 안의 콘텐츠 위에 표시되지 않도록 stacking */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) > * {{ position: relative; z-index: 1; }}

/* ── 1행: 헤더 ── 종목명 + 메타 + ✕ */
.hc-head {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-width: 0;
    padding-right: 44px;          /* ✕ 버튼 absolute 자리 확보 */
}}
.hc-name {{
    font-size: 18px;
    font-weight: 700;
    color: {C.TEXT};
    letter-spacing: -0.025em;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: var(--font-sans);
    background: linear-gradient(180deg, {C.TEXT} 0%, #d0dcd5 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.hc-meta {{
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    font-size: 11.5px;
    color: {C.MUTED};
    line-height: 1;
    font-variant-numeric: tabular-nums;
}}
.hc-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 11px;
    border-radius: 999px;
    font-size: 9.5px;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    border: 1px solid;
    font-family: var(--font-sans);
    line-height: 1;
}}
.hc-chip::before {{
    content: '';
    width: 4px; height: 4px;
    border-radius: 50%;
    background: currentColor;
    box-shadow: 0 0 8px currentColor;
}}
.hc-chip.kr {{
    background: {C.PRIMARY_SOFT};
    color: {C.PRIMARY_HOVER};
    border-color: {C.BORDER_PRIMARY};
}}
.hc-chip.us {{
    background: rgba(61,127,175,0.10);
    color: {C.US_BRIGHT};
    border-color: rgba(61,127,175,0.34);
}}
.hc-chip.cash {{
    background: {C.BRONZE_SOFT};
    color: {C.BRONZE};
    border-color: rgba(200,153,104,0.32);
}}
.hc-code {{
    font-family: var(--font-numeric);
    font-weight: 700;
    color: {C.TEXT_2};
    letter-spacing: 0.04em;
    font-size: 11px;
    padding: 3px 9px;
    background: rgba(255,255,255,0.022);
    border: 1px solid {C.BORDER};
    border-radius: 4px;
}}
.hc-price {{
    color: {C.MUTED};
    font-variant-numeric: tabular-nums;
    font-size: 11.5px;
    margin-left: auto;
    font-weight: 600;
    letter-spacing: 0.01em;
}}

/* 카드 내부 horizontal row 간격 */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"] {{
    gap: 16px !important;
    align-items: flex-end !important;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:nth-of-type(2) {{
    margin-top: 22px !important;
}}

/* ── 2행: 입력창 ── emerald 톤 일관, focus 시 primary border */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stNumberInput"] {{
    width: 100%;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stNumberInput"] [data-baseweb="base-input"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stNumberInput"] [data-baseweb="input"] {{
    height: 48px !important;
    min-height: 48px !important;
    border-radius: var(--radius-md) !important;
    overflow: visible !important;
    background: transparent !important;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) .stNumberInput input {{
    height: 48px !important;
    min-height: 48px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 0 16px !important;
    border: 1px solid {C.BORDER_STRONG} !important;
    border-radius: var(--radius-md) !important;
    background:
        linear-gradient(180deg, rgba(0,0,0,0.22) 0%, transparent 100%),
        {C.BG_2} !important;
    color: {C.TEXT} !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02) !important;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.015em;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) .stNumberInput input:focus {{
    border-color: {C.PRIMARY_HOVER} !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.02),
        inset 0 0 0 1px {C.PRIMARY_HOVER},
        0 0 0 4px {C.PRIMARY_SOFT} !important;
    outline: none !important;
    background:
        linear-gradient(180deg, rgba(28,158,110,0.04) 0%, transparent 100%),
        {C.BG_2} !important;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) label {{
    font-size: 9.5px !important;
    font-weight: 700 !important;
    color: {C.MUTED} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.22em !important;
    margin-bottom: 8px !important;
    display: inline-flex !important;
    align-items: center;
    gap: 6px;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) label::before {{
    content: '';
    width: 4px; height: 4px;
    background: {C.PRIMARY_HOVER};
    border-radius: 50%;
    box-shadow: 0 0 6px {C.PRIMARY_HOVER};
    flex-shrink: 0;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stNumberInput"] button {{
    height: 23px !important;
    width: 28px !important;
    background: {C.SURFACE_2} !important;
    border: 1px solid {C.BORDER} !important;
    color: {C.MUTED} !important;
    border-radius: 4px !important;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stNumberInput"] button:hover {{
    color: {C.PRIMARY_BRIGHT} !important;
    background: {C.PRIMARY_SOFT} !important;
    border-color: {C.BORDER_PRIMARY} !important;
}}

/* ── ✕ 삭제 버튼 ── 카드 우측, 헤더 종목명 수직 중앙에 정렬 */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type {{
    align-items: center !important;
    position: static;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"]:last-of-type {{
    position: absolute !important;
    top: 24px;          /* 카드 padding-top과 일치 */
    right: 24px;        /* 카드 padding-right과 일치 */
    width: auto !important;
    flex: 0 0 auto !important;
    z-index: 3;
    display: flex !important;
    align-items: center;
    justify-content: center;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"]:last-of-type > div {{
    display: flex !important;
    align-items: center;
    justify-content: center;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type .stButton {{
    margin: 0 !important;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type .stButton button {{
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid {C.BORDER} !important;
    color: {C.MUTED_DEEP} !important;
    font-size: 26px !important;
    font-weight: 400 !important;
    padding: 0 !important;
    height: 36px !important;
    min-height: 36px !important;
    width: 36px !important;
    min-width: 36px !important;
    border-radius: 7px !important;
    box-shadow: none !important;
    line-height: 1 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    transition: all 0.18s var(--ease);
}}
/* Streamlit 버튼 내부 <div><p> 마진/패딩 제거 + 폰트 크기 강제 ── × 문자가 정확히 중앙에 32px로 오도록 */
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type .stButton button > div,
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type .stButton button > div > p,
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type .stButton button [data-testid="stMarkdownContainer"],
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type .stButton button [data-testid="stMarkdownContainer"] p {{
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 26px !important;
    font-weight: 400 !important;
}}

/* :has() 미지원 환경 대비 — Streamlit이 버튼 key별로 부여하는 클래스로 직접 타겟 */
[class*="st-key-_del_"] button,
[class*="st-key-_del_"] button *,
[class*="st-key-_del_"] button p,
[class*="st-key-_del_"] button [data-testid="stMarkdownContainer"] p {{
    font-size: 26px !important;
    font-weight: 400 !important;
    line-height: 1 !important;
}}
[class*="st-key-_del_"] button {{
    height: 36px !important;
    min-height: 36px !important;
    width: 36px !important;
    min-width: 36px !important;
}}
[data-testid="stVerticalBlockBorderWrapper"]:has(.hc-head) [data-testid="stHorizontalBlock"]:first-of-type .stButton button:hover {{
    background: rgba(196,84,98,0.14) !important;
    color: {C.SELL} !important;
    border-color: rgba(196,84,98,0.45) !important;
    transform: none !important;
    box-shadow: 0 0 0 3px rgba(196,84,98,0.08) !important;
}}
/* 헤더의 종목명/메타 영역이 ✕ 버튼 자리만큼 여유 갖도록 */
.hc-head {{ padding-right: 52px !important; }}

/* ── 3행: 통계 row ── 평가 / 현재 비중 / 이탈 (리밸런싱 결정의 핵심 지표) */
.hc-stats {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0;
    padding: 18px 0 6px;
    margin-top: 22px;
    border-top: 1px solid {C.BORDER};
    position: relative;
}}
.hc-stats::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 44px; height: 1px;
    background: linear-gradient(90deg, {C.PRIMARY_HOVER}, transparent);
}}
.hc-stat {{
    display: flex;
    flex-direction: column;
    gap: 9px;
    padding: 2px 20px;
    min-width: 0;
    border-right: 1px solid {C.BORDER};
    position: relative;
}}
.hc-stat:first-child  {{ padding-left: 0; }}
.hc-stat:last-child   {{ padding-right: 0; border-right: none; text-align: right; align-items: flex-end; }}
.hc-stat:nth-child(2) {{ text-align: center; align-items: center; }}
.hc-stat-label {{
    font-size: 9px;
    font-weight: 800;
    color: {C.MUTED_DEEP};
    text-transform: uppercase;
    letter-spacing: 0.22em;
    font-family: var(--font-sans);
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}
.hc-stat-label::before {{
    content: '';
    width: 4px; height: 4px;
    border-radius: 50%;
    background: {C.PRIMARY_HOVER};
    box-shadow: 0 0 6px {C.PRIMARY_GLOW};
}}
.hc-stat:nth-child(2) .hc-stat-label {{ justify-content: center; }}
.hc-stat:last-child .hc-stat-label   {{ justify-content: flex-end; }}
.hc-stat-value {{
    font-size: 20px;
    font-weight: 800;
    color: {C.TEXT};
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.03em;
    line-height: 1.1;
    font-family: var(--font-sans);
    background: linear-gradient(180deg, {C.TEXT} 0%, #d0dcd5 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.hc-stat-unit {{
    font-size: 11.5px;
    font-weight: 600;
    color: {C.MUTED};
    margin-left: 4px;
    letter-spacing: 0;
    -webkit-text-fill-color: {C.MUTED};
}}
.hc-stat-value.drift-ok    {{
    color: {C.PRIMARY_HOVER};
    -webkit-text-fill-color: {C.PRIMARY_HOVER};
    text-shadow: 0 0 18px {C.PRIMARY_GLOW};
}}
.hc-stat-value.drift-over  {{
    color: {C.SELL};
    -webkit-text-fill-color: {C.SELL};
    text-shadow: 0 0 18px rgba(196,84,98,0.28);
}}
.hc-stat-value.drift-under {{
    color: {C.BRONZE};
    -webkit-text-fill-color: {C.BRONZE};
    text-shadow: 0 0 18px rgba(200,153,104,0.28);
}}

</style>
"""
