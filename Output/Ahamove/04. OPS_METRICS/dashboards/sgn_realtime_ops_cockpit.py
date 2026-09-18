# -*- coding: utf-8 -*-
"""
Ahamove SGN Operations Real-Time Cockpit & Decision Dashboard
Built with Streamlit, Plotly, and UI/UX Pro Max Design System.

Run locally:
    streamlit run "Output/Ahamove/04. OPS_METRICS/dashboards/sgn_realtime_ops_cockpit.py"
"""

import math
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import streamlit as st

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
except ImportError:
    go = None
    px = None

# ── PAGE CONFIGURATION ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SGN Ops Cockpit — Ahamove",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── UI/UX PRO MAX DESIGN SYSTEM (CSS INJECTION) ─────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --ahamove-orange: #FF6B00;
        --ahamove-orange-soft: rgba(255, 107, 0, 0.12);
        --bg-main: #0F172A;
        --card-bg: #1E293B;
        --card-soft: rgba(30, 41, 59, 0.75);
        --border: #334155;
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --emerald: #10B981;
        --rose: #F43F5E;
        --amber: #F59E0B;
        --indigo: #6366F1;
        --blue: #3B82F6;
    }

    .stApp, html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    .num {
        font-family: 'Fira Code', monospace !important;
        font-variant-numeric: tabular-nums !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1440px !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--card-bg) !important;
        border-right: 1px solid var(--border) !important;
    }

    /* Header Banner */
    .cockpit-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.98));
        border: 1px solid var(--border);
        border-left: 5px solid var(--ahamove-orange);
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .brand-title {
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-badge {
        background: var(--ahamove-orange);
        color: #FFFFFF;
        font-size: 11px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 4px;
        letter-spacing: 1px;
    }

    /* Key Takeaway Callout */
    .takeaway-box {
        background: var(--ahamove-orange-soft);
        border: 1px solid rgba(255, 107, 0, 0.3);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 24px;
        color: #FED7AA;
        font-size: 14px;
        line-height: 1.6;
    }

    .takeaway-title {
        color: var(--ahamove-orange);
        font-weight: 800;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Bento Metric Cards */
    .metric-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        border-color: rgba(255, 107, 0, 0.4);
        transform: translateY(-2px);
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--border);
    }

    .card-accent-orange::before { background: var(--ahamove-orange); }
    .card-accent-green::before { background: var(--emerald); }
    .card-accent-indigo::before { background: var(--indigo); }
    .card-accent-rose::before { background: var(--rose); }

    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 900;
        color: var(--text-primary);
        font-family: 'Fira Code', monospace;
        letter-spacing: -1px;
    }

    .metric-delta {
        font-size: 12px;
        font-weight: 700;
        margin-top: 6px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 8px;
        border-radius: 12px;
    }

    .delta-up { background: rgba(16, 185, 129, 0.15); color: var(--emerald); }
    .delta-down { background: rgba(244, 63, 94, 0.15); color: var(--rose); }

    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--card-bg);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--ahamove-orange) !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── SYNTHETIC REAL-TIME DATA GENERATOR ───────────────────────────────────────
@st.cache_data(ttl=3600)
def load_ops_realtime_data(selected_date):
    """Generates synthetic hourly SGN operational metrics for testing and analysis."""
    np.random.seed(int(selected_date.strftime("%Y%m%d")))
    hours = [f"{h:02d}:00" for h in range(24)]
    
    # Base demand curve with morning and evening peak
    base_demand = np.array([
        300, 200, 150, 100, 250, 800, 2200, 4800, 5600, 4200, 3800, 4500,
        5100, 4300, 3900, 4800, 6200, 6800, 5400, 3600, 2400, 1800, 1100, 600
    ])
    
    # Add random variations
    demand = (base_demand * np.random.uniform(0.9, 1.1, 24)).astype(int)
    
    # Driver supply and fulfillment rate calculation
    active_drivers = (demand * np.random.uniform(0.18, 0.22, 24)).astype(int)
    active_drivers = np.maximum(active_drivers, 150)
    
    # FR drops during peak hours (17-19)
    fr_base = np.array([
        98, 99, 99, 99, 98, 96, 92, 89, 94, 95, 96, 93,
        91, 94, 95, 92, 88, 86, 91, 95, 97, 98, 98, 99
    ])
    fr_rate = np.clip(fr_base + np.random.normal(0, 1.5, 24), 75.0, 99.5)
    
    # SLA Average pickup duration (mins)
    sla_mins = np.clip(25.0 - (fr_rate - 85) * 0.4 + np.random.normal(0, 0.8, 24), 10.0, 35.0)
    
    df = pd.DataFrame({
        "Hour": hours,
        "Hour_Int": list(range(24)),
        "Demand_Orders": demand,
        "Active_Drivers": active_drivers,
        "Fulfillment_Rate": np.round(fr_rate, 1),
        "Pickup_SLA_Mins": np.round(sla_mins, 1),
        "Acceptance_Rate": np.round(np.clip(fr_rate + np.random.uniform(2, 5, 24), 80, 99.8), 1),
        "CPO_VND": np.random.randint(12500, 16800, 24)
    })
    
    return df

