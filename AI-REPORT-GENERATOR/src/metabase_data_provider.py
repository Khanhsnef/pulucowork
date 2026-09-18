"""
Metabase Live Data Provider.
Loads pulled API data from raw-data/api-pull-2026-08-20/ and provides
typed accessor methods for slide templates.
"""
import json
from pathlib import Path

DATA_DIR = Path("/Users/ts-1148/Desktop/Pulu-workspace/Output/Ahamove/04. OPS_METRICS/raw-data/api-pull-2026-08-20")


class MetabaseDataProvider:
    def __init__(self):
        self._seg_month = self._load("card_75557.json")
        self._seg_week = self._load("card_75557_weekly.json")
        self._city_month = self._load("card_72864.json")
        self._ar_fr_kpi = self._load("card_75750.json")
        self._overview = self._load("card_77913.json")
        self._service_perf = self._load("card_67888.json")
        self._supply_hour = self._load("card_79066.json")
        self._ctr = self._load("card_75304.json")
        self._retention = self._load("card_79068.json")

    def _load(self, filename):
        path = DATA_DIR / filename
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return []

    def get_overview(self, city: str, period_prefix: str) -> dict:
        """Get overview KPIs for a city and month prefix e.g. '2026-08'.
        city values in card_77913: 'SGN', 'HAN', 'EXP'
        """
        return next(
            (r for r in self._overview if r["city"] == city and r["period"].startswith(period_prefix)),
            {}
        )

    def get_segment_month(self, city: str, period_prefix: str, segment: str) -> dict:
        return next(
            (r for r in self._seg_month
             if r["city_id"] == city and r["period"].startswith(period_prefix) and r["driver_segment"] == segment),
            {}
        )

    def get_segment_week(self, city: str, period: str, segment: str) -> dict:
        return next(
            (r for r in self._seg_week
             if r["city_id"] == city and r["period"] == period and r["driver_segment"] == segment),
            {}
        )

    def get_supply_hour(self, city: str, period_prefix: str) -> float:
        """city prefix in metrics: '[HAN]' or '[SGN]'"""
        r = next(
            (r for r in self._supply_hour
             if f"[{city}]" in r["metrics"] and r["period"].startswith(period_prefix)),
            {}
        )
        return r.get("online_hour", 0)

    def get_retention(self, city: str, period_prefix: str) -> float:
        """city prefix in metrics: '[HAN]' or '[SGN]'"""
        r = next(
            (r for r in self._retention
             if f"[{city}]" in r.get("metrics", "") and r["period"].startswith(period_prefix)),
            {}
        )
        return r.get("retention_rate", 0)

    def get_ctr(self, period_prefix: str) -> float:
        """CTR periods use ISO format: '2026-08-01T00:00:00+07:00'"""
        r = next((r for r in self._ctr if r["period"].startswith(period_prefix)), {})
        return r.get("ctr", 0)

    def get_ar_fr_kpi(self, kpi_name_fragment: str, period_prefix: str) -> float:
        """Match by partial KPI_name e.g. '[HAN] Acceptance rate' or '[SGN] Fulfillment rate'"""
        r = next(
            (r for r in self._ar_fr_kpi
             if kpi_name_fragment in r["KPI_name"] and r["period"].startswith(period_prefix)),
            {}
        )
        return r.get("Actual", 0)

    def get_service_perf(self, region: str, service_type: str, period_prefix: str) -> dict:
        return next(
            (r for r in self._service_perf
             if r["region"] == region and r["service_type"] == service_type and r["period"].startswith(period_prefix)),
            {}
        )

    def get_summary_kpis(self) -> dict:
        """Returns flat dict of key KPIs for Aug 2026 vs Jul 2026, used in executive summary slides."""
        jul = "2026-07"
        aug = "2026-08"

        sgn_aug = self.get_overview("SGN", aug)
        sgn_jul = self.get_overview("SGN", jul)
        han_aug = self.get_overview("HAN", aug)
        han_jul = self.get_overview("HAN", jul)

        def safe_ar(r):
            return r["accept"] / r["requested"] if r.get("requested") else 0

        return {
            # Fulfillment Rate from card_75750 (more accurate than card_77913 fr field)
            "sgn_fr_aug": self.get_ar_fr_kpi("[SGN] Fulfillment rate", aug),
            "sgn_fr_jul": self.get_ar_fr_kpi("[SGN] Fulfillment rate", jul),
            "han_fr_aug": self.get_ar_fr_kpi("[HAN] Fulfillment rate", aug),
            "han_fr_jul": self.get_ar_fr_kpi("[HAN] Fulfillment rate", jul),
            # Acceptance Rate from card_75750
            "sgn_ar_aug": self.get_ar_fr_kpi("[SGN] Acceptance rate", aug),
            "sgn_ar_jul": self.get_ar_fr_kpi("[SGN] Acceptance rate", jul),
            "han_ar_aug": self.get_ar_fr_kpi("[HAN] Acceptance rate", aug),
            "han_ar_jul": self.get_ar_fr_kpi("[HAN] Acceptance rate", jul),
            # Active driver count from card_77913
            "sgn_active_aug": sgn_aug.get("active", 0),
            "han_active_aug": han_aug.get("active", 0),
            "sgn_active_jul": sgn_jul.get("active", 0),
            "han_active_jul": han_jul.get("active", 0),
            # CTR (card_75304 — period uses ISO timestamp prefix)
            "ctr_aug": self.get_ctr("2026-08"),
            "ctr_jul": self.get_ctr("2026-07"),
            # Retention (card_79068)
            "sgn_retention_aug": self.get_retention("SGN", aug),
            "han_retention_aug": self.get_retention("HAN", aug),
            "sgn_retention_jul": self.get_retention("SGN", jul),
            "han_retention_jul": self.get_retention("HAN", jul),
        }
