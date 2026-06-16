import urllib.request
import xml.etree.ElementTree as ET
import json
import os
import datetime
from email.utils import parsedate_to_datetime

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
BASE_DIR = "/Users/ts-1148/Desktop/Pulu-workspace"
MONITOR_DIR = os.path.join(BASE_DIR, "output", "Ahamove", "06. COMPETITIVE_INTEL", "monitoring")
SIGNAL_FILE = os.path.join(MONITOR_DIR, "raw-signals.json")

os.makedirs(MONITOR_DIR, exist_ok=True)

COMPETITORS = {
    "Grab": 'GrabExpress OR "GrabBike" OR "Grab Việt Nam"',
    "Be": '"Be Delivery" OR "Be Group" OR "BeBike" OR "Be Việt Nam"',
    "XanhSM": '"XanhSM" OR "GSM" OR "GreenSM" OR "Xe máy điện Xanh"',
    "Lalamove": '"Lalamove" OR "Lalamove Việt Nam"',
    "ShopeeFood": '"ShopeeFood" OR "ShopeeFood Việt Nam"',
    "Global Platforms": '"Uber" OR "DoorDash" OR "Meituan" OR "Deliveroo" OR "Rappi" OR "iFood"'
}

def fetch_rss_signals(competitor, query):
    encoded_query = urllib.parse.quote(query)
    # Use global English news for global platforms, and Vietnamese for local ones
    if competitor == "Global Platforms":
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en&gl=US&ceid=US:en"
    else:
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=vi&gl=VN&ceid=VN:vi"
    
    signals = []
    try:
        # Fetch RSS XML
        req = urllib.request.Request(
            rss_url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            
        # Parse XML
        root = ET.fromstring(xml_data)
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ""
            link = item.find('link').text if item.find('link') is not None else ""
            pub_date_str = item.find('pubDate').text if item.find('pubDate') is not None else ""
            
            # Parse publication date
            pub_date = parsedate_to_datetime(pub_date_str) if pub_date_str else datetime.datetime.now(datetime.timezone.utc)
            
            # Only keep signals from the last 3 days to avoid duplicate bloat
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
        print(f"⚠️ Error fetching RSS signals for {competitor}: {e}")
        
    return signals

def main():
    print("🚀 Starting Competitor News Signal Crawler...")
    all_signals = []
    
    # Fetch signals for each competitor
    for competitor, query in COMPETITORS.items():
        print(f"Fetching signals for {competitor}...")
        signals = fetch_rss_signals(competitor, query)
        print(f"Found {len(signals)} recent signals for {competitor}.")
        all_signals.extend(signals)
        
    # Read existing signals
    existing_signals = []
    if os.path.exists(SIGNAL_FILE):
        try:
            with open(SIGNAL_FILE, 'r', encoding='utf-8') as f:
                existing_signals = json.load(f)
        except Exception as e:
            print(f"⚠️ Error reading existing signal file: {e}")
            
    # Merge signals based on URL uniqueness
    existing_urls = {s['url'] for s in existing_signals}
    new_signals_added = 0
    for s in all_signals:
        if s['url'] not in existing_urls:
            existing_signals.append(s)
            new_signals_added += 1
            
    # Truncate to keep only the last 200 signals to avoid file bloat
    existing_signals = sorted(
        existing_signals, 
        key=lambda x: x['published_at'], 
        reverse=True
    )[:200]
    
    # Save merged signals
    try:
        with open(SIGNAL_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_signals, f, indent=2, ensure_ascii=False)
        print(f"✅ Finished. Added {new_signals_added} new signals. Total signals tracked: {len(existing_signals)}")
        print(f"Signal log file updated: {SIGNAL_FILE}")
    except Exception as e:
        print(f"❌ Error writing signal file: {e}")

if __name__ == "__main__":
    main()