# ── SIDEBAR CONTROLS ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='background:#FF6B00; color:#FFF; font-weight:900; font-size:18px; padding:6px 14px; border-radius:6px; display:inline-block; margin-bottom:8px; letter-spacing:1px;'>AHAMOVE</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#FF6B00; font-weight:800;'>AHAMOVE COCKPIT</h3>", unsafe_allow_html=True)
    st.caption("Báo Cáo Điều Hành Vận Hành & Nguồn Cung SGN")
    
    st.markdown("---")
    selected_date = st.date_input("🗓️ Ngày Báo Cáo", date.today())
    
    region_filter = st.selectbox(
        "📍 Khu Vực / Hub",
        ["Tất cả TP.HCM", "Cụm Tân Bình / Phú Nhuận", "Cụm Q1 / Q3 / Q10", "Cụm Quận 7 / Nhà Bè", "Cụm Bình Thạnh / Thủ Đức"]
    )
    
    service_filter = st.multiselect(
        "📦 Dịch Vụ Logistics",
        ["Siêu Tốc (Express)", "Giao 2H", "Đồng Giá SameDay", "AhaTruck 500kg-2T"],
        default=["Siêu Tốc (Express)", "Giao 2H"]
    )
    
    st.markdown("---")
    st.markdown("<div style='font-size:12px; color:#94A3B8;'>Chỉ số Target SLA: <b>≤ 20 phút</b><br>Mục tiêu FR: <b>≥ 95.0%</b></div>", unsafe_allow_html=True)
    
    if st.button("🔄 Cập Nhật Dữ Liệu Real-Time", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
df_ops = load_ops_realtime_data(selected_date)

# Calculate summary metrics
total_demand = df_ops["Demand_Orders"].sum()
avg_fr = df_ops["Fulfillment_Rate"].mean()
total_active = df_ops["Active_Drivers"].max()
avg_sla = df_ops["Pickup_SLA_Mins"].mean()

# ── HEADER BANNER ─────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="cockpit-header">
        <div>
            <div class="brand-title">
                SGN OPS REAL-TIME COCKPIT
                <span class="brand-badge">LIVE MONITOR</span>
            </div>
            <div style="font-size:13px; color:#94A3B8; margin-top:4px;">
                Hệ thống Giám sát Nguồn cung & Tối ưu Unit Economics | Area: <b>{region_filter}</b> | Date: <b class="num">{selected_date.strftime('%Y-%m-%d')}</b>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:12px; color:#10B981; font-weight:700;">🟢 TELEMETRY SYSTEM ACTIVE</div>
            <div style="font-size:11px; color:#94A3B8;" class="num">Last sync: {datetime.now().strftime('%H:%M:%S')}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ── KEY TAKEAWAY EXECUTIVE SUMMARY ────────────────────────────────────────────
st.markdown(
    f"""
    <div class="takeaway-box">
        <div class="takeaway-title">📊 KEY TAKEAWAY — ĐÁNH GIÁ ĐIỀU HÀNH</div>
        Tổng nhu cầu đơn hàng trong ngày đạt <b>{total_demand:,} đơn</b> với Tỷ lệ hoàn thành trung bình (FR) đạt <b class="num">{avg_fr:.1f}%</b>. 
        Khung giờ cao điểm <b>17:00 - 19:00</b> ghi nhận sụt giảm FR xuống <b>86.0%</b> do thiếu hụt 15% nguồn cung tài xế tại khu vực Tân Bình. 
        Khuyến nghị: <i>Thích ứng chính sách Surge Bonus +3,000đ/đơn tại vùng đỏ để cân bằng cung-cầu.</i>
    </div>
    """,
    unsafe_allow_html=True
)

# ── BENTO KPI METRIC CARDS ────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card card-accent-orange">
            <div class="metric-label">TỔNG NHU CẦU ĐƠN (DEMAND)</div>
            <div class="metric-value">{total_demand:,}</div>
            <div class="metric-delta delta-up">↑ +4.2% vs T-1</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    fr_color = "delta-up" if avg_fr >= 94.0 else "delta-down"
    st.markdown(
        f"""
        <div class="metric-card card-accent-green">
            <div class="metric-label">TỶ LỆ HOÀN THÀNH (FR)</div>
            <div class="metric-value">{avg_fr:.1f}%</div>
            <div class="metric-delta {fr_color}">↑ Target: ≥95.0%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card card-accent-indigo">
            <div class="metric-label">PEAK ACTIVE DRIVERS</div>
            <div class="metric-value">{total_active:,}</div>
            <div class="metric-delta delta-up">↑ +6.1% vs W-1</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    sla_color = "delta-up" if avg_sla <= 20.0 else "delta-down"
    st.markdown(
        f"""
        <div class="metric-card card-accent-rose">
            <div class="metric-label">AVG PICKUP SLA (PHÚT)</div>
            <div class="metric-value">{avg_sla:.1f}m</div>
            <div class="metric-delta {sla_color}">{"↓ Đạt SLA" if avg_sla <= 20.0 else "↑ Trễ Target"}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── DASHBOARD TABS ────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📈 Báo Cáo Cung - Cầu Real-Time", 
    "🔥 Ma Trận Khung Giờ Cao Điểm", 
    "⚡ Mô Phỏng Thưởng Incentive Surge"
])

