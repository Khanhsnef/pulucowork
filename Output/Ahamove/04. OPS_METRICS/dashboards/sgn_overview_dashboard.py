import io
from datetime import datetime, timedelta
import pandas as pd
import requests
import streamlit as st

try:
    import plotly.graph_objects as go
except ImportError:  # pragma: no cover
    go = None


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

METRIC_ROWS = {
    "request": 22,
    "demand": 29,
    "active_actual": 50,
    "capacity": 58,
    "online_hours": 66,
    "productivity": 74,
    "online_per_driver": 82,
    "prod_per_online_hour": 90,
}

CHANNEL_ROWS = {
    "GHN": 7,
    "KA": 8,
    "MP": 9,
    "SME": 10,
    "TRUCK": 11,
    "WH": 12,
}

SEGMENT_ROWS = {
    "FT": 51,
    "PT": 52,
    "NLM": 53,
    "Return": 54,
    "NIM": 55,
}

ACHIEVEMENT_REQUEST_ROWS = {
    "GHN": 36,
    "KA": 37,
    "MP": 38,
    "SME": 39,
    "TRUCK": 40,
    "WH": 41,
}

ACHIEVEMENT_DEMAND_ROWS = {
    "GHN": 43,
    "KA": 44,
    "MP": 45,
    "SME": 46,
    "TRUCK": 47,
    "WH": 48,
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


def format_percent(value, decimals=2):
    if value is None or pd.isna(value):
        return "—"
    if abs(value) > 1.5:
        value = value / 100
    return f"{value:+.{decimals}%}" if value < 0 or value > 0 else f"{value:.{decimals}%}"


def delta_html(current, baseline, percent=False):
    if current is None or baseline is None or baseline == 0:
        return "<span style='color:#64748B'>No baseline</span>"
    delta = current - baseline
    delta_pct = delta / abs(baseline)
    color = "#34D399" if delta >= 0 else "#F87171"
    arrow = "▲" if delta >= 0 else "▼"
    if percent:
        label = f"{arrow} {delta:+.2%} vs LM"
    else:
        label = f"{arrow} {delta_pct:+.2%} vs LM"
    return f"<span style='color:{color}'>{label}</span>"


def metric_card(label, value, delta, context=""):
    return f"""
    <div class="metric-card">
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
    
    # Drop today's date (17-Jun) to avoid incomplete actuals showing up
    if 'date_today' in globals() and date_today in series.index:
        series = series.drop(index=date_today, errors='ignore')
    else:
        # Fallback to hardcoded date_today value if globals not ready during function ref
        today_ts = pd.Timestamp("2026-06-17")
        if today_ts in series.index:
            series = series.drop(index=today_ts, errors='ignore')

    if time_granularity == "Weekly":
        series = aggregate_weekly(series, is_rate=is_rate, agg_type=agg_type)
    
    # Filter by selected date range
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)
    return series[(series.index >= start_ts) & (series.index <= end_ts)]



def chart_layout(fig, title=""):
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


def render_line_chart(data, title, colors):
    if go is None:
        st.line_chart(pd.DataFrame(data))
        return

    fig = go.Figure()
    for label, series in data.items():
        max_val = series.max() if not series.empty else 0
        text_values = []
        for val in series.values:
            if val is None or pd.isna(val):
                text_values.append("")
            elif max_val > 1000:
                text_values.append(f"{val/1000:.1f}k")
            elif max_val < 50:
                text_values.append(f"{val:.1f}")
            else:
                text_values.append(f"{val:,.0f}")

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
            )
        )
    st.plotly_chart(chart_layout(fig, title), use_container_width=True)


def render_bar_chart(data, title, colors, stacked=False):
    if go is None:
        st.bar_chart(pd.DataFrame(data))
        return

    fig = go.Figure()
    for label, series in data.items():
        max_val = series.max() if not series.empty else 0
        text_values = []
        for val in series.values:
            if val is None or pd.isna(val):
                text_values.append("")
            elif max_val > 1000:
                text_values.append(f"{val/1000:.1f}k")
            else:
                text_values.append(f"{val:,.0f}")

        fig.add_trace(
            go.Bar(
                x=series.index,
                y=series.values,
                name=label,
                text=text_values,
                textposition="inside" if stacked else "outside",
                textfont={"size": 9, "color": "#F8FAFC"},
                marker_color=colors.get(label, "#38BDF8"),
            )
        )
    fig.update_layout(barmode="stack" if stacked else "group")
    st.plotly_chart(chart_layout(fig, title), use_container_width=True)


# ── DRIVER EXP METRICS FALLBACKS ──────────────────────────────────────────────
def get_active_other(date_val, period_type="day"):
    # Reference values for 16-Jun yesterday, 9-Jun last week, MTD (1-16 Jun), LM (May)
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


def get_online_per_driver_other(date_val, period_type="day"):
    if period_type == "day":
        if date_val == pd.Timestamp("2026-06-16"):
            return 3.86
        elif date_val == pd.Timestamp("2026-06-09"):
            return 3.57
        else:
            return 3.8
    elif period_type == "mtd":
        return 3.8
    elif period_type == "lm":
        return 3.8
    return 3.8


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
col_last_week = col_yesterday + 7  # 9-Jun
date_last_week = parse_sheet_date(safe_cell(raw_df, 4, col_last_week))

# Calculate MTD Column Indexes (1-Jun to yesterday 16-Jun)
mtd_cols = []
target_month = date_yesterday.month
target_year = date_yesterday.year
for col_idx, d_val in columns_with_dates:
    if d_val.month == target_month and d_val.year == target_year and d_val <= date_yesterday:
        mtd_cols.append(col_idx)

# Calculate LM MTD Column Indexes (1-May to 16-May)
lm_mtd_cols = []
for col_idx, d_val in columns_with_dates:
    if d_val.month == 5 and d_val.year == 2026 and d_val.day <= date_yesterday.day:
        lm_mtd_cols.append(col_idx)


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


# Helper to calculate average or sum of dynamic planning values over MTD period
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

# 1. Request
cockpit["Request"] = {
    "label": "Request", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(22, col_yesterday),
    "last_week": val(22, col_last_week),
    "planning": val(6, col_yesterday),
    "today": val(6, col_today),
    "mtd": val(22, 3),
    "lm": val(22, 2),
    "lm_mtd": get_row_lm_mtd_sum(22),
    "plan_mtd": get_row_mtd_sum(6)
}

# 2. Complete
cockpit["Complete"] = {
    "label": "Complete", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(29, col_yesterday),
    "last_week": val(29, col_last_week),
    "planning": val(14, col_yesterday),
    "today": val(14, col_today),
    "mtd": val(29, 3),
    "lm": val(29, 2),
    "lm_mtd": get_row_lm_mtd_sum(29),
    "plan_mtd": get_row_mtd_sum(14)
}

# 3. FR
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

cockpit["FR"] = {
    "label": "FR", "is_header": True, "format": "percent", "is_percent": True,
    "yesterday": comp_y / req_y if req_y else None,
    "last_week": comp_lw / req_lw if req_lw else None,
    "planning": val(14, col_yesterday) / val(6, col_yesterday) if val(6, col_yesterday) else None,
    "today": val(14, col_today) / val(6, col_today) if val(6, col_today) else None,
    "mtd": comp_mtd / req_mtd if req_mtd else None,
    "lm": comp_lm / req_lm if req_lm else None,
    "lm_mtd": comp_lm_mtd / req_lm_mtd if req_lm_mtd else None,
    "plan_mtd": comp_plan_mtd / req_plan_mtd if req_plan_mtd else None
}

# Drivers Scaling Fallbacks
def active_plan(val_16jun, fc_req):
    return val_16jun * (fc_req / 69263.0) if fc_req else None


def supply_hour_plan(val_16jun, fc_req):
    return val_16jun * (fc_req / 69263.0) if fc_req else None


act_plan_16jun = {"FT": 2298, "PT": 3588, "NLM": 486, "Return": 263, "NIM": 533, "NID": 54}
cap_plan_16jun = {"FT": 25054, "PT": 22311, "NLM": 3655, "Return": 1659, "NIM": 3546, "NID": 208}
sh_plan_16jun = {"FT": 17079, "PT": 15972, "NLM": 2572, "Return": 1198, "NIM": 2543, "NID": 208}

# 4. Active
cockpit["Active"] = {
    "label": "Active", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(50, col_yesterday),
    "last_week": val(50, col_last_week),
    "planning": sum(act_plan_16jun.values()),
    "today": active_plan(sum(act_plan_16jun.values()), val(6, col_today)),
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
        "mtd": val(r, 3),
        "lm": val(r, 2),
        "lm_mtd": get_row_lm_mtd_mean(r),
        "plan_mtd": get_driver_plan_mtd(act_plan_16jun[seg], mtd_cols, "mean")
    }
cockpit["Active_Other"] = {
    "label": "Other (EXP)", "is_header": False, "format": "number", "is_percent": False,
    "yesterday": val_or_zero(50, col_yesterday) - sum(val_or_zero(active_seg_rows[s], col_yesterday) for s in active_segs),
    "last_week": val_or_zero(50, col_last_week) - sum(val_or_zero(active_seg_rows[s], col_last_week) for s in active_segs),
    "planning": 0.0,
    "today": 0.0,
    "mtd": val_or_zero(50, 3) - sum(val_or_zero(active_seg_rows[s], 3) for s in active_segs),
    "lm": val_or_zero(50, 2) - sum(val_or_zero(active_seg_rows[s], 2) for s in active_segs),
    "lm_mtd": max(0.0, get_row_lm_mtd_mean(50) - sum(get_row_lm_mtd_mean(active_seg_rows[s]) for s in active_segs)),
    "plan_mtd": 0.0
}

# 5. Cap
cap_segs = ["FT", "PT", "NLM", "Return", "NIM", "NID"]
cap_seg_rows = {"FT": 59, "PT": 60, "NLM": 61, "Return": 62, "NIM": 63, "NID": 64}


def get_cap_seg_sum(col):
    return sum(val_or_zero(cap_seg_rows[s], col) for s in cap_segs)


def get_cap_seg_mtd_sum(s):
    return get_row_mtd_sum(cap_seg_rows[s])


cockpit["Cap"] = {
    "label": "Cap", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(58, col_yesterday),
    "last_week": val(58, col_last_week),
    "planning": sum(cap_plan_16jun.values()),
    "today": active_plan(sum(cap_plan_16jun.values()), val(6, col_today)),
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
        "mtd": get_cap_seg_mtd_sum(seg),
        "lm": val(r, 2),
        "lm_mtd": get_row_lm_mtd_sum(r),
        "plan_mtd": get_driver_plan_mtd(cap_plan_16jun[seg], mtd_cols, "sum")
    }
cockpit["Cap_Other"] = {
    "label": "Other (EXP)", "is_header": False, "format": "number", "is_percent": False,
    "yesterday": val_or_zero(58, col_yesterday) - sum(val_or_zero(cap_seg_rows[s], col_yesterday) for s in cap_segs),
    "last_week": val_or_zero(58, col_last_week) - sum(val_or_zero(cap_seg_rows[s], col_last_week) for s in cap_segs),
    "planning": 0.0,
    "today": 0.0,
    "mtd": val_or_zero(58, 3) - sum(get_cap_seg_mtd_sum(s) for s in cap_segs),
    "lm": val_or_zero(58, 2) - sum(val_or_zero(cap_seg_rows[s], 2) for s in cap_segs),
    "lm_mtd": max(0.0, get_row_lm_mtd_sum(58) - sum(get_row_lm_mtd_sum(cap_seg_rows[s]) for s in cap_segs)),
    "plan_mtd": 0.0
}

# 6. Supply hour
sh_segs = ["FT", "PT", "NLM", "Return", "NIM", "NID"]
sh_seg_rows = {"FT": 67, "PT": 68, "NLM": 69, "Return": 70, "NIM": 71, "NID": 72}


def get_sh_seg_sum(col):
    return sum(val_or_zero(sh_seg_rows[s], col) for s in sh_segs)


def get_sh_seg_mtd_sum(s):
    return get_row_mtd_sum(sh_seg_rows[s])


cockpit["Supply hour"] = {
    "label": "Supply hour", "is_header": True, "format": "number", "is_percent": False,
    "yesterday": val(66, col_yesterday),
    "last_week": val(66, col_last_week),
    "planning": sum(sh_plan_16jun.values()),
    "today": supply_hour_plan(sum(sh_plan_16jun.values()), val(6, col_today)),
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
        "mtd": get_sh_seg_mtd_sum(seg),
        "lm": val(r, 2),
        "lm_mtd": get_row_lm_mtd_sum(r),
        "plan_mtd": get_driver_plan_mtd(sh_plan_16jun[seg], mtd_cols, "sum")
    }
cockpit["Supply_hour_Other"] = {
    "label": "Other (EXP)", "is_header": False, "format": "number", "is_percent": False,
    "yesterday": val_or_zero(66, col_yesterday) - sum(val_or_zero(sh_seg_rows[s], col_yesterday) for s in sh_segs),
    "last_week": val_or_zero(66, col_last_week) - sum(val_or_zero(sh_seg_rows[s], col_last_week) for s in sh_segs),
    "planning": 0.0,
    "today": 0.0,
    "mtd": val_or_zero(66, 3) - sum(get_sh_seg_mtd_sum(s) for s in sh_segs),
    "lm": val_or_zero(66, 2) - sum(val_or_zero(sh_seg_rows[s], 2) for s in sh_segs),
    "lm_mtd": max(0.0, get_row_lm_mtd_sum(66) - sum(get_row_lm_mtd_sum(sh_seg_rows[s]) for s in sh_segs)),
    "plan_mtd": 0.0
}

# Helper for derived rows
def make_derived_row(label, num_key, den_key, format_type):
    derived = {}
    for col_name in ["yesterday", "last_week", "planning", "today", "mtd", "lm", "lm_mtd", "plan_mtd"]:
        num = cockpit[num_key][col_name]
        den = cockpit[den_key][col_name]
        derived[col_name] = num / den if num is not None and den is not None and den > 0 else None
    return {
        "label": label, "is_header": True, "format": format_type, "is_percent": False,
        **derived
    }


# 7. online/driver
cockpit["online/driver"] = make_derived_row("online/driver", "Supply hour", "Active", "decimal")
for seg in sh_segs:
    cockpit[f"online/driver_{seg}"] = make_derived_row(seg, f"Supply_hour_{seg}", f"Active_{seg}", "decimal")
cockpit["online/driver_Other"] = {
    "label": "Other (EXP)", "is_header": False, "format": "decimal", "is_percent": False,
    "yesterday": cockpit["Supply_hour_Other"]["yesterday"] / cockpit["Active_Other"]["yesterday"] if cockpit["Active_Other"]["yesterday"] else 0.0,
    "last_week": cockpit["Supply_hour_Other"]["last_week"] / cockpit["Active_Other"]["last_week"] if cockpit["Active_Other"]["last_week"] else 0.0,
    "planning": 0.0,
    "today": 0.0,
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
    "planning": 0.0,
    "today": 0.0,
    "mtd": get_prod_other_col("mtd"),
    "lm": get_prod_other_col("lm"),
    "lm_mtd": get_prod_other_col("lm_mtd"),
    "plan_mtd": get_prod_other_col("plan_mtd")
}

# WoW and vs Planning Delta Calculations
for key, row in cockpit.items():
    y = row["yesterday"]
    lw = row["last_week"]
    is_pct = row["is_percent"]

    if y is not None and lw is not None and lw != 0:
        row["wow"] = y - lw if is_pct else (y - lw) / lw
    else:
        row["wow"] = None

    plan = row["planning"]
    if y is not None and plan is not None and plan != 0:
        row["vs_planning"] = y - plan if is_pct else (y - plan) / plan
    else:
        row["vs_planning"] = None

    mtd = row["mtd"]
    lm = row["lm"]
    lm_mtd = row.get("lm_mtd")

    if mtd is not None and lm is not None and lm != 0:
        row["mom_whole"] = mtd - lm if is_pct else (mtd - lm) / lm
    else:
        row["mom_whole"] = None

    if mtd is not None and lm_mtd is not None and lm_mtd != 0:
        row["mom_mtd"] = mtd - lm_mtd if is_pct else (mtd - lm_mtd) / lm_mtd
    else:
        row["mom_mtd"] = None

    plan_mtd = row["plan_mtd"]
    if mtd is not None and plan_mtd is not None and plan_mtd != 0:
        row["vs_planning_mtd"] = mtd - plan_mtd if is_pct else (mtd - plan_mtd) / plan_mtd
    else:
        row["vs_planning_mtd"] = None


# ── RENDER TOP METRIC CARDS ───────────────────────────────────────────────────
request_mtd = metric_snapshot(raw_df, METRIC_ROWS["request"])
demand_mtd = metric_snapshot(raw_df, METRIC_ROWS["demand"])
active_latest_date, active_latest_value = latest_available(daily_series(raw_df, METRIC_ROWS["active_actual"]))
productivity_mtd = metric_snapshot(raw_df, METRIC_ROWS["productivity"])

cols = st.columns(4)
cols[0].markdown(
    metric_card(
        "Requests MTD",
        format_number(request_mtd["mtd"]),
        delta_html(request_mtd["mtd"], request_mtd["lm"]),
        f"LM: {format_number(request_mtd['lm'])}",
    ),
    unsafe_allow_html=True,
)
cols[1].markdown(
    metric_card(
        "Demand MTD (Complete)",
        format_number(demand_mtd["mtd"]),
        delta_html(demand_mtd["mtd"], demand_mtd["lm"]),
        f"LM: {format_number(demand_mtd['lm'])}",
    ),
    unsafe_allow_html=True,
)
cols[2].markdown(
    metric_card(
        "Active Drivers",
        format_number(cockpit["Active"]["yesterday"]),
        delta_html(cockpit["Active"]["yesterday"], cockpit["Active"]["last_week"]),
        f"Last Week: {format_number(cockpit['Active']['last_week'])}",
    ),
    unsafe_allow_html=True,
)
cols[3].markdown(
    metric_card(
        "Productivity MTD",
        format_number(productivity_mtd["mtd"], 2),
        delta_html(productivity_mtd["mtd"], productivity_mtd["lm"]),
        f"LM: {format_number(productivity_mtd['lm'], 2)}",
    ),
    unsafe_allow_html=True,
)


# ── RENDER OPS COCKPIT GRID ───────────────────────────────────────────────────
st.markdown("<div class='section-header'>🎛️ Daily Operating Cockpit (SGN)</div>", unsafe_allow_html=True)


def get_cell_html(row, col_key, format_type, is_delta=False):
    val_to_format = row.get(col_key)
    if val_to_format is None:
        return "<td class='val-neutral'>—</td>"

    if is_delta:
        is_pct_metric = row.get("is_percent")
        if is_pct_metric:
            color = "val-positive" if val_to_format >= 0 else "val-negative"
            return f"<td class='{color}'>{val_to_format:+.2%}</td>"
        else:
            color = "val-positive" if val_to_format >= 0 else "val-negative"
            return f"<td class='{color}'>{val_to_format:+.2%}</td>"

    if format_type == "percent":
        return f"<td>{val_to_format:.2%}</td>"
    elif format_type == "decimal":
        if col_key == "today":
            return f"<td class='val-planning-today'>{val_to_format:.2f}</td>"
        return f"<td>{val_to_format:.2f}</td>"
    else:
        if col_key == "today":
            return f"<td class='val-planning-today'>{val_to_format:,.0f}</td>"
        return f"<td>{val_to_format:,.0f}</td>"


# Build HTML Table
html_table = f"""
<div class="cockpit-table-container">
    <table class="cockpit-table">
        <thead>
            <tr>
                <th>SGN</th>
                <th class="hdr-actual-current">yesterday<br>{date_yesterday.strftime('%d-%b')}</th>
                <th class="hdr-actual-past">last week<br>{date_last_week.strftime('%d-%b')}</th>
                <th class="hdr-plan">planning<br>{date_yesterday.strftime('%d-%b')}</th>
                <th class="hdr-today">today<br>{date_today.strftime('%d-%b')}</th>
                <th class="hdr-actual-past">WoW</th>
                <th class="hdr-plan">vs planning</th>
                <th class="hdr-actual-current">MTD<br>Jun-2026</th>
                <th class="hdr-actual-past">LM (Whole)<br>May-2026</th>
                <th class="hdr-actual-past">LM (MTD)<br>1-{date_yesterday.strftime('%d')} May</th>
                <th class="hdr-plan">planning<br>Jun-2026</th>
                <th class="hdr-actual-current">MoM (Whole)</th>
                <th class="hdr-actual-current">MoM (MTD)</th>
                <th class="hdr-plan">vs planning MTD</th>
            </tr>
        </thead>
        <tbody>
"""

cockpit_rows_order = [
    # Label, key, parent_key (for styling)
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
    td_class = "" if parent is None else "class='sub-row-header'"
    
    html_table += f"<tr class='{tr_class}'>"
    html_table += f"<td {td_class}>{label}</td>"
    html_table += get_cell_html(row, "yesterday", fmt)
    html_table += get_cell_html(row, "last_week", fmt)
    html_table += get_cell_html(row, "planning", fmt)
    html_table += get_cell_html(row, "today", fmt)
    html_table += get_cell_html(row, "wow", fmt, is_delta=True)
    html_table += get_cell_html(row, "vs_planning", fmt, is_delta=True)
    html_table += get_cell_html(row, "mtd", fmt)
    html_table += get_cell_html(row, "lm", fmt)
    html_table += get_cell_html(row, "lm_mtd", fmt)
    html_table += get_cell_html(row, "plan_mtd", fmt)
    html_table += get_cell_html(row, "mom_whole", fmt, is_delta=True)
    html_table += get_cell_html(row, "mom_mtd", fmt, is_delta=True)
    html_table += get_cell_html(row, "vs_planning_mtd", fmt, is_delta=True)
    html_table += "</tr>"

html_table += """
        </tbody>
    </table>
</div>
"""

st.markdown(html_table, unsafe_allow_html=True)


# ── CHARTS CONTAINER WITH DYNAMIC DATES & SMOOTH CURVES ───────────────────────
st.markdown("<div class='section-header'>📊 Visual Analytics & Performance Trends</div>", unsafe_allow_html=True)

request_series = process_series(daily_series(raw_df, METRIC_ROWS["request"]), start_date, end_date, time_granularity)
demand_series = process_series(daily_series(raw_df, METRIC_ROWS["demand"]), start_date, end_date, time_granularity)

col_chart_left, col_chart_right = st.columns([2, 1])

with col_chart_left:
    volume_tab, channel_tab = st.tabs(["Request vs Demand", "Channel Breakdown"])
    with volume_tab:
        render_line_chart(
            {"Request": request_series, "Demand": demand_series},
            f"{time_granularity} Request vs Demand ({start_date.strftime('%d-%b')} to {end_date.strftime('%d-%b')})",
            {"Request": "#FF7F32", "Demand": "#38BDF8"},
        )

    with channel_tab:
        stacked_channels = st.checkbox("Stack channel bars", value=True)
        channel_data = {
            channel: process_series(daily_series(raw_df, CHANNEL_ROWS[channel]), start_date, end_date, time_granularity)
            for channel in selected_channels
        }
        if channel_data:
            render_bar_chart(
                channel_data,
                "Daily Request by Channel",
                {
                    "GHN": "#38BDF8",
                    "KA": "#FF7F32",
                    "MP": "#10B981",
                    "SME": "#6366F1",
                    "TRUCK": "#94A3B8",
                    "WH": "#F59E0B",
                },
                stacked=stacked_channels,
            )
        else:
            st.info("Chọn ít nhất một channel để hiển thị chart.")

    # Driver Supply Segment Chart
    segment_colors = {
        "FT": "#38BDF8",
        "PT": "#FF7F32",
        "NLM": "#10B981",
        "Return": "#6366F1",
        "NIM": "#EF4444",
    }
    segment_data = {
        segment: process_series(daily_series(raw_df, SEGMENT_ROWS[segment]), start_date, end_date, time_granularity, agg_type="mean")
        for segment in selected_segments
    }
    if segment_data:
        render_line_chart(
            segment_data, 
            f"{time_granularity} Active Drivers by Segment", 
            segment_colors
        )
    else:
        st.info("Chọn ít nhất một driver segment để hiển thị chart.")

with col_chart_right:
    # ── LEADERBOARD: TOP 3 DAYS (ACTUAL REQUEST) ──────────────────────────────
    leaderboard_req = []
    for col_idx in mtd_cols:
        d_val = parse_sheet_date(safe_cell(raw_df, 4, col_idx))
        val_req = parse_value(safe_cell(raw_df, 21, col_idx))
        if d_val is not None and val_req is not None and val_req > 0:
            leaderboard_req.append((d_val, val_req))
    leaderboard_req.sort(key=lambda x: x[1], reverse=True)
    
    req_rows_html = ""
    for rank, (d, v) in enumerate(leaderboard_req[:3]):
        req_rows_html += f"""<div class="leaderboard-row rank-{rank+1}">
<div class="rank-badge">Top {rank+1} &nbsp;&nbsp; {d.strftime('%d-%b')}</div>
<div style="font-weight:700;">{v:,.0f} reqs</div>
</div>"""
        
    st.markdown(
        f"""<div class='leaderboard-card'>
<div class='leaderboard-title'>🏆 Leaderboard - Top 3 ngày Actual Request SGN</div>
{req_rows_html}
</div>""",
        unsafe_allow_html=True
    )

    # ── LEADERBOARD: TOP 3 DAYS (ACTUAL DEMAND) ───────────────────────────────
    leaderboard_dem = []
    for col_idx in mtd_cols:
        d_val = parse_sheet_date(safe_cell(raw_df, 4, col_idx))
        val_dem = parse_value(safe_cell(raw_df, 28, col_idx))
        if d_val is not None and val_dem is not None and val_dem > 0:
            leaderboard_dem.append((d_val, val_dem))
    leaderboard_dem.sort(key=lambda x: x[1], reverse=True)
    
    dem_rows_html = ""
    for rank, (d, v) in enumerate(leaderboard_dem[:3]):
        dem_rows_html += f"""<div class="leaderboard-row rank-{rank+1}">
<div class="rank-badge">Top {rank+1} &nbsp;&nbsp; {d.strftime('%d-%b')}</div>
<div style="font-weight:700;">{v:,.0f} orders</div>
</div>"""
        
    st.markdown(
        f"""<div class='leaderboard-card'>
<div class='leaderboard-title'>🏆 Leaderboard - Top 3 ngày Actual Demand SGN</div>
{dem_rows_html}
</div>""",
        unsafe_allow_html=True
    )

    # ── ACCURACY TABLE: DAYS IN METRIC ACCURACY ────────────────────────────────
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
                # Proportional forecast based on SGN Forecast Request (Row 5)
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
</tr>"""
        
    st.markdown(
        f"""<div class='leaderboard-card'>
<div class='leaderboard-title'>🎯 Số ngày các chỉ số đạt % FC SGN</div>
<table style='width:100%; font-size:0.78rem; border-collapse:collapse; color:#F8FAFC;'>
<thead>
<tr style='border-bottom:1px solid #334155; text-align:left; color:#94A3B8;'>
<th style='padding:0.4rem;'>Metric</th>
<th style='padding:0.4rem;'>Target</th>
<th style='padding:0.4rem; text-align:center;'>Pass</th>
<th style='padding:0.4rem; text-align:center;'>%</th>
<th style='padding:0.4rem; text-align:center;'>Under</th>
<th style='padding:0.4rem; text-align:center;'>Over</th>
</tr>
</thead>
<tbody>
{accuracy_rows_html}
</tbody>
</table>
</div>""",
        unsafe_allow_html=True
    )


# ── FOOTER NOTE ───────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="footer-note">
        Source: <a href="{SHEET_URL}" target="_blank">Google Sheet — SGN Overview</a> ·
        Last fetched: {fetched_at} · Cache TTL: {CACHE_TTL_SECONDS // 60} phút ·
        Built for Ahamove Driver Management SGN Ops cockpit.
    </div>
    """,
    unsafe_allow_html=True,
)
