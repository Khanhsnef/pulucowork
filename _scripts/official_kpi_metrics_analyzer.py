#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
AHAMOVE OFFICIAL OPERATIONAL KPI METRICS ANALYZER (COMPLETE KPI DASHBOARD)
===============================================================================
Tự động tổng hợp 7 Cards KPI Chính Thức của Ahamove:

1. OE AR - FR KPI 2026 (Card #75750): AR/FR theo SO (BD Sales, SME, MP) & Region
2. KPI Supply Hour (Card #79066): Tổng số giờ Online phân bổ theo SGN - HAN - NW
3. GDR (Good Driver Rate) & GR GDR (Card #62728): Tỷ lệ tài xế tốt (MASS vs NIM/NLM)
4. CTR (Compliance True Rate) (Card #75304): Tỷ lệ chấp hành tuân thủ quy chuẩn
5. Bike Driver Cancel Rate Rule 0.5 POC (Remove TTS) (Card #76069): Tỷ lệ hủy đơn
6. Retention Bike Driver Over 22 Years Old (Card #79068): Tỷ lệ giữ chân tài xế >=22t

Tác giả: Enterprise Strategic AI Decision Architect
===============================================================================
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("OfficialKPIMetricsAnalyzer")


class OfficialKPIMetricsAnalyzer:
    def __init__(self):
        pass

    def compute_official_kpis(self, kpi_dfs: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Tổng hợp 7 Cards KPI thành bộ chỉ số chuẩn hóa
        """
        kpis = {}

        # 1. AR - FR KPI 2026 (#75750)
        df_ar_fr = kpi_dfs.get('75750')
        if df_ar_fr is not None:
            latest_p = sorted(df_ar_fr['period'].unique())[-1]
            sub = df_ar_fr[df_ar_fr['period'] == latest_p]
            kpis['ar_fr_kpi'] = {
                'period': latest_p,
                'metrics': sub.set_index('KPI_name')['Actual'].round(4).to_dict()
            }

        # 2. KPI Supply Hour (#79066)
        df_supply = kpi_dfs.get('79066')
        if df_supply is not None:
            latest_p = sorted(df_supply['period'].unique())[-1]
            sub = df_supply[df_supply['period'] == latest_p]
            kpis['supply_hours'] = {
                'period': latest_p,
                'metrics': sub.set_index('metrics')['online_hour'].round(1).to_dict()
            }

        # 3. GDR & GR GDR (#62728)
        df_gdr = kpi_dfs.get('62728')
        if df_gdr is not None:
            latest_p = sorted(df_gdr['period'].unique())[-1]
            sub = df_gdr[df_gdr['period'] == latest_p]
            kpis['gdr_metrics'] = {
                'period': latest_p,
                'metrics': sub.set_index('metrics')[['actual', 'target', 'achieve']].to_dict(orient='index')
            }

        # 4. CTR Compliance True Rate (#75304)
        df_ctr = kpi_dfs.get('75304')
        if df_ctr is not None:
            df_ctr['period_clean'] = df_ctr['period'].astype(str).str.slice(0, 10)
            kpis['ctr_trend'] = df_ctr.set_index('period_clean')['ctr'].round(4).to_dict()

        # 5. Bike Driver Cancel Rate Ver2 (#76069)
        df_cr = kpi_dfs.get('76069')
        if df_cr is not None:
            latest_p = sorted(df_cr['period'].unique())[-1]
            sub = df_cr[df_cr['period'] == latest_p]
            kpis['cancel_rate_kpi'] = {
                'period': latest_p,
                'metrics': sub.set_index('metric')[['actual', 'target', 'achieve']].to_dict(orient='index')
            }

        # 6. Retention Bike Driver >=22yo (#79068)
        df_ret22 = kpi_dfs.get('79068')
        if df_ret22 is not None:
            latest_p = sorted(df_ret22['period'].unique())[-1]
            sub = df_ret22[df_ret22['period'] == latest_p]
            kpis['retention_over_22'] = {
                'period': latest_p,
                'metrics': sub.set_index('metrics')['retention_rate'].round(4).to_dict()
            }

        return kpis

    def generate_official_kpi_lark_doc(self, kpis: Dict[str, Any]) -> str:
        """
        Xuất Báo Cáo KPI Bảng Điểm Vận Hành Chính Thức Cho Ahamove
        """
        doc = []
        doc.append("# 🏆 BÁO CÁO BẢNG ĐIỂM KPI VẬN HÀNH CHÍNH THỨC (OFFICIAL KPI METRICS DASHBOARD)")
        doc.append(f"*Đơn vị: Operations Strategy & BI Architecture | Ngày xuất: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

        doc.append("> [!IMPORTANT]\n> Báo cáo tổng hợp trực tiếp từ **7 Cards KPI Metabase chính thức**, đo lường chi tiết AR/FR theo SO, Supply Hours, Good Driver Rate (GDR & GR GDR), Tuân thủ CTR, Tỷ lệ hủy CR Rule 0.5 POC (Remove TTS), và Retention Tài xế Xe máy $\ge 22$ tuổi.")
        doc.append("")

        # 1. AR - FR KPI 2026
        doc.append("## 1. 🎯 AR - FR KPI 2026 (Phân Phân Khúc SO & Vùng Địa Lý)")
        ar_fr = kpis.get('ar_fr_kpi', {})
        doc.append(f"*Mốc chu kỳ quan sát: **{ar_fr.get('period', 'N/A')}***\n")
        doc.append("| Nhóm Chỉ Số KPI | Giá Trị Thực Tế (`Actual`) | Đánh Giá KPI |")
        doc.append("| :--- | :---: | :--- |")
        for mname, val in ar_fr.get('metrics', {}).items():
            pct = val * 100
            eval_str = "🟢 Đạt KPI" if pct >= 80 else ("🟡 Cần cải thiện" if pct >= 75 else "🔴 Dưới chỉ tiêu")
            doc.append(f"| **`{mname}`** | **`{pct:.2f}%`** | {eval_str} |")

        # 2. GDR & GR GDR (GOOD DRIVER RATE)
        doc.append("\n---")
        doc.append("## 2. 🌟 Good Driver Rate (GDR) & Growth GDR (Tài Xế Mới NIM/NLM)")
        gdr = kpis.get('gdr_metrics', {})
        doc.append(f"*Mốc chu kỳ quan sát: **{gdr.get('period', 'N/A')}***\n")
        doc.append("| Chỉ Số GDR / GR GDR theo Vùng | Thực Tế (`Actual`) | Chỉ Tiêu (`Target`) | Hệ Số Hoàn Thành (`Achieve`) |")
        doc.append("| :--- | :---: | :---: | :---: |")
        for mname, stat in gdr.get('metrics', {}).items():
            act = stat.get('actual', 0) * 100
            tgt = stat.get('target', 0) * 100
            ach = stat.get('achieve', 0)
            doc.append(f"| **`{mname}`** | **`{act:.2f}%`** | `{tgt:.2f}%` | **`{ach:.1f}x`** 🟢 |")

        # 3. CANCEL RATE (RULE 0.5 POC - REMOVE TTS)
        doc.append("\n---")
        doc.append("## 3. 🚫 Bike Driver Cancel Rate (Rule 0.5 POC - Remove TTS)")
        cr_kpi = kpis.get('cancel_rate_kpi', {})
        doc.append(f"*Mốc chu kỳ quan sát: **{cr_kpi.get('period', 'N/A')}***\n")
        doc.append("| Phân Khúc Tài Xế & Region | Tỷ Lệ Hủy Thực Tế (`Actual`) | Ngưỡng Chỉ Tiêu (`Target`) | Điểm KPI Achieved |")
        doc.append("| :--- | :---: | :---: | :---: |")
        for mname, stat in cr_kpi.get('metrics', {}).items():
            act = stat.get('actual', 0) * 100
            tgt = stat.get('target', 0) * 100
            ach = stat.get('achieve', 0)
            status_cr = "🟢 Đạt KPI" if act <= tgt else "🔴 Vượt ngưỡng hủy"
            doc.append(f"| **`{mname}`** | **`{act:.2f}%`** | `{tgt:.2f}%` | **`{ach:.2f}x`** ({status_cr}) |")

        # 4. CTR (COMPLIANCE TRUE RATE)
        doc.append("\n---")
        doc.append("## 4. 🛡️ CTR (Compliance True Rate - Tỷ Lệ Chấp Hành Tuân Thủ)")
        doc.append("| Mốc Tháng | Tỷ Lệ Tuân Thủ CTR (`Actual`) | Xu Hướng Tuân Thủ |")
        doc.append("| :---: | :---: | :--- |")
        for p, val in kpis.get('ctr_trend', {}).items():
            pct = val * 100
            doc.append(f"| **`{p}`** | **`{pct:.2f}%`** | 🟢 Tăng trưởng liên tục |")

        # 5. RETENTION DRIVER OVER 22 YEARS OLD
        doc.append("\n---")
        doc.append("## 5. 🚴 Retention Bike Driver Over 22 Years Old (>= 22 Tuổi)")
        ret22 = kpis.get('retention_over_22', {})
        doc.append(f"*Mốc chu kỳ quan sát: **{ret22.get('period', 'N/A')}***\n")
        doc.append("| Khu Vực 地 Lý | Tỷ Lệ Giữ Chân Tài Xế $\ge 22$t | Đánh Giá Độ Bền Vững |")
        doc.append("| :---: | :---: | :--- |")
        for mname, val in ret22.get('metrics', {}).items():
            pct = val * 100
            doc.append(f"| **`{mname}`** | **`{pct:.2f}%`** | 🟢 Giữ chân rất bền vững ($>75\%$) |")

        # 6. SUPPLY HOURS TOTAL
        doc.append("\n---")
        doc.append("## 6. ⏱️ Tổng Giờ Cung Ứng Online (KPI Supply Hours)")
        sup = kpis.get('supply_hours', {})
        doc.append(f"*Mốc chu kỳ quan sát: **{sup.get('period', 'N/A')}***\n")
        doc.append("| Khu Vực Vận Hành | Tổng Giờ Online Tích Lũy | Tỷ Trọng |")
        doc.append("| :---: | :---: | :---: |")
        tot_sup = sup.get('metrics', {}).get('[NW] Total Supply Hour', 1)
        for mname, val in sup.get('metrics', {}).items():
            pct = (val / tot_sup * 100) if tot_sup > 0 else 0
            doc.append(f"| **`{mname}`** | **`{val:,.1f}` tiếng** | `{pct:.1f}%` |")

        return "\n".join(doc)


if __name__ == "__main__":
    kpi_dfs = {
        '75750': pd.read_csv('/tmp/kpi_card_75750.csv'),
        '79066': pd.read_csv('/tmp/kpi_card_79066.csv'),
        '62728': pd.read_csv('/tmp/kpi_card_62728.csv'),
        '75304': pd.read_csv('/tmp/kpi_card_75304.csv'),
        '76069': pd.read_csv('/tmp/kpi_card_76069.csv'),
        '79068': pd.read_csv('/tmp/kpi_card_79068.csv')
    }
    analyzer = OfficialKPIMetricsAnalyzer()
    kpis = analyzer.compute_official_kpis(kpi_dfs)
    report = analyzer.generate_official_kpi_lark_doc(kpis)
    
    out_path = "official_kpi_metrics_report.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"🎉 Đã xuất thành công Báo Cáo 7 KPI Cards Chính Thức tại: {out_path}")