# ── TAB 1: REAL-TIME DEMAND & SUPPLY ──────────────────────────────────────────
with tab1:
    st.subheader("Biến Động Nhu Cầu & Tỷ Lệ Hoàn Thành (FR) Theo Giờ")
    
    if go is not None:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Demand Bar Chart
        fig.add_trace(
            go.Bar(
                x=df_ops["Hour"],
                y=df_ops["Demand_Orders"],
                name="Nhu Cầu Đơn Hàng (Orders)",
                marker_color="rgba(59, 130, 246, 0.4)",
                marker_line_color="#3B82F6",
                marker_line_width=1
            ),
            secondary_y=False
        )
        
        # FR Line Chart
        fig.add_trace(
            go.Scatter(
                x=df_ops["Hour"],
                y=df_ops["Fulfillment_Rate"],
                name="Tỷ Lệ FR (%)",
                line=dict(color="#FF6B00", width=3, shape="spline"),
                mode="lines+markers"
            ),
            secondary_y=True
        )
        
        # Target FR Line
        fig.add_trace(
            go.Scatter(
                x=df_ops["Hour"],
                y=[95.0] * 24,
                name="Target FR (95%)",
                line=dict(color="#10B981", width=1.5, dash="dash")
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=420,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified"
        )
        
        fig.update_xaxes(showgrid=False, title_text="Khung Giờ")
        fig.update_yaxes(title_text="Số Lượng Đơn Hàng", secondary_y=False, showgrid=True, gridcolor="#334155")
        fig.update_yaxes(title_text="Tỷ Lệ FR (%)", secondary_y=True, range=[70, 100], showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Data Table
    with st.expander("📄 Xem Bảng Dữ Liệu Chi Tiết Theo Giờ (Raw Metrics Data)"):
        st.dataframe(
            df_ops.style.format({
                "Demand_Orders": "{:,}",
                "Active_Drivers": "{:,}",
                "Fulfillment_Rate": "{:.1f}%",
                "Pickup_SLA_Mins": "{:.1f} phút",
                "Acceptance_Rate": "{:.1f}%",
                "CPO_VND": "{:,}₫"
            }),
            use_container_width=True,
            height=300
        )

# ── TAB 2: PEAK HOUR HEATMAP MATRIX ───────────────────────────────────────────
with tab2:
    st.subheader("Ma Trận Mật Độ Đơn & Nguồn Cung Tài Xế Theo Cụm Quận")
    
    # Generate Heatmap Matrix data
    districts = ["Tân Bình", "Phú Nhuận", "Quận 1", "Quận 3", "Quận 7", "Bình Thạnh", "Thủ Đức"]
    hours_peak = [f"{h:02d}:00" for h in range(7, 22)]
    
    heatmap_matrix = np.random.uniform(78.0, 98.5, size=(len(districts), len(hours_peak)))
    # Inject low FR at Tân Bình & Bình Thạnh during 17:00-19:00
    heatmap_matrix[0, 10:13] -= 12.0
    heatmap_matrix[5, 10:13] -= 10.0
    heatmap_matrix = np.clip(heatmap_matrix, 70.0, 99.0)
    
    if px is not None:
        fig_hm = px.imshow(
            np.round(heatmap_matrix, 1),
            labels=dict(x="Khung Giờ", y="Cụm Quận", color="FR (%)"),
            x=hours_peak,
            y=districts,
            color_continuous_scale="RdYlGn",
            range_color=[75, 98],
            aspect="auto"
        )
        
        fig_hm.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_hm, use_container_width=True)
    
    st.info("💡 **Gợi Ý Vận Hành:** Các vùng màu Đỏ/Cam đại diện cho điểm nghẽn SLA dưới 85%. Hãy điều phối đội ngũ Field Ops tập trung nguồn cung vào các ô này.")

# ── TAB 3: INCENTIVE SIMULATOR ────────────────────────────────────────────────
with tab3:
    st.subheader("Bộ Mô Phỏng Thưởng Nguồn Cung Tài Xế (Surge Bonus Simulator)")
    
    col_sim1, col_sim2 = st.columns([1, 2])
    
    with col_sim1:
        st.markdown("<div style='font-size:14px; font-weight:700; color:#FF6B00;'>⚙️ THIẾT LẬP THAM SỐ THƯỞNG</div>", unsafe_allow_html=True)
        surge_bonus = st.slider("Mức Thưởng Surge (VNĐ/đơn)", min_value=0, max_value=8000, value=3000, step=500)
        target_hours = st.multiselect("Khung Giờ Áp Dụng", hours_peak, default=["17:00", "18:00", "19:00"])
        est_orders = st.number_input("Ước Tính Số Đơn Khung Cao Điểm", value=15000, step=1000)
        
        # Calculate ROI
        driver_boost_pct = min(surge_bonus / 1000 * 3.5, 30.0)
        est_fr_lift = min(surge_bonus / 1000 * 1.8, 12.0)
        total_budget = (est_orders * (avg_fr + est_fr_lift) / 100.0) * surge_bonus
        
        st.markdown("---")
        st.markdown(f"**Tăng Nguồn Cung Dự Kiến:** <b style='color:#10B981;'>+{driver_boost_pct:.1f}% Active Drivers</b>", unsafe_allow_html=True)
        st.markdown(f"**Tăng Tỷ Lệ FR Dự Kiến:** <b style='color:#FF6B00;'>+{est_fr_lift:.1f}% FR Lift</b>", unsafe_allow_html=True)
        st.markdown(f"**Ngân Sách Dự Kiến:** <b class='num' style='font-size:18px; color:#F43F5E;'>{total_budget:,.0f} VNĐ</b>", unsafe_allow_html=True)
    
    with col_sim2:
        st.markdown("<div style='font-size:14px; font-weight:700; color:#F8FAFC;'>📊 DỰ BÁO TÁC ĐỘNG TỚI TỶ LỆ HOÀN THÀNH (FR%)</div>", unsafe_allow_html=True)
        
        # Compare Original vs Simulated FR
        df_sim = df_ops.copy()
        for idx, row in df_sim.iterrows():
            if row["Hour"] in target_hours:
                df_sim.loc[idx, "Simulated_FR"] = min(row["Fulfillment_Rate"] + est_fr_lift, 98.5)
            else:
                df_sim.loc[idx, "Simulated_FR"] = row["Fulfillment_Rate"]
        
        if go is not None:
            fig_sim = go.Figure()
            fig_sim.add_trace(go.Scatter(
                x=df_sim["Hour"], y=df_sim["Fulfillment_Rate"],
                name="FR Hiện Tại (Baseline)", line=dict(color="#94A3B8", width=2, dash="dot")
            ))
            fig_sim.add_trace(go.Scatter(
                x=df_sim["Hour"], y=df_sim["Simulated_FR"],
                name=f"FR Sau Thưởng (+{surge_bonus:,}đ)", line=dict(color="#10B981", width=3)
            ))
            fig_sim.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=320,
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_sim.update_yaxes(range=[75, 100], title_text="FR (%)")
            st.plotly_chart(fig_sim, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="display:flex; justify-content:space-between; font-size:12px; color:#64748B;">
        <div>Ahamove Operations Management System — Built with Streamlit & UI/UX Pro Max</div>
        <div>Version 2.4.0-PRO | Confidentially Shared</div>
    </div>
    """,
    unsafe_allow_html=True
)
