# -*- coding: utf-8 -*-
"""Mô phỏng điều phối đội cắm chốt ĐMX Mega Sale (dùng chung cho dashboard dmx_mega_sale_ops.py).

Logic: tài xế về kho là lấy chuyến tiếp ngay. Mỗi chuyến chọn mốc SLA gần nhất còn đơn,
trong đó chọn cụm phường giao kịp được nhiều đơn nhất, rồi ghép thêm đơn mốc sau cùng cụm cho đầy sọt.
"""
import heapq
import numpy as np
import pandas as pd

SPEED = {'TB': 20, 'BC': 22, 'TD': 22, 'TH': 18, 'DA': 22}
DEADLINE = {12: 12 * 60, 14: 14 * 60, 18: 18 * 60}

WH_NAME = {'TB': 'Tân Bình', 'BC': 'Bình Chánh', 'TD': 'Thủ Đức 1', 'TH': 'Tam Hiệp', 'DA': 'Đông Anh'}
WH_REGION = {'TB': 'SGN', 'BC': 'SGN', 'TD': 'SGN', 'TH': 'HAN', 'DA': 'HAN'}

# Hướng ước lượng của cụm so với kho (độ, 0 = Bắc, theo chiều kim đồng hồ). Không phải tọa độ thật.
BEARING = {
    'TB1': 0, 'TB2': 335, 'TB3': 245, 'TB4': 205, 'TB5': 70, 'TB6': 150, 'TB7': 25, 'TB8': 48,
    'TB9': 112, 'TB10': 92, 'TB11': 135,
    'BC1': 315, 'BC2': 35, 'BC3': 75, 'BC4': 130,
    'TD1': 85, 'TD2': 120, 'TD3': 335, 'TD4': 270, 'TD5': 230, 'TD6': 175,
    'TH1': 0, 'TH2': 35, 'TH3': 340, 'TH4': 270, 'TH5': 310, 'TH6': 15, 'TH7': 180,
    'DA1': 0, 'DA2': 200, 'DA3': 165, 'DA4': 228,
}

DEFAULT_PARAMS = dict(cap=15.0, drop_min=4.0, inter_km=1.0, docks=10, load_min=10,
                      start=9 * 60, speed_mult=1.0, cutoff=17 * 60)

PLAN_ALLOC = {'20': {'TB': 20, 'BC': 7, 'TD': 3},
              '29': {'TB': 25, 'BC': 7, 'TD': 10, 'TH': 30, 'DA': 8}}


def simulate(orders: pd.DataFrame, wh: str, n_drivers: int, p: dict | None = None):
    """orders: đơn của 1 kho trong 1 ngày (cột slot, km, unit, cluster, order_code).
    Trả về (orders kèm done/trip/driver/late, trips DataFrame)."""
    p = {**DEFAULT_PARAMS, **(p or {})}
    mpk = 60 / (SPEED[wh] * p['speed_mult'])
    per_drop = p['drop_min'] + p['inter_km'] * mpk
    rem = orders.reset_index(drop=True).copy()
    rem['done'] = np.nan
    rem['trip'] = -1
    rem['driver'] = 0
    slot = rem.slot.to_numpy(); km = rem.km.to_numpy(); unit = rem.unit.to_numpy()
    cl = rem.cluster.to_numpy()
    done = np.full(len(rem), np.nan)
    trip_of = np.full(len(rem), -1); drv_of = np.zeros(len(rem), dtype=int)
    order_idx = np.argsort(km, kind='stable')
    drivers = [(p['start'] - 60, i) for i in range(n_drivers)]
    heapq.heapify(drivers)
    dock = []
    trips = []
    tid = 0
    while drivers:
        t, i = heapq.heappop(drivers)
        open_mask = np.isnan(done)
        if not open_mask.any() or t > p['cutoff']:
            continue
        dock = [d for d in dock if d > t]
        if len(dock) >= p['docks']:
            t = min(dock)
        dep = max(t + p['load_min'], p['start'])
        best = None
        for s in sorted(set(slot[open_mask])):
            cand = []
            sel_mask = open_mask & (slot == s)
            for c in set(cl[sel_mask]):
                idx = order_idx[(sel_mask & (cl == c))[order_idx]]
                arr0 = dep + km[idx[0]] * mpk
                k = 0; u = 0.0
                for j, ix in enumerate(idx):
                    if u + unit[ix] > p['cap'] or arr0 + j * per_drop + p['drop_min'] > DEADLINE[s]:
                        break
                    k += 1; u += unit[ix]
                if k:
                    cand.append((k, float(np.median(km[idx])), c, idx[:k]))
            if cand:
                cand.sort(key=lambda x: (-x[0], -x[1]))
                best = (s, cand[0])
                break
        if best is None:
            continue
        s, (k, _, c, prim) = best
        u = unit[prim].sum()
        extra_idx = order_idx[(open_mask & (cl == c) & (slot > s))[order_idx]]
        ext = []
        for ix in extra_idx:
            if u + unit[ix] <= p['cap']:
                ext.append(ix); u += unit[ix]
        seq = list(prim) + ext
        arr0 = dep + km[seq[0]] * mpk
        times = [arr0 + j * per_drop + p['drop_min'] for j in range(len(seq))]
        done[seq] = times; trip_of[seq] = tid; drv_of[seq] = i + 1
        last_drop = times[-1]
        back = last_drop + km[seq[-1]] * mpk
        trips.append(dict(trip=tid, driver=i + 1, load=t, dep=dep, last_drop=last_drop, end=back,
                          cluster=c, slot=int(s), n=len(seq), unit=float(u),
                          n12=int((slot[seq] == 12).sum()), n14=int((slot[seq] == 14).sum()),
                          n18=int((slot[seq] == 18).sum())))
        dock.append(t + p['load_min'])
        tid += 1
        heapq.heappush(drivers, (back, i))
    rem['done'] = done; rem['trip'] = trip_of; rem['driver'] = drv_of
    rem['deadline'] = rem.slot.map(DEADLINE)
    rem['late'] = rem.done.isna() | (rem.done > rem.deadline)
    tr = pd.DataFrame(trips, columns=['trip', 'driver', 'load', 'dep', 'last_drop', 'end', 'cluster',
                                      'slot', 'n', 'unit', 'n12', 'n14', 'n18'])
    return rem, tr


def fmt(m) -> str:
    if m is None or (isinstance(m, float) and np.isnan(m)):
        return '–'
    m = int(round(m))
    return f'{m // 60:02d}:{m % 60:02d}'
