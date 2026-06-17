import io
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

try:
    import plotly.graph_objects as go
except ImportError:  # pragma: no cover - Streamlit fallback if Plotly is unavailable
    go = None


# ── PAGE CONFIGURATION ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SGN Ops Overview — Ahamove",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── BRAND SYSTEM (CSS INJECTION) ──────────────────────────────────────────────
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Lexend', sans-serif;
        background-color: #F9FAFB;
    }
    .main-title {
        color: #0E4174;
        font-weight: 800;
        font-size: 2.6rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.04em;
    }
    .subtitle {
        color: #64748B;
        font-weight: 500;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .section-header {
        color: #0E4174;
        font-weight: 800;
        font-size: 1.35rem;
        border-left: 6px solid #FF7F32;
        padding-left: 0.8rem;
        margin: 1.4rem 0 0.8rem 0;
        letter-spacing: -0.02em;
    }
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 1.5rem;
        padding: 1.2rem;
        box-shadow: 0 10px 24px -18px rgba(14, 65, 116, 0.35);
        text-align: center;
        min-height: 142px;
    }
    .metric-label {
        font-size: 0.78rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 0.35rem;
        letter-spacing: 0.04em;
    }
    .metric-value {
        font-size: 2.05rem;
        font-weight: 800;
        color: #0E4174;
        letter-spacing: -0.05em;
    }
    .metric-delta {
        font-size: 0.88rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }
    .metric-context {
        color: #94A3B8;
        font-size: 0.78rem;
        margin-top: 0.15rem;
    }
    .status-pill {
        display: inline-block;
        background: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        border-radius: 999px;
        padding: 0.25rem 0.7rem;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .footer-note {
        color: #64748B;
        font-size: 0.82rem;
        padding-top: 1rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 2rem;
    }
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
    "request": 5,
    "demand": 13,
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


def format_percent(value, decimals=0):
    if value is None or pd.isna(value):
        return "—"
    if abs(value) > 1.5:
        value = value / 100
    return f"{value:.{decimals}%}"


def delta_html(current, baseline, percent=False):
    if current is None or baseline is None or baseline == 0:
        return "<span style='color:#94A3B8'>No baseline</span>"
    delta = current - baseline
    delta_pct = delta / abs(baseline)
    color = "#10B981" if delta >= 0 else "#EF4444"
    arrow = "▲" if delta >= 0 else "▼"
    if percent:
        label = f"{arrow} {delta:+.1%} vs LM"
    else:
        label = f"{arrow} {delta_pct:+.1%} vs LM"
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


def filter_series(series, start_date, end_date):
    if series.empty:
        return series
    return series[(series.index >= pd.Timestamp(start_date)) & (series.index <= pd.Timestamp(end_date))]


def chart_layout(fig, title=""):
    fig.update_layout(
        title=title,
        font={"family": "Lexend, sans-serif", "color": "#0F172A"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
        hovermode="x unified",
    )
    fig.update_xaxes(showgrid=False, linecolor="#E2E8F0")
    fig.update_yaxes(gridcolor="#E2E8F0", zerolinecolor="#E2E8F0")
    return fig


def render_line_chart(data, title, colors):
    if go is None:
        st.line_chart(pd.DataFrame(data))
        return

    fig = go.Figure()
    for label, series in data.items():
        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series.values,
                mode="lines+markers",
                name=label,
                line={"width": 3, "color": colors.get(label, "#0E4174")},
                marker={"size": 6},
            )
        )
    st.plotly_chart(chart_layout(fig, title), use_container_width=True)


def render_bar_chart(data, title, colors, stacked=False):
    if go is None:
        st.bar_chart(pd.DataFrame(data))
        return

    fig = go.Figure()
    for label, series in data.items():
        fig.add_trace(
            go.Bar(
                x=series.index,
                y=series.values,
                name=label,
                marker_color=colors.get(label, "#0E4174"),
            )
        )
    fig.update_layout(barmode="stack" if stacked else "group")
    st.plotly_chart(chart_layout(fig, title), use_container_width=True)


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
    "<div style='text-align: center;'><img src='https://www.ahamove.com/_next/static/media/logo.5c234a9f.svg' width='150'></div>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Bộ lọc Dashboard")
