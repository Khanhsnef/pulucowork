import io
from datetime import datetime, timedelta
import pandas as pd
import requests
import streamlit as st

try:
    import plotly.graph_objects as go
    import plotly.express as px
except ImportError:  # pragma: no cover
    go = None
    px = None


# ── PAGE CONFIGURATION ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SGN Ops Overview — Ahamove",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── BRAND SYSTEM (CSS INJECTION - PREMIUM DARK MODE) ──────────────────────────
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    :root {
        --bg: #0f172a;
        --card: #1e293b;
        --card-soft: rgba(30, 41, 59, 0.55);
        --border: #334155;
        --text: #f8fafc;
        --muted: #94a3b8;
        --emerald: #10b981;
        --rose: #fb7185;
        --amber: #fbbf24;
        --blue: #3b82f6;
    }

    .stApp, html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    [class*="css"], table, th, td, input, select, button, div, span, p {
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background: var(--card) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }
    [data-testid="stSidebar"] .stButton button {
        background: #0f172a !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.75rem !important;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background: #334155 !important;
        border-color: var(--blue) !important;
    }

    .main-title {
        color: var(--text) !important;
        font-weight: 900;
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.035em;
        background: none !important;
        -webkit-text-fill-color: var(--text) !important;
    }
    .subtitle {
        color: var(--muted) !important;
        font-weight: 600;
        font-size: 0.98rem;
        margin-bottom: 1.1rem;
    }
    .section-header {
        color: var(--text) !important;
        font-weight: 900;
        font-size: 1.18rem;
        border-left: 4px solid var(--blue);
        padding-left: 0.75rem;
        margin: 1.5rem 0 0.85rem 0;
        letter-spacing: -0.02em;
    }
    .metric-group-label {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted) !important;
        padding: 0.75rem 0 0.45rem;
        border-top: 1px solid rgba(51,65,85,0.7);
        margin-top: 0.9rem;
    }

    .metric-card {
        background: var(--card) !important;
        border: 1px solid var(--border);
        border-radius: 1rem;
        padding: 1.15rem 1.15rem;
        min-height: 128px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: none;
        transition: background-color 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
    }
    .metric-card * { background-color: transparent !important; }
    .metric-card:hover {
        background: rgba(30,41,59,0.82) !important;
        border-color: #475569;
        transform: translateY(-1px);
    }
    .metric-card-accent, .metric-card-green, .metric-card-blue { border-color: var(--border) !important; }
    .metric-card-header {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.55rem;
    }
    .metric-icon { color: #60a5fa !important; font-size: 1rem; line-height: 1; }
    .metric-label {
        color: var(--muted) !important;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: -0.01em;
    }
    .metric-value {
        color: var(--text) !important;
        font-size: 1.82rem;
        font-weight: 900;
        letter-spacing: -0.045em;
        line-height: 1.05;
        margin: 0.15rem 0 0.35rem;
        font-variant-numeric: tabular-nums;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: clip;
    }
    .metric-value-lg { font-size: 2.1rem; font-weight: 900; letter-spacing: -0.045em; }
    .metric-context { color: var(--muted) !important; font-size: 0.72rem; line-height: 1.45; margin-top: 0.35rem; }
    .metric-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.5rem; }

    .delta-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.2rem;
        min-width: 4.35rem;
        padding: 0.26rem 0.5rem;
        border-radius: 0.18rem;
        font-size: 0.74rem;
        font-weight: 900;
        line-height: 1;
        white-space: nowrap;
        border: 1px solid transparent;
        font-variant-numeric: tabular-nums;
    }
    .delta-badge .badge-label { color: var(--muted) !important; font-size: 0.72rem; font-weight: 800; margin-right: 0.1rem; }
    .delta-badge.pos { color: var(--emerald) !important; background: rgba(16,185,129,0.10) !important; border-color: rgba(16,185,129,0.16); }
    .delta-badge.neg { color: var(--rose) !important; background: rgba(251,113,133,0.10) !important; border-color: rgba(251,113,133,0.16); }
    .delta-badge.neu { color: var(--muted) !important; background: rgba(148,163,184,0.10) !important; border-color: rgba(148,163,184,0.14); }

    .pill-on-track { display:inline-flex; padding:0.22rem 0.6rem; border-radius:0.5rem; font-size:0.72rem; font-weight:800; background:rgba(16,185,129,0.10); color:var(--emerald); border:1px solid rgba(16,185,129,0.16); }
    .pill-attention { display:inline-flex; padding:0.22rem 0.6rem; border-radius:0.5rem; font-size:0.72rem; font-weight:800; background:rgba(251,191,36,0.10); color:var(--amber); border:1px solid rgba(251,191,36,0.16); }
    .pill-below { display:inline-flex; padding:0.22rem 0.6rem; border-radius:0.5rem; font-size:0.72rem; font-weight:800; background:rgba(251,113,133,0.10); color:var(--rose); border:1px solid rgba(251,113,133,0.16); }
    .status-pill { display:inline-flex; background:rgba(16,185,129,0.10); color:var(--emerald); border:1px solid rgba(16,185,129,0.16); border-radius:999px; padding:0.25rem 0.65rem; font-weight:800; font-size:0.75rem; }

    .cockpit-table-container {
        overflow-x: auto;
        margin: 1rem 0;
        border-radius: 1rem;
        border: 1px solid var(--border);
        background: var(--card-soft);
    }
    .cockpit-table {
        width: 100%;
        border-collapse: collapse;
        table-layout: auto;
        color: var(--text);
        font-size: 0.8rem;
        text-align: left;
        font-variant-numeric: tabular-nums;
    }
    .cockpit-table th {
        background: #0f172a !important;
        color: var(--muted) !important;
        font-weight: 800;
        padding: 0.5rem 0.7rem;
        border-bottom: 1px solid var(--border);
        text-transform: uppercase;
        font-size: 0.66rem;
        letter-spacing: 0.06em;
        white-space: nowrap;
    }
    .cockpit-table td {
        background: transparent !important;
        padding: 0.48rem 0.7rem;
        border-bottom: 1px solid var(--border);
        font-weight: 700;
        white-space: nowrap;
        text-align: right;
        height: 2.25rem;
    }
    .cockpit-table th:first-child, .cockpit-table td:first-child { text-align: left; }
    .cockpit-table tr { transition: background-color 0.12s ease; }
    .cockpit-table tr:hover { background-color: #334155 !important; filter: none; }
    .cockpit-table .row-header { color: #60a5fa !important; font-weight: 800; }
    .cockpit-table .row-header td { border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); font-size: 0.86rem; }
    .cockpit-table .sub-row-header { color: #cbd5e1 !important; padding-left: 1.65rem !important; font-weight: 600; }
    .cockpit-table .sticky-col { position: sticky; left: 0; z-index: 3; background: #0f172a !important; box-shadow: 8px 0 14px -14px rgba(0,0,0,0.9); }
    .cockpit-table td.sticky-col { background: #111827 !important; }
    .cockpit-table tr:hover td.sticky-col { background: #334155 !important; }
    .cockpit-table .delta-badge { min-width: 3.9rem; padding: 0.18rem 0.35rem; border-radius: 0; font-size: 0.76rem; }
    .cockpit-table .delta-badge .badge-label { display: none; }

    .hdr-actual-current, .hdr-actual-past, .hdr-plan, .hdr-today {
        background: #0f172a !important;
        color: var(--muted) !important;
        text-align: center !important;
        border-color: var(--border) !important;
    }
    .val-positive { color: var(--emerald) !important; font-weight: 800; }
    .val-negative { color: var(--rose) !important; font-weight: 800; }
    .val-neutral { color: var(--muted) !important; }
    .val-planning-today { color: var(--emerald) !important; background: rgba(16,185,129,0.10) !important; border-radius: 0.35rem; padding: 0.1rem 0.35rem; }

    .analysis-table { width:100%; border-collapse:collapse; color:var(--text); font-size:0.84rem; }
    .analysis-table th { background:#0f172a !important; color:var(--muted) !important; font-weight:800; padding:0.6rem 0.65rem; border-bottom:1px solid var(--border); text-transform:uppercase; font-size:0.68rem; letter-spacing:0.05em; text-align:center; white-space:nowrap; }
    .analysis-table th:first-child { text-align:left; }
    .analysis-table td { padding:0.58rem 0.65rem; border-bottom:1px solid var(--border); text-align:center; }
    .analysis-table td:first-child { text-align:left; font-weight:800; }
    .analysis-table tr:hover { background-color:#334155 !important; }
    .analysis-table .total-row { background:rgba(59,130,246,0.08) !important; font-weight:800; color:#60a5fa !important; border-top:1px solid var(--border); }

    .leaderboard-card { background:var(--card); border:1px solid var(--border); border-radius:1rem; padding:1rem; margin-bottom:0.75rem; }
    .leaderboard-title { color:var(--text); font-weight:800; font-size:0.9rem; margin-bottom:0.65rem; text-transform:uppercase; letter-spacing:0.05em; }
    .leaderboard-row { display:flex; justify-content:space-between; align-items:center; padding:0.42rem 0.65rem; margin-bottom:0.35rem; border-radius:0.5rem; background:rgba(15,23,42,0.45); }
    .rank-1, .rank-2, .rank-3 { border:1px solid var(--border); }
    .rank-1 .rank-badge { color:var(--emerald); }
    .rank-2 .rank-badge { color:var(--amber); }
    .rank-3 .rank-badge { color:#60a5fa; }

    .hm-pass { background:rgba(16,185,129,0.18); color:var(--emerald); font-weight:800; }
    .hm-under { background:rgba(251,113,133,0.18); color:var(--rose); font-weight:800; }
    .hm-over { background:rgba(251,191,36,0.16); color:var(--amber); font-weight:800; }
    .hm-na { color:#475569; }
    .footer-note { color: var(--muted); font-size: 0.78rem; padding-top: 0.6rem; border-top: 1px solid var(--border); margin-top: 1.5rem; }
    .footer-note a { color: #60a5fa; text-decoration: none; }
</style>
""",
    unsafe_allow_html=True,
)

# ── SOURCE CONFIGURATION ──────────────────────────────────────────────────────
SHEET_ID = "1Nbc4NYg3u8TxEh1acuWvDH-p6_8Nz8bDNF3j4bLGWvM"
SHEET_GID = "743032311"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit?gid={SHEET_GID}#gid={SHEET_GID}"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SHEET_GID}"
CACHE_TTL_SECONDS = 900

COL_LM = 2
COL_MTD = 3
COL_MOM = 4
DAILY_START_COL = 5
REPORT_YEAR = 2026

# ── ROW MAPPINGS (verified against live sheet) ────────────────────────────────
# FC rows (row 5 = Total, 6=SME+MP+KA, 7=GHN, 8=KA, 9=MP, 10=SME, 11=TRUCK, 12=WH)
FC_REQUEST_ROW = 5
FC_DEMAND_ROW = 13

# Actual rows (row 21=Total, 22=SME+MP+KA, 23=GHN, 24=KA, 25=MP, 26=SME, 27=WH)
ACTUAL_REQUEST_ROW = 21
ACTUAL_DEMAND_ROW = 28

# % FC Achievement rows
PCT_REQUEST_ROW = 35     # row 35 = Total % Request
PCT_DEMAND_ROW = 42      # row 42 = Total % Demand

# FR % by channel rows (row 180=Total, 181=SME+MP+KA, 182=GHN, 183=KA, 184=MP, 185=SME, 186=WH)
FR_ROWS = {
    "Total": 180,
    "SME+MP+KA": 181,
    "GHN": 182,
    "KA": 183,
    "MP": 184,
    "SME": 185,
    "WH": 186,
}

# Supply rows
ACTIVE_TOTAL_ROW = 50
CAPACITY_TOTAL_ROW = 58
ONLINE_HOURS_TOTAL_ROW = 66
PRODUCTIVITY_TOTAL_ROW = 74
ONLINE_PER_DRIVER_TOTAL_ROW = 82
PROD_PER_ONLINEHOUR_TOTAL_ROW = 90

# Active by segment (rows 50-57: total, FT, PT, NLM, Return, NIM, NID, NIM)
ACTIVE_SEG_ROWS = {"FT": 51, "PT": 52, "NLM": 53, "Return": 54, "NIM": 55, "NID": 56}
CAP_SEG_ROWS = {"FT": 59, "PT": 60, "NLM": 61, "Return": 62, "NIM": 63, "NID": 64}
SH_SEG_ROWS = {"FT": 67, "PT": 68, "NLM": 69, "Return": 70, "NIM": 71, "NID": 72}
PROD_SEG_ROWS = {"FT": 75, "PT": 76, "NLM": 77, "Return": 78, "NIM": 79}
ONLINE_DR_SEG_ROWS = {"FT": 83, "PT": 84, "NLM": 85, "Return": 86, "NIM": 87}
PROD_ONLINE_SEG_ROWS = {"FT": 91, "PT": 92, "NLM": 93, "Return": 94, "NIM": 95}

# Active by time window (active_1h/2h/4h per segment)
ACTIVE_TIME_ROWS = {
    "FT":     {"total": 99,  "1h": 100, "2h": 105, "4h": 110},
    "PT":     {"total": 112, "1h": 113, "2h": 118, "4h": 123},
    "NLM":    {"total": 125, "1h": 126, "2h": 131, "4h": 136},
    "NIM":    {"total": 151, "1h": 154, "2h": 159, "4h": 164},
    "Total":  {"total": 166, "1h": 167, "2h": 172, "4h": 177},
}

# Channel FC rows
CHANNEL_FC_REQ_ROWS = {"GHN": 7, "KA": 8, "MP": 9, "SME": 10, "TRUCK": 11, "WH": 12}
CHANNEL_FC_DEM_ROWS = {"GHN": 15, "KA": 16, "MP": 17, "SME": 18, "TRUCK": 19, "WH": 20}
CHANNEL_ACT_REQ_ROWS = {"GHN": 23, "KA": 24, "MP": 25, "SME": 26, "WH": 27}
CHANNEL_ACT_DEM_ROWS = {"GHN": 30, "KA": 31, "MP": 32, "SME": 33, "WH": 34}
PCT_REQ_CH_ROWS = {"GHN": 37, "KA": 38, "MP": 39, "SME": 40, "TRUCK": 41, "WH": 41}
PCT_DEM_CH_ROWS = {"GHN": 44, "KA": 45, "MP": 46, "SME": 47, "TRUCK": 48, "WH": 48}

METRIC_ROWS = {
    "request": ACTUAL_REQUEST_ROW,
    "demand": ACTUAL_DEMAND_ROW,
    "active_actual": ACTIVE_TOTAL_ROW,
    "capacity": CAPACITY_TOTAL_ROW,
    "online_hours": ONLINE_HOURS_TOTAL_ROW,
    "productivity": PRODUCTIVITY_TOTAL_ROW,
    "online_per_driver": ONLINE_PER_DRIVER_TOTAL_ROW,
    "prod_per_online_hour": PROD_PER_ONLINEHOUR_TOTAL_ROW,
}

CHANNEL_ROWS = {
    "GHN": 7, "KA": 8, "MP": 9, "SME": 10, "TRUCK": 11, "WH": 12,
}
SEGMENT_ROWS = {"FT": 51, "PT": 52, "NLM": 53, "Return": 54, "NIM": 55}

ACHIEVEMENT_REQUEST_ROWS = {"GHN": 37, "KA": 38, "MP": 39, "SME": 40, "TRUCK": 41, "WH": 41}
ACHIEVEMENT_DEMAND_ROWS = {"GHN": 44, "KA": 45, "MP": 46, "SME": 47, "TRUCK": 48, "WH": 48}

CHANNEL_COLORS = {
    "GHN": "#3b82f6", "KA": "#3b82f6", "MP": "#10B981",
    "SME": "#6366F1", "TRUCK": "#94A3B8", "WH": "#F59E0B",
    "SME+MP+KA": "#A78BFA", "Total": "#F8FAFC",
}
SEGMENT_COLORS = {
    "FT": "#3b82f6", "PT": "#3b82f6", "NLM": "#10B981",
    "Return": "#6366F1", "NIM": "#EF4444", "NID": "#F59E0B",
}


# ── DATA LOADING & TRANSFORMATION ────────────────────────────────────────────
@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner="Đang tải dữ liệu từ Google Sheet...")
def load_raw_sheet():
    response = requests.get(SHEET_CSV_URL, timeout=20)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()
    text_head = response.text[:300].lower()
    if "text/html" in content_type or "<html" in text_head or "accounts.google" in text_head:
        raise ValueError("Google Sheet không trả về CSV. Kiểm tra quyền public/share của file.")

    raw_df = pd.read_csv(io.StringIO(response.text), header=None, dtype=str, keep_default_na=False)
    fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return raw_df, fetched_at


def parse_value(value):
    if value is None:
        return None
    if pd.isna(value):
        return None

    text = str(value).strip()
    if text in {"", "-", "nan", "None"}:
        return None

    is_percent = "%" in text
    text = text.replace(",", "").replace("%", "").strip()
    if text == "":
        return None

    try:
        number = float(text)
    except ValueError:
        return None

    if is_percent:
        return number / 100
    return number


def safe_cell(df, row_idx, col_idx):
    if row_idx >= len(df.index) or col_idx >= len(df.columns):
        return ""
    return df.iat[row_idx, col_idx]


def row_label(df, row_idx):
    return str(safe_cell(df, row_idx, 1)).strip()


def validate_sheet_structure(df):
    checks = {
        5: "Request",
        13: "Demand",
        50: "Active actual",
        58: "Capacity",
        74: "Productivity",
        90: "Prod/Onlinehour",
    }
    mismatches = []
    for row_idx, expected in checks.items():
        actual = row_label(df, row_idx)
        if actual.lower() != expected.lower():
            mismatches.append(f"Row {row_idx + 1}: expected '{expected}', got '{actual}'")
    return mismatches


def parse_sheet_date(label):
    label = str(label).strip()
    if not label or label.lower() == "nan":
        return None
    try:
        parsed = datetime.strptime(f"{label}-{REPORT_YEAR}", "%d-%b-%Y")
        return pd.Timestamp(parsed.date())
    except ValueError:
        return None


def daily_columns(df):
    columns = []
    for col_idx in range(DAILY_START_COL, len(df.columns)):
        date_value = parse_sheet_date(safe_cell(df, 4, col_idx))
        if date_value is not None:
            columns.append((col_idx, date_value))
    return columns


def daily_series(df, row_idx):
    values = []
    for col_idx, date_value in daily_columns(df):
        metric_value = parse_value(safe_cell(df, row_idx, col_idx))
        values.append({"date": date_value, "value": metric_value})

    series_df = pd.DataFrame(values)
    if series_df.empty:
        return pd.Series(dtype="float64")

    series_df = series_df.dropna(subset=["value"]).sort_values("date")
    return pd.Series(series_df["value"].values, index=series_df["date"], dtype="float64")


def metric_snapshot(df, row_idx):
    return {
        "label": row_label(df, row_idx),
        "lm": parse_value(safe_cell(df, row_idx, COL_LM)),
        "mtd": parse_value(safe_cell(df, row_idx, COL_MTD)),
        "mom": parse_value(safe_cell(df, row_idx, COL_MOM)),
    }


def latest_available(series, skip_zero=True):
    if series.empty:
        return None, None
    usable = series.dropna()
    if skip_zero:
        usable = usable[usable != 0]
    if usable.empty:
        return None, None
    return usable.index.max(), float(usable.loc[usable.index.max()])


def format_number(value, decimals=0, suffix=""):
    if value is None or pd.isna(value):
        return "—"
    if decimals == 0:
        return f"{value:,.0f}{suffix}"
    return f"{value:,.{decimals}f}{suffix}"


def format_percent(value, decimals=1):
    if value is None or pd.isna(value):
        return "—"
    if abs(value) > 1.5:
        value = value / 100
    return f"{value:.{decimals}%}"


def delta_html(current, baseline, percent=False, label_suffix="vs LM"):
    """Returns a Slate pill badge for use inside .metric-badges."""
    if current is None or baseline is None or baseline == 0:
        return f"<span class='delta-badge neu'><span class='badge-label'>{label_suffix}</span>—</span>"
    delta = current - baseline
    delta_pct = delta / abs(baseline)
    pos = delta >= 0
    cls = "pos" if pos else "neg"
    arrow = "▲" if pos else "▼"
    val_str = f"{arrow}{abs(delta):.1%}" if percent else f"{arrow}{abs(delta_pct):.1%}"
    return f"<span class='delta-badge {cls}'><span class='badge-label'>{label_suffix}</span>{val_str}</span>"


def metric_card(label, value, delta, context="", accent_class=""):
    """Render a clean Slate KPI card. Data values are passed in unchanged."""
    icon = "◎"
    if "FR" in label or "Fulfillment" in label:
        icon = "⌁"
    elif "Active" in label or "Driver" in label:
        icon = "♙"
    elif "Productivity" in label or "EPH" in label or "Prod" in label:
        icon = "↯"
    elif "Supply" in label:
        icon = "◷"
    elif "Demand" in label or "Complete" in label:
        icon = "⌁"
    return f"""
    <div class="metric-card {accent_class}">
        <div class="metric-card-header">
            <span class="metric-icon">{icon}</span>
            <span class="metric-label">{label}</span>
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-badges">{delta}</div>
        <div class="metric-context">{context}</div>
    </div>
    """


def _delta_badge(pct_val, base_val, label="", is_pct_metric=False, positive_is_good=True):
    """Render a Slate semantic delta pill."""
    if pct_val is None or base_val is None or base_val == 0:
        return f"<span class='delta-badge neu'><span class='badge-label'>{label}</span>—</span>"
    d = (pct_val - base_val) if is_pct_metric else (pct_val - base_val) / base_val
    good = d >= 0 if positive_is_good else d <= 0
    cls = "pos" if good else "neg"
    arrow = "▲" if d >= 0 else "▼"
    abs_d = f"{abs(d):.1%}"
    if is_pct_metric:
        abs_d = f"{abs(d):.1%}"
    return f"<span class='delta-badge {cls}'><span class='badge-label'>{label}</span>{arrow}{abs_d}</span>"


# ── TIME GRANULARITY AGGREGATION ENGINE ───────────────────────────────────────
def aggregate_weekly(series, is_rate=False, agg_type="sum"):
    if series.empty:
        return series
    if is_rate or agg_type == "mean":
        return series.resample("W-MON").mean()
    return series.resample("W-MON").sum()


def process_series(series, start_date, end_date, time_granularity, is_rate=False, agg_type="sum"):
    if series.empty:
        return series

    today_ts = pd.Timestamp(datetime.now().date())
    if today_ts in series.index:
        series = series.drop(index=today_ts, errors="ignore")

    if time_granularity == "Weekly":
        series = aggregate_weekly(series, is_rate=is_rate, agg_type=agg_type)

    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)
    return series[(series.index >= start_ts) & (series.index <= end_ts)]


def chart_layout(fig, title="", secondary_y=False):
    if go is None:
        return fig
    fig.update_layout(
        title={"text": title, "font": {"size": 14, "color": "#F8FAFC"}},
        font={"family": "Inter, sans-serif", "color": "#F8FAFC"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 30, "r": 30, "t": 60, "b": 30},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1, "font": {"color": "#F8FAFC"}},
        hovermode="x unified",
        hoverlabel={"bgcolor": "#1E293B", "bordercolor": "#334155", "font": {"family": "Inter, sans-serif", "color": "#F8FAFC", "size": 12}},
        template="plotly_dark",
    )
    fig.update_xaxes(showgrid=False, linecolor="rgba(51,65,85,0.75)", gridcolor="rgba(51,65,85,0.35)", tickfont={"color": "#94A3B8"})
    fig.update_yaxes(gridcolor="rgba(51,65,85,0.35)", zerolinecolor="rgba(51,65,85,0.55)", linecolor="rgba(51,65,85,0.75)", tickfont={"color": "#94A3B8"})
    return fig


def add_text_labels(series, max_val=None):
    if max_val is None:
        max_val = series.max() if not series.empty else 0
    text_values = []
    for val in series.values:
        if val is None or pd.isna(val):
            text_values.append("")
        elif max_val > 1000:
            text_values.append(f"{val/1000:.1f}k")
        elif max_val < 5:
            text_values.append(f"{val:.2f}")
        elif max_val < 50:
            text_values.append(f"{val:.1f}")
        else:
            text_values.append(f"{val:,.0f}")
    return text_values


def render_line_chart(data, title, colors, is_rate=False):
    if go is None:
        st.line_chart(pd.DataFrame(data))
        return

    fig = go.Figure()
    all_vals = [v for s in data.values() if not s.empty for v in s.values if v is not None and not pd.isna(v)]
    max_val = max(all_vals) if all_vals else 0

    for label, series in data.items():
        text_values = add_text_labels(series, max_val if not is_rate else None)
        is_forecast = label.upper().startswith("FC") or "FORECAST" in label.upper()
        base_color = colors.get(label, "#3b82f6")
        line_color = "#94a3b8" if is_forecast else base_color
        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series.values,
                mode="lines+markers" if is_forecast else "lines+markers+text",
                name=label,
                text=None if is_forecast else text_values,
                textposition="top center",
                textfont={"size": 9, "color": "#f8fafc"},
                line={"width": 2 if is_forecast else 3, "color": line_color, "dash": "dash" if is_forecast else "solid", "shape": "spline", "smoothing": 1.3},
                marker={"size": 4 if is_forecast else 5, "symbol": "circle", "opacity": 0.65 if is_forecast else 0.95},
                fill=None if is_forecast else "tozeroy",
                fillcolor=None if is_forecast else "rgba(59,130,246,0.14)",
                hovertemplate=f"%{{x|%d-%b}}: %{{y{':.1%' if is_rate else ':,.0f'}}}<extra>{label}</extra>",
            )
        )
    st.plotly_chart(chart_layout(fig, title), use_container_width=True)


def render_bar_chart(data, title, colors, stacked=False, is_rate=False):
    if go is None:
        st.bar_chart(pd.DataFrame(data))
        return

    fig = go.Figure()
    all_vals = [v for s in data.values() if not s.empty for v in s.values if v is not None and not pd.isna(v)]
    max_val = max(all_vals) if all_vals else 0

    for label, series in data.items():
        text_values = add_text_labels(series, max_val if not is_rate else None)
        fig.add_trace(
            go.Bar(
                x=series.index,
                y=series.values,
                name=label,
                text=text_values,
                textposition="inside" if stacked else "outside",
                textfont={"size": 9, "color": "#F8FAFC"},
                marker_color=colors.get(label, "#3b82f6"),
                hovertemplate=f"%{{x|%d-%b}}: %{{y{':.1%' if is_rate else ':,.0f'}}}<extra>{label}</extra>",
            )
        )
    fig.update_layout(barmode="stack" if stacked else "group")
    st.plotly_chart(chart_layout(fig, title), use_container_width=True)


def render_dual_axis_chart(data_left, data_right, title, colors_left, colors_right, left_label="", right_label="%"):
    """Dual-axis chart: left=absolute values, right=percentage."""
    if go is None:
        return

    from plotly.subplots import make_subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    all_left = [v for s in data_left.values() if not s.empty for v in s.values if v is not None and not pd.isna(v)]
    max_left = max(all_left) if all_left else 0

    for label, series in data_left.items():
        text_values = add_text_labels(series, max_left)
        is_forecast = label.upper().startswith("FC") or "FORECAST" in label.upper()
        line_color = colors_left.get(label, "#3b82f6")
        if "Demand" in label and not is_forecast:
            line_color = "#10b981"
        fill_color = "rgba(59,130,246,0.14)" if "Request" in label else "rgba(16,185,129,0.12)"
        fig.add_trace(
            go.Scatter(
                x=series.index, y=series.values,
                mode="lines+markers+text" if not is_forecast else "lines+markers", name=label,
                text=text_values if not is_forecast else None, textposition="top center",
                textfont={"size": 8, "color": "#f8fafc"},
                line={"width": 3 if not is_forecast else 2, "color": line_color if not is_forecast else "#94a3b8", "dash": "solid" if not is_forecast else "dash", "shape": "spline", "smoothing": 1.3},
                marker={"size": 5 if not is_forecast else 4, "opacity": 0.9 if not is_forecast else 0.6},
                fill="tozeroy" if not is_forecast else None,
                fillcolor=fill_color if not is_forecast else None,
                hovertemplate=f"%{{x|%d-%b}}: %{{y:,.0f}}<extra>{label}</extra>",
            ),
            secondary_y=False,
        )

    for label, series in data_right.items():
        fig.add_trace(
            go.Scatter(
                x=series.index, y=series.values,
                mode="lines+markers", name=label,
                line={"width": 2.5, "color": colors_right.get(label, "#10B981"), "dash": "dot", "shape": "spline"},
                marker={"size": 5, "symbol": "diamond"},
                hovertemplate=f"%{{x|%d-%b}}: %{{y:.1%}}<extra>{label}</extra>",
                yaxis="y2",
            ),
            secondary_y=True,
        )

    fig.update_layout(
        title={"text": title, "font": {"size": 14, "color": "#F8FAFC"}},
        font={"family": "Inter, sans-serif", "color": "#F8FAFC"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 30, "r": 60, "t": 60, "b": 30},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1, "font": {"color": "#F8FAFC"}},
        hovermode="x unified",
        hoverlabel={"bgcolor": "#1E293B", "bordercolor": "#334155", "font": {"family": "Inter, sans-serif", "color": "#F8FAFC", "size": 12}},
        template="plotly_dark",
    )
    fig.update_xaxes(showgrid=False, linecolor="rgba(51,65,85,0.75)", gridcolor="rgba(51,65,85,0.35)", tickfont={"color": "#94A3B8"})
    fig.update_yaxes(title_text=left_label, gridcolor="rgba(51,65,85,0.35)", zerolinecolor="rgba(51,65,85,0.55)", linecolor="rgba(51,65,85,0.75)", tickfont={"color": "#94A3B8"}, secondary_y=False)
    fig.update_yaxes(title_text=right_label, showgrid=False, zerolinecolor="rgba(51,65,85,0.55)", linecolor="rgba(51,65,85,0.75)", tickfont={"color": "#10B981"}, tickformat=".0%", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)


# ── DRIVER EXP METRICS FALLBACKS ──────────────────────────────────────────────
def get_active_other(date_val, period_type="day"):
    if period_type == "day":
        if date_val == pd.Timestamp("2026-06-16"):
            return 101.0
        elif date_val == pd.Timestamp("2026-06-09"):
            return 97.0
        else:
            return 0.0
    elif period_type == "mtd":
        return 515.0
    elif period_type == "lm":
        return 645.0
    return 0.0


# ── DATA FETCHING ─────────────────────────────────────────────────────────────
try:
    raw_df, fetched_at = load_raw_sheet()
except Exception as exc:
    st.error("❌ Không thể tải dữ liệu từ Google Sheet.")
    st.info("Vui lòng kiểm tra quyền chia sẻ public của sheet hoặc kết nối mạng.")
    st.caption(f"Chi tiết lỗi: {exc}")
    st.stop()

structure_warnings = validate_sheet_structure(raw_df)
available_dates = [date for _, date in daily_columns(raw_df)]
if not available_dates:
    st.error("❌ Không tìm thấy daily date columns trong sheet SGN Overview.")
    st.stop()

min_date = min(available_dates)
max_date = max(available_dates)


# ── SIDEBAR CONTROLS ──────────────────────────────────────────────────────────
st.sidebar.markdown(
    "<div style='text-align: center; margin-top:1rem;'><img src='https://www.ahamove.com/_next/static/media/logo.5c234a9f.svg' width='150'></div>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Bộ lọc Dashboard")
st.sidebar.markdown("<span class='status-pill'>Live Google Sheet</span>", unsafe_allow_html=True)
st.sidebar.caption(f"Last fetched: {fetched_at}")

if st.sidebar.button("🔄 Refresh data"):
    st.cache_data.clear()
    st.rerun()

# Time Granularity Radio Button
time_granularity = st.sidebar.radio(
    "Granularity view",
    ["Daily", "Weekly"],
    horizontal=True,
)

# Date range selection: default to last 30 days
default_start = max(min_date.date(), max_date.date() - timedelta(days=30))
selected_range = st.sidebar.date_input(
    "Date range filter",
    value=(default_start, max_date.date()),
    min_value=min_date.date(),
    max_value=max_date.date(),
)
if isinstance(selected_range, tuple) and len(selected_range) == 2:
    start_date, end_date = selected_range
else:
    start_date, end_date = min_date.date(), max_date.date()

selected_channels = st.sidebar.multiselect(
    "Channel request",
    list(CHANNEL_ROWS.keys()),
    default=["KA", "MP", "SME"],
)
selected_segments = st.sidebar.multiselect(
    "Driver segment",
    list(SEGMENT_ROWS.keys()),
    default=list(SEGMENT_ROWS.keys()),
)

# FR target threshold
fr_target = st.sidebar.slider("Target FR% (ngưỡng đạt)", min_value=0.60, max_value=0.90, value=0.81, step=0.01, format="%.0f%%")

st.sidebar.markdown("---")
st.sidebar.caption("City view: **SGN**")
st.sidebar.caption("Cache TTL: **15 phút**")
st.sidebar.link_button("Mở Google Sheet", SHEET_URL)


# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("<div class='main-title'>SGN Ops Overview Dashboard</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Daily operating cockpit — Request/Demand, Driver Supply, Productivity & Forecast Achievement</div>",
    unsafe_allow_html=True,
)

if structure_warnings:
    with st.expander("⚠️ Sheet structure warning — kiểm tra row mapping", expanded=False):
        for warning in structure_warnings:
            st.warning(warning)


# ── DYNAMIC COCKPIT DATA CALCULATIONS ─────────────────────────────────────────
columns_with_dates = daily_columns(raw_df)
col_today, date_today = columns_with_dates[0]
col_yesterday, date_yesterday = columns_with_dates[1]
col_last_week = col_yesterday + 7  # 7 days back
date_last_week = parse_sheet_date(safe_cell(raw_df, 4, col_last_week))
col_dod_global = columns_with_dates[2][0] if len(columns_with_dates) > 2 else None  # day before yesterday (D-2)
date_dod = columns_with_dates[2][1] if len(columns_with_dates) > 2 else None

# Calculate MTD Column Indexes (1-Jun to yesterday)
mtd_cols = []
target_month = date_yesterday.month
target_year = date_yesterday.year
for col_idx, d_val in columns_with_dates:
    if d_val.month == target_month and d_val.year == target_year and d_val <= date_yesterday:
        mtd_cols.append(col_idx)

# Find the column for the SAME DAY in the previous month (e.g. May 16 when today is Jun 16)
lm_same_day_col = None
for col_idx, d_val in columns_with_dates:
    if d_val.month == (date_yesterday.month - 1 if date_yesterday.month > 1 else 12) and \
       d_val.year == (date_yesterday.year if date_yesterday.month > 1 else date_yesterday.year - 1) and \
       d_val.day == date_yesterday.day:
        lm_same_day_col = col_idx
        break
# If exact day not found, use closest available day (e.g. end of Feb)
if lm_same_day_col is None:
    best_diff = 999
    lm_month = date_yesterday.month - 1 if date_yesterday.month > 1 else 12
    lm_year = date_yesterday.year if date_yesterday.month > 1 else date_yesterday.year - 1
    for col_idx, d_val in columns_with_dates:
        if d_val.month == lm_month and d_val.year == lm_year:
            diff = abs(d_val.day - date_yesterday.day)
            if diff < best_diff:
                best_diff = diff
                lm_same_day_col = col_idx

# Calculate LM MTD Column Indexes (same period last month)
lm_mtd_cols = []
for col_idx, d_val in columns_with_dates:
    if d_val.month == 5 and d_val.year == 2026 and d_val.day <= date_yesterday.day:
        lm_mtd_cols.append(col_idx)

# WTD (Week to Date): Monday of current week → yesterday
_weekday_idx = date_yesterday.weekday()  # Monday=0
_monday_this_week = date_yesterday - pd.Timedelta(days=_weekday_idx)
_monday_last_week = _monday_this_week - pd.Timedelta(days=7)
_last_week_same_dow = _monday_last_week + pd.Timedelta(days=_weekday_idx)

wtd_cols = [col_idx for col_idx, d_val in columns_with_dates
            if _monday_this_week <= d_val <= date_yesterday]
lwtd_cols = [col_idx for col_idx, d_val in columns_with_dates
             if _monday_last_week <= d_val <= _last_week_same_dow]

wtd_start_label = _monday_this_week.strftime('%d-%b')
lwtd_start_label = _monday_last_week.strftime('%d-%b')


def val(row, col):
    return parse_value(safe_cell(raw_df, row, col))


def val_or_zero(row, col):
    v = val(row, col)
    return v if v is not None else 0.0


def get_row_mtd_sum(row_idx):
    total = 0.0
    for col_idx in mtd_cols:
        v = val(row_idx, col_idx)
        if v is not None:
            total += v
    return total


def get_row_lm_mtd_sum(row_idx):
    total = 0.0
    for col_idx in lm_mtd_cols:
        v = val_or_zero(row_idx, col_idx)
        total += v
    return total


def get_row_lm_mtd_mean(row_idx):
    vals = []
    for col_idx in lm_mtd_cols:
        v = val(row_idx, col_idx)
        if v is not None:
            vals.append(v)
    return sum(vals) / len(vals) if vals else 0.0


def get_row_wtd_sum(row_idx):
    total = 0.0
    for col_idx in wtd_cols:
        v = val(row_idx, col_idx)
        if v is not None:
            total += v
    return total


def get_row_wtd_mean(row_idx):
    vals = []
    for col_idx in wtd_cols:
        v = val(row_idx, col_idx)
        if v is not None:
            vals.append(v)
    return sum(vals) / len(vals) if vals else None


def get_row_lwtd_sum(row_idx):
    total = 0.0
    for col_idx in lwtd_cols:
        v = val(row_idx, col_idx)
        if v is not None:
            total += v
    return total


def get_row_lwtd_mean(row_idx):
    vals = []
    for col_idx in lwtd_cols:
        v = val(row_idx, col_idx)
        if v is not None:
            vals.append(v)
    return sum(vals) / len(vals) if vals else None


def get_driver_plan_mtd(plan_16jun_val, mtd_cols, agg_type="sum"):
    vals = []
    for c_idx in mtd_cols:
        fc_req = val(6, c_idx)
        if fc_req is not None:
            vals.append(plan_16jun_val * (fc_req / 69263.0))
    if not vals:
        return 0.0
    if agg_type == "mean":
        return sum(vals) / len(vals)
    return sum(vals)


# Build Cockpit Grid Dictionary
cockpit = {}

act_plan_16jun = {"FT": 2298, "PT": 3588, "NLM": 486, "Return": 263, "NIM": 533, "NID": 54}
cap_plan_16jun = {"FT": 25054, "PT": 22311, "NLM": 3655, "Return": 1659, "NIM": 3546, "NID": 208}
sh_plan_16jun = {"FT": 17079, "PT": 15972, "NLM": 2572, "Return": 1198, "NIM": 2543, "NID": 208}


def active_plan(val_16jun, fc_req):
    return val_16jun * (fc_req / 69263.0) if fc_req else None


def supply_hour_plan(val_16jun, fc_req):
    return val_16jun * (fc_req / 69263.0) if fc_req else None


# 1. Request (Actual rows 21 for aggregate, FC row 6 for plan SME+MP+KA)
cockpit["Request"] = {
    "label": "Request", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(22, col_yesterday),
    "last_week": val(22, col_last_week),
    "planning": val(6, col_yesterday),
    "today": val(6, col_today),
    "wtd": get_row_wtd_sum(22),
    "lwtd": get_row_lwtd_sum(22),
    "plan_wtd": get_row_wtd_sum(6),
    "mtd": val(22, 3),
    "lm": val(22, 2),
    "lm_mtd": get_row_lm_mtd_sum(22),
    "plan_mtd": get_row_mtd_sum(6)
}

# 2. Complete (Actual Demand rows 29 for aggregate)
cockpit["Complete"] = {
    "label": "Complete", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(29, col_yesterday),
    "last_week": val(29, col_last_week),
    "planning": val(14, col_yesterday),
    "today": val(14, col_today),
    "wtd": get_row_wtd_sum(29),
    "lwtd": get_row_lwtd_sum(29),
    "plan_wtd": get_row_wtd_sum(14),
    "mtd": val(29, 3),
    "lm": val(29, 2),
    "lm_mtd": get_row_lm_mtd_sum(29),
    "plan_mtd": get_row_mtd_sum(14)
}

# 3. FR (derived from actual demand / actual request)
req_y = cockpit["Request"]["yesterday"]
comp_y = cockpit["Complete"]["yesterday"]
req_lw = cockpit["Request"]["last_week"]
comp_lw = cockpit["Complete"]["last_week"]
req_mtd = cockpit["Request"]["mtd"]
comp_mtd = cockpit["Complete"]["mtd"]
req_lm = cockpit["Request"]["lm"]
comp_lm = cockpit["Complete"]["lm"]
req_lm_mtd = cockpit["Request"]["lm_mtd"]
comp_lm_mtd = cockpit["Complete"]["lm_mtd"]
req_plan_mtd = cockpit["Request"]["plan_mtd"]
comp_plan_mtd = cockpit["Complete"]["plan_mtd"]
req_wtd = cockpit["Request"]["wtd"]
comp_wtd = cockpit["Complete"]["wtd"]
req_lwtd = cockpit["Request"]["lwtd"]
comp_lwtd = cockpit["Complete"]["lwtd"]
req_plan_wtd = cockpit["Request"]["plan_wtd"]
comp_plan_wtd = cockpit["Complete"]["plan_wtd"]

cockpit["FR"] = {
    "label": "FR", "is_header": True, "format": "percent", "is_percent": True,
    "yesterday": comp_y / req_y if req_y else None,
    "last_week": comp_lw / req_lw if req_lw else None,
    "planning": val(14, col_yesterday) / val(6, col_yesterday) if val(6, col_yesterday) else None,
    "today": val(14, col_today) / val(6, col_today) if val(6, col_today) else None,
    "wtd": comp_wtd / req_wtd if req_wtd else None,
    "lwtd": comp_lwtd / req_lwtd if req_lwtd else None,
    "plan_wtd": comp_plan_wtd / req_plan_wtd if req_plan_wtd else None,
    "mtd": comp_mtd / req_mtd if req_mtd else None,
    "lm": comp_lm / req_lm if req_lm else None,
    "lm_mtd": comp_lm_mtd / req_lm_mtd if req_lm_mtd else None,
    "plan_mtd": comp_plan_mtd / req_plan_mtd if req_plan_mtd else None
}

# 4. Active
cockpit["Active"] = {
    "label": "Active", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(50, col_yesterday),
    "last_week": val(50, col_last_week),
    "planning": sum(act_plan_16jun.values()),
    "today": active_plan(sum(act_plan_16jun.values()), val(6, col_today)),
    "wtd": get_row_wtd_mean(50),
    "lwtd": get_row_lwtd_mean(50),
    "plan_wtd": get_driver_plan_mtd(sum(act_plan_16jun.values()), wtd_cols, "mean"),
    "mtd": val(50, 3),
    "lm": val(50, 2),
    "lm_mtd": get_row_lm_mtd_mean(50),
    "plan_mtd": get_driver_plan_mtd(sum(act_plan_16jun.values()), mtd_cols, "mean")
}

active_segs = ["FT", "PT", "NLM", "Return", "NIM", "NID"]
active_seg_rows = {"FT": 51, "PT": 52, "NLM": 53, "Return": 54, "NIM": 55, "NID": 56}
for seg in active_segs:
    r = active_seg_rows[seg]
    cockpit[f"Active_{seg}"] = {
        "label": seg, "is_header": False, "format": "number", "is_percent": False,
        "yesterday": val(r, col_yesterday),
        "last_week": val(r, col_last_week),
        "planning": act_plan_16jun[seg],
        "today": active_plan(act_plan_16jun[seg], val(6, col_today)),
        "wtd": get_row_wtd_mean(r),
        "lwtd": get_row_lwtd_mean(r),
        "plan_wtd": get_driver_plan_mtd(act_plan_16jun[seg], wtd_cols, "mean"),
        "mtd": val(r, 3),
        "lm": val(r, 2),
        "lm_mtd": get_row_lm_mtd_mean(r),
        "plan_mtd": get_driver_plan_mtd(act_plan_16jun[seg], mtd_cols, "mean")
    }
cockpit["Active_Other"] = {
    "label": "Other (EXP)", "is_header": False, "format": "number", "is_percent": False,
    "yesterday": val_or_zero(50, col_yesterday) - sum(val_or_zero(active_seg_rows[s], col_yesterday) for s in active_segs),
    "last_week": val_or_zero(50, col_last_week) - sum(val_or_zero(active_seg_rows[s], col_last_week) for s in active_segs),
    "planning": 0.0, "today": 0.0,
    "wtd": None, "lwtd": None, "plan_wtd": None,
    "mtd": val_or_zero(50, 3) - sum(val_or_zero(active_seg_rows[s], 3) for s in active_segs),
    "lm": val_or_zero(50, 2) - sum(val_or_zero(active_seg_rows[s], 2) for s in active_segs),
    "lm_mtd": max(0.0, get_row_lm_mtd_mean(50) - sum(get_row_lm_mtd_mean(active_seg_rows[s]) for s in active_segs)),
    "plan_mtd": 0.0
}

# 5. Cap
cap_segs = ["FT", "PT", "NLM", "Return", "NIM", "NID"]
cap_seg_rows = {"FT": 59, "PT": 60, "NLM": 61, "Return": 62, "NIM": 63, "NID": 64}


def get_cap_seg_mtd_sum(s):
    return get_row_mtd_sum(cap_seg_rows[s])


cockpit["Cap"] = {
    "label": "Cap", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(58, col_yesterday),
    "last_week": val(58, col_last_week),
    "planning": sum(cap_plan_16jun.values()),
    "today": active_plan(sum(cap_plan_16jun.values()), val(6, col_today)),
    "wtd": get_row_wtd_sum(58),
    "lwtd": get_row_lwtd_sum(58),
    "plan_wtd": get_driver_plan_mtd(sum(cap_plan_16jun.values()), wtd_cols, "sum"),
    "mtd": val(58, 3),
    "lm": val(58, 2),
    "lm_mtd": get_row_lm_mtd_sum(58),
    "plan_mtd": get_driver_plan_mtd(sum(cap_plan_16jun.values()), mtd_cols, "sum")
}

for seg in cap_segs:
    r = cap_seg_rows[seg]
    cockpit[f"Cap_{seg}"] = {
        "label": seg, "is_header": False, "format": "number", "is_percent": False,
        "yesterday": val(r, col_yesterday),
        "last_week": val(r, col_last_week),
        "planning": cap_plan_16jun[seg],
        "today": active_plan(cap_plan_16jun[seg], val(6, col_today)),
        "wtd": get_row_wtd_sum(r),
        "lwtd": get_row_lwtd_sum(r),
        "plan_wtd": get_driver_plan_mtd(cap_plan_16jun[seg], wtd_cols, "sum"),
        "mtd": get_cap_seg_mtd_sum(seg),
        "lm": val(r, 2),
        "lm_mtd": get_row_lm_mtd_sum(r),
        "plan_mtd": get_driver_plan_mtd(cap_plan_16jun[seg], mtd_cols, "sum")
    }
cockpit["Cap_Other"] = {
    "label": "Other (EXP)", "is_header": False, "format": "number", "is_percent": False,
    "yesterday": val_or_zero(58, col_yesterday) - sum(val_or_zero(cap_seg_rows[s], col_yesterday) for s in cap_segs),
    "last_week": val_or_zero(58, col_last_week) - sum(val_or_zero(cap_seg_rows[s], col_last_week) for s in cap_segs),
    "planning": 0.0, "today": 0.0,
    "wtd": None, "lwtd": None, "plan_wtd": None,
    "mtd": val_or_zero(58, 3) - sum(get_cap_seg_mtd_sum(s) for s in cap_segs),
    "lm": val_or_zero(58, 2) - sum(val_or_zero(cap_seg_rows[s], 2) for s in cap_segs),
    "lm_mtd": max(0.0, get_row_lm_mtd_sum(58) - sum(get_row_lm_mtd_sum(cap_seg_rows[s]) for s in cap_segs)),
    "plan_mtd": 0.0
}

# 6. Supply hour
sh_segs = ["FT", "PT", "NLM", "Return", "NIM", "NID"]
sh_seg_rows = {"FT": 67, "PT": 68, "NLM": 69, "Return": 70, "NIM": 71, "NID": 72}


def get_sh_seg_mtd_sum(s):
    return get_row_mtd_sum(sh_seg_rows[s])


cockpit["Supply hour"] = {
    "label": "Supply hour", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(66, col_yesterday),
    "last_week": val(66, col_last_week),
    "planning": sum(sh_plan_16jun.values()),
    "today": supply_hour_plan(sum(sh_plan_16jun.values()), val(6, col_today)),
    "wtd": get_row_wtd_sum(66),
    "lwtd": get_row_lwtd_sum(66),
    "plan_wtd": get_driver_plan_mtd(sum(sh_plan_16jun.values()), wtd_cols, "sum"),
    "mtd": val(66, 3),
    "lm": val(66, 2),
    "lm_mtd": get_row_lm_mtd_sum(66),
    "plan_mtd": get_driver_plan_mtd(sum(sh_plan_16jun.values()), mtd_cols, "sum")
}

for seg in sh_segs:
    r = sh_seg_rows[seg]
    cockpit[f"Supply_hour_{seg}"] = {
        "label": seg, "is_header": False, "format": "number", "is_percent": False,
        "yesterday": val(r, col_yesterday),
        "last_week": val(r, col_last_week),
        "planning": sh_plan_16jun[seg],
        "today": supply_hour_plan(sh_plan_16jun[seg], val(6, col_today)),
        "wtd": get_row_wtd_sum(r),
        "lwtd": get_row_lwtd_sum(r),
        "plan_wtd": get_driver_plan_mtd(sh_plan_16jun[seg], wtd_cols, "sum"),
        "mtd": get_sh_seg_mtd_sum(seg),
        "lm": val(r, 2),
        "lm_mtd": get_row_lm_mtd_sum(r),
        "plan_mtd": get_driver_plan_mtd(sh_plan_16jun[seg], mtd_cols, "sum")
    }
cockpit["Supply_hour_Other"] = {
    "label": "Other (EXP)", "is_header": False, "format": "number", "is_percent": False,
    "yesterday": val_or_zero(66, col_yesterday) - sum(val_or_zero(sh_seg_rows[s], col_yesterday) for s in sh_segs),
    "last_week": val_or_zero(66, col_last_week) - sum(val_or_zero(sh_seg_rows[s], col_last_week) for s in sh_segs),
    "planning": 0.0, "today": 0.0,
    "wtd": None, "lwtd": None, "plan_wtd": None,
    "mtd": val_or_zero(66, 3) - sum(get_sh_seg_mtd_sum(s) for s in sh_segs),
    "lm": val_or_zero(66, 2) - sum(val_or_zero(sh_seg_rows[s], 2) for s in sh_segs),
    "lm_mtd": max(0.0, get_row_lm_mtd_sum(66) - sum(get_row_lm_mtd_sum(sh_seg_rows[s]) for s in sh_segs)),
    "plan_mtd": 0.0
}


def make_derived_row(label, num_key, den_key, format_type):
    derived = {}
    for col_name in ["yesterday", "last_week", "planning", "today", "wtd", "lwtd", "plan_wtd", "mtd", "lm", "lm_mtd", "plan_mtd"]:
        num = cockpit[num_key][col_name]
        den = cockpit[den_key][col_name]
        derived[col_name] = num / den if num is not None and den is not None and den > 0 else None
    return {"label": label, "is_header": True, "format": format_type, "is_percent": False, **derived}


# 7. online/driver
cockpit["online/driver"] = make_derived_row("online/driver", "Supply hour", "Active", "decimal")
for seg in sh_segs:
    cockpit[f"online/driver_{seg}"] = make_derived_row(seg, f"Supply_hour_{seg}", f"Active_{seg}", "decimal")
cockpit["online/driver_Other"] = {
    "label": "Other (EXP)", "is_header": False, "format": "decimal", "is_percent": False,
    "yesterday": cockpit["Supply_hour_Other"]["yesterday"] / cockpit["Active_Other"]["yesterday"] if cockpit["Active_Other"]["yesterday"] else 0.0,
    "last_week": cockpit["Supply_hour_Other"]["last_week"] / cockpit["Active_Other"]["last_week"] if cockpit["Active_Other"]["last_week"] else 0.0,
    "planning": 0.0, "today": 0.0,
    "wtd": None, "lwtd": None, "plan_wtd": None,
    "mtd": cockpit["Supply_hour_Other"]["mtd"] / cockpit["Active_Other"]["mtd"] if cockpit["Active_Other"]["mtd"] else 0.0,
    "lm": cockpit["Supply_hour_Other"]["lm"] / cockpit["Active_Other"]["lm"] if cockpit["Active_Other"]["lm"] else 0.0,
    "lm_mtd": cockpit["Supply_hour_Other"]["lm_mtd"] / cockpit["Active_Other"]["lm_mtd"] if cockpit["Active_Other"]["lm_mtd"] else 0.0,
    "plan_mtd": 0.0
}

# 8. Prod
cockpit["Prod"] = make_derived_row("Prod", "Cap", "Active", "decimal")
for seg in cap_segs:
    cockpit[f"Prod_{seg}"] = make_derived_row(seg, f"Cap_{seg}", f"Active_{seg}", "decimal")


def get_prod_other_col(col_name):
    num = cockpit["Cap_Other"][col_name]
    den = cockpit["Active_Other"][col_name]
    return num / den if num is not None and den is not None and den > 0 else None


cockpit["Prod_Other"] = {
    "label": "Other (EXP)", "is_header": False, "format": "decimal", "is_percent": False,
    "yesterday": get_prod_other_col("yesterday"),
    "last_week": get_prod_other_col("last_week"),
    "planning": 0.0, "today": 0.0,
    "wtd": None, "lwtd": None, "plan_wtd": None,
    "mtd": get_prod_other_col("mtd"),
    "lm": get_prod_other_col("lm"),
    "lm_mtd": get_prod_other_col("lm_mtd"),
    "plan_mtd": get_prod_other_col("plan_mtd")
}

# Delta Calculations
for key, row in cockpit.items():
    y = row["yesterday"]
    lw = row["last_week"]
    is_pct = row["is_percent"]

    # Daily: WoW + vs Plan (DoD computed at render time per row, needs raw sheet row)
    row["wow"] = (y - lw if is_pct else (y - lw) / lw) if (y is not None and lw is not None and lw != 0) else None
    row["wow_abs"] = (y - lw) if (y is not None and lw is not None) else None
    plan = row["planning"]
    row["vs_planning"] = (y - plan if is_pct else (y - plan) / plan) if (y is not None and plan is not None and plan != 0) else None
    row["vs_planning_abs"] = (y - plan) if (y is not None and plan is not None) else None

    # WTD
    wtd = row.get("wtd")
    lwtd = row.get("lwtd")
    plan_wtd = row.get("plan_wtd")
    row["wow_wtd"] = (wtd - lwtd if is_pct else (wtd - lwtd) / lwtd) if (wtd is not None and lwtd is not None and lwtd != 0) else None
    row["vs_plan_wtd"] = (wtd - plan_wtd if is_pct else (wtd - plan_wtd) / plan_wtd) if (wtd is not None and plan_wtd is not None and plan_wtd != 0) else None

    # MTD
    mtd = row["mtd"]
    lm = row["lm"]
    lm_mtd = row.get("lm_mtd")
    plan_mtd = row["plan_mtd"]
    row["mom_whole"] = (mtd - lm if is_pct else (mtd - lm) / lm) if (mtd is not None and lm is not None and lm != 0) else None
    row["mom_mtd"] = (mtd - lm_mtd if is_pct else (mtd - lm_mtd) / lm_mtd) if (mtd is not None and lm_mtd is not None and lm_mtd != 0) else None
    row["vs_planning_mtd"] = (mtd - plan_mtd if is_pct else (mtd - plan_mtd) / plan_mtd) if (mtd is not None and plan_mtd is not None and plan_mtd != 0) else None
    row["mom_mtd_abs"] = (mtd - lm_mtd) if (mtd is not None and lm_mtd is not None) else None
    row["mom_whole_abs"] = (mtd - lm) if (mtd is not None and lm is not None) else None
    row["wow_wtd_abs"] = (wtd - lwtd) if (row.get("wtd") is not None and row.get("lwtd") is not None) else None

# Sheet row lookup for DoD calculation (raw data rows, not derived)
COCKPIT_SHEET_ROW = {
    "Request": 22, "Complete": 29, "Active": 50,
    "Active_FT": 51, "Active_PT": 52, "Active_NLM": 53, "Active_Return": 54, "Active_NIM": 55, "Active_NID": 56,
    "Cap": 58,
    "Cap_FT": 59, "Cap_PT": 60, "Cap_NLM": 61, "Cap_Return": 62, "Cap_NIM": 63, "Cap_NID": 64,
    "Supply hour": 66,
    "Supply_hour_FT": 67, "Supply_hour_PT": 68, "Supply_hour_NLM": 69, "Supply_hour_Return": 70, "Supply_hour_NIM": 71, "Supply_hour_NID": 72,
    "Prod": 74, "online/driver": 82,
    # FR, Other rows are derived — DoD computed from component rows
}

def get_cockpit_dod(key, row):
    """Return (dod_pct, dod_abs) for a cockpit row."""
    if col_dod_global is None:
        return None, None
    r = COCKPIT_SHEET_ROW.get(key)
    is_pct = row["is_percent"]
    y = row["yesterday"]
    if r is not None:
        dod_val = val(r, col_dod_global)
    elif key == "FR":
        # FR derived: comp_dod / req_dod
        req_dod = val(22, col_dod_global)
        comp_dod = val(29, col_dod_global)
        dod_val = comp_dod / req_dod if req_dod else None
    else:
        dod_val = None
    if y is None or dod_val is None:
        return None, None
    pct = (y - dod_val) if is_pct else ((y - dod_val) / dod_val if dod_val != 0 else None)
    abs_d = (y - dod_val)
    return pct, abs_d


# ── LAYER 1: EXECUTIVE SUMMARY - KPI CARDS ───────────────────────────────────
st.markdown("<div class='section-header'>🔴 Executive Summary — KPI Pulse</div>", unsafe_allow_html=True)

# ── Pre-compute all KPI values ─────────────────────────────────────────────
fr_yest           = val(180, col_yesterday)
fr_lm_same_day    = val(180, lm_same_day_col) if lm_same_day_col else None
fr_lm_mtd_avg     = get_row_lm_mtd_mean(180)
fr_lm_full        = val(180, 2)

active_total_4h   = val(177, col_yesterday)
active_total      = val(166, col_yesterday)
active_4h_pct     = (active_total_4h / active_total) if active_total and active_total > 0 and active_total_4h else None

prod_yest         = val(74, col_yesterday)
prod_lm_same_day  = val(74, lm_same_day_col) if lm_same_day_col else None
prod_lm_mtd_avg   = get_row_lm_mtd_mean(74)
prod_lm_full      = val(74, 2)
opd_yest          = val(82, col_yesterday)

col_dod_kpi       = columns_with_dates[2][0] if len(columns_with_dates) > 2 else None
lm_day_str        = date_yesterday.replace(month=date_yesterday.month - 1).strftime('%d-%b') if lm_same_day_col else ""

sh_yest           = val(66, col_yesterday)
sh_dod_val        = val(66, col_dod_kpi) if col_dod_kpi else None
sh_lw             = val(66, col_last_week)
sh_mtd_val        = cockpit["Supply hour"]["mtd"]
sh_wtd_val        = cockpit["Supply hour"]["wtd"]
sh_lm_mtd         = get_row_lm_mtd_sum(66)

lm_period_label   = f"1–{date_yesterday.strftime('%d')} May"
request_lm_full   = val(22, 2)
demand_lm_full    = val(29, 2)
req_lm_mtd_sum    = get_row_lm_mtd_sum(22)
dem_lm_mtd_sum    = get_row_lm_mtd_sum(29)
request_mtd_val   = val(22, 3)
demand_mtd_val    = val(29, 3)
prod_mtd          = val(74, 3)
prod_lm_mtd_v     = get_row_lm_mtd_mean(74)
active_mtd_avg    = get_row_lm_mtd_mean(50)
sh_lm_full        = val(66, 2)

# ── GROUP 1: DAILY — Hôm qua + WoW comparison ─────────────────────────────
st.markdown(
    f"<div class='metric-group-label'>⚡ DAILY — {date_yesterday.strftime('%d %b')} &nbsp;·&nbsp; DoD vs {columns_with_dates[2][1].strftime('%d-%b') if len(columns_with_dates)>2 else '—'} &nbsp;|&nbsp; WoW vs {date_last_week.strftime('%d-%b')}</div>",
    unsafe_allow_html=True,
)
cols = st.columns(6)

# 1. Request
cols[0].markdown(metric_card(
    "Request",
    format_number(val(21, col_yesterday)),
    (delta_html(val(21, col_yesterday), val(21, col_dod_kpi), label_suffix="DoD") if col_dod_kpi else "")
    + "" + delta_html(val(21, col_yesterday), val(21, col_last_week), label_suffix="WoW"),
    delta_html(val(21, col_yesterday), val(6, col_yesterday), label_suffix="vs FC") + f" &nbsp;|&nbsp; FC: {format_number(val(6, col_yesterday))}",
    "metric-card-accent"
), unsafe_allow_html=True)

# 2. Demand
cols[1].markdown(metric_card(
    "Demand",
    format_number(val(28, col_yesterday)),
    (delta_html(val(28, col_yesterday), val(28, col_dod_kpi), label_suffix="DoD") if col_dod_kpi else "")
    + "" + delta_html(val(28, col_yesterday), val(28, col_last_week), label_suffix="WoW"),
    delta_html(val(28, col_yesterday), val(13, col_yesterday), label_suffix="vs FC") + f" &nbsp;|&nbsp; FC: {format_number(val(13, col_yesterday))}",
), unsafe_allow_html=True)

# 3. FR%
fr_color = "#10b981" if fr_yest and fr_yest >= fr_target else ("#fbbf24" if fr_yest and fr_yest >= fr_target * 0.9 else "#fb7185")
fr_wow_delta = delta_html(fr_yest, val(180, col_last_week), percent=True, label_suffix="WoW")
fr_dod_delta = delta_html(fr_yest, val(180, col_dod_kpi), percent=True, label_suffix="DoD") if col_dod_kpi else ""
fr_daily_html = metric_card(
    "FR%",
    format_percent(fr_yest),
    f"{fr_dod_delta}{fr_wow_delta}<span class='delta-badge {'pos' if fr_yest and fr_yest >= fr_target else 'neg'}'><span class='badge-label'>Target</span>{fr_target:.0%}</span>",
    f"LM avg: {format_percent(fr_lm_mtd_avg)}",
    "metric-card-green"
)
cols[2].markdown(fr_daily_html, unsafe_allow_html=True)

# 4. Active Drivers
active_dod = val(50, col_dod_kpi) if col_dod_kpi else None
cols[3].markdown(metric_card(
    "Active Drivers",
    format_number(val(50, col_yesterday)),
    (delta_html(val(50, col_yesterday), active_dod, label_suffix="DoD") if active_dod else "")
    + "" + delta_html(val(50, col_yesterday), val(50, col_last_week), label_suffix="WoW"),
    f"Plan: {format_number(sum(act_plan_16jun.values()))}",
    "metric-card-blue"
), unsafe_allow_html=True)

# 5. Supply Hours
cols[4].markdown(metric_card(
    "Supply Hours",
    format_number(sh_yest),
    (delta_html(sh_yest, sh_dod_val, label_suffix="DoD") if sh_dod_val else "")
    + "" + delta_html(sh_yest, sh_lw, label_suffix="WoW"),
    f"WTD: {format_number(sh_wtd_val)} &nbsp;·&nbsp; MTD: {format_number(sh_mtd_val)}",
    "metric-card-blue"
), unsafe_allow_html=True)

# 6. Productivity (EPH)
cols[5].markdown(metric_card(
    "Productivity (EPH)",
    format_number(prod_yest, 1),
    (delta_html(prod_yest, val(74, col_dod_kpi), label_suffix="DoD") if col_dod_kpi else "")
    + " &nbsp; " + (delta_html(prod_yest, prod_lm_same_day, label_suffix=f"vs {lm_day_str}") if prod_lm_same_day else delta_html(prod_yest, prod_lm_mtd_avg, label_suffix="vs LM avg")),
    f"Online/Dr: {format_number(opd_yest, 1)}h &nbsp;·&nbsp; LM avg: {format_number(prod_lm_mtd_avg, 1)}",
), unsafe_allow_html=True)

# ── GROUP 2: MTD — Lũy kế tháng + vs LM same period & whole month ─────────
st.markdown(
    f"<div class='metric-group-label'>📅 MTD — {date_yesterday.strftime('%b %Y')} &nbsp;·&nbsp; vs LM same period ({lm_period_label}) &amp; LM whole May</div>",
    unsafe_allow_html=True,
)
cols2 = st.columns(6)

# 1. Request MTD
cols2[0].markdown(metric_card(
    "Request MTD",
    format_number(request_mtd_val),
    delta_html(request_mtd_val, req_lm_mtd_sum, label_suffix=f"vs LM period"),
    f"LM period: {format_number(req_lm_mtd_sum)} &nbsp;·&nbsp; LM whole: {format_number(request_lm_full)}",
    "metric-card-accent"
), unsafe_allow_html=True)

# 2. Demand MTD
cols2[1].markdown(metric_card(
    "Demand MTD",
    format_number(demand_mtd_val),
    delta_html(demand_mtd_val, dem_lm_mtd_sum, label_suffix=f"vs LM period"),
    f"LM period: {format_number(dem_lm_mtd_sum)} &nbsp;·&nbsp; LM whole: {format_number(demand_lm_full)}",
), unsafe_allow_html=True)

# 3. FR% MTD avg
fr_mtd_avg = get_row_lm_mtd_mean(180)
fr_color_mtd = "#10b981" if fr_mtd_avg and fr_mtd_avg >= fr_target else ("#fbbf24" if fr_mtd_avg and fr_mtd_avg >= fr_target * 0.9 else "#fb7185")
fr_mtd_html = metric_card(
    "FR% MTD avg",
    format_percent(fr_mtd_avg),
    delta_html(fr_mtd_avg, fr_lm_mtd_avg, percent=True, label_suffix="vs LM"),
    f"LM same period: {format_percent(fr_lm_mtd_avg)} &nbsp;·&nbsp; LM whole: {format_percent(fr_lm_full)}",
    "metric-card-green"
)
cols2[2].markdown(fr_mtd_html, unsafe_allow_html=True)

# 4. Supply Hours MTD
cols2[3].markdown(metric_card(
    "Supply Hours MTD",
    format_number(sh_mtd_val),
    delta_html(sh_mtd_val, sh_lm_mtd, label_suffix="vs LM period"),
    f"LM period: {format_number(sh_lm_mtd)} &nbsp;·&nbsp; LM whole: {format_number(sh_lm_full)}",
    "metric-card-blue"
), unsafe_allow_html=True)

# 5. Productivity MTD avg
cols2[4].markdown(metric_card(
    "Productivity MTD avg",
    format_number(prod_mtd, 1),
    delta_html(prod_mtd, prod_lm_mtd_v, label_suffix="vs LM period"),
    f"LM period: {format_number(prod_lm_mtd_v, 1)} &nbsp;·&nbsp; LM whole: {format_number(prod_lm_full, 1)}",
), unsafe_allow_html=True)

# 6. Nhóm DV 4H
active_4h_str = format_percent(active_4h_pct) if active_4h_pct else "—"
cols2[5].markdown(metric_card(
    "Nhóm DV 4H (Hôm qua)",
    active_4h_str,
    f"<span style='color:#94A3B8'>4H: {format_number(active_total_4h)} / {format_number(active_total)} tài xế</span>",
    "Đo lường độ gắn bó (Txế hoạt động liên tục >=4h/ngày)",
    "metric-card-green"
), unsafe_allow_html=True)

# ── GROUP 3: WTD — Lũy kế tuần ────────────────────────────────────────────────
wtd_label = f"WTD ({wtd_start_label} - {date_yesterday.strftime('%d-%b')})"
lwtd_label = f"LWTD ({lwtd_start_label} - {date_last_week.strftime('%d-%b')})"

st.markdown(
    f"<div class='metric-group-label'>📆 WTD — Tuần này &nbsp;·&nbsp; vs {lwtd_label}</div>",
    unsafe_allow_html=True,
)
cols3 = st.columns(6)

req_wtd = cockpit["Request"]["wtd"]
req_lwtd = cockpit["Request"]["lwtd"]
dem_wtd = cockpit["Complete"]["wtd"]
dem_lwtd = cockpit["Complete"]["lwtd"]
fr_wtd = cockpit["FR"]["wtd"]
fr_lwtd = cockpit["FR"]["lwtd"]
active_wtd = cockpit["Active"]["wtd"]
active_lwtd = cockpit["Active"]["lwtd"]
sh_lwtd = cockpit["Supply hour"]["lwtd"]
prod_wtd = cockpit["Prod"]["wtd"]
prod_lwtd = cockpit["Prod"]["lwtd"]

cols3[0].markdown(metric_card(
    "Request WTD",
    format_number(req_wtd),
    delta_html(req_wtd, req_lwtd, label_suffix=f"vs LWTD"),
    f"LWTD: {format_number(req_lwtd)}",
    "metric-card-accent"
), unsafe_allow_html=True)

cols3[1].markdown(metric_card(
    "Demand WTD",
    format_number(dem_wtd),
    delta_html(dem_wtd, dem_lwtd, label_suffix=f"vs LWTD"),
    f"LWTD: {format_number(dem_lwtd)}",
), unsafe_allow_html=True)

fr_color_wtd = "#10b981" if fr_wtd and fr_wtd >= fr_target else ("#fbbf24" if fr_wtd and fr_wtd >= fr_target * 0.9 else "#fb7185")
fr_wtd_html = metric_card(
    "FR% WTD",
    format_percent(fr_wtd),
    delta_html(fr_wtd, fr_lwtd, percent=True, label_suffix="vs LWTD"),
    f"LWTD: {format_percent(fr_lwtd)}",
    "metric-card-green"
)
cols3[2].markdown(fr_wtd_html, unsafe_allow_html=True)

cols3[3].markdown(metric_card(
    "Active WTD",
    format_number(active_wtd),
    delta_html(active_wtd, active_lwtd, label_suffix="vs LWTD"),
    f"LWTD: {format_number(active_lwtd)}",
    "metric-card-blue"
), unsafe_allow_html=True)

cols3[4].markdown(metric_card(
    "Supply Hours WTD",
    format_number(sh_wtd_val),
    delta_html(sh_wtd_val, sh_lwtd, label_suffix="vs LWTD"),
    f"LWTD: {format_number(sh_lwtd)} &nbsp;·&nbsp; MTD: {format_number(sh_mtd_val)}",
    "metric-card-blue"
), unsafe_allow_html=True)

cols3[5].markdown(metric_card(
    "Productivity WTD",
    format_number(prod_wtd, 1),
    delta_html(prod_wtd, prod_lwtd, label_suffix="vs LWTD"),
    f"LWTD: {format_number(prod_lwtd, 1)} &nbsp;·&nbsp; MTD: {format_number(prod_mtd, 1)}",
), unsafe_allow_html=True)


# ── LAYER 1: DAILY OPERATING COCKPIT TABLE ────────────────────────────────────
st.markdown("<div class='section-header'>🎛️ Daily Operating Cockpit (SGN)</div>", unsafe_allow_html=True)


def fmt_cell(v, fmt, is_today=False):
    if v is None:
        return "<td class='val-neutral'>—</td>"
    today_cls = " class='val-planning-today'" if is_today else ""
    if fmt == "percent":
        return f"<td{today_cls}>{v:.1%}</td>"
    elif fmt == "decimal":
        return f"<td{today_cls}>{v:.2f}</td>"
    else:
        return f"<td{today_cls}>{v:,.0f}</td>"


def delta_cell(v, positive_is_good=True):
    if v is None:
        return "<td class='val-neutral'>—</td>"
    cls = ("val-positive" if v >= 0 else "val-negative") if positive_is_good else ("val-negative" if v >= 0 else "val-positive")
    arrow = "▲" if v >= 0 else "▼"
    return f"<td class='{cls}'>{arrow}{abs(v):.1%}</td>"


def fc_vs_cell(actual, fc, fmt):
    """Show actual vs FC with a Slate ratio pill inline."""
    if actual is None:
        return "<td class='val-neutral'>—</td>"
    actual_str = f"{actual:.1%}" if fmt == "percent" else (f"{actual:.2f}" if fmt == "decimal" else f"{actual:,.0f}")
    if fc is None or fc == 0:
        return f"<td>{actual_str}</td>"
    ratio = actual / fc
    r_cls = "pos" if ratio >= 0.95 else ("neu" if ratio >= 0.85 else "neg")
    r_str = f"{ratio:.0%}"
    fc_str = f"{fc:.1%}" if fmt == "percent" else (f"{fc:.2f}" if fmt == "decimal" else f"{fc:,.0f}")
    return f"<td>{actual_str}<br><span class='delta-badge {r_cls}' style='margin-top:0.25rem;'><span class='badge-label'>vs FC</span>{r_str}</span><br><small class='val-neutral' style='font-size:0.68rem;'>FC {fc_str}</small></td>"


_lm_period = f"1–{date_yesterday.strftime('%d')} May"
_wtd_label = f"{wtd_start_label}–{date_yesterday.strftime('%d-%b')}"
_lwtd_label = f"{lwtd_start_label}–{_last_week_same_dow.strftime('%d-%b')}"

_dod_lbl = date_dod.strftime('%d-%b') if date_dod else "D-2"

def delta_cell_abs(pct_v, abs_v, positive_is_good=True, is_pct_metric=False):
    """Delta cell: pill percentage on top, absolute number below in muted text."""
    if pct_v is None:
        return "<td class='val-neutral'>—</td>"
    good = pct_v >= 0 if positive_is_good else pct_v < 0
    cls = "pos" if good else "neg"
    arrow = "▲" if pct_v >= 0 else "▼"
    pct_str = f"{arrow}{abs(pct_v):.1%}"
    return f"<td><span class='delta-badge {cls}' title='{abs_v if abs_v is not None else ''}'>{pct_str}</span></td>"
html_table = f"""
<div class="cockpit-table-container">
  <table class="cockpit-table">
    <thead>
      <tr>
        <th rowspan="2" class="sticky-col" style="vertical-align:bottom;">SGN</th>
        <!-- DAILY group: 5 cols -->
        <th colspan="5" class="hdr-actual-current" style="text-align:center;border-bottom:1px solid #475569;">
          DAILY — {date_yesterday.strftime('%d-%b')}
        </th>
        <!-- WTD group: 4 cols -->
        <th colspan="4" class="hdr-actual-past" style="text-align:center;border-bottom:1px solid #475569;">
          WTD — {_wtd_label}
        </th>
        <!-- MTD group: 3 cols -->
        <th colspan="3" class="hdr-plan" style="text-align:center;border-bottom:1px solid #475569;">
          MTD — Jun-2026
        </th>
      </tr>
      <tr>
        <!-- DAILY sub-headers -->
        <th class="hdr-actual-current">Actual</th>
        <th class="hdr-plan">FC</th>
        <th class="hdr-actual-past">DoD Δ<br><small style="font-size:0.65rem;color:#94A3B8;">vs {_dod_lbl}</small></th>
        <th class="hdr-actual-past">vs prev week<br><small style="font-size:0.65rem;color:#94A3B8;">vs {date_last_week.strftime('%d-%b')}</small></th>
        <th class="hdr-plan">vs FC</th>
        <!-- WTD sub-headers -->
        <th class="hdr-actual-current">Actual</th>
        <th class="hdr-plan">FC</th>
        <th class="hdr-actual-past">vs LWTD<br><small style="font-size:0.65rem;color:#94A3B8;">{_lwtd_label}</small></th>
        <th class="hdr-plan">vs FC</th>
        <!-- MTD sub-headers -->
        <th class="hdr-actual-current">Actual</th>
        <th class="hdr-actual-past">MoM<br><small style="font-size:0.65rem;color:#94A3B8;">vs {_lm_period}</small></th>
        <th class="hdr-plan">vs FC / LM</th>
      </tr>
    </thead>
    <tbody>
"""

cockpit_rows_order = [
    ("Request", "Request", None),
    ("Complete", "Complete", None),
    ("FR", "FR", None),
    ("Active", "Active", None),
    ("FT", "Active_FT", "Active"),
    ("PT", "Active_PT", "Active"),
    ("NLM", "Active_NLM", "Active"),
    ("Return", "Active_Return", "Active"),
    ("NIM", "Active_NIM", "Active"),
    ("NID", "Active_NID", "Active"),
    ("Other (EXP)", "Active_Other", "Active"),
    ("Cap", "Cap", None),
    ("FT", "Cap_FT", "Cap"),
    ("PT", "Cap_PT", "Cap"),
    ("NLM", "Cap_NLM", "Cap"),
    ("Return", "Cap_Return", "Cap"),
    ("NIM", "Cap_NIM", "Cap"),
    ("NID", "Cap_NID", "Cap"),
    ("Other (EXP)", "Cap_Other", "Cap"),
    ("online/driver", "online/driver", None),
    ("FT", "online/driver_FT", "online/driver"),
    ("PT", "online/driver_PT", "online/driver"),
    ("NLM", "online/driver_NLM", "online/driver"),
    ("Return", "online/driver_Return", "online/driver"),
    ("NIM", "online/driver_NIM", "online/driver"),
    ("NID", "online/driver_NID", "online/driver"),
    ("Other (EXP)", "online/driver_Other", "online/driver"),
    ("Prod", "Prod", None),
    ("FT", "Prod_FT", "Prod"),
    ("PT", "Prod_PT", "Prod"),
    ("NLM", "Prod_NLM", "Prod"),
    ("Return", "Prod_Return", "Prod"),
    ("NIM", "Prod_NIM", "Prod"),
    ("NID", "Prod_NID", "Prod"),
    ("Other (EXP)", "Prod_Other", "Prod"),
    ("Supply hour", "Supply hour", None),
    ("FT", "Supply_hour_FT", "Supply hour"),
    ("PT", "Supply_hour_PT", "Supply hour"),
    ("NLM", "Supply_hour_NLM", "Supply hour"),
    ("Return", "Supply_hour_Return", "Supply hour"),
    ("NIM", "Supply_hour_NIM", "Supply hour"),
    ("NID", "Supply_hour_NID", "Supply hour"),
    ("Other (EXP)", "Supply_hour_Other", "Supply hour")
]

_ACTIVE_KEYS = {"Active", "Active_FT", "Active_PT", "Active_NLM", "Active_Return", "Active_NIM", "Active_NID", "Active_Other"}

for label, key, parent in cockpit_rows_order:
    row = cockpit[key]
    fmt = row["format"]
    is_pct_metric = row["is_percent"]
    tr_class = "row-header" if parent is None else ""
    td_label_cls = "sticky-col" if parent is None else "sticky-col sub-row-header"
    display_label = label if parent is None else f"↳ {label}"
    is_active_row = key in _ACTIVE_KEYS

    # Compute DoD
    dod_pct, dod_abs = get_cockpit_dod(key, row)

    html_table += f"<tr class='{tr_class}'>"
    html_table += f"<td class='{td_label_cls}'>{display_label}</td>"

    # ── DAILY (5 cols) ──────────────────────────────────────────
    html_table += fmt_cell(row.get("yesterday"), fmt)
    html_table += fmt_cell(row.get("planning"), fmt)
    html_table += delta_cell_abs(dod_pct, dod_abs, is_pct_metric=is_pct_metric)
    html_table += delta_cell_abs(row.get("wow"), row.get("wow_abs"), is_pct_metric=is_pct_metric)
    html_table += delta_cell_abs(row.get("vs_planning"), row.get("vs_planning_abs"), is_pct_metric=is_pct_metric)

    # ── WTD (4 cols) ─────────────────────────────────────────────
    html_table += fmt_cell(row.get("wtd"), fmt)
    html_table += fmt_cell(row.get("plan_wtd"), fmt)
    html_table += delta_cell_abs(row.get("wow_wtd"), row.get("wow_wtd_abs"), is_pct_metric=is_pct_metric)
    html_table += delta_cell_abs(row.get("vs_plan_wtd"), None, is_pct_metric=is_pct_metric)

    # ── MTD (3 cols) — Active: no FC comparison, use LM whole instead ────────
    html_table += fmt_cell(row.get("mtd"), fmt)
    html_table += delta_cell_abs(row.get("mom_mtd"), row.get("mom_mtd_abs"), is_pct_metric=is_pct_metric)
    if is_active_row:
        # Active MTD vs FC is meaningless (distinct driver count vs daily plan) — show vs LM whole month
        html_table += delta_cell_abs(row.get("mom_whole"), row.get("mom_whole_abs"), is_pct_metric=is_pct_metric)
    else:
        html_table += delta_cell_abs(row.get("vs_planning_mtd"), None, is_pct_metric=is_pct_metric)
    html_table += "</tr>"

html_table += f"""
    </tbody>
  </table>
</div>
<div style='margin-top:0.4rem;font-size:0.72rem;color:#64748B;'>
  💡 DAILY DoD = vs ngày hôm trước ({_dod_lbl}) &nbsp;·&nbsp; vs prev week = cùng thứ tuần trước &nbsp;·&nbsp; WTD Mon–{date_yesterday.strftime('%d-%b')} &nbsp;·&nbsp; Active MTD "vs FC/LM" = vs LM whole month (FC không có nghĩa cho distinct driver count)
</div>
"""
st.markdown(html_table, unsafe_allow_html=True)


# ── LAYER 2: DEMAND ANALYSIS ──────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Demand Analysis — Request, Demand & Fulfillment</div>", unsafe_allow_html=True)

request_series = process_series(daily_series(raw_df, ACTUAL_REQUEST_ROW), start_date, end_date, time_granularity)
demand_series = process_series(daily_series(raw_df, ACTUAL_DEMAND_ROW), start_date, end_date, time_granularity)
fc_request_series = process_series(daily_series(raw_df, FC_REQUEST_ROW), start_date, end_date, time_granularity)
fc_demand_series = process_series(daily_series(raw_df, FC_DEMAND_ROW), start_date, end_date, time_granularity)
fr_series = process_series(daily_series(raw_df, FR_ROWS["Total"]), start_date, end_date, time_granularity, is_rate=True)

dem_tab1, dem_tab2, dem_tab3, dem_tab4 = st.tabs([
    "📈 Request vs Demand vs FR", "🏪 Channel Performance", "📊 Channel Mix", "🔥 FR Heatmap"
])

with dem_tab1:
    col_d1, col_d2 = st.columns([3, 1])
    with col_d1:
        render_dual_axis_chart(
            data_left={"Actual Request": request_series, "Actual Demand": demand_series,
                       "FC Request": fc_request_series, "FC Demand": fc_demand_series},
            data_right={"FR% (Actual)": fr_series},
            title=f"{time_granularity} Actual vs FC — Request, Demand & FR%",
            colors_left={"Actual Request": "#3b82f6", "Actual Demand": "#3b82f6",
                         "FC Request": "rgba(255,127,50,0.35)", "FC Demand": "rgba(56,189,248,0.35)"},
            colors_right={"FR% (Actual)": "#10B981"},
            left_label="Số đơn",
            right_label="FR%"
        )
    with col_d2:
        # FR% snapshot per channel yesterday
        st.markdown("**🎯 FR% by Channel (Hôm qua)**")
        fr_ch_html = """<table class='analysis-table'>
<thead><tr><th>Channel</th><th>FR%</th><th>Status</th></tr></thead><tbody>"""
        for ch_name, ch_row in FR_ROWS.items():
            fr_ch_val = val(ch_row, col_yesterday)
            if fr_ch_val is None:
                continue
            status = "✅" if fr_ch_val >= fr_target else ("⚠️" if fr_ch_val >= fr_target * 0.9 else "🔴")
            color = "#10b981" if fr_ch_val >= fr_target else ("#fbbf24" if fr_ch_val >= fr_target * 0.9 else "#fb7185")
            fr_ch_html += f"<tr><td>{ch_name}</td><td style='color:{color};font-weight:700;'>{fr_ch_val:.1%}</td><td>{status}</td></tr>"
        fr_ch_html += "</tbody></table>"
        st.markdown(f"<div style='background:#1E293B;padding:1rem;border-radius:0.5rem;border:1px solid #334155;'>{fr_ch_html}</div>", unsafe_allow_html=True)

with dem_tab2:
    channels = ["GHN", "KA", "MP", "SME", "WH"]
    _dod_col2 = columns_with_dates[2][0] if len(columns_with_dates) > 2 else None
    _dod_date2 = columns_with_dates[2][1] if len(columns_with_dates) > 2 else None

    def _abs_delta_cell(curr, base, is_pct=False):
        """Delta % + số tuyệt đối bên dưới."""
        if curr is None:
            return "<td class='val-neutral'>—</td>"
        if base is None or base == 0:
            actual_str = f"{curr:.1%}" if is_pct else format_number(curr)
            return f"<td>{actual_str}<br><small style='color:#64748B;'>no base</small></td>"
        d = curr - base if is_pct else (curr - base) / base
        abs_diff = curr - base
        cls = "val-positive" if d >= 0 else "val-negative"
        arrow = "▲" if d >= 0 else "▼"
        pct_str = f"{arrow}{abs(d):.1%}"
        abs_str = f"{abs_diff:+,.0f}" if not is_pct else f"{abs_diff:+.1%}"
        return f"<td class='{cls}'>{pct_str}<br><small style='opacity:0.75;'>{abs_str}</small></td>"

    def _abs_val_cell(curr, is_pct=False):
        if curr is None:
            return "<td class='val-neutral'>—</td>"
        return f"<td>{'  {:.1%}'.format(curr) if is_pct else format_number(curr)}</td>"

    def pct_fc_cell(actual, fc):
        if actual is None or fc is None or fc == 0:
            return "<td class='val-neutral'>—</td>"
        r = actual / fc
        color = "#10b981" if r >= 0.95 else ("#fbbf24" if r >= 0.85 else "#fb7185")
        diff = actual - fc
        return f"<td style='color:{color};font-weight:700;'>{r:.1%}<br><small style='opacity:0.75;'>{diff:+,.0f}</small></td>"

    def fr_cell(v):
        if v is None:
            return "<td class='val-neutral'>—</td>"
        color = "#10b981" if v >= fr_target else ("#fbbf24" if v >= fr_target * 0.9 else "#fb7185")
        return f"<td style='color:{color};font-weight:700;'>{v:.1%}</td>"

    _dod_lbl = _dod_date2.strftime('%d-%b') if _dod_date2 else "D-2"
    ch_table_html = f"""<div class='cockpit-table-container'><table class='analysis-table'>
<thead>
  <tr>
    <th rowspan="2" style="vertical-align:bottom;">Channel</th>
    <th colspan="3" class="hdr-actual-current" style="text-align:center;border-bottom:1px solid #475569;">
      DAILY — {date_yesterday.strftime('%d-%b')} (Actual vs FC)
    </th>
    <th colspan="2" class="hdr-actual-past" style="text-align:center;border-bottom:1px solid #475569;">
      DoD — vs {_dod_lbl}
    </th>
    <th colspan="2" class="hdr-actual-past" style="text-align:center;border-bottom:1px solid #475569;">
      WoW — vs {date_last_week.strftime('%d-%b')}
    </th>
    <th colspan="3" class="hdr-actual-current" style="text-align:center;border-bottom:1px solid #475569;">
      WTD — {_wtd_label}
    </th>
    <th colspan="3" class="hdr-plan" style="text-align:center;border-bottom:1px solid #475569;">
      MTD — Jun-2026
    </th>
    <th rowspan="2" class="hdr-actual-current" style="vertical-align:bottom;text-align:center;">FR%<br><small style='color:#94A3B8;font-size:0.65rem;'>Hôm qua</small></th>
  </tr>
  <tr>
    <th class="hdr-actual-current">Actual Req</th>
    <th class="hdr-plan">FC Req</th>
    <th class="hdr-plan">Actual vs FC</th>
    <th class="hdr-actual-past">Req Δ</th>
    <th class="hdr-actual-past">Dem Δ</th>
    <th class="hdr-actual-past">Req Δ</th>
    <th class="hdr-actual-past">Dem Δ</th>
    <th class="hdr-actual-current">Req</th>
    <th class="hdr-actual-current">Dem</th>
    <th class="hdr-actual-past">vs LWTD Req</th>
    <th class="hdr-plan">Req</th>
    <th class="hdr-plan">Dem</th>
    <th class="hdr-actual-past">MoM Req</th>
  </tr>
</thead><tbody>"""

    all_ch_rows = [("SGN Total", 21, 5, 28, 13, 180, "total")] + \
                  [(ch, CHANNEL_ACT_REQ_ROWS.get(ch), CHANNEL_FC_REQ_ROWS.get(ch),
                    CHANNEL_ACT_DEM_ROWS.get(ch), CHANNEL_FC_DEM_ROWS.get(ch),
                    FR_ROWS.get(ch), ch) for ch in channels]

    for ch_name, act_req_r, fc_req_r, act_dem_r, fc_dem_r, fr_r, ch_key in all_ch_rows:
        if act_req_r is None:
            continue
        act_req_y   = val(act_req_r, col_yesterday)
        fc_req_y    = val(fc_req_r, col_yesterday) if fc_req_r else None
        act_dem_y   = val(act_dem_r, col_yesterday) if act_dem_r else None
        act_req_dod = val(act_req_r, _dod_col2) if _dod_col2 else None
        act_dem_dod = val(act_dem_r, _dod_col2) if _dod_col2 and act_dem_r else None
        act_req_lw  = val(act_req_r, col_last_week)
        act_dem_lw  = val(act_dem_r, col_last_week) if act_dem_r else None
        wtd_req     = get_row_wtd_sum(act_req_r)
        wtd_dem     = get_row_wtd_sum(act_dem_r) if act_dem_r else None
        lwtd_req    = get_row_lwtd_sum(act_req_r)
        mtd_req     = get_row_mtd_sum(act_req_r)
        mtd_dem     = get_row_mtd_sum(act_dem_r) if act_dem_r else None
        lm_mtd_req  = get_row_lm_mtd_sum(act_req_r)
        fr_v        = val(fr_r, col_yesterday) if fr_r else None

        ch_color = CHANNEL_COLORS.get(ch_key, "#3b82f6") if ch_key != "total" else "#3b82f6"
        tr_cls = "class='total-row'" if ch_key == "total" else ""

        ch_table_html += f"""<tr {tr_cls}>
<td style='color:{ch_color};font-weight:700;'>{ch_name}</td>
{_abs_val_cell(act_req_y)}
{_abs_val_cell(fc_req_y)}
{pct_fc_cell(act_req_y, fc_req_y)}
{_abs_delta_cell(act_req_y, act_req_dod)}
{_abs_delta_cell(act_dem_y, act_dem_dod)}
{_abs_delta_cell(act_req_y, act_req_lw)}
{_abs_delta_cell(act_dem_y, act_dem_lw)}
{_abs_val_cell(wtd_req)}
{_abs_val_cell(wtd_dem)}
{_abs_delta_cell(wtd_req, lwtd_req)}
{_abs_val_cell(mtd_req)}
{_abs_val_cell(mtd_dem)}
{_abs_delta_cell(mtd_req, lm_mtd_req)}
{fr_cell(fr_v)}
</tr>"""

    ch_table_html += "</tbody></table></div>"
    st.markdown(ch_table_html, unsafe_allow_html=True)

    # Channel actual trend chart
    st.markdown("**📈 Actual Request by Channel (30 ngày)**")
    ch_actual_data = {}
    for ch in channels:
        act_r = CHANNEL_ACT_REQ_ROWS.get(ch)
        if act_r:
            s = process_series(daily_series(raw_df, act_r), start_date, end_date, time_granularity)
            if not s.empty:
                ch_actual_data[ch] = s
    if ch_actual_data:
        render_bar_chart(ch_actual_data, "Actual Request by Channel", CHANNEL_COLORS, stacked=True)

with dem_tab3:
    # Channel Mix % stacked area
    st.markdown("**📊 Request Channel Mix % (Tỷ trọng từng channel)**")
    all_ch_actual = {}
    for ch in ["GHN", "KA", "MP", "SME", "WH"]:
        act_r = CHANNEL_ACT_REQ_ROWS.get(ch)
        if act_r:
            s = daily_series(raw_df, act_r)
            if not s.empty:
                all_ch_actual[ch] = s

    # Build mix % series aligned to total
    total_s = daily_series(raw_df, ACTUAL_REQUEST_ROW)
    mix_data = {}
    for ch, s in all_ch_actual.items():
        combined = pd.DataFrame({"ch": s, "total": total_s}).dropna()
        combined = combined[combined["total"] > 0]
        mix_s = combined["ch"] / combined["total"]
        mix_s = process_series(mix_s, start_date, end_date, time_granularity, is_rate=True, agg_type="mean")
        if not mix_s.empty:
            mix_data[ch] = mix_s

    if mix_data and go:
        fig_mix = go.Figure()
        for ch, s in mix_data.items():
            text_labels = [f"{v:.0%}" for v in s.values]
            fig_mix.add_trace(go.Bar(
                x=s.index, y=s.values, name=ch,
                text=text_labels, textposition="inside",
                textfont={"size": 8, "color": "#F8FAFC"},
                marker_color=CHANNEL_COLORS.get(ch, "#3b82f6"),
                hovertemplate=f"%{{x|%d-%b}}: %{{y:.1%}}<extra>{ch}</extra>",
            ))
        fig_mix.update_layout(
            barmode="stack",
            title={"text": "Channel Mix % (Actual Request)", "font": {"size": 14, "color": "#F8FAFC"}},
            yaxis={"tickformat": ".0%"},
            font={"family": "Inter, sans-serif", "color": "#F8FAFC"},
            paper_bgcolor="#1E293B", plot_bgcolor="#1E293B",
            margin={"l": 30, "r": 30, "t": 60, "b": 30},
            legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
            hovermode="x unified", template="plotly_dark",
        )
        fig_mix.update_xaxes(showgrid=False, linecolor="#334155", tickfont={"color": "#94A3B8"})
        fig_mix.update_yaxes(gridcolor="#334155", zerolinecolor="#334155", tickfont={"color": "#94A3B8"})
        st.plotly_chart(fig_mix, use_container_width=True)

    # FR% trend by channel
    st.markdown("**🎯 FR% Trend by Channel**")
    fr_ch_data = {}
    for ch in ["GHN", "KA", "MP", "SME", "WH"]:
        fr_r = FR_ROWS.get(ch)
        if fr_r:
            s = process_series(daily_series(raw_df, fr_r), start_date, end_date, time_granularity, is_rate=True)
            if not s.empty:
                fr_ch_data[ch] = s
    if fr_ch_data:
        render_line_chart(fr_ch_data, "FR% Trend by Channel", CHANNEL_COLORS, is_rate=True)

with dem_tab4:
    # Forecast Accuracy Heatmap: channel × last 15 days
    st.markdown("**🔥 Forecast Accuracy Heatmap — Actual vs FC (last 15 ngày)**")
    
    hm_days = columns_with_dates[1:16]  # yesterday back 15 days (skip today)
    hm_channels = ["Total", "GHN", "KA", "MP", "SME", "WH"]
    hm_channel_act = {
        "Total": 21, "GHN": 23, "KA": 24, "MP": 25, "SME": 26, "WH": 27
    }
    hm_channel_fc = {
        "Total": 5, "GHN": 7, "KA": 8, "MP": 9, "SME": 10, "WH": 12
    }

    hm_html = """<div class='cockpit-table-container'><table class='analysis-table' style='font-size:0.75rem;'>
<thead><tr><th>Channel</th>"""
    for col_i, dt in hm_days:
        hm_html += f"<th>{dt.strftime('%d-%b')}<br><span style='color:#64748B;font-size:0.65rem;'>{dt.strftime('%a')}</span></th>"
    hm_html += "</tr></thead><tbody>"

    for ch in hm_channels:
        act_r = hm_channel_act.get(ch)
        fc_r = hm_channel_fc.get(ch)
        ch_color = CHANNEL_COLORS.get(ch, "#F8FAFC")
        hm_html += f"<tr><td style='color:{ch_color};'>{ch}</td>"
        for col_i, dt in hm_days:
            act_v = val(act_r, col_i) if act_r else None
            fc_v = val(fc_r, col_i) if fc_r else None
            if act_v is None or fc_v is None or fc_v == 0:
                hm_html += "<td class='hm-na'>—</td>"
            else:
                ratio = act_v / fc_v
                ratio_str = f"{ratio:.0%}"
                if 0.95 <= ratio <= 1.05:
                    hm_html += f"<td class='hm-pass'>{ratio_str}</td>"
                elif ratio < 0.95:
                    hm_html += f"<td class='hm-under'>{ratio_str}</td>"
                else:
                    hm_html += f"<td class='hm-over'>{ratio_str}</td>"
        hm_html += "</tr>"

    hm_html += """</tbody></table></div>
<div style='margin-top:0.5rem;font-size:0.75rem;color:#94A3B8;'>
🟢 Pass (95-105%) &nbsp; 🔴 Under (<95%) &nbsp; 🟡 Over (>105%)
</div>"""
    st.markdown(hm_html, unsafe_allow_html=True)


# ── LAYER 3: SUPPLY & DRIVER ANALYTICS ───────────────────────────────────────
st.markdown("<div class='section-header'>🚗 Supply & Driver Analytics</div>", unsafe_allow_html=True)

sup_tab1, sup_tab2, sup_tab3 = st.tabs([
    "📉 Active Driver Trend", "⚡ Segment Efficiency", "📦 Service Type Mix"
])

with sup_tab1:
    # Charts: side by side (2 columns)
    col_s1, col_s2_chart = st.columns(2)
    with col_s1:
        # Supply Hours trend (Online Hours = tổng giờ online của tài xế)
        onlineh_series = process_series(daily_series(raw_df, ONLINE_HOURS_TOTAL_ROW), start_date, end_date, time_granularity)
        sh_by_seg = {
            seg: process_series(daily_series(raw_df, sh_seg_rows[seg]), start_date, end_date, time_granularity)
            for seg in ["FT", "PT", "NLM", "Return", "NIM"]
            if sh_seg_rows.get(seg)
        }
        render_line_chart(
            {"Total Supply Hours": onlineh_series, **sh_by_seg},
            f"{time_granularity} Supply Hours (Online Hours) by Segment",
            {"Total Supply Hours": "#F8FAFC", **{s: SEGMENT_COLORS[s] for s in sh_by_seg}}
        )

    with col_s2_chart:
        # Active drivers by segment
        segment_data = {
            seg: process_series(daily_series(raw_df, SEGMENT_ROWS[seg]), start_date, end_date, time_granularity, agg_type="mean")
            for seg in selected_segments
        }
        if segment_data:
            render_line_chart(segment_data, f"{time_granularity} Active Drivers by Segment", SEGMENT_COLORS)

    # Tables: full-width below charts
    # ── Supply tables: two columns full-width below charts ─────────────────
    lm_sd_label = date_yesterday.strftime('%d') + "-" + (date_yesterday.replace(month=date_yesterday.month-1).strftime('%b') if date_yesterday.month > 1 else "")
    dod_label = columns_with_dates[2][1].strftime('%d-%b') if len(columns_with_dates) > 2 else "D-2"
    col_dod = columns_with_dates[2][0] if len(columns_with_dates) > 2 else None

    _tbl_col1, _tbl_col2 = st.columns([5, 3])

    with _tbl_col1:
        st.markdown(f"**Supply Hours — DoD / WoW / WTD / MTD**")
        sh_detail_html = f"""<table class='analysis-table' style='font-size:0.75rem;width:100%;'>
<thead><tr>
<th>Segment</th>
<th>Hôm qua<br><span style='color:#64748B;'>{date_yesterday.strftime('%d-%b')}</span></th>
<th>DoD Δ<br><span style='color:#64748B;'>{dod_label}</span></th>
<th>WoW Δ<br><span style='color:#64748B;'>{date_last_week.strftime('%d-%b')}</span></th>
<th>WTD<br><span style='color:#64748B;'>{_wtd_label}</span></th>
<th>WTD vs LWTD<br><span style='color:#64748B;'>{_lwtd_label}</span></th>
<th>MTD<br><span style='color:#64748B;'>Jun</span></th>
<th>MoM Δ<br><span style='color:#64748B;'>vs {lm_period_label}</span></th>
</tr></thead><tbody>"""

        def _sh_delta_td(curr, base):
            if curr is None or base is None or base == 0:
                return "<td class='val-neutral'>—</td>"
            d = (curr - base) / base
            abs_diff = curr - base
            cls = "val-positive" if d >= 0 else "val-negative"
            arrow = "▲" if d >= 0 else "▼"
            return f"<td class='{cls}'>{arrow}{abs(d):.1%}<br><small style='opacity:0.75;'>{abs_diff:+,.0f}</small></td>"

        sh_detail_segs = [("Total", 66), ("FT", 67), ("PT", 68), ("NLM", 69), ("Return", 70), ("NIM", 71)]
        for seg_name, row_idx in sh_detail_segs:
            yv = val(row_idx, col_yesterday)
            dod_v = val(row_idx, col_dod) if col_dod else None
            wow_v = val(row_idx, col_last_week)
            wtd_v = get_row_wtd_sum(row_idx)
            lwtd_v = get_row_lwtd_sum(row_idx)
            mtd_v = get_row_mtd_sum(row_idx)
            lm_mtd_v = get_row_lm_mtd_sum(row_idx)
            seg_color = "#3b82f6" if seg_name == "Total" else SEGMENT_COLORS.get(seg_name, "#F8FAFC")
            row_cls = "class='total-row'" if seg_name == "Total" else ""
            sh_detail_html += f"""<tr {row_cls}>
<td style='color:{seg_color};font-weight:700;'>{seg_name}</td>
<td>{format_number(yv)}</td>
{_sh_delta_td(yv, dod_v)}
{_sh_delta_td(yv, wow_v)}
<td>{format_number(wtd_v)}</td>
{_sh_delta_td(wtd_v, lwtd_v)}
<td>{format_number(mtd_v)}</td>
{_sh_delta_td(mtd_v, lm_mtd_v)}
</tr>"""
        sh_detail_html += "</tbody></table>"
        st.markdown(f"<div style='overflow-x:auto;background:#1E293B;padding:1rem;border-radius:0.5rem;border:1px solid #334155;'>{sh_detail_html}</div>", unsafe_allow_html=True)

    with _tbl_col2:
        st.markdown(f"**Supply Snapshot — Yest vs LM cùng kỳ**")
        snap_rows = [
            ("Active Total",   val(50, col_yesterday), val(50, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(50), False),
            ("Supply Hours",   val(66, col_yesterday), val(66, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(66), False),
            ("Productivity",   val(74, col_yesterday), val(74, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(74), True),
            ("Online/Driver",  val(82, col_yesterday), val(82, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(82), True),
            ("Prod/Online Hr", val(90, col_yesterday), val(90, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(90), True),
        ]
        supply_snap_html = f"""<table class='analysis-table' style='font-size:0.75rem;width:100%;'>
<thead><tr>
<th>Metric</th>
<th>Yest<br><span style='color:#64748B;'>{date_yesterday.strftime('%d-%b')}</span></th>
<th>LM same day<br><span style='color:#64748B;'>{lm_sd_label}</span></th>
<th>LM MTD avg<br><span style='color:#64748B;'>1–{date_yesterday.strftime('%d')} May</span></th>
</tr></thead><tbody>"""
        for name, yv, lm_sd, lm_mtd_a, is_dec in snap_rows:
            fmt = lambda v: (f"{v:.2f}" if is_dec else format_number(v)) if v else "—"
            if yv and lm_sd and lm_sd > 0:
                diff_sd = (yv - lm_sd) / lm_sd
                sd_color = "#10b981" if diff_sd >= 0 else "#fb7185"
                sd_arrow = "▲" if diff_sd >= 0 else "▼"
                sd_str = f"<span style='color:{sd_color};'>{sd_arrow} {diff_sd:+.1%}</span><br><small>{fmt(lm_sd)}</small>"
            else:
                sd_str = f"<span style='color:#64748B;'>—</span><br><small>{fmt(lm_sd)}</small>"
            if yv and lm_mtd_a and lm_mtd_a > 0:
                diff_mtd = (yv - lm_mtd_a) / lm_mtd_a
                mtd_color = "#10b981" if diff_mtd >= 0 else "#fb7185"
                mtd_arrow = "▲" if diff_mtd >= 0 else "▼"
                mtd_str = f"<span style='color:{mtd_color};'>{mtd_arrow} {diff_mtd:+.1%}</span><br><small>{fmt(lm_mtd_a)}</small>"
            else:
                mtd_str = f"<span style='color:#64748B;'>—</span><br><small>{fmt(lm_mtd_a)}</small>"
            supply_snap_html += f"<tr><td><b>{name}</b></td><td>{fmt(yv)}</td><td>{sd_str}</td><td>{mtd_str}</td></tr>"
        supply_snap_html += "</tbody></table>"
        st.markdown(f"<div style='background:#1E293B;padding:1rem;border-radius:0.5rem;border:1px solid #334155;'>{supply_snap_html}</div>", unsafe_allow_html=True)

with sup_tab2:
    # Segment Efficiency Table: Active / Cap / OnlineHrs / Prod / Online/Driver / Prod/OnlineHr
    segs_eff = ["FT", "PT", "NLM", "Return", "NIM"]
    # Helper: format value with MoM delta vs LM same-period
    def eff_cell(v, lm_v, dec=0):
        fmt = lambda x: f"{x:.{dec}f}" if dec > 0 else format_number(x)
        if v is None:
            return "—"
        if lm_v and lm_v > 0:
            diff = (v - lm_v) / lm_v
            color = "#10b981" if diff >= 0 else "#fb7185"
            arrow = "▲" if diff >= 0 else "▼"
            return f"{fmt(v)}<br><small style='color:{color};'>{arrow} {diff:+.1%}</small>"
        return fmt(v)

    lm_sd_col = lm_same_day_col  # alias
    seg_eff_html = f"""<div class='cockpit-table-container'><table class='analysis-table'>
<thead><tr>
<th>Segment</th>
<th>Active (Yest)<br><small style='color:#64748B;'>vs LM same day</small></th>
<th>Active MTD<br><small style='color:#64748B;'>vs LM same period</small></th>
<th>Active LM MTD avg</th>
<th>Capacity (Yest)</th><th>Online Hrs (Yest)</th>
<th>Productivity (Yest)<br><small style='color:#64748B;'>vs LM same day</small></th>
<th>Prod LM MTD avg</th>
<th>Online/Driver (Yest)<br><small style='color:#64748B;'>vs LM same day</small></th>
<th>OPD LM MTD avg</th>
<th>Prod/OnlineHr</th>
</tr></thead><tbody>"""

    # Total row — LM comparisons use same-period (lm_same_day_col for daily, lm_mtd for MTD)
    tot_active_lm_sd = val(50, lm_sd_col) if lm_sd_col else None
    tot_active_lm_mtd_avg = get_row_lm_mtd_mean(50)
    tot_active_mtd = val(50, 3)
    tot_active_lm_mtd_sum = get_row_lm_mtd_sum(50) if False else None  # not used for avg metric
    # For MTD sums (cumulative): compare request MTD sum vs lm_mtd_sum
    # For daily avg (active, prod): compare yesterday vs lm_same_day; MTD avg vs lm_mtd_avg
    seg_eff_html += f"""<tr class='total-row'>
<td>Total</td>
<td>{eff_cell(val(50, col_yesterday), tot_active_lm_sd)}</td>
<td>{eff_cell(tot_active_mtd, get_row_lm_mtd_sum(50) if False else None)}{format_number(tot_active_mtd)}<br><small style='color:#64748B;'>LM MTD avg: {format_number(tot_active_lm_mtd_avg)}</small></td>
<td>{format_number(tot_active_lm_mtd_avg)}</td>
<td>{format_number(val(58, col_yesterday))}</td>
<td>{format_number(val(66, col_yesterday))}</td>
<td>{eff_cell(val(74, col_yesterday), val(74, lm_sd_col) if lm_sd_col else None, dec=1)}</td>
<td>{format_number(get_row_lm_mtd_mean(74), 1)}</td>
<td>{eff_cell(val(82, col_yesterday), val(82, lm_sd_col) if lm_sd_col else None, dec=1)}</td>
<td>{format_number(get_row_lm_mtd_mean(82), 1)}</td>
<td>{format_number(val(90, col_yesterday), 2)}</td>
</tr>"""

    for seg in segs_eff:
        act_r = active_seg_rows.get(seg)
        cap_r = cap_seg_rows.get(seg)
        sh_r = sh_seg_rows.get(seg)
        prod_r = PROD_SEG_ROWS.get(seg)
        opd_r = ONLINE_DR_SEG_ROWS.get(seg)
        poh_r = PROD_ONLINE_SEG_ROWS.get(seg)

        seg_color = SEGMENT_COLORS.get(seg, "#F8FAFC")
        act_yest = val(act_r, col_yesterday) if act_r else None
        act_lm_sd = val(act_r, lm_sd_col) if act_r and lm_sd_col else None
        act_lm_mtd_avg = get_row_lm_mtd_mean(act_r) if act_r else None
        prod_yest_seg = val(prod_r, col_yesterday) if prod_r else None
        prod_lm_sd_seg = val(prod_r, lm_sd_col) if prod_r and lm_sd_col else None
        prod_lm_mtd_seg = get_row_lm_mtd_mean(prod_r) if prod_r else None
        opd_yest_seg = val(opd_r, col_yesterday) if opd_r else None
        opd_lm_sd_seg = val(opd_r, lm_sd_col) if opd_r and lm_sd_col else None
        opd_lm_mtd_seg = get_row_lm_mtd_mean(opd_r) if opd_r else None

        seg_eff_html += f"""<tr>
<td style='color:{seg_color};font-weight:700;'>{seg}</td>
<td>{eff_cell(act_yest, act_lm_sd)}</td>
<td>{format_number(val(act_r, 3)) if act_r else '—'}<br><small style='color:#64748B;'>LM: {format_number(act_lm_mtd_avg)}</small></td>
<td>{format_number(act_lm_mtd_avg)}</td>
<td>{format_number(val(cap_r, col_yesterday)) if cap_r else '—'}</td>
<td>{format_number(val(sh_r, col_yesterday)) if sh_r else '—'}</td>
<td>{eff_cell(prod_yest_seg, prod_lm_sd_seg, dec=1)}</td>
<td>{format_number(prod_lm_mtd_seg, 1) if prod_lm_mtd_seg else '—'}</td>
<td>{eff_cell(opd_yest_seg, opd_lm_sd_seg, dec=1)}</td>
<td>{format_number(opd_lm_mtd_seg, 1) if opd_lm_mtd_seg else '—'}</td>
<td>{format_number(val(poh_r, col_yesterday), 2) if poh_r else '—'}</td>
</tr>"""

    seg_eff_html += "</tbody></table></div>"
    st.markdown(seg_eff_html, unsafe_allow_html=True)

    # Productivity by segment trend chart
    st.markdown("**📈 Productivity Trend by Segment**")
    prod_seg_data = {}
    for seg in segs_eff:
        prod_r = PROD_SEG_ROWS.get(seg)
        if prod_r:
            s = process_series(daily_series(raw_df, prod_r), start_date, end_date, time_granularity, is_rate=False, agg_type="mean")
            if not s.empty:
                prod_seg_data[seg] = s
    if prod_seg_data:
        render_line_chart(prod_seg_data, "Productivity by Segment (Cap/Active)", SEGMENT_COLORS)

with sup_tab3:
    # Active by Service Type (1h=Giao ngay 1H, 2h=Siêu tốc 2H, 4h=4H/Ghép đơn)
    st.markdown("**📦 Active by Service Type — Nhóm dịch vụ (Hôm qua)**")
    st.caption("Nhóm dịch vụ 1H = Giao ngay 1H &nbsp;|&nbsp; Nhóm dịch vụ 2H = Siêu tốc 2H &nbsp;|&nbsp; Nhóm dịch vụ 4H = Giao trong 4H / Ghép đơn")

    tw_segs = ["Total", "FT", "PT", "NLM", "NIM"]
    tw_html = """<div class='cockpit-table-container'><table class='analysis-table'>
<thead><tr>
<th>Segment</th>
<th>Total Active</th>
<th>Nhóm DV 1H<br><small style="color:#94A3B8;font-size:0.65rem;">Giao ngay 1H</small></th><th>1H%</th>
<th>Nhóm DV 2H<br><small style="color:#94A3B8;font-size:0.65rem;">Siêu tốc 2H</small></th><th>2H%</th>
<th>Nhóm DV 4H<br><small style="color:#94A3B8;font-size:0.65rem;">Giao 4H / Ghép đơn</small></th><th>4H%</th>
</tr></thead><tbody>"""

    for seg in tw_segs:
        seg_rows_map = ACTIVE_TIME_ROWS.get(seg, {})
        total_v = val(seg_rows_map.get("total", 0), col_yesterday) if seg_rows_map else None
        v_1h = val(seg_rows_map.get("1h", 0), col_yesterday) if seg_rows_map else None
        v_2h = val(seg_rows_map.get("2h", 0), col_yesterday) if seg_rows_map else None
        v_4h = val(seg_rows_map.get("4h", 0), col_yesterday) if seg_rows_map else None

        pct_1h = v_1h / total_v if total_v and v_1h else None
        pct_2h = v_2h / total_v if total_v and v_2h else None
        pct_4h = v_4h / total_v if total_v and v_4h else None

        seg_color = SEGMENT_COLORS.get(seg, "#F8FAFC") if seg != "Total" else "#3b82f6"
        row_cls = "class='total-row'" if seg == "Total" else ""

        def pct_svc_cell(v, threshold_hi=0.5, threshold_lo=0.3):
            if v is None:
                return "<td class='val-neutral'>—</td>"
            color = "#10b981" if v >= threshold_hi else ("#fbbf24" if v >= threshold_lo else "#fb7185")
            return f"<td style='color:{color};font-weight:700;'>{v:.1%}</td>"

        tw_html += f"""<tr {row_cls}>
<td style='color:{seg_color};font-weight:700;'>{seg}</td>
<td>{format_number(total_v)}</td>
<td>{format_number(v_1h)}</td>{pct_svc_cell(pct_1h, 0.5, 0.3)}
<td>{format_number(v_2h)}</td>{pct_svc_cell(pct_2h, 0.3, 0.15)}
<td>{format_number(v_4h)}</td>{pct_svc_cell(pct_4h, 0.2, 0.10)}
</tr>"""

    tw_html += """</tbody></table></div>
<div style='margin-top:0.5rem;font-size:0.75rem;color:#94A3B8;'>
💡 Phân bổ theo loại dịch vụ tài xế phục vụ hôm qua — không phải thời gian online.
</div>"""
    st.markdown(tw_html, unsafe_allow_html=True)

    # Service type trend total
    st.markdown("**📈 Active by Service Type — Trend (Total)**")
    active_4h_series = process_series(daily_series(raw_df, 177), start_date, end_date, time_granularity, agg_type="mean")
    active_2h_series = process_series(daily_series(raw_df, 172), start_date, end_date, time_granularity, agg_type="mean")
    active_1h_series = process_series(daily_series(raw_df, 167), start_date, end_date, time_granularity, agg_type="mean")
    active_total_series_2 = process_series(daily_series(raw_df, 166), start_date, end_date, time_granularity, agg_type="mean")
    render_line_chart(
        {"Giao ngay 1H": active_1h_series, "Siêu tốc 2H": active_2h_series,
         "Giao 4H/Ghép": active_4h_series, "Active Total": active_total_series_2},
        f"{time_granularity} Active by Service Type",
        {"Giao ngay 1H": "#3b82f6", "Siêu tốc 2H": "#3b82f6", "Giao 4H/Ghép": "#10b981", "Active Total": "#94A3B8"}
    )



# ── LAYER 4: ADVANCED ANALYTICS ──────────────────────────────────────────────
st.markdown("<div class='section-header'>📈 Trend & Pattern Analysis</div>", unsafe_allow_html=True)

adv_tab1, adv_tab2, adv_tab3, adv_tab4 = st.tabs([
    "📅 Long-term Trend", "🗓️ Weekday Pattern", "📐 Accuracy Counter", "🏆 Leaderboard"
])

with adv_tab1:
    # 90-day Request + Demand trend with month bands
    all_req = daily_series(raw_df, ACTUAL_REQUEST_ROW)
    all_dem = daily_series(raw_df, ACTUAL_DEMAND_ROW)
    all_fr = daily_series(raw_df, FR_ROWS["Total"])

    # Filter last 90 days
    cutoff_90 = max_date - pd.Timedelta(days=90)
    req_90 = all_req[all_req.index >= cutoff_90]
    dem_90 = all_dem[all_dem.index >= cutoff_90]
    fr_90 = all_fr[all_fr.index >= cutoff_90]

    render_dual_axis_chart(
        data_left={"Actual Request": req_90, "Actual Demand": dem_90},
        data_right={"FR% (Actual)": fr_90},
        title="90-Day Trend — Actual Request, Demand & FR%",
        colors_left={"Actual Request": "#3b82f6", "Actual Demand": "#3b82f6"},
        colors_right={"FR% (Actual)": "#10B981"},
        left_label="Số đơn",
        right_label="FR%"
    )

with adv_tab2:
    # Weekday pattern: group by Mon-Sun, show avg Request per weekday
    st.markdown("**🗓️ Average Actual Request by Weekday (last 90 ngày)**")
    cutoff_90 = max_date - pd.Timedelta(days=90)
    req_90_2 = all_req[all_req.index >= cutoff_90].copy()
    
    if not req_90_2.empty and go:
        req_90_2 = req_90_2[req_90_2 > 0]
        req_90_2.index = pd.to_datetime(req_90_2.index)
        req_90_df = pd.DataFrame({"value": req_90_2.values, "date": req_90_2.index})
        req_90_df["weekday"] = req_90_df["date"].dt.day_name()
        req_90_df["weekday_num"] = req_90_df["date"].dt.dayofweek
        
        weekday_avg = req_90_df.groupby(["weekday", "weekday_num"])["value"].agg(["mean", "std", "count"]).reset_index()
        weekday_avg = weekday_avg.sort_values("weekday_num")
        
        fig_wd = go.Figure()
        bar_colors = ["#3b82f6" if d in [0, 1, 2, 3, 4] else "#6366F1" for d in weekday_avg["weekday_num"]]
        fig_wd.add_trace(go.Bar(
            x=weekday_avg["weekday"],
            y=weekday_avg["mean"],
            text=[f"{v/1000:.1f}k" for v in weekday_avg["mean"]],
            textposition="outside",
            textfont={"size": 10, "color": "#F8FAFC"},
            marker_color=bar_colors,
            error_y=dict(type="data", array=weekday_avg["std"].fillna(0).tolist(), visible=True, color="#475569"),
            hovertemplate="<b>%{x}</b><br>Avg: %{y:,.0f}<br>n=%{customdata} ngày<extra></extra>",
            customdata=weekday_avg["count"],
        ))
        fig_wd.update_layout(
            title={"text": "Average Actual Request by Weekday (90 ngày gần nhất)", "font": {"size": 14, "color": "#F8FAFC"}},
            font={"family": "Inter, sans-serif", "color": "#F8FAFC"},
            paper_bgcolor="#1E293B", plot_bgcolor="#1E293B",
            margin={"l": 30, "r": 30, "t": 60, "b": 30},
            hovermode="closest", template="plotly_dark",
        )
        fig_wd.update_xaxes(showgrid=False, linecolor="#334155", tickfont={"color": "#94A3B8"})
        fig_wd.update_yaxes(gridcolor="#334155", linecolor="#334155", tickfont={"color": "#94A3B8"})
        st.plotly_chart(fig_wd, use_container_width=True)

    # Weekday FR% pattern
    st.markdown("**🎯 Average FR% by Weekday**")
    if not all_fr.empty and go:
        fr_90_3 = all_fr[all_fr.index >= cutoff_90].copy()
        fr_90_3 = fr_90_3[fr_90_3 > 0]
        fr_90_df = pd.DataFrame({"value": fr_90_3.values, "date": fr_90_3.index})
        fr_90_df["weekday"] = pd.to_datetime(fr_90_df["date"]).dt.day_name()
        fr_90_df["weekday_num"] = pd.to_datetime(fr_90_df["date"]).dt.dayofweek
        fr_wd_avg = fr_90_df.groupby(["weekday", "weekday_num"])["value"].mean().reset_index()
        fr_wd_avg = fr_wd_avg.sort_values("weekday_num")
        
        fig_fr_wd = go.Figure()
        fr_bar_colors = ["#10b981" if v >= fr_target else ("#fbbf24" if v >= fr_target * 0.9 else "#fb7185")
                         for v in fr_wd_avg["value"]]
        fig_fr_wd.add_trace(go.Bar(
            x=fr_wd_avg["weekday"],
            y=fr_wd_avg["value"],
            text=[f"{v:.1%}" for v in fr_wd_avg["value"]],
            textposition="outside",
            textfont={"size": 10, "color": "#F8FAFC"},
            marker_color=fr_bar_colors,
            hovertemplate="<b>%{x}</b>: %{y:.1%}<extra>FR%</extra>",
        ))
        fig_fr_wd.add_hline(y=fr_target, line_dash="dot", line_color="#3b82f6",
                            annotation_text=f"Target FR {fr_target:.0%}",
                            annotation_position="bottom right",
                            annotation={"font": {"color": "#3b82f6"}})
        fig_fr_wd.update_layout(
            title={"text": "Average FR% by Weekday", "font": {"size": 14, "color": "#F8FAFC"}},
            yaxis={"tickformat": ".0%"},
            font={"family": "Inter, sans-serif", "color": "#F8FAFC"},
            paper_bgcolor="#1E293B", plot_bgcolor="#1E293B",
            margin={"l": 30, "r": 30, "t": 60, "b": 30},
            hovermode="closest", template="plotly_dark",
        )
        fig_fr_wd.update_xaxes(showgrid=False, linecolor="#334155", tickfont={"color": "#94A3B8"})
        fig_fr_wd.update_yaxes(gridcolor="#334155", linecolor="#334155", tickfont={"color": "#94A3B8"})
        st.plotly_chart(fig_fr_wd, use_container_width=True)

with adv_tab3:
    # Accuracy Counter: how many days each metric was within 95-105% of forecast
    accuracy_metrics = {
        "Actual Request": (21, 5),
        "Actual Demand": (28, 13),
        "Active Drivers": (50, None),
        "Online Hours": (66, None)
    }

    accuracy_rows_html = ""
    for name, (act_row, fcast_row) in accuracy_metrics.items():
        day_pass = 0
        day_under = 0
        day_over = 0
        valid_days = 0

        for col_idx in mtd_cols:
            act_val = parse_value(safe_cell(raw_df, act_row, col_idx))
            if act_val is None or act_val == 0:
                continue

            if fcast_row is not None:
                fc_val = parse_value(safe_cell(raw_df, fcast_row, col_idx))
            else:
                fc_req = parse_value(safe_cell(raw_df, 5, col_idx))
                if fc_req is not None:
                    if name == "Active Drivers":
                        fc_val = fc_req * (sum(act_plan_16jun.values()) / 77392.0)
                    else:
                        fc_val = fc_req * (sum(sh_plan_16jun.values()) / 77392.0)
                else:
                    fc_val = None

            if fc_val is not None and fc_val > 0:
                valid_days += 1
                ratio = act_val / fc_val
                if 0.95 <= ratio <= 1.05:
                    day_pass += 1
                elif ratio < 0.95:
                    day_under += 1
                else:
                    day_over += 1

        acc_rate = day_pass / valid_days if valid_days > 0 else 0.0
        acc_rate_color = "val-positive" if acc_rate >= 0.80 else ("val-neutral" if acc_rate >= 0.50 else "val-negative")

        accuracy_rows_html += f"""<tr>
<td style='padding: 0.4rem; font-weight:700;'>{name}</td>
<td style='padding: 0.4rem;'>95% - 105%</td>
<td style='padding: 0.4rem; text-align:center;'>{day_pass}</td>
<td style='padding: 0.4rem; text-align:center;' class='{acc_rate_color}'>{acc_rate:.1%}</td>
<td style='padding: 0.4rem; text-align:center;'>{day_under}</td>
<td style='padding: 0.4rem; text-align:center;'>{day_over}</td>
<td style='padding: 0.4rem; text-align:center; color:#64748B;'>{valid_days}</td>
</tr>"""

    st.markdown(
        f"""<div class='leaderboard-card'>
<div class='leaderboard-title'>🎯 Số ngày các chỉ số đạt % FC SGN (MTD)</div>
<table style='width:100%; font-size:0.78rem; border-collapse:collapse; color:#F8FAFC;'>
<thead>
<tr style='border-bottom:1px solid #334155; text-align:left; color:#94A3B8;'>
<th style='padding:0.4rem;'>Metric</th>
<th style='padding:0.4rem;'>Target Range</th>
<th style='padding:0.4rem; text-align:center;'>Pass ✅</th>
<th style='padding:0.4rem; text-align:center;'>% Pass</th>
<th style='padding:0.4rem; text-align:center;'>Under 🔴</th>
<th style='padding:0.4rem; text-align:center;'>Over 🟡</th>
<th style='padding:0.4rem; text-align:center;'>Valid Days</th>
</tr>
</thead>
<tbody>
{accuracy_rows_html}
</tbody>
</table>
</div>""",
        unsafe_allow_html=True
    )

with adv_tab4:
    # Leaderboard: Top 3 days for Actual Request & Actual Demand
    col_lb1, col_lb2 = st.columns(2)

    with col_lb1:
        leaderboard_req = []
        for col_idx in mtd_cols:
            d_val = parse_sheet_date(safe_cell(raw_df, 4, col_idx))
            val_req = parse_value(safe_cell(raw_df, 21, col_idx))
            if d_val is not None and val_req is not None and val_req > 0:
                leaderboard_req.append((d_val, val_req))
        leaderboard_req.sort(key=lambda x: x[1], reverse=True)

        req_rows_html = ""
        for rank, (d, v) in enumerate(leaderboard_req[:5]):
            req_rows_html += f"""<div class="leaderboard-row rank-{min(rank+1,3)}">
<div class="rank-badge">Top {rank+1} &nbsp;&nbsp; {d.strftime('%d-%b')}</div>
<div style="font-weight:700;">{v:,.0f} reqs</div>
</div>"""

        st.markdown(
            f"""<div class='leaderboard-card'>
<div class='leaderboard-title'>🏆 Leaderboard — Top 5 ngày Actual Request SGN</div>
{req_rows_html}
</div>""",
            unsafe_allow_html=True
        )

    with col_lb2:
        leaderboard_dem = []
        for col_idx in mtd_cols:
            d_val = parse_sheet_date(safe_cell(raw_df, 4, col_idx))
            val_dem = parse_value(safe_cell(raw_df, 28, col_idx))
            if d_val is not None and val_dem is not None and val_dem > 0:
                leaderboard_dem.append((d_val, val_dem))
        leaderboard_dem.sort(key=lambda x: x[1], reverse=True)

        dem_rows_html = ""
        for rank, (d, v) in enumerate(leaderboard_dem[:5]):
            dem_rows_html += f"""<div class="leaderboard-row rank-{min(rank+1,3)}">
<div class="rank-badge">Top {rank+1} &nbsp;&nbsp; {d.strftime('%d-%b')}</div>
<div style="font-weight:700;">{v:,.0f} orders</div>
</div>"""

        st.markdown(
            f"""<div class='leaderboard-card'>
<div class='leaderboard-title'>🏆 Leaderboard — Top 5 ngày Actual Demand SGN</div>
{dem_rows_html}
</div>""",
            unsafe_allow_html=True
        )


# ── FOOTER NOTE ───────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="footer-note">
        Source: <a href="{SHEET_URL}" target="_blank">Google Sheet — SGN Overview</a> ·
        Last fetched: {fetched_at} · Cache TTL: {CACHE_TTL_SECONDS // 60} phút ·
        Dashboard v3.0 — Built for Ahamove Driver Management SGN Ops cockpit.
    </div>
    """,
    unsafe_allow_html=True,
)
