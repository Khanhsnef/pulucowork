"""Module News & Sentiment — 2 tầng scoring.

Tầng 1 (free, tức thì): rule-based keyword scoring tiếng Việt + tiếng Anh.
Tầng 2 (on-demand):     LLM scoring qua `claude -p` headless — xem llm_scoring.py.

Nguồn tin lấy theo danh mục nguồn uy tín của Khanh
(vn_stock_and_crypto_trusted_sources.md):
- VN stock : Vietstock RSS, CafeF RSS (báo chí chuyên ngành, tin doanh nghiệp)
- Crypto   : Binance announcements, CoinDesk RSS, The Block RSS
- Vĩ mô VN : VnEconomy RSS

Store: SQLite append-only, dedup theo hash(title). Fetch qua stdlib
(urllib + xml.etree) — không thêm dependency mới.
"""

from __future__ import annotations

import hashlib
import re
import sqlite3
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data_cache" / "news.sqlite"

# ── Nguồn RSS (từ danh mục nguồn uy tín) ─────────────────────────────────────
VN_FEEDS = [
    ("vietstock", "https://vietstock.vn/830/chung-khoan/co-phieu.rss"),
    ("vietstock-vimo", "https://vietstock.vn/761/kinh-te/vi-mo.rss"),
    ("cafef-ck", "https://cafef.vn/thi-truong-chung-khoan.rss"),
    ("cafef-vimo", "https://cafef.vn/vi-mo-dau-tu.rss"),
    ("vneconomy", "https://vneconomy.vn/chung-khoan.rss"),
]
CRYPTO_FEEDS = [
    ("coindesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("theblock", "https://www.theblock.co/rss.xml"),
    ("cointelegraph", "https://cointelegraph.com/rss"),
]

FETCH_TIMEOUT = 12
UA = "Mozilla/5.0 (TradingSystem/2.0; personal research tool)"


# ── Rule-based sentiment lexicon (tầng 1, free) ──────────────────────────────
# Trọng số: ±3 tin rất mạnh (pháp lý/sự kiện lớn), ±2 mạnh, ±1 thường.
NEG_VI = {
    r"khởi tố|bắt tạm giam|truy tố|lừa đảo|chiếm đoạt": -3,
    r"thanh tra|điều tra|xử phạt|vi phạm|cưỡng chế thuế": -2,
    r"hủy niêm yết|đình chỉ giao dịch|diện cảnh báo|kiểm soát đặc biệt": -3,
    r"thua lỗ|lỗ ròng|lỗ lũy kế|âm vốn": -2,
    r"giảm sàn|bán tháo|thoái vốn ồ ạt|dư bán sàn": -2,
    r"lợi nhuận giảm|doanh thu giảm|sụt giảm|đi lùi": -1,
    r"nợ xấu|áp lực nợ|mất khả năng thanh toán|vỡ nợ": -2,
    r"cắt giảm nhân sự|đóng cửa nhà máy|dừng dự án": -1,
    r"khối ngoại bán ròng": -1,
}
POS_VI = {
    r"lãi kỷ lục|lợi nhuận kỷ lục|doanh thu kỷ lục": 3,
    r"vượt kế hoạch|hoàn thành sớm|về đích sớm": 2,
    r"lợi nhuận tăng|doanh thu tăng|tăng trưởng": 1,
    r"trúng thầu|ký hợp đồng|mở rộng nhà máy|dự án mới": 2,
    r"chia cổ tức|cổ tức tiền mặt|phát hành thêm.*giá ưu đãi": 1,
    r"khối ngoại mua ròng|tự doanh mua ròng": 1,
    r"nâng hạng|thăng hạng|vào rổ chỉ số|FTSE|MSCI": 3,
    r"nới room|tăng room ngoại": 2,
    r"giảm lãi suất|hạ lãi suất điều hành|nới lỏng tiền tệ": 2,
    r"đầu tư công|giải ngân.*tăng": 1,
}
NEG_EN = {
    r"\bhack(ed)?\b|\bexploit(ed)?\b|\brug ?pull\b|\bscam\b": -3,
    r"\bban(ned)?\b|\bcrackdown\b|\blawsuit\b|\bsue[sd]?\b|\bSEC charges\b": -2,
    r"\bdelist(ing|ed)?\b|\bliquidation(s)?\b|\bbankrupt(cy)?\b|\binsolven": -3,
    r"\bsell-?off\b|\bplunge[sd]?\b|\bcrash(ed|es)?\b|\btumble[sd]?\b": -2,
    r"\boutflow(s)?\b|\bdump(ed|ing)?\b|\bfear\b|\bbearish\b": -1,
    r"\brate hike\b|\btightening\b|\bhawkish\b": -1,
}
POS_EN = {
    r"\bETF approv(al|ed)\b|\binstitutional adoption\b|\bhalving\b": 3,
    r"\blist(ing|ed)? on\b|\bpartnership\b|\bintegration\b|\bmainnet\b": 2,
    r"\ball-?time high\b|\brally\b|\bsurge[sd]?\b|\bbreakout\b": 2,
    r"\binflow(s)?\b|\baccumulation\b|\bbullish\b|\bupgrade[sd]?\b": 1,
    r"\brate cut\b|\beasing\b|\bdovish\b|\bstimulus\b": 2,
}


@dataclass
class NewsItem:
    id: str                  # hash(title)
    source: str
    title: str
    link: str
    published: str           # ISO
    market: str              # 'vn' | 'crypto'
    matched_symbols: str     # CSV các mã trong watchlist khớp
    rule_score: int          # tổng điểm keyword (±)
    rule_hits: str           # keyword đã khớp, để debug/hiển thị


# ─────────────────────────────────────────────────────────────────────────────
# Store
# ─────────────────────────────────────────────────────────────────────────────
def _db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS news (
        id TEXT PRIMARY KEY, source TEXT, title TEXT, link TEXT,
        published TEXT, market TEXT, matched_symbols TEXT,
        rule_score INTEGER, rule_hits TEXT, fetched_at TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS llm_scores (
        symbol TEXT, scored_at TEXT, score INTEGER, n_items INTEGER,
        summary TEXT, detail_json TEXT,
        PRIMARY KEY (symbol, scored_at))""")
    return conn


# ─────────────────────────────────────────────────────────────────────────────
# Fetch RSS (stdlib only)
# ─────────────────────────────────────────────────────────────────────────────
def _fetch_feed(name: str, url: str) -> list[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as r:
            raw = r.read()
    except Exception:
        return []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []
    out = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        if not title:
            continue
        pub = item.findtext("pubDate") or ""
        try:
            pub_iso = parsedate_to_datetime(pub).isoformat()
        except Exception:
            pub_iso = datetime.now().isoformat(timespec="seconds")
        out.append({"source": name, "title": title,
                    "link": (item.findtext("link") or "").strip(),
                    "published": pub_iso})
    return out


def _score_rules(title: str, market: str) -> tuple[int, list[str]]:
    t = title.lower()
    score, hits = 0, []
    lex = [(NEG_VI, POS_VI), (NEG_EN, POS_EN)][1 if market == "crypto" else 0]
    for table in lex:
        for pattern, w in table.items():
            if re.search(pattern, t, re.IGNORECASE):
                score += w
                hits.append(pattern.split("|")[0].replace("\\b", ""))
    return score, hits


def _match_symbols(title: str, market: str, watchlist: dict) -> list[str]:
    t = title.upper()
    matched = []
    if market == "vn":
        for sym in watchlist.get("vn_stocks", []):
            if re.search(rf"\b{sym}\b", t):
                matched.append(sym)
    else:
        for sym in watchlist.get("crypto", []):
            base = sym.replace("USDT", "").replace("BUSD", "")
            names = {"BTC": ["BTC", "BITCOIN"], "ETH": ["ETH", "ETHEREUM"],
                     "BNB": ["BNB", "BINANCE COIN"], "SOL": ["SOL", "SOLANA"],
                     "XRP": ["XRP", "RIPPLE"], "DOGE": ["DOGE", "DOGECOIN"]}
            for alias in names.get(base, [base]):
                if re.search(rf"\b{alias}\b", t):
                    matched.append(sym)
                    break
    return matched


def refresh_news(watchlist: dict) -> dict:
    """Kéo mọi feed, dedup, chấm rule score, lưu SQLite. Trả thống kê."""
    conn = _db()
    n_new = 0
    for market, feeds in (("vn", VN_FEEDS), ("crypto", CRYPTO_FEEDS)):
        for name, url in feeds:
            for it in _fetch_feed(name, url):
                nid = hashlib.sha1(it["title"].encode()).hexdigest()[:16]
                if conn.execute("SELECT 1 FROM news WHERE id=?", (nid,)).fetchone():
                    continue
                score, hits = _score_rules(it["title"], market)
                syms = _match_symbols(it["title"], market, watchlist)
                conn.execute("INSERT OR IGNORE INTO news VALUES (?,?,?,?,?,?,?,?,?,?)",
                             (nid, it["source"], it["title"], it["link"], it["published"],
                              market, ",".join(syms), score, ",".join(hits),
                              datetime.now().isoformat(timespec="seconds")))
                n_new += 1
    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM news").fetchone()[0]
    conn.close()
    return {"new_items": n_new, "total_items": total}


# ─────────────────────────────────────────────────────────────────────────────
# Aggregate → News Score (tầng 1)
# ─────────────────────────────────────────────────────────────────────────────
def rule_news_score(symbol: str, market: str, days: int = 7) -> dict:
    """Điểm 1-100 từ rule scoring: 50 = trung tính.

    Tin khớp đúng mã: trọng số x3. Tin thị trường chung: x1.
    Decay theo tuổi tin: exp(-age/3 ngày).
    """
    import math
    conn = _db()
    since = (datetime.now() - timedelta(days=days)).isoformat()
    rows = conn.execute(
        "SELECT title, published, matched_symbols, rule_score, rule_hits FROM news "
        "WHERE market=? AND published>=? ORDER BY published DESC", (market, since)).fetchall()
    conn.close()

    weighted, n_direct, items = 0.0, 0, []
    for title, pub, syms, score, hits in rows:
        if score == 0:
            continue
        try:
            age_days = max(0.0, (datetime.now() - datetime.fromisoformat(pub).replace(tzinfo=None)).total_seconds() / 86400)
        except Exception:
            age_days = days
        decay = math.exp(-age_days / 3)
        direct = symbol in (syms or "").split(",")
        w = 3.0 if direct else 1.0
        weighted += score * w * decay
        if direct:
            n_direct += 1
            items.append({"title": title, "score": score, "hits": hits})
    # Không có tin trực tiếp về mã → tin chung chỉ được kéo lệch tối đa ±15 điểm
    # (tránh score cực đoan chỉ vì sentiment thị trường chung).
    delta = weighted * 2
    if n_direct == 0:
        delta = max(-15.0, min(15.0, delta * 0.5))
    final = int(max(1, min(100, 50 + delta)))
    return {"score": final, "n_scanned": len(rows), "n_direct": n_direct,
            "direct_items": items[:10],
            "label": "Tích cực" if final >= 60 else ("Tiêu cực" if final <= 40 else "Trung tính")}


def recent_news(symbol: str, market: str, days: int = 7, limit: int = 20) -> list[dict]:
    """Tin mới nhất: tin khớp mã trước, rồi tin chung có score != 0."""
    conn = _db()
    since = (datetime.now() - timedelta(days=days)).isoformat()
    rows = conn.execute(
        "SELECT source, title, link, published, matched_symbols, rule_score FROM news "
        "WHERE market=? AND published>=? ORDER BY published DESC LIMIT 300",
        (market, since)).fetchall()
    conn.close()
    direct = [r for r in rows if symbol in (r[4] or "").split(",")]
    general = [r for r in rows if r not in direct and r[5] != 0]
    out = []
    for src, title, link, pub, _, score in (direct + general)[:limit]:
        out.append({"source": src, "title": title, "link": link,
                    "published": pub[:16].replace("T", " "), "rule_score": score,
                    "impact": "Tích cực" if score > 0 else ("Tiêu cực" if score < 0 else "Trung lập")})
    return out


# ─────────────────────────────────────────────────────────────────────────────
# LLM scores store (tầng 2 ghi vào đây — xem llm_scoring.py)
# ─────────────────────────────────────────────────────────────────────────────
def save_llm_score(symbol: str, score: int, n_items: int, summary: str, detail_json: str) -> None:
    conn = _db()
    conn.execute("INSERT OR REPLACE INTO llm_scores VALUES (?,?,?,?,?,?)",
                 (symbol, datetime.now().isoformat(timespec="seconds"),
                  score, n_items, summary, detail_json))
    conn.commit()
    conn.close()


def latest_llm_score(symbol: str) -> dict | None:
    conn = _db()
    row = conn.execute(
        "SELECT scored_at, score, n_items, summary, detail_json FROM llm_scores "
        "WHERE symbol=? ORDER BY scored_at DESC LIMIT 1", (symbol,)).fetchone()
    conn.close()
    if not row:
        return None
    return {"scored_at": row[0][:16].replace("T", " "), "score": row[1],
            "n_items": row[2], "summary": row[3]}