st.sidebar.markdown("<span class='status-pill'>Live Google Sheet</span>", unsafe_allow_html=True)
st.sidebar.caption(f"Last fetched: {fetched_at}")

if st.sidebar.button("🔄 Refresh data"):
    st.cache_data.clear()
    st.rerun()

selected_range = st.sidebar.date_input(
    "Date range",
    value=(min_date.date(), max_date.date()),
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

request = metric_snapshot(raw_df, METRIC_ROWS["request"])
demand = metric_snapshot(raw_df, METRIC_ROWS["demand"])
active = metric_snapshot(raw_df, METRIC_ROWS["active_actual"])
productivity = metric_snapshot(raw_df, METRIC_ROWS["productivity"])
active_latest_date, active_latest_value = latest_available(daily_series(raw_df, METRIC_ROWS["active_actual"]))

cols = st.columns(4)
cols[0].markdown(
    metric_card(
        "Requests MTD",
        format_number(request["mtd"]),
        delta_html(request["mtd"], request["lm"]),
        f"LM: {format_number(request['lm'])}",
    ),
    unsafe_allow_html=True,
)
cols[1].markdown(
    metric_card(
        "Demand MTD",
        format_number(demand["mtd"]),
        delta_html(demand["mtd"], demand["lm"]),
        f"LM: {format_number(demand['lm'])}",
    ),
    unsafe_allow_html=True,
)
cols[2].markdown(
    metric_card(
        "Active Drivers",
        format_number(active_latest_value),
        delta_html(active_latest_value, active["lm"]),
        f"Latest: {active_latest_date.strftime('%d-%b') if active_latest_date is not None else '—'}",
    ),
    unsafe_allow_html=True,
)
cols[3].markdown(
    metric_card(
        "Productivity",
        format_number(productivity["mtd"], 2),
        delta_html(productivity["mtd"], productivity["lm"]),
        f"LM: {format_number(productivity['lm'], 2)}",
    ),
    unsafe_allow_html=True,
)

# ── ORDER VOLUME TRENDS ──────────────────────────────────────────────────────
st.markdown("<div class='section-header'>1. Order Volume Trends</div>", unsafe_allow_html=True)
request_series = filter_series(daily_series(raw_df, METRIC_ROWS["request"]), start_date, end_date)
demand_series = filter_series(daily_series(raw_df, METRIC_ROWS["demand"]), start_date, end_date)

volume_tab, channel_tab = st.tabs(["Request vs Demand", "Channel Breakdown"])
with volume_tab:
    render_line_chart(
        {"Request": request_series, "Demand": demand_series},
        "Daily Request vs Demand",
        {"Request": "#FF7F32", "Demand": "#0E4174"},
    )

with channel_tab:
    stacked_channels = st.checkbox("Stack channel bars", value=True)
    channel_data = {
        channel: filter_series(daily_series(raw_df, CHANNEL_ROWS[channel]), start_date, end_date)
        for channel in selected_channels
    }
    if channel_data:
        render_bar_chart(
            channel_data,
            "Daily Request by Channel",
            {
                "GHN": "#0E4174",
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

# ── DRIVER SUPPLY METRICS ────────────────────────────────────────────────────
st.markdown("<div class='section-header'>2. Driver Supply Metrics</div>", unsafe_allow_html=True)
segment_colors = {
    "FT": "#0E4174",
    "PT": "#FF7F32",
    "NLM": "#10B981",
    "Return": "#6366F1",
    "NIM": "#EF4444",
}
segment_data = {
    segment: filter_series(daily_series(raw_df, SEGMENT_ROWS[segment]), start_date, end_date)
    for segment in selected_segments
}
left_col, right_col = st.columns([1.55, 1])
with left_col:
    if segment_data:
        render_line_chart(segment_data, "Active Drivers by Segment", segment_colors)
    else:
        st.info("Chọn ít nhất một driver segment để hiển thị chart.")

with right_col:
    snapshot_rows = []
    for segment, row_idx in SEGMENT_ROWS.items():
        latest_date, latest_value = latest_available(daily_series(raw_df, row_idx))
        snapshot = metric_snapshot(raw_df, row_idx)
        snapshot_rows.append(
            {
                "Segment": segment,
                "Latest Active": latest_value,
                "Latest Date": latest_date.strftime("%d-%b") if latest_date is not None else "—",
                "LM": snapshot["lm"],
                "MTD": snapshot["mtd"],
            }
        )
    snapshot_df = pd.DataFrame(snapshot_rows)
    st.markdown("**Latest Active Snapshot**")
    st.dataframe(
        snapshot_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Latest Active": st.column_config.NumberColumn(format="%,.0f"),
            "LM": st.column_config.NumberColumn(format="%,.0f"),
            "MTD": st.column_config.NumberColumn(format="%,.0f"),
        },
    )

# ── EFFICIENCY METRICS ───────────────────────────────────────────────────────
st.markdown("<div class='section-header'>3. Efficiency Metrics</div>", unsafe_allow_html=True)
online_per_driver = metric_snapshot(raw_df, METRIC_ROWS["online_per_driver"])
prod_per_online_hour = metric_snapshot(raw_df, METRIC_ROWS["prod_per_online_hour"])
capacity = metric_snapshot(raw_df, METRIC_ROWS["capacity"])

eff_cols = st.columns(4)
eff_cols[0].markdown(
    metric_card(
        "Capacity MTD",
        format_number(capacity["mtd"]),
        delta_html(capacity["mtd"], capacity["lm"]),
        f"LM: {format_number(capacity['lm'])}",
    ),
    unsafe_allow_html=True,
)
eff_cols[1].markdown(
    metric_card(
        "Productivity",
        format_number(productivity["mtd"], 2),
        delta_html(productivity["mtd"], productivity["lm"]),
        "orders / driver / day",
    ),
    unsafe_allow_html=True,
)
eff_cols[2].markdown(
    metric_card(
        "Online / Driver",
        format_number(online_per_driver["mtd"], 2),
        delta_html(online_per_driver["mtd"], online_per_driver["lm"]),
        "hours / driver",
    ),
    unsafe_allow_html=True,
)
eff_cols[3].markdown(
    metric_card(
        "Prod / Online Hour",
        format_number(prod_per_online_hour["mtd"], 2),
        delta_html(prod_per_online_hour["mtd"], prod_per_online_hour["lm"]),
        "orders / online hour",
    ),
    unsafe_allow_html=True,
)

# ── ACHIEVEMENT RATES ────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>4. Forecast Achievement</div>", unsafe_allow_html=True)

def achievement_table(row_map):
    records = []
    for channel, row_idx in row_map.items():
        snapshot = metric_snapshot(raw_df, row_idx)
        value = snapshot["mtd"]
        if value is None:
            status = "No data"
        elif value >= 0.95:
            status = "🟢 On track"
        elif value >= 0.85:
            status = "🟠 Watch"
        else:
            status = "🔴 Gap"
        records.append({"Channel": channel, "MTD Achievement": value, "Status": status})
    return pd.DataFrame(records)

with st.expander("Tỷ lệ đạt FC — % Request & % Demand", expanded=True):
    req_ach, demand_ach = st.columns(2)
    with req_ach:
        st.markdown("**% Request Achievement**")
        st.dataframe(
            achievement_table(ACHIEVEMENT_REQUEST_ROWS),
            use_container_width=True,
            hide_index=True,
            column_config={"MTD Achievement": st.column_config.NumberColumn(format="%.1f%%")},
        )
    with demand_ach:
        st.markdown("**% Demand Achievement**")
        st.dataframe(
            achievement_table(ACHIEVEMENT_DEMAND_ROWS),
            use_container_width=True,
            hide_index=True,
            column_config={"MTD Achievement": st.column_config.NumberColumn(format="%.1f%%")},
        )

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
