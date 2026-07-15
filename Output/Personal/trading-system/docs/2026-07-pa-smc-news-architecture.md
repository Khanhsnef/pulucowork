# Kiến trúc V2 — Price Action/SMC + News/Macro NLP + Multi-tier Zones

*Cập nhật: 2026-07-15 · Trạng thái: PA/SMC đã triển khai ✅ · News/Macro chờ confirm nguồn dữ liệu ⏳*

## 1. Sơ đồ hệ thống dữ liệu (Data Architecture)

```text
                        ┌────────────────────────────┐
                        │        USER INPUT          │
                        │  FPT | HPG | BTCUSDT ...   │
                        └─────────────┬──────────────┘
                                      ▼
        ┌─────────────────────────────────────────────────────┐
        │                   ASSET ROUTER                       │
        └───┬──────────────────┬──────────────────────┬────────┘
            ▼                  ▼                      ▼
   ┌────────────────┐ ┌────────────────┐  ┌─────────────────────┐
   │ PRICE STORE    │ │ FUNDAMENTAL    │  │ NEWS/MACRO STORE    │
   │ (đã có)        │ │ STORE (đã có)  │  │ (MỚI — phase 2)     │
   │ vnstock OHLCV  │ │ vnstock BCTC   │  │ RSS CafeF/VnEconomy │
   │ Binance klines │ │ Binance ticker │  │ Binance announcements│
   │ Parquet 12h TTL│ │ funding/depth  │  │ GDELT (địa chính trị)│
   └───────┬────────┘ └───────┬────────┘  │ SBV/Fed rate (API)  │
           │                  │           │ SQLite + dedup hash │
           │                  │           └──────────┬──────────┘
           ▼                  ▼                      ▼
   ┌───────────────────────────────────────────────────────────┐
   │                    ANALYSIS LAYER                          │
   │  ┌─────────────┐ ┌──────────────┐ ┌───────────────────┐  │
   │  │ TA Engine   │ │ FA Gate      │ │ NLP Sentiment     │  │
   │  │ (đã có)     │ │ + F-Score    │ │ Engine (phase 2)  │  │
   │  │             │ │ + Z-Score    │ │ 2 tầng: keyword   │  │
   │  ├─────────────┤ │ (phase 2)    │ │ rule → LLM judge  │  │
   │  │ PA/SMC ✅   │ └──────────────┘ └───────────────────┘  │
   │  │ BOS/CHoCH   │                                          │
   │  │ OB/FVG/Liq  │                                          │
   │  │ VCP/Pinbar  │                                          │
   │  └─────────────┘                                          │
   └────────────────────────────┬──────────────────────────────┘
                                ▼
   ┌───────────────────────────────────────────────────────────┐
   │        BACKTEST + WALK-FORWARD OPTIMIZER (đã có)           │
   │  Grid: RSI/ATR/TP-R  +  PA params (fvg_min_atr, ob_vol,   │
   │  pivot_k...) — phase 2 gộp chung một lưới walk-forward     │
   └────────────────────────────┬──────────────────────────────┘
                                ▼
   ┌───────────────────────────────────────────────────────────┐
   │              DECISION ENGINE (đã nâng cấp ✅)               │
   │  TA signal × FA gate × PA structure filter × News score    │
   │  → MUA/BÁN/ĐỨNG NGOÀI theo 3 khung + conviction            │
   │  → Multi-tier zones (Tier 1 An toàn / Tier 2 Tấn công)     │
   │  → Invalidation level từ Market Structure                  │
   └────────────────────────────┬──────────────────────────────┘
                                ▼
              JSON + Markdown + Web UI (dark TradingView)
```

**Điểm thiết kế then chốt:**
- News store là **append-only SQLite** (không phải Parquet như giá) vì tin tức cần dedup theo `hash(title)`, query theo khoảng thời gian, và giữ vĩnh viễn để backtest sentiment.
- Mọi score từ NLP đều lưu kèm **model version + timestamp** để tái lập (reproducibility).
- PA scan chạy **sau** cleaning, **trước** decision — kết quả nhúng vào `Decision.price_action`.

## 2. Thuật toán xử lý tin tức Vĩ mô bằng LLM/NLP (phase 2 — thiết kế)

### 2.1 Pipeline 2 tầng (rẻ trước, đắt sau)

