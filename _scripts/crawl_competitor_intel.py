import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import os
import datetime
from email.utils import parsedate_to_datetime

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
BASE_DIR = "/Users/ts-1148/Desktop/Pulu-workspace"
MONITOR_DIR = os.path.join(BASE_DIR, "Output/Ahamove/06. COMPETITIVE_INTEL", "monitoring")
SIGNAL_FILE = os.path.join(MONITOR_DIR, "raw-signals.json")
ENV_PATH = os.path.join(BASE_DIR, ".env")

os.makedirs(MONITOR_DIR, exist_ok=True)

COMPETITORS = {
    "Grab": 'GrabExpress OR "GrabBike" OR "Grab Việt Nam"',
    "Be": '"Be Delivery" OR "Be Group" OR "BeBike" OR "Be Việt Nam"',
    "XanhSM": '"XanhSM" OR "GSM" OR "GreenSM" OR "Xe máy điện Xanh"',
    "Lalamove": '"Lalamove" OR "Lalamove Việt Nam"',
    "ShopeeFood": '"ShopeeFood" OR "ShopeeFood Việt Nam"',
    "Global Platforms": '"Uber" OR "DoorDash" OR "Meituan" OR "Deliveroo" OR "Rappi" OR "iFood"'
}

FIRECRAWL_SEARCH_TARGETS = {
    "Grab": ["https://www.grab.com/vn/press/", "https://help.grab.com/driver/vi/"],
    "Be": ["https://be.com.vn/tin-tuc/"],
    "XanhSM": ["https://xanhsm.com/tin-tuc/"],
}


def load_env():
    env = {}
    if os.path.exists(ENV_PATH):
        for line in open(ENV_PATH, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            env[key.strip()] = val.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if v})
    return env


def fetch_rss_signals(competitor, query):
    encoded_query = urllib.parse.quote(query)
    if competitor == "Global Platforms":
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en&gl=US&ceid=US:en"
    else:
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=vi&gl=VN&ceid=VN:vi"

    signals = []
    try:
        req = urllib.request.Request(
            rss_url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        for item in root.findall(".//item"):
            title = item.find("title").text if item.find("title") is not None else ""
            link = item.find("link").text if item.find("link") is not None else ""
            pub_date_str = item.find("pubDate").text if item.find("pubDate") is not None else ""
            pub_date = parsedate_to_datetime(pub_date_str) if pub_date_str else datetime.datetime.now(datetime.timezone.utc)

            cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=3)
            if pub_date >= cutoff:
                signals.append({
                    "competitor": competitor,
                    "title": title,
                    "url": link,
                    "published_at": pub_date.isoformat(),
                    "source": "Google News RSS",
                    "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                })
    except Exception as e:
        print(f"⚠️ RSS error for {competitor}: {e}")

    return signals


def fetch_firecrawl_signals(competitor, urls, api_key):
    """Scrape competitor pages via Firecrawl API → richer content than RSS."""
    signals = []
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    for url in urls:
        try:
            payload = json.dumps({
                "url": url,
                "formats": ["markdown"],
                "onlyMainContent": True,
            }).encode()
            req = urllib.request.Request(
                "https://api.firecrawl.dev/v1/scrape",
                data=payload,
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())

            if data.get("success") and data.get("data", {}).get("markdown"):
                content = data["data"]["markdown"][:2000]  # cap to avoid huge payloads
                signals.append({
                    "competitor": competitor,
                    "title": f"[Firecrawl] {url}",
                    "url": url,
                    "content_preview": content,
                    "published_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "source": "Firecrawl",
                    "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                })
                print(f"  ✅ Firecrawl OK: {url}")
        except Exception as e:
            print(f"  ⚠️ Firecrawl error {url}: {e}")

    return signals


def firecrawl_search(query, api_key, limit=5):
    """Use Firecrawl /search endpoint for broader web coverage."""
    signals = []
    try:
        payload = json.dumps({"query": query, "limit": limit}).encode()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        req = urllib.request.Request(
            "https://api.firecrawl.dev/v1/search",
            data=payload,
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())

        for item in data.get("data", []):
            signals.append({
                "competitor": "Search",
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content_preview": item.get("markdown", "")[:500],
                "published_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "source": "Firecrawl Search",
                "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
    except Exception as e:
        print(f"⚠️ Firecrawl search error: {e}")

    return signals


def main():
    print("🚀 Starting Competitor Intel Crawler...")
    env = load_env()
    firecrawl_key = env.get("FIRECRAWL_API_KEY", "")

    all_signals = []

    # ── Layer 1: Google News RSS (always runs) ────────────────────────────────
    print("\n📡 Layer 1: Google News RSS")
    for competitor, query in COMPETITORS.items():
        print(f"  Fetching {competitor}...")
        sigs = fetch_rss_signals(competitor, query)
        print(f"  → {len(sigs)} signals")
        all_signals.extend(sigs)

    # ── Layer 2: Firecrawl page scrape (if API key present) ───────────────────
    if firecrawl_key:
        print("\n🔥 Layer 2: Firecrawl direct scrape")
        for competitor, urls in FIRECRAWL_SEARCH_TARGETS.items():
            sigs = fetch_firecrawl_signals(competitor, urls, firecrawl_key)
            all_signals.extend(sigs)

        # ── Layer 3: Firecrawl web search ─────────────────────────────────────
        print("\n🔍 Layer 3: Firecrawl web search")
        search_queries = [
            "Grab Express Vietnam khuyến mãi tài xế 2026",
            "Be Delivery Vietnam promo driver June 2026",
            "XanhSM tuyển tài xế xe điện 2026",
        ]
        for q in search_queries:
            sigs = firecrawl_search(q, firecrawl_key, limit=3)
            all_signals.extend(sigs)
    else:
        print("\n⚠️  FIRECRAWL_API_KEY not set — skipping Layers 2 & 3.")
        print("   Add FIRECRAWL_API_KEY=fc-xxx to .env to enable full scraping.")

    # ── Merge & dedupe ────────────────────────────────────────────────────────
    existing_signals = []
    if os.path.exists(SIGNAL_FILE):
        try:
            with open(SIGNAL_FILE, "r", encoding="utf-8") as f:
                existing_signals = json.load(f)
        except Exception as e:
            print(f"⚠️ Error reading signal file: {e}")

    existing_urls = {s["url"] for s in existing_signals}
    new_count = 0
    for s in all_signals:
        if s["url"] not in existing_urls:
            existing_signals.append(s)
            new_count += 1
            existing_urls.add(s["url"])

    # Keep last 300 signals (increased from 200 to accommodate Firecrawl)
    existing_signals = sorted(
        existing_signals,
        key=lambda x: x["published_at"],
        reverse=True
    )[:300]

    with open(SIGNAL_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_signals, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done. +{new_count} new signals. Total: {len(existing_signals)}")
    print(f"   Saved to: {SIGNAL_FILE}")
    if not firecrawl_key:
        print("\n   To enable Firecrawl: add FIRECRAWL_API_KEY=fc-... to .env")
        print("   Get free API key at: https://firecrawl.dev")


if __name__ == "__main__":
    main()
