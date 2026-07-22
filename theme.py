"""Karben4 brand theme for the Streamlit QM Yield Tool.

Colors/fonts pulled directly from karben4.com (2026-07-07):
navy #161B23 (body/bg), green #7BE72D (primary accent), gold #F5D500 (secondary
accent), Bebas Neue (headings), Mulish (body), Exo (buttons/labels).

Design pass (2026-07-14, ui-ux-pro-max): pattern = Data-Dense Dashboard. Kept the
Karben4 brand as the industry palette; hardened it against the skill's rules —
semantic status tokens (amber/red, not green-only), tabular numerals for data,
reduced-motion support, keyboard focus rings on every control, a differentiated
heading scale, denser dashboard spacing, and an on-brand Altair chart theme so
every chart matches (green/gold, subtle gridlines, tooltips).
"""

import altair as alt
import streamlit as st

NAVY = "#161B23"
NAVY_SURFACE = "#1E2530"
NAVY_SURFACE_2 = "#252D3A"
GREEN = "#7BE72D"
GOLD = "#F5D500"
TEXT = "#F4F6F8"
TEXT_MUTED = "#A7B0BD"   # lightened from #9AA4B2 → ~5.6:1 on navy (WCAG AA for body)
BORDER = "#333B47"

# Semantic status colors — distinct from the green *accent* so meaning is never
# carried by "is it green?" alone (WCAG color-not-only). Tuned for ≥4.5:1 on navy.
AMBER = "#F5A623"   # warning / caution
RED = "#FF6B6B"     # error / destructive
INFO = "#5AB8FF"    # neutral information

# Categorical chart palette — brand-led, then colorblind-distinguishable hues.
CHART_CATEGORY = [GREEN, GOLD, INFO, "#FF8A65", "#BA68C8", "#4DB6AC", "#F5A623", "#E57373"]

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Exo:wght@500;600;700&family=Mulish:wght@400;500;600;700&display=swap');

:root {{
  --k4-navy: {NAVY};
  --k4-surface: {NAVY_SURFACE};
  --k4-surface-2: {NAVY_SURFACE_2};
  --k4-green: {GREEN};
  --k4-gold: {GOLD};
  --k4-amber: {AMBER};
  --k4-red: {RED};
  --k4-info: {INFO};
  --k4-text: {TEXT};
  --k4-text-muted: {TEXT_MUTED};
  --k4-border: {BORDER};
}}

html, body, [class*="css"] {{
  font-family: 'Mulish', sans-serif;
  color: var(--k4-text);
}}

.stApp {{
  background:
    radial-gradient(1200px 500px at 10% -10%, rgba(123,231,45,0.06), transparent 60%),
    var(--k4-navy);
}}

/* Density: tighten the default Streamlit shell for a data-dashboard feel (density dial 8).
   Reclaims vertical space up top and narrows side gutters so more data is above the fold. */
.block-container {{ padding-top: 2.4rem !important; padding-bottom: 2.5rem !important; }}
[data-testid="stVerticalBlock"] {{ gap: 0.75rem; }}

/* Tabular figures everywhere numbers are read as data — stops columns/metrics from
   jittering as digits change (number-tabular). */
[data-testid="stMetricValue"], [data-testid="stDataFrame"], [data-testid="stTable"],
[data-testid="stMetricDelta"], .stCode, code, pre,
[data-testid="stText"], [data-testid="stNumberInput"] input {{
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum" 1;
}}

/* Honeycomb watermark strip under the header, echoing the K4 logo hexagons.
   Clear top margin so the hexagons sit BELOW the H1's green underline instead of
   the green rule cutting through them. */
.k4-hex-rule {{
  display: flex;
  gap: 6px;
  margin: 1.5rem 0 1.2rem 0;
}}
/* Tight line-height + no bottom margin so the green underline hugs the text and
   its line-box leading doesn't push the following hex strip up into the rule. */
h1 {{ margin-bottom: 0 !important; line-height: 1.02 !important; }}
.k4-hex-rule span {{
  width: 22px;
  height: 22px;
  clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
}}

/* Small on-brand status badges (replace ✅/⚠️ emoji — token-driven, theme-consistent) */
.k4-badge {{
  display: inline-flex; align-items: center; gap: 6px;
  font-family: 'Exo', sans-serif; font-weight: 600; font-size: 0.72rem;
  letter-spacing: 0.03em; text-transform: uppercase;
  padding: 2px 9px; border-radius: 999px; border: 1px solid transparent;
}}
.k4-badge::before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; background: currentColor; }}
.k4-badge--ok {{ color: var(--k4-green); border-color: rgba(123,231,45,0.35); background: rgba(123,231,45,0.10); }}
.k4-badge--warn {{ color: var(--k4-amber); border-color: rgba(245,166,35,0.35); background: rgba(245,166,35,0.10); }}