```text
RSS/API feeds ──▶ Dedup (hash title+source)
                       │
                       ▼
        TẦNG 1: Rule-based Pre-filter (mọi tin, ~0 chi phí)
        - Keyword map theo mã: "FPT" ← {FPT, FRT chuỗi, công nghệ...}
        - Phân loại thô: earnings / policy / geopolitics / sector
        - Bỏ tin không liên quan → giảm 90% khối lượng
                       │
                       ▼
        TẦNG 2: LLM Structured Scoring (chỉ tin đã lọc, batch 10 tin/call)
        - Model: Claude Haiku (rẻ, đủ cho scoring) qua API
        - Prompt trả JSON THEO SCHEMA CỐ ĐỊNH:
          {
            "relevance": 0-100,        // mức liên quan trực tiếp tới mã
            "sentiment": -100..+100,   // tiêu cực ↔ tích cực
            "horizon": "short|mid|long", // tác động chủ yếu khung nào
            "impact_channel": "demand|supply|cost|regulation|flow",
            "weight": 1-5,             // trọng số ảnh hưởng
            "one_line_vi": "tóm tắt 1 câu tiếng Việt"
          }
        - Guardrail: temperature=0, JSON schema validation, retry 1 lần
                       │
                       ▼
        AGGREGATION → News Score (1-100) mỗi mã:
        score = 50 + Σ(sentiment_i × weight_i × decay(age_i)) / Σ(weight_i) / 2
        - decay: exp(-age_days/7) cho short, /30 cho mid, /90 cho long
        - Tách 3 score: news_short, news_mid, news_long
        - Political risk flag riêng nếu có tin geopolitics weight ≥ 4
```

### 2.2 Nguồn dữ liệu đề xuất (cần Khanh confirm)

| Nguồn | Loại | Phí | Ghi chú |
| :--- | :--- | :--- | :--- |
| CafeF RSS / Vietstock RSS | Tin doanh nghiệp VN | Free | Scraping title + summary, tôn trọng robots.txt |
| VnEconomy / TBKTVN RSS | Vĩ mô VN (lãi suất, tỷ giá) | Free | |
| Binance Announcements API | Listing/delisting, quy định | Free | Tác động mạnh ngắn hạn crypto |
| GDELT 2.0 API | Địa chính trị toàn cầu | Free | Query theo country+theme, có tone score sẵn |
| FiinGroup / WiChart API | F-Score, Z-Score tính sẵn | Trả phí | HOẶC tự tính từ vnstock BCTC (free, chậm hơn) |
| Claude API (Haiku) | LLM scoring | ~$0.25/1M tokens | ~200 tin/ngày ≈ $0.05/ngày |

### 2.3 F-Score & Z-Score (tự tính từ vnstock, không cần mua API)

- **Piotroski F-Score (0-9):** 9 tiêu chí từ BCTC 2 năm — ROA>0, CFO>0, ΔROA>0, CFO>LNST (accruals), Δđòn bẩy<0, Δthanh khoản>0, không pha loãng CP, Δbiên gộp>0, Δvòng quay tài sản>0. Map field từ `stock.finance.balance_sheet() / income_statement() / cash_flow()`.
- **Altman Z-Score (bản emerging market):** Z = 3.25 + 6.56×X1 + 3.26×X2 + 6.72×X3 + 1.05×X4. Ngưỡng: >5.85 an toàn, 4.35-5.85 xám, <4.35 nguy hiểm.
- Cả 2 nhúng vào `FAGate.details`, tính lại mỗi quý.

## 3. Những gì ĐÃ triển khai turn này (PA/SMC core)

| Thành phần | File | Logic chính |
| :--- | :--- | :--- |
| Swing pivots | `price_action.py:find_pivots` | Fractal k-bar, confirm trễ k bar — không look-ahead |
| BOS/CHoCH | `detect_structure` | Máy trạng thái tuần tự theo bar, close phá swing → event |
| Order Blocks | `extract_order_blocks` | Nến ngược chiều cuối trước break + lọc volume ≥1.2×SMA20 (VSA) |
| FVG | `extract_fvgs` | Gap 3 nến ≥ 0.3×ATR, track mitigated/invalidated |
| Liquidity Pools | `find_liquidity_pools` | Equal highs/lows trong 0.15×ATR, track swept |
| Pinbar/Engulfing | `detect_reversal_patterns` | Chỉ tại key levels (OB/liquidity/protected swing) + VSA ≥1.5× |
| VCP | `detect_vcp` | 3 sóng co dần ≤75% + volume giảm + giá sát pivot line |
| **Win rate thật** | `replay_ob_retest`, `replay_sweep_reclaim` | Replay từng setup lịch sử với SL-trước-TP, fill giá open |
| Multi-tier zones | `_build_tiers` | Tier 1 = OB retest thuận trend; Tier 2 = liquidity sweep&reclaim |
| Invalidation | từ `StructureEvent.origin_level` | Protected swing của cấu trúc hiện tại |

**Tích hợp:** `Decision.price_action` (JSON đầy đủ) + section mới trong Markdown report + card mới trên Web UI + PA trend filter điều chỉnh conviction của khuyến nghị chính.

## 4. Việc còn lại (phase 2 — chờ confirm)

1. **News/NLP module** — cần chốt: nguồn RSS nào, có dùng Claude API không (cần API key), tần suất poll (đề xuất 1h/lần cùng scheduler).
2. **F-Score/Z-Score** — tự tính từ vnstock (free) hay mua FiinGroup.
3. **PA params vào walk-forward grid** — thêm `fvg_min_atr`, `ob_vol_mult`, `pivot_k` vào `DEFAULT_PARAM_GRID` (lưới tăng ~27×, cần chuyển grid search sang random search 200 mẫu để giữ tốc độ).
4. **Multi-timeframe structure** — hiện chỉ daily; thêm weekly resample để lọc trend lớn.
```
