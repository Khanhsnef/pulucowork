# -*- coding: utf-8 -*-
"""ĐMX Mega Sale Ops — trực quan hoá vận hành đội tài xế cắm chốt & lượng đơn ngày 20/11 và 29/11.

Chạy:
    streamlit run "output/Ahamove/04. OPS_METRICS/dashboards/dmx_mega_sale_ops.py"

Nguồn dữ liệu:
    - raw-data/dmx-mega-sale/orders.parquet  (danh sách đơn ĐMX đã gom cụm phường)
    - CSV trạng thái đơn export từ Ahamove trong ngày chạy (tải lên ở tab "Kế hoạch vs Thực tế")
"""
import math
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

BASE = Path('/Users/ts-1148/Desktop/Pulu-workspace/output/Ahamove/04. OPS_METRICS')
sys.path.insert(0, str(BASE / 'dashboards'))
from dmx_sim_engine import (BEARING, DEADLINE, DEFAULT_PARAMS, PLAN_ALLOC, WH_NAME, WH_REGION,  # noqa: E402
                            fmt, simulate)

DATA = BASE / 'raw-data' / 'dmx-mega-sale' / 'orders.parquet'

BLUE, ORANGE, OK, BAD = '#0E4174', '#FF7F32', '#10B981', '#EF4444'
GREY, LINE, MUTED = '#94A3B8', '#E8EDF3', '#5B6B80'
SLOT_COLOR = {12: ORANGE, 14: BLUE, 18: GREY}
STATE_COLOR = {'Chờ tại kho': '#CBD5E1', 'Đang giao': ORANGE, 'Đã giao kịp': OK, 'Trễ mốc': BAD}