/* Headings — Bebas Neue, condensed industrial, gold like the brewery's H1s.
   Differentiated scale so h1 > h2 > h3 read as distinct hierarchy levels, not
   three equally-loud all-caps shouts (visual-hierarchy). */
h1, h2, h3, .stApp [data-testid="stMarkdownContainer"] h1,
.stApp [data-testid="stMarkdownContainer"] h2, .stApp [data-testid="stMarkdownContainer"] h3 {{
  font-family: 'Bebas Neue', sans-serif;
  letter-spacing: 0.03em;
  color: var(--k4-gold);
  text-transform: uppercase;
}}
h1 {{ font-size: 2.6rem !important; border-bottom: 3px solid var(--k4-green); padding-bottom: 0.4rem; display: inline-block; }}
h2 {{ font-size: 1.7rem !important; letter-spacing: 0.04em; }}
h3 {{ font-size: 1.32rem !important; color: var(--k4-text) !important; letter-spacing: 0.05em; }}
h4, h5, h6 {{ font-family: 'Exo', sans-serif; color: var(--k4-text); }}

/* Caption under the title */
[data-testid="stCaptionContainer"] {{ color: var(--k4-text-muted); font-family: 'Mulish', sans-serif; }}

/* Sidebar */
[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #10141B 0%, var(--k4-navy) 100%);
  border-right: 1px solid var(--k4-border);
}}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
  color: var(--k4-green);
  font-family: 'Bebas Neue', sans-serif;
}}

/* Tabs styled like the brewery's top nav pills */
.stTabs [data-baseweb="tab-list"] {{
  gap: 4px;
  background: var(--k4-surface);
  padding: 6px;
  border-radius: 10px;
  border: 1px solid var(--k4-border);
  flex-wrap: wrap;   /* 9 tabs shouldn't force a horizontal scroll on narrower windows */
}}
.stTabs [data-baseweb="tab"] {{
  font-family: 'Exo', sans-serif;
  font-weight: 600;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  font-size: 0.85rem;
  color: var(--k4-text-muted);
  border-radius: 7px;
  padding: 8px 16px;
  transition: color 120ms ease, background 120ms ease;
}}
.stTabs [data-baseweb="tab"]:hover {{ color: var(--k4-text); background: var(--k4-surface-2); }}
.stTabs [aria-selected="true"] {{
  background: var(--k4-green) !important;
  color: var(--k4-navy) !important;
}}
.stTabs [data-baseweb="tab"]:focus-visible {{ outline: 2px solid var(--k4-gold); outline-offset: 2px; }}
.stTabs [data-baseweb="tab-highlight"] {{ background-color: transparent; }}
.stTabs [data-baseweb="tab-border"] {{ display: none; }}

/* Buttons — bright green "SHOP"-style CTA */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
  font-family: 'Exo', sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  background: var(--k4-green);
  color: var(--k4-navy);
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1.1rem;
  transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
}}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {{
  background: #8FF23F;
  box-shadow: 0 0 0 3px rgba(123,231,45,0.25);
  transform: translateY(-1px);
}}
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible,
.stFormSubmitButton > button:focus-visible {{ outline: 2px solid var(--k4-gold); outline-offset: 2px; }}
.stButton > button:disabled {{ opacity: 0.45; cursor: not-allowed; }}

/* Secondary / delete-style buttons keep gold outline instead of solid green fill */
button[kind="secondary"] {{
  background: transparent !important;
  color: var(--k4-gold) !important;
  border: 1.5px solid var(--k4-gold) !important;
}}
/* Destructive (type="primary" used for Delete) reads as danger, not another green CTA
   (destructive-emphasis: dangerous actions use the semantic danger color). */
button[kind="primary"] {{
  background: transparent !important;
  color: var(--k4-red) !important;
  border: 1.5px solid var(--k4-red) !important;
}}
button[kind="primary"]:hover {{ background: rgba(255,107,107,0.12) !important; box-shadow: none !important; }}

/* Metrics / stat tiles */
[data-testid="stMetric"] {{
  background: var(--k4-surface);
  border: 1px solid var(--k4-border);
  border-left: 4px solid var(--k4-green);
  border-radius: 8px;
  padding: 0.9rem 1rem;
}}
[data-testid="stMetricLabel"] {{
  font-family: 'Exo', sans-serif;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  color: var(--k4-text-muted);
}}
[data-testid="stMetricValue"] {{
  font-family: 'Bebas Neue', sans-serif;
  color: var(--k4-gold);
  font-size: 2rem;
}}

/* Dataframes / tables */
[data-testid="stDataFrame"], [data-testid="stTable"] {{
  border: 1px solid var(--k4-border);
  border-radius: 8px;
  overflow: hidden;
}}
[data-testid="stDataFrame"] div[role="columnheader"] {{
  background: var(--k4-surface-2) !important;
  color: var(--k4-gold) !important;
  font-family: 'Exo', sans-serif;
  text-transform: uppercase;
  font-size: 0.78rem;
  letter-spacing: 0.03em;
}}
/* Row hover highlight — makes scanning wide data tables easier (chart/table best practice) */
[data-testid="stDataFrame"] div[role="row"]:hover {{ background: rgba(123,231,45,0.06) !important; }}

