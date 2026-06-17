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
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;800&display=swap');

    /* Global styles forcing dark background */
    .stApp, html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Lexend', sans-serif;
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] .stButton button {
        background-color: #334155 !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #475569 !important;
        border-color: #FF7F32 !important;
    }

    /* Main Typography */
    .main-title {
        color: #F8FAFC;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.04em;
        background: linear-gradient(90deg, #F8FAFC 0%, #FF7F32 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        color: #94A3B8;
        font-weight: 500;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .section-header {
        color: #38BDF8;
        font-weight: 800;
        font-size: 1.4rem;
        border-left: 6px solid #FF7F32;
        padding-left: 0.8rem;
        margin: 1.8rem 0 1rem 0;
        letter-spacing: -0.02em;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 1.25rem;
        padding: 1.2rem;
        box-shadow: 0 10px 30px -15px rgba(0, 0, 0, 0.5);
        text-align: center;
        min-height: 142px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.6);
        border-color: #475569;
    }
    .metric-card-accent {
        border-color: #FF7F32 !important;
        background: linear-gradient(135deg, #1E293B 0%, #1a2235 100%) !important;
    }
    .metric-card-green {
        border-color: #10B981 !important;
    }
    .metric-card-blue {
        border-color: #38BDF8 !important;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #94A3B8;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 0.35rem;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 2.15rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.04em;
    }
    .metric-value-lg {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.04em;
    }
    .metric-delta {
        font-size: 0.88rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }
    .metric-context {
        color: #64748B;
        font-size: 0.75rem;
        margin-top: 0.15rem;
    }
    .status-pill {
        display: inline-block;
        background: #064E3B;
        color: #34D399;
        border: 1px solid #059669;
        border-radius: 999px;
        padding: 0.25rem 0.7rem;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .footer-note {
        color: #64748B;
        font-size: 0.82rem;
        padding-top: 1rem;
        border-top: 1px solid #334155;
        margin-top: 2.5rem;
    }
    .footer-note a {
        color: #FF7F32;
        text-decoration: none;
    }
    .footer-note a:hover {
        text-decoration: underline;
    }

    /* Custom CSS Table for Cockpit Grid */
    .cockpit-table-container {
        overflow-x: auto;
        margin: 1.5rem 0;
        border-radius: 0.75rem;
        border: 1px solid #334155;
        background-color: #1E293B;
    }
    .cockpit-table {
        width: 100%;
        border-collapse: collapse;
        color: #F8FAFC;
        font-size: 0.85rem;
        text-align: left;
    }
    .cockpit-table th {
        background-color: #0F172A;
        color: #94A3B8;
        font-weight: 700;
        padding: 0.75rem 1rem;
        border-bottom: 2px solid #334155;
        text-transform: uppercase;
        font-size: 0.72rem;
        letter-spacing: 0.05em;
    }
    .cockpit-table td {
        padding: 0.65rem 1rem;
        border-bottom: 1px solid #334155;
        font-weight: 500;
    }
    .cockpit-table tr:hover {
        background-color: #1E293B !important;
        filter: brightness(1.15);
    }
    .cockpit-table .row-header {
        font-weight: 700;
        color: #38BDF8;
        background-color: #1A202C;
    }
    .cockpit-table .row-header td {
        border-bottom: 2px solid #475569;
        font-size: 0.9rem;
    }
    .cockpit-table .sub-row-header {
        font-weight: 500;
        color: #E2E8F0;
        padding-left: 2rem !important;
    }
    .hdr-actual-current {
        background-color: #1E3A8A !important;
        color: #F8FAFC !important;
        text-align: center !important;
    }
    .hdr-actual-past {
        background-color: #334155 !important;
        color: #E2E8F0 !important;
        text-align: center !important;
    }
    .hdr-plan {
        background-color: #0F766E !important;
        color: #F8FAFC !important;
        text-align: center !important;
    }
    .hdr-today {
        background-color: #D97706 !important;
        color: #F8FAFC !important;
        text-align: center !important;
        border: 1px solid #FF7F32;
    }
    .val-positive {
        color: #34D399 !important;
        font-weight: 700;
    }
    .val-negative {
        color: #F87171 !important;
        font-weight: 700;
    }
    .val-neutral {
        color: #94A3B8 !important;
    }
    .val-planning-today {
        color: #34D399 !important;
        background-color: rgba(52, 211, 153, 0.1);
        border-radius: 4px;
        padding: 2px 6px;
    }

    /* Leaderboard Card Styling */
    .leaderboard-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 0.75rem;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .leaderboard-title {
        color: #38BDF8;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .leaderboard-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.4rem;
        border-radius: 0.35rem;
    }
    .rank-1 { background-color: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); }
    .rank-2 { background-color: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); }
    .rank-3 { background-color: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); }
    
    .rank-badge {
        font-weight: 800;
        font-size: 0.95rem;
    }
    .rank-1 .rank-badge { color: #34D399; }
    .rank-2 .rank-badge { color: #FBBF24; }
    .rank-3 .rank-badge { color: #818CF8; }

    /* Channel/Segment Analysis Table */
    .analysis-table {
        width: 100%;
        border-collapse: collapse;
        color: #F8FAFC;
        font-size: 0.82rem;
    }
    .analysis-table th {
        background-color: #0F172A;
        color: #94A3B8;
        font-weight: 700;
        padding: 0.6rem 0.75rem;
        border-bottom: 2px solid #334155;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.04em;
        text-align: center;
    }
    .analysis-table th:first-child { text-align: left; }
    .analysis-table td {
        padding: 0.55rem 0.75rem;
        border-bottom: 1px solid #1E293B;
        text-align: center;
    }
    .analysis-table td:first-child { text-align: left; font-weight: 700; }
    .analysis-table tr:hover { background-color: rgba(255,255,255,0.03); }
    .analysis-table .total-row {
        background-color: #1a2840;
        font-weight: 700;
        color: #38BDF8;
        border-top: 2px solid #334155;
    }

    /* Heatmap Cell Styles */
    .hm-pass { background-color: rgba(16,185,129,0.25); color: #34D399; font-weight: 700; }
    .hm-under { background-color: rgba(248,113,113,0.25); color: #F87171; font-weight: 700; }
    .hm-over { background-color: rgba(251,191,36,0.20); color: #FBBF24; font-weight: 700; }
    .hm-na { color: #475569; }
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
    "GHN": "#38BDF8", "KA": "#FF7F32", "MP": "#10B981",
    "SME": "#6366F1", "TRUCK": "#94A3B8", "WH": "#F59E0B",
    "SME+MP+KA": "#A78BFA", "Total": "#F8FAFC",
}
SEGMENT_COLORS = {
    "FT": "#38BDF8", "PT": "#FF7F32", "NLM": "#10B981",
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
    if current is None or baseline is None or baseline == 0:
        return "<span style='color:#64748B'>No baseline</span>"
    delta = current - baseline
    delta_pct = delta / abs(baseline)
    color = "#34D399" if delta >= 0 else "#F87171"
    arrow = "▲" if delta >= 0 else "▼"
    if percent:
        label = f"{arrow} {delta:+.2%} {label_suffix}"
    else:
        label = f"{arrow} {delta_pct:+.2%} {label_suffix}"
    return f"<span style='color:{color}'>{label}</span>"


def metric_card(label, value, delta, context="", accent_class=""):
    return f"""
    <div class="metric-card {accent_class}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta">{delta}</div>
        <div class="metric-context">{context}</div>
    </div>
    """


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
        font={"family": "Lexend, sans-serif", "color": "#F8FAFC"},
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        margin={"l": 30, "r": 30, "t": 60, "b": 30},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1, "font": {"color": "#F8FAFC"}},
        hovermode="x unified",
        template="plotly_dark",
    )
    fig.update_xaxes(showgrid=False, linecolor="#334155", gridcolor="#334155", tickfont={"color": "#94A3B8"})
    fig.update_yaxes(gridcolor="#334155", zerolinecolor="#334155", linecolor="#334155", tickfont={"color": "#94A3B8"})
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
        fmt = ".1%" if is_rate else None

        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series.values,
                mode="lines+markers+text",
                name=label,
                text=text_values,
                textposition="top center",
                textfont={"size": 9, "color": "#F8FAFC"},
                line={"width": 3, "color": colors.get(label, "#38BDF8"), "shape": "spline", "smoothing": 1.3},
                marker={"size": 6, "symbol": "circle"},
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
                marker_color=colors.get(label, "#38BDF8"),
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
        fig.add_trace(
            go.Scatter(
                x=series.index, y=series.values,
                mode="lines+markers+text", name=label,
                text=text_values, textposition="top center",
                textfont={"size": 8, "color": "#F8FAFC"},
                line={"width": 3, "color": colors_left.get(label, "#38BDF8"), "shape": "spline", "smoothing": 1.3},
                marker={"size": 5},
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
        font={"family": "Lexend, sans-serif", "color": "#F8FAFC"},
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        margin={"l": 30, "r": 60, "t": 60, "b": 30},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1, "font": {"color": "#F8FAFC"}},
        hovermode="x unified",
        template="plotly_dark",
    )
    fig.update_xaxes(showgrid=False, linecolor="#334155", gridcolor="#334155", tickfont={"color": "#94A3B8"})
    fig.update_yaxes(title_text=left_label, gridcolor="#334155", zerolinecolor="#334155", linecolor="#334155", tickfont={"color": "#94A3B8"}, secondary_y=False)
    fig.update_yaxes(title_text=right_label, gridcolor="#334155", zerolinecolor="#334155", linecolor="#334155", tickfont={"color": "#10B981"}, tickformat=".0%", secondary_y=True)
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
fr_target = st.sidebar.slider("Target FR% (ngưỡng đạt)", min_value=0.60, max_value=0.90, value=0.75, step=0.01, format="%.0f%%") 

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

    # Daily: WoW + vs Plan
    row["wow"] = (y - lw if is_pct else (y - lw) / lw) if (y is not None and lw is not None and lw != 0) else None
    plan = row["planning"]
    row["vs_planning"] = (y - plan if is_pct else (y - plan) / plan) if (y is not None and plan is not None and plan != 0) else None

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


# ── LAYER 1: EXECUTIVE SUMMARY - KPI CARDS ───────────────────────────────────
st.markdown("<div class='section-header'>🔴 Executive Summary — KPI Pulse</div>", unsafe_allow_html=True)

# Compute derived KPIs
fr_yest = val(180, col_yesterday)  # % Actual FR Total row 180
utilization_yest = None
active_4h_pct = None

cap_yest = val(58, col_yesterday)
online_yest = val(66, col_yesterday)
active_total_4h = val(177, col_yesterday)   # Total active_4h
active_total = val(166, col_yesterday)       # Total Active (row 166)

if cap_yest and online_yest and cap_yest > 0:
    utilization_yest = online_yest / cap_yest

if active_total and active_total > 0 and active_total_4h is not None:
    active_4h_pct = active_total_4h / active_total

# LM equivalents for comparison — all use SAME PERIOD (LM MTD = same day range last month)
# lm_same_day_col: exact same calendar day in previous month (e.g. May 16 for Jun 16)
# get_row_lm_mtd_mean/sum: period May 1–{date_yesterday.day} (mirrors current MTD Jun 1–{date_yesterday.day})
fr_lm_same_day = val(180, lm_same_day_col) if lm_same_day_col else None

# Utilization: use LM MTD averages (not full LM totals which inflate the denominator)
util_lm_cap_mtd = get_row_lm_mtd_mean(58)   # avg daily Capacity in LM same period
util_lm_sh_mtd = get_row_lm_mtd_mean(66)    # avg daily Online Hours in LM same period
util_lm = util_lm_sh_mtd / util_lm_cap_mtd if util_lm_cap_mtd and util_lm_sh_mtd else None

prod_yest = val(74, col_yesterday)
prod_lm_same_day = val(74, lm_same_day_col) if lm_same_day_col else None
prod_lm_mtd_avg = get_row_lm_mtd_mean(74)   # avg Productivity May 1–{date_yesterday.day}
opd_yest = val(82, col_yesterday)
opd_lm_same_day = val(82, lm_same_day_col) if lm_same_day_col else None
opd_lm_mtd_avg = get_row_lm_mtd_mean(82)

# Keep full-LM as secondary context only
util_lm_full_cap = val(58, 2)
util_lm_full_sh = val(66, 2)
prod_lm_full = val(74, 2)
opd_lm_full = val(82, 2)

# Row 1: 6 KPI cards
cols = st.columns(6)

cols[0].markdown(
    metric_card(
        "Actual Request (Hôm qua)",
        format_number(val(21, col_yesterday)),
        delta_html(val(21, col_yesterday), val(22, col_last_week), label_suffix="WoW"),
        f"FC: {format_number(val(6, col_yesterday))} | {date_yesterday.strftime('%d-%b')}",
        "metric-card-accent"
    ),
    unsafe_allow_html=True,
)

cols[1].markdown(
    metric_card(
        "Actual Demand (Hôm qua)",
        format_number(val(28, col_yesterday)),
        delta_html(val(28, col_yesterday), val(29, col_last_week), label_suffix="WoW"),
        f"FC: {format_number(val(13, col_yesterday))} | {date_yesterday.strftime('%d-%b')}",
    ),
    unsafe_allow_html=True,
)

# FR% card with color
fr_color = "#34D399" if fr_yest and fr_yest >= fr_target else ("#FBBF24" if fr_yest and fr_yest >= fr_target * 0.9 else "#F87171")
fr_html = f"""
<div class="metric-card" style="border-color: {fr_color}33;">
    <div class="metric-label">Fulfillment Rate (Hôm qua)</div>
    <div class="metric-value" style="color:{fr_color};">{format_percent(fr_yest)}</div>
    <div class="metric-delta"><span style="color:{fr_color};">{'✅' if fr_yest and fr_yest >= fr_target else '⚠️'} Target: {fr_target:.0%}</span></div>
    <div class="metric-context">vs {date_yesterday.strftime('%d-%b')}</div>
</div>
"""
cols[2].markdown(fr_html, unsafe_allow_html=True)

cols[3].markdown(
    metric_card(
        "Active Drivers (Hôm qua)",
        format_number(val(50, col_yesterday)),
        delta_html(val(50, col_yesterday), val(50, col_last_week), label_suffix="WoW"),
        f"Plan: {format_number(sum(act_plan_16jun.values()))}",
        "metric-card-blue"
    ),
    unsafe_allow_html=True,
)

util_pct_str = format_percent(utilization_yest) if utilization_yest else "—"
util_lm_mtd_str = format_percent(util_lm) if util_lm else "—"
cols[4].markdown(
    metric_card(
        "Supply Utilization (Hôm qua)",
        util_pct_str,
        delta_html(utilization_yest, util_lm, percent=True, label_suffix=f"vs LM {date_yesterday.strftime('%d')}-day MTD") if utilization_yest and util_lm else "<span style='color:#64748B'>vs LM MTD</span>",
        f"LM MTD avg: {util_lm_mtd_str}",
        "metric-card-green"
    ),
    unsafe_allow_html=True,
)

# Productivity: compare yesterday vs SAME DAY last month (best apples-to-apples daily)
lm_day_str = date_yesterday.replace(month=date_yesterday.month - 1).strftime('%d-%b') if lm_same_day_col else ""
cols[5].markdown(
    metric_card(
        "Productivity (Hôm qua)",
        format_number(prod_yest, 1),
        delta_html(prod_yest, prod_lm_same_day, label_suffix=f"vs {lm_day_str}") if prod_lm_same_day else delta_html(prod_yest, prod_lm_mtd_avg, label_suffix="vs LM MTD avg"),
        f"LM MTD avg: {format_number(prod_lm_mtd_avg, 1)} | Online/Dr: {format_number(opd_yest, 1)}h",
    ),
    unsafe_allow_html=True,
)

# Row 2: MTD comparison cards — all deltas vs LM same-period (LM MTD), full LM as context
cols2 = st.columns(4)
request_mtd_val = val(22, 3)
demand_mtd_val = val(29, 3)
request_lm_full = val(22, 2)       # full May
demand_lm_full = val(29, 2)        # full May
req_lm_mtd_sum = get_row_lm_mtd_sum(22)   # May 1–{date_yesterday.day} (same period)
dem_lm_mtd_sum = get_row_lm_mtd_sum(29)   # May 1–{date_yesterday.day} (same period)
lm_period_label = f"1–{date_yesterday.strftime('%d')} May"

cols2[0].markdown(
    metric_card(
        "Request MTD",
        format_number(request_mtd_val),
        delta_html(request_mtd_val, req_lm_mtd_sum, label_suffix=f"vs LM ({lm_period_label})"),
        f"LM same period: {format_number(req_lm_mtd_sum)} | LM whole May: {format_number(request_lm_full)}",
    ),
    unsafe_allow_html=True,
)
cols2[1].markdown(
    metric_card(
        "Demand MTD",
        format_number(demand_mtd_val),
        delta_html(demand_mtd_val, dem_lm_mtd_sum, label_suffix=f"vs LM ({lm_period_label})"),
        f"LM same period: {format_number(dem_lm_mtd_sum)} | LM whole May: {format_number(demand_lm_full)}",
    ),
    unsafe_allow_html=True,
)

prod_mtd = val(74, 3)
prod_lm_whole = val(74, 2)
prod_lm_mtd_v = get_row_lm_mtd_mean(74)   # avg Productivity May 1–{date_yesterday.day}
cols2[2].markdown(
    metric_card(
        "Productivity MTD avg",
        format_number(prod_mtd, 1),
        delta_html(prod_mtd, prod_lm_mtd_v, label_suffix=f"vs LM ({lm_period_label})"),
        f"LM same period: {format_number(prod_lm_mtd_v, 1)} | LM whole May: {format_number(prod_lm_whole, 1)}",
    ),
    unsafe_allow_html=True,
)

active_4h_str = format_percent(active_4h_pct) if active_4h_pct else "—"
cols2[3].markdown(
    metric_card(
        "Active 4h+ Retention (Hôm qua)",
        active_4h_str,
        f"<span style='color:#94A3B8'>4h+: {format_number(active_total_4h)} / {format_number(active_total)} tài xế</span>",
        "Proxy: tài xế gắn bó cao",
        "metric-card-green"
    ),
    unsafe_allow_html=True,
)


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
    """Show actual vs FC with ratio badge inline."""
    if actual is None:
        return "<td class='val-neutral'>—</td>"
    actual_str = f"{actual:.1%}" if fmt == "percent" else (f"{actual:.2f}" if fmt == "decimal" else f"{actual:,.0f}")
    if fc is None or fc == 0:
        return f"<td>{actual_str}</td>"
    ratio = actual / fc
    r_cls = "val-positive" if ratio >= 0.95 else ("val-neutral" if ratio >= 0.85 else "val-negative")
    r_str = f"{ratio:.0%}"
    fc_str = f"{fc:.1%}" if fmt == "percent" else (f"{fc:.2f}" if fmt == "decimal" else f"{fc:,.0f}")
    return f"<td>{actual_str}<br><small class='{r_cls}' style='font-size:0.7rem;'>vs FC {r_str} ({fc_str})</small></td>"


_lm_period = f"1–{date_yesterday.strftime('%d')} May"
_wtd_label = f"{wtd_start_label}–{date_yesterday.strftime('%d-%b')}"
_lwtd_label = f"{lwtd_start_label}–{_last_week_same_dow.strftime('%d-%b')}"

html_table = f"""
<div class="cockpit-table-container">
  <table class="cockpit-table">
    <thead>
      <tr>
        <th rowspan="2" style="vertical-align:bottom;">SGN</th>
        <!-- DAILY group -->
        <th colspan="4" class="hdr-actual-current" style="text-align:center;border-bottom:1px solid #475569;">
          DAILY — {date_yesterday.strftime('%d-%b')}
        </th>
        <!-- WTD group -->
        <th colspan="4" class="hdr-actual-past" style="text-align:center;border-bottom:1px solid #475569;">
          WTD — {_wtd_label}
        </th>
        <!-- MTD group -->
        <th colspan="4" class="hdr-plan" style="text-align:center;border-bottom:1px solid #475569;">
          MTD — Jun-2026
        </th>
      </tr>
      <tr>
        <!-- DAILY sub-headers -->
        <th class="hdr-actual-current">Actual</th>
        <th class="hdr-plan">FC</th>
        <th class="hdr-actual-past">WoW<br><small style="font-size:0.65rem;color:#94A3B8;">vs {date_last_week.strftime('%d-%b')}</small></th>
        <th class="hdr-plan">vs FC</th>
        <!-- WTD sub-headers -->
        <th class="hdr-actual-current">Actual</th>
        <th class="hdr-plan">FC</th>
        <th class="hdr-actual-past">WoW<br><small style="font-size:0.65rem;color:#94A3B8;">vs {_lwtd_label}</small></th>
        <th class="hdr-plan">vs FC</th>
        <!-- MTD sub-headers -->
        <th class="hdr-actual-current">Actual</th>
        <th class="hdr-plan">FC</th>
        <th class="hdr-actual-past">MoM<br><small style="font-size:0.65rem;color:#94A3B8;">vs {_lm_period}</small></th>
        <th class="hdr-plan">vs FC</th>
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

for label, key, parent in cockpit_rows_order:
    row = cockpit[key]
    fmt = row["format"]
    tr_class = "row-header" if parent is None else ""
    td_label_cls = "" if parent is None else "class='sub-row-header'"

    html_table += f"<tr class='{tr_class}'>"
    html_table += f"<td {td_label_cls}>{label}</td>"
    # DAILY
    html_table += fmt_cell(row.get("yesterday"), fmt)
    html_table += fmt_cell(row.get("planning"), fmt)
    html_table += delta_cell(row.get("wow"))
    html_table += delta_cell(row.get("vs_planning"))
    # WTD
    html_table += fmt_cell(row.get("wtd"), fmt)
    html_table += fmt_cell(row.get("plan_wtd"), fmt)
    html_table += delta_cell(row.get("wow_wtd"))
    html_table += delta_cell(row.get("vs_plan_wtd"))
    # MTD
    html_table += fmt_cell(row.get("mtd"), fmt)
    html_table += fmt_cell(row.get("plan_mtd"), fmt)
    html_table += delta_cell(row.get("mom_mtd"))
    html_table += delta_cell(row.get("vs_planning_mtd"))
    html_table += "</tr>"

html_table += """
    </tbody>
  </table>
</div>
<div style='margin-top:0.4rem;font-size:0.72rem;color:#64748B;'>
  💡 WTD = Week-to-date (Mon → hôm qua) &nbsp;|&nbsp; FC = Forecast Plan &nbsp;|&nbsp; MoM so với cùng kỳ tháng trước ({_lm_period})
</div>
""".format(_lm_period=_lm_period)
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
            colors_left={"Actual Request": "#FF7F32", "Actual Demand": "#38BDF8",
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
            color = "#34D399" if fr_ch_val >= fr_target else ("#FBBF24" if fr_ch_val >= fr_target * 0.9 else "#F87171")
            fr_ch_html += f"<tr><td>{ch_name}</td><td style='color:{color};font-weight:700;'>{fr_ch_val:.1%}</td><td>{status}</td></tr>"
        fr_ch_html += "</tbody></table>"
        st.markdown(f"<div style='background:#1E293B;padding:1rem;border-radius:0.5rem;border:1px solid #334155;'>{fr_ch_html}</div>", unsafe_allow_html=True)

with dem_tab2:
    # Channel Achievement table: FC Request / Actual Request / % / FC Demand / Actual Demand / FR%
    channels = ["GHN", "KA", "MP", "SME", "WH"]
    ch_table_html = """<div class='cockpit-table-container'><table class='analysis-table'>
<thead><tr>
<th>Channel</th>
<th>FC Req (Hôm qua)</th><th>Actual Req</th><th>% FC Req</th>
<th>FC Demand</th><th>Actual Demand</th><th>% FC Dem</th>
<th>FR%</th>
<th>Actual Req MTD</th><th>Actual Dem MTD</th>
</tr></thead><tbody>"""

    # Total row first
    total_fc_req_y = val(5, col_yesterday)
    total_act_req_y = val(21, col_yesterday)
    total_fc_dem_y = val(13, col_yesterday)
    total_act_dem_y = val(28, col_yesterday)
    total_fr_y = val(180, col_yesterday)
    total_act_req_mtd = val(21, 3)
    total_act_dem_mtd = val(28, 3)
    pct_r_total = total_act_req_y / total_fc_req_y if total_fc_req_y else None
    pct_d_total = total_act_dem_y / total_fc_dem_y if total_fc_dem_y else None

    def pct_cell(v):
        if v is None:
            return "<td class='val-neutral'>—</td>"
        color = "#34D399" if v >= 0.95 else ("#FBBF24" if v >= 0.85 else "#F87171")
        return f"<td style='color:{color};font-weight:700;'>{v:.1%}</td>"

    def fr_cell(v):
        if v is None:
            return "<td class='val-neutral'>—</td>"
        color = "#34D399" if v >= fr_target else ("#FBBF24" if v >= fr_target * 0.9 else "#F87171")
        return f"<td style='color:{color};font-weight:700;'>{v:.1%}</td>"

    ch_table_html += f"""<tr class='total-row'>
<td>SGN Total</td>
<td>{format_number(total_fc_req_y)}</td><td>{format_number(total_act_req_y)}</td>{pct_cell(pct_r_total)}
<td>{format_number(total_fc_dem_y)}</td><td>{format_number(total_act_dem_y)}</td>{pct_cell(pct_d_total)}
{fr_cell(total_fr_y)}
<td>{format_number(total_act_req_mtd)}</td><td>{format_number(total_act_dem_mtd)}</td>
</tr>"""

    for ch in channels:
        fc_req_r = CHANNEL_FC_REQ_ROWS.get(ch)
        fc_dem_r = CHANNEL_FC_DEM_ROWS.get(ch)
        act_req_r = CHANNEL_ACT_REQ_ROWS.get(ch)
        act_dem_r = CHANNEL_ACT_DEM_ROWS.get(ch)
        fr_r = FR_ROWS.get(ch)

        fc_req_y = val(fc_req_r, col_yesterday) if fc_req_r else None
        act_req_y = val(act_req_r, col_yesterday) if act_req_r else None
        fc_dem_y = val(fc_dem_r, col_yesterday) if fc_dem_r else None
        act_dem_y = val(act_dem_r, col_yesterday) if act_dem_r else None
        fr_ch = val(fr_r, col_yesterday) if fr_r else None
        act_req_mtd = val(act_req_r, 3) if act_req_r else None
        act_dem_mtd = val(act_dem_r, 3) if act_dem_r else None
        pct_r = act_req_y / fc_req_y if fc_req_y and act_req_y else None
        pct_d = act_dem_y / fc_dem_y if fc_dem_y and act_dem_y else None

        ch_color = CHANNEL_COLORS.get(ch, "#F8FAFC")
        ch_table_html += f"""<tr>
<td style='color:{ch_color};font-weight:700;'>{ch}</td>
<td>{format_number(fc_req_y)}</td><td>{format_number(act_req_y)}</td>{pct_cell(pct_r)}
<td>{format_number(fc_dem_y)}</td><td>{format_number(act_dem_y)}</td>{pct_cell(pct_d)}
{fr_cell(fr_ch)}
<td>{format_number(act_req_mtd)}</td><td>{format_number(act_dem_mtd)}</td>
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
                marker_color=CHANNEL_COLORS.get(ch, "#38BDF8"),
                hovertemplate=f"%{{x|%d-%b}}: %{{y:.1%}}<extra>{ch}</extra>",
            ))
        fig_mix.update_layout(
            barmode="stack",
            title={"text": "Channel Mix % (Actual Request)", "font": {"size": 14, "color": "#F8FAFC"}},
            yaxis={"tickformat": ".0%"},
            font={"family": "Lexend, sans-serif", "color": "#F8FAFC"},
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

sup_tab1, sup_tab2, sup_tab3, sup_tab4 = st.tabs([
    "📉 Active Driver Trend", "⚡ Segment Efficiency", "⏱️ Active Time Windows", "📊 Supply Utilization"
])

with sup_tab1:
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        # Active drivers + Capacity + Online Hours on dual axis
        active_total_series = process_series(daily_series(raw_df, ACTIVE_TOTAL_ROW), start_date, end_date, time_granularity, agg_type="mean")
        cap_series = process_series(daily_series(raw_df, CAPACITY_TOTAL_ROW), start_date, end_date, time_granularity)
        onlineh_series = process_series(daily_series(raw_df, ONLINE_HOURS_TOTAL_ROW), start_date, end_date, time_granularity)
        render_dual_axis_chart(
            data_left={"Capacity (giờ)": cap_series, "Online Hours (giờ)": onlineh_series},
            data_right={},
            title=f"{time_granularity} Capacity vs Online Hours",
            colors_left={"Capacity (giờ)": "#6366F1", "Online Hours (giờ)": "#10B981"},
            colors_right={},
            left_label="Giờ tổng",
        )
        # Active drivers by segment
        segment_data = {
            seg: process_series(daily_series(raw_df, SEGMENT_ROWS[seg]), start_date, end_date, time_granularity, agg_type="mean")
            for seg in selected_segments
        }
        if segment_data:
            render_line_chart(segment_data, f"{time_granularity} Active Drivers by Segment", SEGMENT_COLORS)

    with col_s2:
        lm_sd_label = date_yesterday.strftime('%d') + "-" + (date_yesterday.replace(month=date_yesterday.month-1).strftime('%b') if date_yesterday.month > 1 else "")
        st.markdown(f"**Supply Snapshot — Yest vs LM cùng kỳ**")
        # snap_rows: (name, yest_val, lm_same_day_val, lm_mtd_avg_val, is_decimal)
        snap_rows = [
            ("Active Total",   val(50, col_yesterday), val(50, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(50), False),
            ("Capacity",       val(58, col_yesterday), val(58, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(58), False),
            ("Online Hours",   val(66, col_yesterday), val(66, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(66), False),
            ("Productivity",   val(74, col_yesterday), val(74, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(74), True),
            ("Online/Driver",  val(82, col_yesterday), val(82, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(82), True),
            ("Prod/Online Hr", val(90, col_yesterday), val(90, lm_same_day_col) if lm_same_day_col else None, get_row_lm_mtd_mean(90), True),
        ]
        supply_snap_html = f"""<table class='analysis-table' style='font-size:0.78rem;'>
<thead><tr>
<th>Metric</th>
<th>Yest<br><span style='color:#64748B;'>{date_yesterday.strftime('%d-%b')}</span></th>
<th>LM same day<br><span style='color:#64748B;'>{lm_sd_label}</span></th>
<th>LM MTD avg<br><span style='color:#64748B;'>1–{date_yesterday.strftime('%d')} May</span></th>
</tr></thead><tbody>"""
        for name, yv, lm_sd, lm_mtd_a, is_dec in snap_rows:
            fmt = lambda v: (f"{v:.2f}" if is_dec else format_number(v)) if v else "—"
            # vs LM same day
            if yv and lm_sd and lm_sd > 0:
                diff_sd = (yv - lm_sd) / lm_sd
                sd_color = "#34D399" if diff_sd >= 0 else "#F87171"
                sd_arrow = "▲" if diff_sd >= 0 else "▼"
                sd_str = f"<span style='color:{sd_color};'>{sd_arrow} {diff_sd:+.1%}</span><br><small>{fmt(lm_sd)}</small>"
            else:
                sd_str = f"<span style='color:#64748B;'>—</span><br><small>{fmt(lm_sd)}</small>"
            # vs LM MTD avg
            if yv and lm_mtd_a and lm_mtd_a > 0:
                diff_mtd = (yv - lm_mtd_a) / lm_mtd_a
                mtd_color = "#34D399" if diff_mtd >= 0 else "#F87171"
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
            color = "#34D399" if diff >= 0 else "#F87171"
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
    st.markdown("**📦 Active by Service Type Breakdown (Hôm qua)**")
    st.caption("1h = Giao ngay 1H &nbsp;|&nbsp; 2h = Siêu tốc 2H &nbsp;|&nbsp; 4h = Giao trong 4H / Ghép đơn")

    tw_segs = ["Total", "FT", "PT", "NLM", "NIM"]
    tw_html = """<div class='cockpit-table-container'><table class='analysis-table'>
<thead><tr>
<th>Segment</th>
<th>Total Active</th>
<th>Giao ngay 1H</th><th>1H%</th>
<th>Siêu tốc 2H</th><th>2H%</th>
<th>Giao 4H / Ghép</th><th>4H%</th>
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

        seg_color = SEGMENT_COLORS.get(seg, "#F8FAFC") if seg != "Total" else "#38BDF8"
        row_cls = "class='total-row'" if seg == "Total" else ""

        def pct_svc_cell(v, threshold_hi=0.5, threshold_lo=0.3):
            if v is None:
                return "<td class='val-neutral'>—</td>"
            color = "#34D399" if v >= threshold_hi else ("#FBBF24" if v >= threshold_lo else "#F87171")
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
        {"Giao ngay 1H": "#FF7F32", "Siêu tốc 2H": "#38BDF8", "Giao 4H/Ghép": "#34D399", "Active Total": "#94A3B8"}
    )

with sup_tab4:
    # Supply Utilization Rate trend (Online Hours / Capacity)
    col_u1, col_u2 = st.columns([2, 1])
    with col_u1:
        cap_s = daily_series(raw_df, CAPACITY_TOTAL_ROW)
        sh_s = daily_series(raw_df, ONLINE_HOURS_TOTAL_ROW)
        combined_util = pd.DataFrame({"sh": sh_s, "cap": cap_s}).dropna()
        combined_util = combined_util[combined_util["cap"] > 0]
        util_s = combined_util["sh"] / combined_util["cap"]
        util_series = process_series(util_s, start_date, end_date, time_granularity, is_rate=True, agg_type="mean")

        if not util_series.empty and go:
            fig_util = go.Figure()
            fig_util.add_trace(go.Scatter(
                x=util_series.index, y=util_series.values,
                mode="lines+markers+text",
                name="Utilization Rate",
                text=[f"{v:.0%}" for v in util_series.values],
                textposition="top center",
                textfont={"size": 9, "color": "#F8FAFC"},
                fill="tozeroy",
                fillcolor="rgba(16,185,129,0.1)",
                line={"width": 3, "color": "#10B981", "shape": "spline", "smoothing": 1.3},
                marker={"size": 6},
                hovertemplate="%{x|%d-%b}: %{y:.1%}<extra>Utilization</extra>",
            ))
            fig_util.update_layout(
                title={"text": "Supply Utilization Rate (Online Hours / Capacity)", "font": {"size": 14, "color": "#F8FAFC"}},
                yaxis={"tickformat": ".0%"},
                font={"family": "Lexend, sans-serif", "color": "#F8FAFC"},
                paper_bgcolor="#1E293B", plot_bgcolor="#1E293B",
                margin={"l": 30, "r": 30, "t": 60, "b": 30},
                hovermode="x unified", template="plotly_dark",
            )
            fig_util.update_xaxes(showgrid=False, linecolor="#334155", tickfont={"color": "#94A3B8"})
            fig_util.update_yaxes(gridcolor="#334155", linecolor="#334155", tickfont={"color": "#94A3B8"})
            st.plotly_chart(fig_util, use_container_width=True)

    with col_u2:
        st.markdown("**Utilization by Segment (Hôm qua)**")
        util_seg_html = """<table class='analysis-table'>
<thead><tr><th>Segment</th><th>Online Hrs</th><th>Capacity</th><th>Util%</th></tr></thead><tbody>"""
        for seg in segs_eff:
            sh_r = sh_seg_rows.get(seg)
            cap_r = cap_seg_rows.get(seg)
            sh_v = val(sh_r, col_yesterday) if sh_r else None
            cap_v = val(cap_r, col_yesterday) if cap_r else None
            util_v = sh_v / cap_v if sh_v and cap_v and cap_v > 0 else None
            color = "#34D399" if util_v and util_v >= 0.70 else ("#FBBF24" if util_v and util_v >= 0.55 else "#F87171")
            seg_color = SEGMENT_COLORS.get(seg, "#F8FAFC")
            util_seg_html += f"""<tr>
<td style='color:{seg_color};'>{seg}</td>
<td>{format_number(sh_v)}</td>
<td>{format_number(cap_v)}</td>
<td style='color:{color};font-weight:700;'>{format_percent(util_v)}</td>
</tr>"""
        util_seg_html += "</tbody></table>"
        st.markdown(f"<div style='background:#1E293B;padding:1rem;border-radius:0.5rem;border:1px solid #334155;'>{util_seg_html}</div>", unsafe_allow_html=True)


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
        colors_left={"Actual Request": "#FF7F32", "Actual Demand": "#38BDF8"},
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
        bar_colors = ["#38BDF8" if d in [0, 1, 2, 3, 4] else "#6366F1" for d in weekday_avg["weekday_num"]]
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
            font={"family": "Lexend, sans-serif", "color": "#F8FAFC"},
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
        fr_bar_colors = ["#34D399" if v >= fr_target else ("#FBBF24" if v >= fr_target * 0.9 else "#F87171")
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
        fig_fr_wd.add_hline(y=fr_target, line_dash="dot", line_color="#FF7F32",
                            annotation_text=f"Target FR {fr_target:.0%}",
                            annotation_position="bottom right",
                            annotation={"font": {"color": "#FF7F32"}})
        fig_fr_wd.update_layout(
            title={"text": "Average FR% by Weekday", "font": {"size": 14, "color": "#F8FAFC"}},
            yaxis={"tickformat": ".0%"},
            font={"family": "Lexend, sans-serif", "color": "#F8FAFC"},
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
