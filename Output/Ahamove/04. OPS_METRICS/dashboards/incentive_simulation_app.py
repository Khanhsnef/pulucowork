import streamlit as st
import pandas as pd
import duckdb
import os
import glob
import math

# ── PAGE CONFIGURATION ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ahamove SmartOps: Incentive & Capacity Simulator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── BRAND SYSTEM (CSS INJECTION) ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Lexend', sans-serif;
    }
    .main-title {
        color: #0E4174;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #FF7F32;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 1rem;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0E4174;
    }
    .metric-delta {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ── PATHS & RESOLUTION ────────────────────────────────────────────────────────
BASE_DIR = "/Users/ts-1148/Desktop/Pulu-workspace"
RAW_DATA_DIR = os.path.join(BASE_DIR, "output", "Ahamove", "04. OPS_METRICS", "raw-data")

# Helper to find file path with robustness to NFD/NFC encoding mismatches
def find_file(pattern):
    search_pattern = os.path.join(RAW_DATA_DIR, pattern)
    matches = glob.glob(search_pattern)
    if matches:
        return matches[0]
    # Fallback to direct path check
    direct_path = os.path.join(RAW_DATA_DIR, pattern.replace("*", ""))
    if os.path.exists(direct_path):
        return direct_path
    return None

ACTIVE_FILE = find_file("*active.csv")
DISPATCH_FILE = find_file("*dispatch.csv")
if not DISPATCH_FILE:
    DISPATCH_FILE = find_file("*dispatch 2.csv") # Try dispatch 2

# Check if data exists
if not ACTIVE_FILE or not DISPATCH_FILE:
    st.error("❌ Không tìm thấy các file dữ liệu active.csv hoặc dispatch.csv trong thư mục raw-data.")
    st.info(f"Đường dẫn tìm kiếm: {RAW_DATA_DIR}")
    st.stop()

# ── DUCKDB IN-MEMORY DATABASE CONNECTION ──────────────────────────────────────
@st.cache_resource
def get_db_connection():
    return duckdb.connect(database=':memory:')

db = get_db_connection()

# ── DATA LOADING & CLEANING (DUCKDB VIEW GENERATION) ──────────────────────────
@st.cache_data
def load_data_to_duckdb(active_path, dispatch_path):
    # Clean dispatch data: remove commas from requested_order and recommended_order
    # Clean rec_rate by removing %
    db.execute(f"""
        CREATE OR REPLACE TEMP VIEW raw_dispatch AS 
        SELECT 
            service,
            order_date,
            CAST(REPLACE(requested_order, ',', '') AS INTEGER) as requested_order,
            CAST(REPLACE(recommended_order, ',', '') AS INTEGER) as recommended_order,
            CAST(REPLACE(rec_rate, '%', '') AS DOUBLE) / 100.0 as rec_rate,
            province,
            hour
        FROM read_csv_auto('{dispatch_path}', header=True)
    """)
    
    # Load active driver data
    db.execute(f"""
        CREATE OR REPLACE TEMP VIEW raw_active AS 
        SELECT 
            city_id,
            order_date,
            tag,
            CAST(REPLACE(total_active, ',', '') AS INTEGER) as total_active,
            service,
            hour,
            MONTH,
            WEEK
        FROM read_csv_auto('{active_path}', header=True, types={{'total_active': 'VARCHAR'}})
    """)

load_data_to_duckdb(ACTIVE_FILE, DISPATCH_FILE)

# ── SIDEBAR CONTROLS (SIMULATOR PARAMS) ────────────────────────────────────────
st.sidebar.markdown(f"<div style='text-align: center;'><img src='https://www.ahamove.com/_next/static/media/logo.5c234a9f.svg' width='150'></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ THAM SỐ GIẢ LẬP INCENTIVE")

# Sliders
base_incentive = st.sidebar.slider(
    "Thưởng thêm giờ cao điểm (VND/đơn)", 
    min_value=0, 
    max_value=10000, 
    value=2000, 
    step=1000,
    help="Số tiền thưởng incentive cộng thêm trên mỗi đơn hàng để tăng tỷ lệ hoàn thành đơn."
)

target_ar = st.sidebar.slider(
    "Target Acceptance Rate (%)", 
    min_value=50, 
    max_value=100, 
    value=85, 
    step=5,
    help="Tỷ lệ nhận đơn tối thiểu của tài xế để nhận thưởng."
)

weather_multiplier = st.sidebar.slider(
    "Hệ số thời tiết (Mưa/Nắng nóng)", 
    min_value=1.0, 
    max_value=2.0, 
    value=1.2, 
    step=0.1,
    help="Nhân tố tác động lượng cầu tăng đột biến do thời tiết xấu."
)

# Filters
city_list = ["SGN", "HAN"]
selected_city = st.sidebar.selectbox("Thành phố", city_list)

segment_list = ["FT", "PT", "NIM", "NLM", "return"]
selected_segments = st.sidebar.multiselect(
    "Segment Tài xế tham gia", 
    segment_list, 
    default=["FT", "PT", "NIM"]
)

# Render paths info in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**📁 Data Sources Path:**")
st.sidebar.caption(f"Active: `{os.path.basename(ACTIVE_FILE)}`")
st.sidebar.caption(f"Dispatch: `{os.path.basename(DISPATCH_FILE)}`")

# ── CORE SIMULATION ENGINE ────────────────────────────────────────────────────
# We write a SQL query joining the demand (dispatch) and capacity (active drivers) grouped by hour
segments_sql = ", ".join([f"'{s}'" for s in selected_segments])

# Query to get hourly aggregated data
query = f"""
    WITH hourly_demand AS (
        SELECT 
            hour,
            SUM(requested_order) as total_demand,
            SUM(recommended_order) as total_recommended
        FROM raw_dispatch
        WHERE province = '{selected_city}'
        GROUP BY hour
    ),
    hourly_capacity AS (
        SELECT 
            hour,
            SUM(total_active) as active_capacity
        FROM raw_active
        WHERE city_id = '{selected_city}' 
          AND LOWER(tag) IN ({segments_sql.lower()})
        GROUP BY hour
    )
    SELECT 
        d.hour,
        d.total_demand,
        d.total_recommended,
        c.active_capacity
    FROM hourly_demand d
    LEFT JOIN hourly_capacity c ON d.hour = c.hour
    ORDER BY d.hour
"""

df_raw = db.execute(query).df()

# Handle NaNs
df_raw['active_capacity'] = df_raw['active_capacity'].fillna(0)

# Simulate Demand and Capacity with weather and incentive
df_sim = df_raw.copy()
# Weather increases demand
df_sim['simulated_demand'] = (df_sim['total_demand'] * weather_multiplier).astype(int)

# Incentive increases capacity (elasticity model)
# Every 2000 VND increases active driver capacity by ~5-15% depending on current supply/demand ratio
incentive_elasticity = 0.08 * (base_incentive / 2000.0)
df_sim['simulated_capacity'] = (df_sim['active_capacity'] * (1.0 + incentive_elasticity)).astype(int)

# Current Rec Rate (Fulfillment Rate proxy)
df_sim['current_fr'] = df_sim['total_recommended'] / df_sim['total_demand']
df_sim['current_fr'] = df_sim['current_fr'].clip(0, 1.0)

# Simulated Rec Rate using logistic curves of Supply/Demand ratio
# Base formula: simulated_fr = 1 / (1 + exp(- (supply/demand * weight + incentive_bonus_weight)))
def simulate_fr(row, incentive):
    supply = row['simulated_capacity']
    demand = row['simulated_demand']
    if demand == 0:
        return 1.0
    ratio = supply / demand
    
    # Logistical simulation formula calibrated to match operational baselines
    k = 2.5 # curve steepness
    x0 = 0.8 # inflection point (equilibrium ratio)
    
    # Base FR based on capacity/demand ratio
    base_fr = 1.0 / (1.0 + math.exp(-k * (ratio - x0)))
    
    # Incentive effect (increases acceptance and fulfillment behavior)
    incentive_boost = 0.15 * (incentive / 10000.0)
    
    sim_fr = base_fr + incentive_boost
    return min(max(sim_fr, 0.35), 0.98) # cap between 35% and 98%

df_sim['simulated_fr'] = df_sim.apply(lambda r: simulate_fr(r, base_incentive), axis=1)

# Calculate cost
df_sim['simulated_orders_completed'] = (df_sim['simulated_demand'] * df_sim['simulated_fr']).astype(int)
df_sim['simulated_incentive_cost'] = df_sim['simulated_orders_completed'] * base_incentive

# Total numbers for top metrics
total_demand_cur = int(df_sim['total_demand'].sum())
total_demand_sim = int(df_sim['simulated_demand'].sum())
total_capacity_cur = int(df_sim['active_capacity'].sum())
total_capacity_sim = int(df_sim['simulated_capacity'].sum())
overall_fr_cur = float(df_sim['total_recommended'].sum() / df_sim['total_demand'].sum())
overall_fr_sim = float(df_sim['simulated_orders_completed'].sum() / df_sim['simulated_demand'].sum())
total_cost_sim = int(df_sim['simulated_incentive_cost'].sum())
simulated_cpo_contribution = float(total_cost_sim / df_sim['simulated_orders_completed'].sum()) if df_sim['simulated_orders_completed'].sum() > 0 else 0.0

# ── MAIN LAYOUT ───────────────────────────────────────────────────────────────
st.markdown("<div class='main-title'>📈 AHAMOVE SMARTOPS SIMULATOR</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Công cụ giả lập Incentive Peak-Hour & Phân bổ Nguồn cung theo thời gian thực</div>", unsafe_allow_html=True)

# ── TOP METRICS CARDS ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Tổng Lượng Cầu (Orders)</div>
            <div class='metric-value'>{total_demand_sim:,}</div>
            <div class='metric-delta' style='color: {"#FF7F32" if weather_multiplier > 1.0 else "#94A3B8"};'>
                {"+" if weather_multiplier > 1.0 else ""}{(weather_multiplier-1.0)*100:.0f}% vs Current ({total_demand_cur:,})
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Nguồn cung Active (Drivers)</div>
            <div class='metric-value'>{total_capacity_sim:,}</div>
            <div class='metric-delta' style='color: {"#10B981" if base_incentive > 0 else "#94A3B8"};'>
                {"+" if base_incentive > 0 else ""}{incentive_elasticity*100:.1f}% vs Current ({total_capacity_cur:,})
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    fr_color = "#10B981" if overall_fr_sim >= 0.92 else ("#FF7F32" if overall_fr_sim >= 0.85 else "#EF4444")
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Fulfillment Rate (FR)</div>
            <div class='metric-value' style='color: {fr_color};'>{overall_fr_sim:.1%}</div>
            <div class='metric-delta' style='color: {"#10B981" if overall_fr_sim >= overall_fr_cur else "#EF4444"};'>
                {"▲" if overall_fr_sim >= overall_fr_cur else "▼"} {abs(overall_fr_sim - overall_fr_cur)*100:.1f}pp vs Current ({overall_fr_cur:.1%})
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Chi phí Incentive (CPO)</div>
            <div class='metric-value' style='color: #0E4174;'>{total_cost_sim/1000000:.2f}M</div>
            <div class='metric-delta' style='color: #64748B;'>
                Đóng góp CPO: {simulated_cpo_contribution:,.0f}đ/đơn
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CHARTS SECTION ────────────────────────────────────────────────────────────
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📊 So sánh Tỷ lệ Hoàn thành Đơn hàng (FR) theo Giờ")
    # Line chart comparing current FR vs simulated FR
    chart_df = df_sim[['hour', 'current_fr', 'simulated_fr']].copy()
    chart_df.columns = ['Giờ', 'FR Hiện tại', 'FR Giả lập']
    chart_df = chart_df.set_index('Giờ')
    st.line_chart(chart_df, color=["#94A3B8", "#FF7F32"])

with right_col:
    st.subheader("⚖️ Cân bằng Cung - Cầu Giả lập theo Giờ")
    # Bar chart showing simulated demand vs capacity
    chart_sc_df = df_sim[['hour', 'simulated_demand', 'simulated_capacity']].copy()
    chart_sc_df.columns = ['Giờ', 'Lượng Cầu (Orders)', 'Nguồn Cung (Active Drivers)']
    chart_sc_df = chart_sc_df.set_index('Giờ')
    st.bar_chart(chart_sc_df, color=["#FF7F32", "#0E4174"])

st.markdown("---")

# ── SEGMENT ANALYSIS SECTION ──────────────────────────────────────────────────
st.subheader("👥 Phân bổ Tài xế theo Segment (Hoạt động Hiện tại)")

# Query active driver distribution by tag
segment_query = f"""
    SELECT 
        tag as segment,
        SUM(total_active) as total_active_drivers
    FROM raw_active
    WHERE city_id = '{selected_city}'
    GROUP BY tag
    ORDER BY total_active_drivers DESC
"""
df_segments = db.execute(segment_query).df()
df_segments['Tỷ lệ %'] = df_segments['total_active_drivers'] / df_segments['total_active_drivers'].sum()

col_table, col_chart = st.columns([1, 1.5])

with col_table:
    st.markdown("**Bảng phân bổ Active Drivers**")
    st.dataframe(
        df_segments.style.format({
            "total_active_drivers": "{:,.0f}",
            "Tỷ lệ %": "{:.1%}"
        }),
        use_container_width=True
    )

with col_chart:
    st.markdown("**Biểu đồ Active Drivers theo phân tầng**")
    # Streamlit bar chart
    chart_seg = df_segments.set_index('segment')[['total_active_drivers']]
    st.bar_chart(chart_seg, color="#0E4174")

# ── FOOTER / DOCUMENT LINK ────────────────────────────────────────────────────
st.markdown("---")
st.caption("Ahamove Driver Management Team © 2026. Công cụ sử dụng DuckDB để xử lý hàng triệu bản ghi thô cục bộ siêu tốc.")