/* Inputs, selects, sliders */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div, .stDateInput input {{
  background: var(--k4-surface) !important;
  color: var(--k4-text) !important;
  border: 1px solid var(--k4-border) !important;
  border-radius: 6px !important;
}}
/* Keyboard focus rings on every interactive control, not just buttons (focus-states) */
.stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus,
.stSelectbox div[data-baseweb="select"]:focus-within,
.stMultiSelect div[data-baseweb="select"]:focus-within {{
  border-color: var(--k4-green) !important;
  box-shadow: 0 0 0 2px rgba(123,231,45,0.30) !important;
}}
.stSlider [role="slider"]:focus-visible {{ outline: 2px solid var(--k4-gold); outline-offset: 2px; }}
.stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"] {{ color: var(--k4-text-muted); }}

/* Expanders / containers */
[data-testid="stExpander"] {{
  background: var(--k4-surface);
  border: 1px solid var(--k4-border);
  border-radius: 8px;
}}

/* Alerts — semantic left-border per severity so meaning isn't color-fill-only */
[data-testid="stAlert"] {{ border-radius: 8px; font-family: 'Mulish', sans-serif; }}
.stSuccess {{ border-left: 4px solid var(--k4-green) !important; }}
.stWarning {{ border-left: 4px solid var(--k4-amber) !important; }}
.stError {{ border-left: 4px solid var(--k4-red) !important; }}
.stInfo {{ border-left: 4px solid var(--k4-info) !important; }}

/* Charts (Vega/Altair) sit on a themed surface */
[data-testid="stArrowVegaLiteChart"], .vega-embed {{
  background: var(--k4-surface) !important;
  border-radius: 8px;
  padding: 0.5rem;
  border: 1px solid var(--k4-border);
}}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {{
  background: var(--k4-surface);
  border: 1.5px dashed var(--k4-border);
  border-radius: 8px;
}}

hr {{ border-color: var(--k4-border); }}

/* Respect the OS "reduce motion" setting — kill transforms/transitions for users who
   opt out (WCAG reduced-motion; motion here is decorative, so it's safe to drop). */
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    animation-duration: 0.001ms !important;
    transition-duration: 0.001ms !important;
  }}
  .stButton > button:hover, .stDownloadButton > button:hover,
  .stFormSubmitButton > button:hover {{ transform: none !important; }}
}}
</style>
"""

HEX_RULE_HTML = (
    '<div class="k4-hex-rule">'
    f'<span style="background:{TEXT_MUTED};"></span>'
    f'<span style="background:{GREEN};"></span>'
    f'<span style="background:{NAVY_SURFACE_2};border:1px solid {BORDER};"></span>'
    f'<span style="background:{TEXT_MUTED};"></span>'
    '</div>'
)


def badge(text: str, kind: str = "ok") -> str:
    """Inline on-brand status badge (HTML). kind ∈ {'ok','warn'}. Use with
    st.markdown(..., unsafe_allow_html=True) in place of ✅/⚠️ emoji."""
    cls = {"ok": "k4-badge--ok", "warn": "k4-badge--warn"}.get(kind, "k4-badge--ok")
    return f'<span class="k4-badge {cls}">{text}</span>'


def _altair_theme():
    """On-brand Altair/Vega config so every chart matches the app: dark surface,
    Karben4 categorical palette, subtle gridlines, readable axis labels."""
    return {
        "config": {
            "background": NAVY_SURFACE,
            "view": {"stroke": "transparent"},
            "title": {"color": TEXT, "font": "Exo", "fontSize": 14, "fontWeight": 600},
            "axis": {
                "labelColor": TEXT_MUTED, "titleColor": TEXT,
                "labelFont": "Mulish", "titleFont": "Exo", "titleFontWeight": 600,
                "gridColor": "#2A3340", "gridOpacity": 0.6,   # subtle, low-contrast gridlines
                "domainColor": BORDER, "tickColor": BORDER,
                "labelFontSize": 11, "titleFontSize": 12,
            },
            "legend": {
                "labelColor": TEXT, "titleColor": TEXT_MUTED,
                "labelFont": "Mulish", "titleFont": "Exo",
            },
            "range": {"category": CHART_CATEGORY},
            "line": {"color": GREEN, "strokeWidth": 2.5},
            "point": {"color": GREEN, "size": 55},
            "circle": {"color": GREEN},
            "bar": {"color": GREEN},
        }
    }


def apply():
    """Inject the Karben4 brand theme + register the brand Altair chart theme.
    Call once, right after st.set_page_config()."""
    st.markdown(CSS, unsafe_allow_html=True)
    try:
        alt.themes.register("karben4", _altair_theme)
        alt.themes.enable("karben4")
    except Exception:
        # Never let a charting-lib quirk brick the app's startup.
        pass