st.set_page_config(page_title='ĐMX Mega Sale Ops', page_icon='🚚', layout='wide', initial_sidebar_state='expanded')
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;600;800&display=swap');
html, body, [class*="css"], .stApp, button, input, select, textarea {{ font-family: 'Lexend', system-ui, sans-serif !important; }}
.stApp {{ background: #F9FAFB; }}
h1, h2, h3 {{ letter-spacing: -.02em; font-weight: 800 !important; color: {BLUE}; }}
.block-container {{ padding-top: 1.6rem; max-width: 1400px; }}
.kpi {{ background: #fff; border: 1px solid {LINE}; border-radius: 1.75rem; padding: 16px 20px; height: 100%; }}
.kpi .v {{ font-size: 1.9rem; font-weight: 800; letter-spacing: -.03em; line-height: 1.1; font-variant-numeric: tabular-nums; color: #0F1B2D; }}
.kpi .l {{ font-size: .74rem; color: {MUTED}; text-transform: uppercase; letter-spacing: .06em; }}
.kpi .s {{ font-size: .78rem; color: {MUTED}; margin-top: 2px; }}
.kpi.ok .v {{ color: {OK}; }} .kpi.bad .v {{ color: {BAD}; }} .kpi.or .v {{ color: {ORANGE}; }}
.pill {{ display:inline-block; font-size:.72rem; font-weight:600; padding:3px 10px; border-radius:999px; margin-right:6px; }}
.pill.ok {{ background:#E7F8F1; color:{OK}; }} .pill.bad {{ background:#FDECEC; color:{BAD}; }} .pill.or {{ background:#FFF0E6; color:{ORANGE}; }}
[data-testid="stSidebar"] {{ background: #fff; border-right: 1px solid {LINE}; }}
.stTabs [data-baseweb="tab"] {{ font-weight: 600; }}
.note {{ font-size: .8rem; color: {MUTED}; }}
</style>
""", unsafe_allow_html=True)


# ── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_orders() -> pd.DataFrame:
    con = duckdb.connect(':memory:')
    df = con.execute(f"SELECT * FROM read_parquet('{DATA.as_posix()}')").df()
    df['cluster_code'] = df.cluster.str.split(' ').str[0]
    df['cluster_name'] = df.cluster.str.split(' ', n=1).str[1]
    return df


@st.cache_data(show_spinner=False)
def run_sim(day: str, alloc: tuple, params: tuple):
    o = load_orders()
    p = dict(params)
    R, T = [], []
    for wh, n in alloc:
        g = o[(o.day == day) & (o.wh == wh)]
        if g.empty or n <= 0:
            if not g.empty:
                g = g.copy(); g['done'] = np.nan; g['trip'] = -1; g['driver'] = 0
                g['deadline'] = g.slot.map(DEADLINE); g['late'] = True; R.append(g)
            continue
        r, t = simulate(g, wh, int(n), p)
        r['wh'] = wh; t['wh'] = wh
        R.append(r); T.append(t)
    R = pd.concat(R, ignore_index=True)
    T = pd.concat(T, ignore_index=True) if T else pd.DataFrame(columns=['wh', 'driver', 'trip', 'load', 'dep', 'last_drop', 'end', 'cluster', 'slot', 'n', 'unit', 'n12', 'n14', 'n18'])
    # trip timing per order: departure time of the trip it rides on
    dep = T.set_index(['wh', 'trip']).dep
    R['trip_dep'] = [dep.get((w, t), np.nan) if t >= 0 else np.nan for w, t in zip(R.wh, R.trip)]
    return R, T


def order_state(R: pd.DataFrame, now: float) -> pd.Series:
    s = pd.Series('Chờ tại kho', index=R.index)
    s[(R.trip_dep <= now) & ~(R.done <= now)] = 'Đang giao'
    s[R.done <= now] = 'Đã giao kịp'
    s[(R.done <= now) & (R.done > R.deadline)] = 'Trễ mốc'
    s[R.done.isna() & (R.deadline <= now)] = 'Trễ mốc'
    s[(R.done > R.deadline) & (R.deadline <= now) & ~(R.done <= now)] = 'Trễ mốc'
    return s


def driver_state(T: pd.DataFrame, wh_drivers: dict, now: float) -> pd.DataFrame:
    rows = []
    for wh, n in wh_drivers.items():
        t = T[T.wh == wh]
        for d in range(1, n + 1):
            td = t[t.driver == d]
            cur = td[(td.load <= now) & (td.end > now)]
            if not cur.empty:
                x = cur.iloc[0]
                if now < x.dep:
                    stt = 'Bốc hàng'
                elif now <= x.last_drop:
                    stt = 'Đang giao'
                else:
                    stt = 'Quay về kho'
                rows.append((wh, d, stt, x.cluster))
            elif not td.empty and now >= td.end.max():
                rows.append((wh, d, 'Xong ca', None))
            else:
                rows.append((wh, d, 'Chờ tại kho', None))
    return pd.DataFrame(rows, columns=['wh', 'driver', 'state', 'cluster'])


def kpi(col, label, value, sub='', tone=''):
    col.markdown(f'<div class="kpi {tone}"><div class="l">{label}</div><div class="v">{value}</div><div class="s">{sub}</div></div>', unsafe_allow_html=True)


def base_layout(fig, h=360, **kw):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#fff',
                      font=dict(family='Lexend, sans-serif', size=12, color='#0F1B2D'),
                      legend=dict(orientation='h', yanchor='bottom', y=1.02, x=0), **kw)
    fig.update_xaxes(gridcolor=LINE, zeroline=False)
    fig.update_yaxes(gridcolor=LINE, zeroline=False)
    return fig


TIME_TICKS = list(range(8 * 60, 18 * 60 + 1, 60))


def time_axis(fig, lo=8 * 60, hi=18 * 60):
    fig.update_xaxes(range=[lo, hi], tickvals=TIME_TICKS, ticktext=[fmt(t) for t in TIME_TICKS])
    for m, c in ((720, ORANGE), (840, BAD)):
        fig.add_vline(x=m, line=dict(color=c, width=1.5, dash='dot'))
    return fig


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
orders = load_orders()
st.sidebar.markdown(f"<h2 style='margin:0'>ĐMX Mega Sale</h2><div class='note'>Đội cắm chốt · 5 kho SGN/HAN</div>", unsafe_allow_html=True)
day = st.sidebar.radio('Ngày chạy', ['20', '29'], format_func=lambda d: {'20': 'Thứ Sáu 20/11', '29': 'Chủ Nhật 29/11'}[d], horizontal=True, key='day')
whs = [w for w in ['TB', 'BC', 'TD', 'TH', 'DA'] if ((orders.day == day) & (orders.wh == w)).any()]

st.sidebar.markdown('#### Số tài xế cắm chốt')
alloc = {}
for w in whs:
    alloc[w] = st.sidebar.number_input(f'{WH_REGION[w]} · {WH_NAME[w]}', min_value=0, max_value=120,
                                       value=PLAN_ALLOC[day][w], step=1, key=f'n_{day}_{w}')
st.sidebar.caption(f'Tổng: **{sum(alloc.values())}** tài xế · Kế hoạch gốc: {sum(PLAN_ALLOC[day].values())}')

with st.sidebar.expander('Giả định vận hành (what-if)', expanded=False):
    cap = st.slider('Sức chở 1 chuyến (đơn vị chảo)', 8, 20, int(DEFAULT_PARAMS['cap']), key='cap')
    drop = st.slider('Phút / điểm giao (gồm thu COD)', 2.0, 10.0, DEFAULT_PARAMS['drop_min'], 0.5, key='drop')
    ikm = st.slider('Km giữa 2 điểm giao', 0.5, 3.0, DEFAULT_PARAMS['inter_km'], 0.25, key='ikm')
    spd = st.slider('Hệ số tốc độ (1.0 = bình thường)', 0.6, 1.3, 1.0, 0.05, key='spd',
                    help='< 1.0 khi kẹt xe / mưa. Tốc độ gốc: Tân Bình 20, Tam Hiệp 18, các kho khác 22 km/h')
    start = st.select_slider('Giờ ĐMX đẩy đơn / xe xuất phát', options=[8 * 60 + 30, 9 * 60, 9 * 60 + 15, 9 * 60 + 30, 10 * 60],
                             value=9 * 60, format_func=fmt, key='start')
    docks = st.slider('Số xe bốc hàng song song / kho', 4, 20, 10, key='docks')
    load = st.slider('Phút bốc hàng / xe', 5, 20, 10, key='load')
params = dict(cap=float(cap), drop_min=float(drop), inter_km=float(ikm), speed_mult=float(spd),
              start=int(start), docks=int(docks), load_min=int(load))
is_base = params == {k: DEFAULT_PARAMS[k] for k in params} and alloc == PLAN_ALLOC[day]
if not is_base and st.sidebar.button('↺ Về kế hoạch gốc', width='stretch'):
    for k in list(st.session_state):
        if k.startswith(f'n_{day}_') or k in ('cap', 'drop', 'ikm', 'spd', 'start', 'docks', 'load'):
            del st.session_state[k]
    st.rerun()

R, T = run_sim(day, tuple(sorted(alloc.items())), tuple(sorted(params.items())))
R['region'] = R.wh.map(WH_REGION); R['kho'] = R.wh.map(lambda w: f'{WH_REGION[w]} · {WH_NAME[w]}')

# ── HEADER ───────────────────────────────────────────────────────────────────
dlabel = {'20': 'Thứ Sáu 20/11', '29': 'Chủ Nhật 29/11'}[day]
st.markdown(f"<h1 style='margin-bottom:0'>Vận hành ĐMX · {dlabel}</h1>", unsafe_allow_html=True)
tag = '<span class="pill ok">Kế hoạch gốc</span>' if is_base else '<span class="pill or">Đang thử phương án</span>'
st.markdown(f"{tag}<span class='note'>Mô phỏng: tài xế về kho là lấy chuyến tiếp ngay · mốc 12h/14h đúng giờ, 16–21h gộp 18h</span>", unsafe_allow_html=True)

n_all = len(R); n_ok = int((~R.late).sum()); n_late = n_all - n_ok
c = st.columns(6)
kpi(c[0], 'Tổng đơn', f'{n_all:,}'.replace(',', '.'), f'12h {int((R.slot==12).sum())} · 14h {int((R.slot==14).sum())} · 18h {int((R.slot==18).sum())}')
kpi(c[1], 'Tài xế', sum(alloc.values()), ' · '.join(f'{WH_NAME[w]} {n}' for w, n in alloc.items()))
kpi(c[2], 'Chuyến', len(T), f'{(T.n.mean() if len(T) else 0):.1f} đơn/chuyến')
kpi(c[3], 'Giao kịp mốc', f'{n_ok / n_all * 100:.1f}%', f'{n_ok:,} / {n_all:,} đơn'.replace(',', '.'), 'ok' if n_late == 0 else ('or' if n_ok / n_all > .97 else 'bad'))
kpi(c[4], 'Trễ mốc', n_late, 'đơn cần xử lý' if n_late else 'không có đơn trễ', 'bad' if n_late else 'ok')
per_drv = T.groupby(['wh', 'driver']).n.sum() if len(T) else pd.Series(dtype=float)
kpi(c[5], 'Đạt thưởng 15 đơn', f'{int((per_drv >= 15).sum())}/{sum(alloc.values())}', f'≈ {int((per_drv >= 15).sum()) * 100:,}k thưởng'.replace(',', '.'))
st.write('')

tab1, tab2, tab3, tab4, tab5 = st.tabs(['⏱ Diễn biến theo giờ', '🗺 Sơ đồ cụm', '📉 Đơn còn lại vs mốc', '🧑‍✈️ Lịch tài xế', '📊 Kế hoạch vs Thực tế'])

# ── TAB 1: TIME SCRUBBER ─────────────────────────────────────────────────────
with tab1:
    now = st.slider('Thời điểm', min_value=8 * 60, max_value=18 * 60, value=12 * 60, step=15, format='%d', key='now',
                    help='Kéo để xem trạng thái đơn và tài xế tại thời điểm đó')
    st.markdown(f"<h3 style='margin:0'>Lúc {fmt(now)}</h3>", unsafe_allow_html=True)
    R['state'] = order_state(R, now)
    D = driver_state(T, alloc, now)
    cols = st.columns(len(whs))
    for col, w in zip(cols, whs):
        r = R[R.wh == w]; d = D[D.wh == w]
        sc = r.state.value_counts()
        ds = d.state.value_counts()
        due12 = r[(r.slot == 12) & ~(r.done <= now)].shape[0]
        due14 = r[(r.slot == 14) & ~(r.done <= now)].shape[0]
        warn = ''
        if now < 720 and due12:
            warn = f'<span class="pill or">còn {due12} đơn mốc 12h</span>'
        elif now < 840 and due14:
            warn = f'<span class="pill or">còn {due14} đơn mốc 14h</span>'
        if sc.get('Trễ mốc', 0):
            warn += f'<span class="pill bad">{sc.get("Trễ mốc", 0)} trễ</span>'
        col.markdown(f"""<div class="kpi"><div class="l">{WH_REGION[w]} · {WH_NAME[w]}</div>
            <div class="v">{sc.get('Đã giao kịp', 0)}<span style="font-size:1rem;color:{MUTED}"> / {len(r)}</span></div>
            <div class="s">đã giao · {sc.get('Đang giao', 0)} đang giao · {sc.get('Chờ tại kho', 0)} chờ</div>
            <div class="s" style="margin-top:8px">🛵 {ds.get('Đang giao', 0)} giao · ↩ {ds.get('Quay về kho', 0)} về · 📦 {ds.get('Bốc hàng', 0)} bốc · ⏸ {ds.get('Chờ tại kho', 0) + ds.get('Xong ca', 0)} rảnh</div>
            <div style="margin-top:8px">{warn}</div></div>""", unsafe_allow_html=True)
    st.write('')
    a, b = st.columns([3, 2])
    with a:
        grid = list(range(8 * 60, 18 * 60 + 1, 15))
        ag = []
        for t in grid:
            s = order_state(R, t).value_counts()
            ag.append({'t': t, **{k: s.get(k, 0) for k in STATE_COLOR}})
        ag = pd.DataFrame(ag)
        fig = go.Figure()
        for k in ['Đã giao kịp', 'Trễ mốc', 'Đang giao', 'Chờ tại kho']:
            fig.add_trace(go.Scatter(x=ag.t, y=ag[k], name=k, stackgroup='one', mode='none', fillcolor=STATE_COLOR[k],
                                     hovertemplate='%{y} đơn<extra>' + k + '</extra>'))
        fig.add_vline(x=now, line=dict(color='#0F1B2D', width=2))
        base_layout(fig, 340, title=dict(text='Trạng thái đơn theo thời gian (tất cả kho)', font=dict(size=14)))
        time_axis(fig)
        st.plotly_chart(fig, width='stretch', key='area')
    with b:
        dd = D.groupby(['wh', 'state']).size().unstack(fill_value=0).reindex(whs)
        fig = go.Figure()
        dcol = {'Bốc hàng': '#CBD5E1', 'Đang giao': ORANGE, 'Quay về kho': BLUE, 'Chờ tại kho': '#E2E8F0', 'Xong ca': OK}
        for k in ['Đang giao', 'Quay về kho', 'Bốc hàng', 'Chờ tại kho', 'Xong ca']:
            if k in dd:
                fig.add_trace(go.Bar(y=[WH_NAME[w] for w in dd.index], x=dd[k], name=k, orientation='h', marker_color=dcol[k]))
        base_layout(fig, 340, barmode='stack', title=dict(text=f'Tài xế lúc {fmt(now)}', font=dict(size=14)))
        st.plotly_chart(fig, width='stretch', key='drvbar')
    st.markdown('##### Số đơn rời kho theo khung giờ')
    bins = [0, 600, 660, 720, 780, 840, 2000]; lbl = ['09–10h', '10–11h', '11–12h', '12–13h', '13–14h', 'Sau 14h']
    if len(T):
        T['bucket'] = pd.cut(T.dep, bins, right=False, labels=lbl)
        hp = pd.pivot_table(T, index='wh', columns='bucket', values='n', aggfunc='sum', fill_value=0, observed=False).reindex(whs)
        hc = pd.pivot_table(T, index='wh', columns='bucket', values='n', aggfunc='size', fill_value=0, observed=False).reindex(whs)
        tbl = hp.astype(str) + ' đơn · ' + hc.astype(str) + ' chuyến'
        tbl.index = [f'{WH_REGION[w]} · {WH_NAME[w]}' for w in tbl.index]
        st.dataframe(tbl, width='stretch')

# ── TAB 2: CLUSTER DIAGRAM ───────────────────────────────────────────────────
with tab2:
    a, b = st.columns([1, 3])
    wsel = a.radio('Kho', whs, format_func=lambda w: f'{WH_REGION[w]} · {WH_NAME[w]}', key='map_wh')
    now2 = a.slider('Thời điểm', 8 * 60, 18 * 60, 11 * 60, 15, key='now2')
    a.caption(f'Lúc **{fmt(now2)}**')
    a.markdown("<div class='note'>Sơ đồ ước lượng: kho ở tâm, mỗi cụm đặt theo hướng và km trung vị. Không phải bản đồ thật. "
               "Kích thước = số đơn. Màu vòng = đơn còn lại của mốc gần nhất. Chấm cam = tài xế đang ở cụm.</div>", unsafe_allow_html=True)
    r = R[R.wh == wsel].copy(); r['state'] = order_state(r, now2)
    D2 = driver_state(T, {wsel: alloc[wsel]}, now2)
    cl = r.groupby(['cluster_code', 'cluster_name']).agg(n=('slot', 'size'), km=('km', 'median'),
                                                         left=('state', lambda x: int((x == 'Chờ tại kho').sum() + (x == 'Đang giao').sum())),
                                                         late=('state', lambda x: int((x == 'Trễ mốc').sum())),
                                                         s12=('slot', lambda x: int((x == 12).sum())), s14=('slot', lambda x: int((x == 14).sum()))).reset_index()
    cl['ang'] = cl.cluster_code.map(BEARING).fillna(0)
    cl['x'] = cl.km * np.sin(np.radians(cl.ang)); cl['y'] = cl.km * np.cos(np.radians(cl.ang))
    pend = r[~(r.done <= now2)]
    def ring(code):
        p = pend[pend.cluster_code == code]
        if (r[(r.cluster_code == code)].state == 'Trễ mốc').any():
            return BAD
        if p.empty:
            return OK
        nxt = p.slot.min()
        mins_left = DEADLINE[nxt] - now2
        return BAD if mins_left < 45 else (ORANGE if mins_left < 120 else BLUE)
    cl['ring'] = cl.cluster_code.map(ring)
    fig = go.Figure()
    rmax = max(cl.km.max() * 1.25, 5)
    for rr in range(5, int(rmax) + 1, 5):
        th = np.linspace(0, 2 * np.pi, 120)
        fig.add_trace(go.Scatter(x=rr * np.sin(th), y=rr * np.cos(th), mode='lines', line=dict(color=LINE, width=1), hoverinfo='skip', showlegend=False))
        fig.add_annotation(x=0, y=rr, text=f'{rr} km', showarrow=False, font=dict(size=10, color=MUTED), yshift=8)
    for _, x in cl.iterrows():
        fig.add_trace(go.Scatter(x=[0, x.x], y=[0, x.y], mode='lines', line=dict(color=LINE, width=1), hoverinfo='skip', showlegend=False))
    fig.add_trace(go.Scatter(x=cl.x, y=cl.y, mode='markers+text', text=cl.cluster_code + '<br>' + cl.left.astype(str) + '/' + cl.n.astype(str),
                             textposition='middle center', textfont=dict(size=10, color='#0F1B2D'),
                             marker=dict(size=np.clip(np.sqrt(cl.n) * 7, 26, 90), color='#fff', line=dict(color=cl.ring, width=4)),
                             customdata=np.stack([cl.cluster_name, cl.n, cl.left, cl.late, cl.s12, cl.s14, cl.km.round(1)], axis=1),
                             hovertemplate='<b>%{customdata[0]}</b><br>%{customdata[1]} đơn · còn %{customdata[2]} · trễ %{customdata[3]}'
                                           '<br>mốc 12h %{customdata[4]} · 14h %{customdata[5]}<br>km TV %{customdata[6]}<extra></extra>',
                             showlegend=False))
    # drivers as dots near their cluster
    on = D2[D2.state.isin(['Đang giao', 'Quay về kho'])]
    if not on.empty:
        pos = cl.set_index(cl.cluster_code)
        xs, ys, tx = [], [], []
        for k, (_, d) in enumerate(on.iterrows()):
            code = d.cluster.split(' ')[0]
            if code not in pos.index:
                continue
            frac = 1.0 if d.state == 'Đang giao' else 0.5
            jit = (k % 7 - 3) * 0.25
            xs.append(pos.loc[code, 'x'] * frac + jit); ys.append(pos.loc[code, 'y'] * frac + jit * .6)
            tx.append(f"TX{d.driver:02d} · {d.state}")
        fig.add_trace(go.Scatter(x=xs, y=ys, mode='markers', marker=dict(size=9, color=ORANGE, line=dict(color='#fff', width=1)),
                                 text=tx, hovertemplate='%{text}<extra></extra>', showlegend=False))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text', text=[f'KHO {WH_NAME[wsel].upper()}'], textposition='bottom center',
                             marker=dict(size=22, color=BLUE, symbol='square'), textfont=dict(color=BLUE, size=11), hoverinfo='skip', showlegend=False))
    base_layout(fig, 640)
    fig.update_xaxes(visible=False, range=[-rmax, rmax], scaleanchor='y'); fig.update_yaxes(visible=False, range=[-rmax, rmax])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    with b:
        st.plotly_chart(fig, width='stretch', key='map')
        st.markdown(f"<span class='pill ok'>Xanh lá: đã giao hết</span><span class='pill' style='background:#E7EEF6;color:{BLUE}'>Xanh: còn hơn 2 giờ tới mốc</span>"
                    f"<span class='pill or'>Cam: còn dưới 2 giờ</span><span class='pill bad'>Đỏ: còn dưới 45 phút hoặc đã trễ</span>", unsafe_allow_html=True)

# ── TAB 3: BURNDOWN ──────────────────────────────────────────────────────────
with tab3:
    st.markdown("<div class='note'>Đường thể hiện số đơn của từng mốc còn chưa giao. Đơn mốc 12h phải về 0 trước vạch cam (12:00). Đơn mốc 14h phải về 0 trước vạch đỏ (14:00).</div>", unsafe_allow_html=True)
    grid = np.arange(8 * 60, 18 * 60 + 1, 5)
    cols = st.columns(2)
    for i, w in enumerate(whs):
        r = R[R.wh == w]
        fig = go.Figure()
        for s in (12, 14, 18):
            rs = r[r.slot == s]
            if rs.empty:
                continue
            done = np.sort(rs.done.fillna(1e9).to_numpy())
            left = len(rs) - np.searchsorted(done, grid, side='right')
            fig.add_trace(go.Scatter(x=grid, y=left, name=f'Mốc {s}h' + (' (gộp 16–21h)' if s == 18 else ''), mode='lines',
                                     line=dict(color=SLOT_COLOR[s], width=3, shape='hv'),
                                     hovertemplate='%{y} đơn còn lại<extra>' + f'Mốc {s}h' + '</extra>'))
            lt = int(r[(r.slot == s) & r.late].shape[0])
            if lt:
                fig.add_annotation(x=DEADLINE[s], y=lt, text=f'{lt} trễ', showarrow=True, arrowhead=0, font=dict(color=BAD, size=11), ax=30, ay=-20)
        base_layout(fig, 300, title=dict(text=f'{WH_REGION[w]} · {WH_NAME[w]} — {len(r)} đơn, {alloc[w]} TX', font=dict(size=13)))
        time_axis(fig)
        cols[i % 2].plotly_chart(fig, width='stretch', key=f'bd_{w}')

# ── TAB 4: DRIVER GANTT ──────────────────────────────────────────────────────
with tab4:
    a, b = st.columns([1, 3])
    wg = a.radio('Kho', whs, format_func=lambda w: f'{WH_REGION[w]} · {WH_NAME[w]}', key='g_wh')
    t = T[T.wh == wg].copy()
    if t.empty:
        b.info('Kho này chưa có tài xế.')
    else:
        a.metric('Tài xế', alloc[wg]); a.metric('Chuyến', len(t)); a.metric('Về kho lần cuối', fmt(t.end.max()))
        fig = go.Figure()
        t['who'] = t.driver.map(lambda d: f'TX{d:02d}')
        t['col'] = np.where(t.n12 > 0, ORANGE, np.where(t.n14 > 0, BLUE, GREY))
        fig.add_trace(go.Bar(y=t.who, x=t.dep - t.load, base=t.load, orientation='h', marker_color='#E2E8F0', name='Bốc hàng', hoverinfo='skip'))
        fig.add_trace(go.Bar(y=t.who, x=t.last_drop - t.dep, base=t.dep, orientation='h', marker_color=t.col, name='Đi giao',
                             text=t.n.astype(str), textposition='inside', insidetextanchor='middle',
                             customdata=np.stack([t.cluster, t.n, t.n12, t.n14, t.n18, t.dep.map(fmt), t.end.map(fmt)], axis=1),
                             hovertemplate='<b>%{customdata[0]}</b><br>%{customdata[5]} → %{customdata[6]}<br>%{customdata[1]} đơn · 12h %{customdata[2]} · 14h %{customdata[3]} · 18h %{customdata[4]}<extra></extra>'))
        fig.add_trace(go.Bar(y=t.who, x=t.end - t.last_drop, base=t.last_drop, orientation='h', marker_color='#CBD5E1', name='Quay về kho', hoverinfo='skip'))
        base_layout(fig, max(360, 26 * alloc[wg] + 80), barmode='overlay', showlegend=True)
        time_axis(fig)
        fig.update_yaxes(categoryorder='array', categoryarray=sorted(t.who.unique(), reverse=True))
        b.plotly_chart(fig, width='stretch', key='gantt')
        b.caption('Màu thanh đi giao: cam là chuyến có đơn mốc 12h, xanh là chuyến có đơn mốc 14h, xám là chuyến chỉ có đơn mốc 18h. Số trên thanh là số đơn của chuyến.')
        with st.expander('Danh sách chuyến & đơn'):
            rr = R[(R.wh == wg) & (R.trip >= 0)].merge(t[['trip', 'who', 'dep', 'end']], on='trip')
            rr = rr.sort_values(['who', 'dep', 'done'])
            st.dataframe(pd.DataFrame({'Tài xế': rr.who, 'Rời kho': rr.dep.map(fmt), 'Cụm': rr.cluster, 'Mã đơn': rr.order_code,
                                       'Phường': rr.ward_s, 'Mốc': rr.slot.astype(str) + 'h', 'Giao dự kiến': rr.done.map(fmt),
                                       'Km': rr.km, 'COD': rr.cod, 'Trễ': rr.late.map({True: '⚠️', False: ''})}),
                         width='stretch', hide_index=True, height=420)

# ── TAB 5: PLAN vs ACTUAL ────────────────────────────────────────────────────
with tab5:
    st.markdown("""**Nạp file trạng thái đơn từ Ahamove** (CSV/XLSX, có thể nạp nhiều lần trong ngày).
Tool tự nhận các cột theo tên, không phân biệt hoa thường:

| Ý nghĩa | Tên cột chấp nhận |
|---|---|
| Mã đơn ĐMX (bắt buộc) | `order_code`, `mã đơn hàng`, `ref_code`, `partner_order_id` |
| Giờ giao thành công | `delivered_at`, `complete_time`, `thời gian giao`, `completed_at` |
| Giờ tài xế lấy hàng | `picked_at`, `pickup_time`, `thời gian lấy hàng` |
| Mã/tên tài xế | `driver_id`, `supplier_id`, `tài xế`, `driver_name` |
| Trạng thái | `status`, `trạng thái` |
""")
    up = st.file_uploader('File trạng thái đơn', type=['csv', 'xlsx'], key='actual')
    ALIAS = {'order_code': ['order_code', 'mã đơn hàng', 'ma don hang', 'ref_code', 'partner_order_id'],
             'delivered_at': ['delivered_at', 'complete_time', 'thời gian giao', 'completed_at'],
             'picked_at': ['picked_at', 'pickup_time', 'thời gian lấy hàng'],
             'driver': ['driver_id', 'supplier_id', 'tài xế', 'driver_name'],
             'status': ['status', 'trạng thái']}
    if up is None:
        st.info('Chưa có dữ liệu thực tế. Trong ngày chạy, cứ 15–30 phút export trạng thái đơn từ hệ thống/Metabase rồi nạp vào đây để so với kế hoạch.')
    else:
        try:
            raw = pd.read_csv(up, dtype=str) if up.name.endswith('.csv') else pd.read_excel(up, dtype=str)
        except Exception as e:  # noqa: BLE001
            st.error(f'Không đọc được file: {e}. Kiểm tra lại định dạng CSV (UTF-8) hoặc XLSX.')
            raw = None
        if raw is not None:
            low = {c.lower().strip(): c for c in raw.columns}
            m = {k: next((low[a] for a in v if a in low), None) for k, v in ALIAS.items()}
            if not m['order_code']:
                st.error(f"Không tìm thấy cột mã đơn. Các cột trong file: {', '.join(raw.columns)}")
            else:
                con = duckdb.connect(':memory:')
                act = pd.DataFrame({k: raw[c] if c else None for k, c in m.items()})
                act['order_code'] = act.order_code.str.strip()
                for k in ('delivered_at', 'picked_at'):
                    if m[k]:
                        ts = pd.to_datetime(act[k], errors='coerce', dayfirst=True)
                        act[k + '_min'] = ts.dt.hour * 60 + ts.dt.minute
                    else:
                        act[k + '_min'] = np.nan
                con.register('plan', R[['order_code', 'wh', 'slot', 'deadline', 'done', 'late', 'cluster']])
                con.register('act', act)
                J = con.execute("""
                    SELECT p.*, a.delivered_at_min, a.picked_at_min, a.driver, a.status
                    FROM plan p LEFT JOIN act a USING (order_code)
                """).df()
                matched = J.delivered_at_min.notna() | J.picked_at_min.notna() | J.status.notna()
                unk = set(act.order_code) - set(R.order_code)
                tnow = st.slider('Tính đến thời điểm', 8 * 60, 18 * 60, int(np.nanmax([J.delivered_at_min.max(), J.picked_at_min.max(), 9 * 60])) // 15 * 15 if matched.any() else 12 * 60, 15, key='tnow')
                plan_done = (J.done <= tnow).sum(); act_done = (J.delivered_at_min <= tnow).sum()
                act_late = ((J.delivered_at_min > J.deadline) | (J.delivered_at_min.isna() & (J.deadline <= tnow))).sum()
                c = st.columns(4)
                kpi(c[0], 'Khớp mã đơn', f'{int(matched.sum())}/{len(J)}', f'{len(unk)} mã trong file không có trong kế hoạch')
                kpi(c[1], f'Kế hoạch giao xong đến {fmt(tnow)}', int(plan_done))
                gap = int(act_done - plan_done)
                kpi(c[2], f'Thực tế giao xong đến {fmt(tnow)}', int(act_done), f'{gap:+d} so với kế hoạch', 'ok' if gap >= 0 else 'bad')
                kpi(c[3], 'Trễ mốc (thực tế)', int(act_late), 'tính trên đơn đã quá mốc', 'bad' if act_late else 'ok')
                grid = np.arange(8 * 60, 18 * 60 + 1, 5)
                fig = go.Figure()
                pd_ = np.sort(J.done.fillna(1e9)); ad_ = np.sort(J.delivered_at_min.fillna(1e9))
                fig.add_trace(go.Scatter(x=grid, y=np.searchsorted(pd_, grid, side='right'), name='Kế hoạch', line=dict(color=GREY, dash='dash', width=2)))
                gg = grid[grid <= tnow]
                fig.add_trace(go.Scatter(x=gg, y=np.searchsorted(ad_, gg, side='right'), name='Thực tế', line=dict(color=ORANGE, width=3)))
                base_layout(fig, 360, title=dict(text='Lũy kế đơn giao xong — kế hoạch vs thực tế', font=dict(size=14)))
                time_axis(fig)
                st.plotly_chart(fig, width='stretch', key='pva')
                byw = J.assign(p=J.done <= tnow, a=J.delivered_at_min <= tnow,
                               risk=(J.delivered_at_min.isna()) & (J.deadline - tnow <= 60) & (J.deadline > tnow)).groupby('wh').agg(
                    **{'Đơn': ('order_code', 'size'), 'KH giao xong': ('p', 'sum'), 'TT giao xong': ('a', 'sum'), 'Chưa giao, mốc ≤ 60 phút': ('risk', 'sum')})
                byw['Chênh lệch'] = byw['TT giao xong'] - byw['KH giao xong']
                byw.index = [f'{WH_REGION[w]} · {WH_NAME[w]}' for w in byw.index]
                st.dataframe(byw, width='stretch')
                risk = J[(J.delivered_at_min.isna()) & (J.deadline > tnow) & (J.deadline - tnow <= 60)]
                if len(risk):
                    st.markdown(f'##### ⚠️ {len(risk)} đơn chưa giao và còn ≤ 60 phút tới mốc')
                    st.dataframe(risk[['wh', 'cluster', 'order_code', 'slot', 'status', 'driver']].rename(columns={'wh': 'Kho', 'cluster': 'Cụm', 'order_code': 'Mã đơn', 'slot': 'Mốc', 'status': 'Trạng thái', 'driver': 'Tài xế'}),
                                 width='stretch', hide_index=True)

st.markdown(f"<div class='note' style='margin-top:24px'>Nguồn: Danh sach giao hang.xlsx (ĐMX) · {len(orders):,} đơn ở 5 kho trong phạm vi · Mô phỏng: dmx_sim_engine.py · Kế hoạch chi tiết: 02. CAMPAIGNS_PROJECTS/2026-11-dmx-*-routing-plan.xlsx</div>".replace(',', '.'), unsafe_allow_html=True)
