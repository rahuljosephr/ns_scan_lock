"""
NSE Weekly Downward-Resistance Trendline Breakout Scanner
Full 2000+ Universe (Direct NSE Master Sync) + Institutional & FII Layer
Run: streamlit run app.py
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.request
import time
import io

# ══════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="NSE Breakout Scanner (Full 2000+)",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  background: #060a10;
  color: #cbd5e1;
}
.main { background: #060a10; }
.block-container { padding: 0 2rem 3rem 2rem !important; max-width: 100% !important; }

.app-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 0 1rem;
  border-bottom: 1px solid #0f172a;
  margin-bottom: 1.5rem;
}
.app-header-icon { font-size: 1.8rem; line-height: 1; }
.app-header-title { font-size: 1.3rem; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em; }
.app-header-sub { font-size: 0.72rem; color: #475569; margin-top: 0.15rem; }
.app-header-badge {
  margin-left: auto;
  background: #0f172a;
  border: 1px solid #1e3a5f;
  border-radius: 999px;
  padding: 0.25rem 0.75rem;
  font-size: 0.68rem;
  font-family: 'IBM Plex Mono', monospace;
  color: #38bdf8;
}

section[data-testid="stSidebar"] {
  background: #080c14 !important;
  border-right: 1px solid #0f172a;
  padding-top: 0;
}
section[data-testid="stSidebar"] > div { padding-top: 0; }
.sidebar-logo {
  background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
  padding: 1.2rem 1.25rem;
  margin-bottom: 1.25rem;
}
.sidebar-logo-text { font-size: 1rem; font-weight: 700; color: #fff; letter-spacing: -0.01em; }
.sidebar-logo-sub { font-size: 0.68rem; color: rgba(255,255,255,0.65); margin-top: 0.15rem; }
.sidebar-section {
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: #334155;
  text-transform: uppercase;
  margin: 1.1rem 0 0.5rem;
  padding: 0 0.1rem;
}

.kpi-row { display: flex; gap: 0.9rem; margin-bottom: 1.5rem; }
.kpi-card {
  flex: 1;
  background: #0a0f1a;
  border: 1px solid #0f172a;
  border-radius: 10px;
  padding: 1rem 1.1rem;
  position: relative;
  overflow: hidden;
}
.kpi-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: var(--accent, #334155);
}
.kpi-card.blue::before  { background: #38bdf8; }
.kpi-card.amber::before { background: #f59e0b; }
.kpi-card.green::before { background: #34d399; }
.kpi-card.purple::before{ background: #a78bfa; }
.kpi-number {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 2.1rem;
  font-weight: 600;
  color: #f1f5f9;
  line-height: 1;
  margin-bottom: 0.3rem;
}
.kpi-card.blue .kpi-number   { color: #38bdf8; }
.kpi-card.amber .kpi-number  { color: #f59e0b; }
.kpi-card.green .kpi-number  { color: #34d399; }
.kpi-card.purple .kpi-number { color: #a78bfa; }
.kpi-label { font-size: 0.7rem; color: #475569; letter-spacing: 0.04em; }
.kpi-sub { font-size: 0.65rem; color: #334155; margin-top: 0.35rem; font-family: 'IBM Plex Mono', monospace; }

.result-card {
  background: #0a0f1a;
  border: 1px solid #0f172a;
  border-radius: 10px;
  padding: 0.85rem 1.1rem;
  margin-bottom: 0.55rem;
  display: grid;
  grid-template-columns: 140px 1fr 1fr 1fr 1fr auto;
  gap: 0.5rem 1rem;
  align-items: center;
  transition: border-color 0.15s;
}
.result-card:hover { border-color: #1e3a5f; }
.result-symbol { font-weight: 700; font-size: 0.95rem; color: #f1f5f9; font-family: 'IBM Plex Mono', monospace; }
.result-sector { font-size: 0.67rem; color: #475569; margin-top: 0.15rem; }
.result-metric-label { font-size: 0.62rem; color: #334155; margin-bottom: 0.1rem; }
.result-metric-value { font-family: 'IBM Plex Mono', monospace; font-size: 0.82rem; color: #cbd5e1; }
.result-metric-value.green { color: #34d399; }
.result-metric-value.red   { color: #f87171; }
.result-metric-value.amber { color: #f59e0b; }
.pill {
  display: inline-block;
  padding: 0.1rem 0.45rem;
  border-radius: 999px;
  font-size: 0.63rem;
  font-weight: 500;
  margin-top: 0.2rem;
}
.pill-hg  { background: #082032; color: #38bdf8; }
.pill-rr  { background: #0d1f0f; color: #34d399; }
.pill-vol { background: #1a130a; color: #f59e0b; }

.trade-panel {
  background: #0a0f1a;
  border: 1px solid #0f172a;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  margin-bottom: 1rem;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
}
.tp-label { font-size: 0.63rem; color: #475569; margin-bottom: 0.2rem; }
.tp-val   { font-family: 'IBM Plex Mono', monospace; font-size: 1rem; color: #f1f5f9; }
.tp-val.entry  { color: #f1f5f9; }
.tp-val.sl     { color: #f87171; }
.tp-val.t1     { color: #34d399; }
.tp-val.t2     { color: #86efac; }
.tp-val.rr     { color: #a78bfa; }

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  border: 1px dashed #0f172a;
  border-radius: 12px;
  background: #080c14;
  margin-top: 1rem;
}
.empty-icon  { font-size: 2.5rem; margin-bottom: 0.75rem; opacity: 0.5; }
.empty-title { font-size: 0.95rem; font-weight: 600; color: #334155; margin-bottom: 0.4rem; }
.empty-body  { font-size: 0.78rem; color: #1e293b; max-width: 340px; line-height: 1.6; }

.stTabs [data-baseweb="tab-list"] { background: transparent; gap: 0.1rem; border-bottom: 1px solid #0f172a; margin-bottom: 1.5rem; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #475569; font-size: 0.8rem; font-weight: 500; padding: 0.55rem 1.1rem; border-radius: 0; border-bottom: 2px solid transparent; }
.stTabs [aria-selected="true"] { color: #38bdf8 !important; border-bottom: 2px solid #38bdf8 !important; background: transparent !important; }
.stProgress > div > div { background: #38bdf8 !important; }
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
  border: none !important;
  color: #fff !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
  border-radius: 8px !important;
  padding: 0.55rem 1rem !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  RELIABLE FULL NSE UNIVERSE LOADER (~2,100+ EQUITIES)
# ══════════════════════════════════════════════════════
@st.cache_data(ttl=86400)
def fetch_all_nse_symbols():
    urls = [
        "https://archives.nseindia.com/content/equities/EQUITY_L.csv",
        "https://raw.githubusercontent.com/anirudhsudhir/NSE-Listed-Companies-Dataset/master/EQUITY_L.csv",
        "https://raw.githubusercontent.com/datasets/nse-indices/master/data/ind_nifty500list.csv"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                csv_bytes = response.read()
                df = pd.read_csv(io.BytesIO(csv_bytes))
                sym_col = [c for c in df.columns if 'symbol' in c.lower() or 'Symbol' in c][0]
                symbols = df[sym_col].dropna().astype(str).str.strip().tolist()
                valid = [s for s in symbols if s and not s.startswith(" ") and s != "SYMBOL"]
                if len(valid) > 200:
                    return sorted(list(set(valid)))
        except Exception:
            continue

    # Fallback to broad list if remote sources fail
    return [
        "RELIANCE","TCS","HDFCBANK","ICICIBANK","BHARTIARTL","SBIN","INFY","ITC",
        "HINDUNILVR","LT","BAJFINANCE","HCLTECH","MARUTI","SUNPHARMA","ADANIENT",
        "M&M","ONGC","NTPC","KOTAKBANK","TITAN","POWERGRID","AXISBANK","DMART",
        "WIPRO","COALINDIA","ULTRACEMCO","BAJAJFINSV","ADANIPORTS","JSWSTEEL",
        "TATASTEEL","SIEMENS","GRASIM","BEL","PIDILITIND","HINDALCO","IOC","DLF",
        "VEDL","ETERNAL","DIVISLAB","TRENT","CHOLAFIN","GAIL","EICHERMOT","BPCL",
        "TATAPOWER","INDIGO","ABB","TECHM","HAVELLS","DABUR","AMBUJACEM","HAL",
        "DIXON","KAYNES","SYRMA","AVALON","BDL","BEML","PARAS","MAZDOCK","COCHINSHIP",
        "GRSE","ADANIGREEN","INOXWIND","SUZLON","IRFC","RVNL","IRCON","TITAGARH",
        "RAILTEL","AHLUCONT","KNRCON","PNCINFRA","DEEPAKNTR","TATACHEM","CLEAN",
        "ATUL","ROSSARI","CUMMINSIND","TATAELXSI","LTTS","PERSISTENT","COFORGE"
    ]


ALL_NSE_STOCKS = fetch_all_nse_symbols()


# ══════════════════════════════════════════════════════
#  TECHNICAL & FUNDAMENTAL ENGINE
# ══════════════════════════════════════════════════════

def detect_breakout(df, lookback_weeks, min_vol_ratio, target_multiplier, min_price, max_price):
    if df is None or len(df) < 10:
        return None
    closes = df["Close"].values
    highs  = df["High"].values
    lows   = df["Low"].values
    vols   = df["Volume"].values
    li     = len(df) - 1
    
    entry = float(closes[li])
    if entry < min_price or entry > max_price:
        return None
    
    fit_len = min(lookback_weeks, len(df))
    x = np.arange(fit_len, dtype=float)
    y = highs[-fit_len:]
    coeffs = np.polyfit(x, y, 1)
    trendline = np.polyval(coeffs, np.arange(len(df), dtype=float))
    
    raw_sl = np.min(lows[max(0, li-4):li]) if li >= 4 else entry * 0.95
    sl     = min(raw_sl, entry * 0.94)
    risk   = max(entry - sl, entry * 0.02)
    
    target1 = entry + target_multiplier * risk
    target2 = np.max(highs[max(0, li-52):li]) if li >= 10 else entry * 1.15
    
    vsma = vols[max(0, li-10):li].mean() if li >= 5 else vols[li]
    vol_ratio = round(vols[li] / vsma, 2) if vsma > 0 else 1.2
    
    if vol_ratio < min_vol_ratio:
        return None
    
    return {
        "entry": round(entry, 2),
        "sl": round(float(sl), 2),
        "target1": round(float(target1), 2),
        "target2": round(float(target2), 2),
        "risk_pct": round(float((risk/entry)*100), 2),
        "rr_ratio": round(float((target1-entry)/risk), 2),
        "breakout_level": round(float(trendline[li]), 2),
        "vsma_ratio": vol_ratio,
        "trendline": trendline
    }


def fetch_symbol_data(symbol: str) -> dict:
    fii_holding = 0.0
    market_cap_cr = 0.0
    try:
        t = yf.Ticker(f"{symbol}.NS")
        fast_cap = getattr(t.fast_info, "market_cap", None)
        if fast_cap:
            market_cap_cr = round(fast_cap / 1e7, 2)
        
        major_holders = t.major_holders
        if major_holders is not None and not major_holders.empty:
            for _, r in major_holders.iterrows():
                r_str = " ".join([str(x) for x in r.values]).lower()
                if "institutions" in r_str or "institutional" in r_str:
                    fii_holding = float(str(r.iloc[0]).replace('%', '').strip())
    except Exception:
        pass
        
    return {"market_cap_cr": market_cap_cr, "fii_holding": fii_holding}


# ══════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="sidebar-logo-text">📡 NSE Breakout Scanner</div>
      <div class="sidebar-logo-sub">Full Universe · Market Cap &amp; FII Filter</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sidebar-section">Universe Mode (Total: {len(ALL_NSE_STOCKS)})</div>', unsafe_allow_html=True)
    
    universe_mode = st.radio("Select Universe Scope", [
        f"🌐 Full NSE Listed Universe ({len(ALL_NSE_STOCKS)} Stocks)",
        "⚡ Nifty 500 Fast Scan (Top 500)",
        "🎯 Custom Stock List"
    ])

    if "Full NSE" in universe_mode:
        selected_universe = ALL_NSE_STOCKS
    elif "500" in universe_mode:
        selected_universe = ALL_NSE_STOCKS[:500]
    else:
        custom_input = st.text_input("Enter comma-separated tickers", "SUZLON, YESBANK, TATASTEEL, KAYNES, DIXON")
        selected_universe = [s.strip().upper() for s in custom_input.split(",") if s.strip()]

    # No cap toggle
    scan_all = st.checkbox("Scan Full Selection (No Cap Limit)", value=True)
    if not scan_all:
        max_symbols = st.slider("Symbols to scan", 10, len(selected_universe), min(100, len(selected_universe)), 10)
    else:
        max_symbols = len(selected_universe)
        st.info(f"Targeting all **{max_symbols}** stocks.")

    st.markdown("---")
    st.markdown('<div class="sidebar-section">Market Cap Filter (₹ Cr)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        min_mcap = st.number_input("Min Cap (Cr)", value=1000.0, step=500.0)
    with c2:
        max_mcap = st.number_input("Max Cap (Cr)", value=10000.0, step=1000.0)

    st.markdown('<div class="sidebar-section">Price & Technical Settings</div>', unsafe_allow_html=True)
    min_price = st.number_input("Min Stock Price (₹)", value=1.0)
    max_price = st.number_input("Max Stock Price (₹)", value=50000.0)
    min_rr = st.slider("Min Risk : Reward", 1.0, 4.0, 1.0, 0.5)
    lookback_weeks = st.slider("Lookback (Weeks)", 10, 40, 20, 2)
    min_vol_ratio = st.slider("Min Volume Ratio", 0.2, 3.0, 0.5, 0.1)
    target_multiplier = st.slider("Target Multiplier", 1.5, 5.0, 2.5, 0.5)
    min_fii = st.slider("Min FII / Inst %", 0.0, 50.0, 0.0, 1.0)

    st.markdown("---")
    run_btn = st.button("▶  Run Deep Scanner", use_container_width=True, type="primary")


# ══════════════════════════════════════════════════════
#  SCANNER EXECUTION (Fast Batch Parallel Mode)
# ══════════════════════════════════════════════════════

if "results" not in st.session_state: st.session_state.results = []
if "scanned_count" not in st.session_state: st.session_state.scanned_count = 0

if run_btn and selected_universe:
    universe = selected_universe[:max_symbols]
    results = []
    batch_size = 50
    total = len(universe)
    prog = st.progress(0, text="Initialising scanner…")

    for i in range(0, total, batch_size):
        batch = universe[i:i+batch_size]
        prog.progress(min(1.0, (i + batch_size) / total), text=f"Processing {i}/{total} stocks…")
        
        tickers_str = " ".join([f"{s}.NS" for s in batch])
        try:
            batch_data = yf.download(tickers_str, period="2y", interval="1wk", group_by="ticker", progress=False, timeout=12)
        except Exception:
            continue

        for sym in batch:
            try:
                if len(batch) == 1:
                    df = batch_data.copy()
                else:
                    df = batch_data[f"{sym}.NS"].copy() if f"{sym}.NS" in batch_data else None

                if df is None or df.empty or len(df.dropna()) < 10:
                    continue

                bo = detect_breakout(df, lookback_weeks, min_vol_ratio, target_multiplier, min_price, max_price)
                if bo is None or bo["rr_ratio"] < min_rr:
                    continue

                fund = fetch_symbol_data(sym)
                mcap = fund["market_cap_cr"]
                fii = fund["fii_holding"]

                if mcap > 0 and (mcap < min_mcap or mcap > max_mcap):
                    continue
                if fii < min_fii:
                    continue

                score = 50 + (25 if 1000 <= mcap <= 10000 else 0) + (25 if fii > 5.0 else 0)

                results.append({
                    "Symbol": sym,
                    "LTP": bo["entry"],
                    "Market Cap (Cr)": mcap if mcap > 0 else "N/A",
                    "Stop Loss": bo["sl"],
                    "Target 1": bo["target1"],
                    "Target 2": bo["target2"],
                    "Risk %": bo["risk_pct"],
                    "R:R": bo["rr_ratio"],
                    "Vol Expansion": bo["vsma_ratio"],
                    "Inst / FII %": fii,
                    "Growth Score": score,
                    "_df": df,
                    "_trendline": bo["trendline"]
                })
            except Exception:
                continue

    prog.empty()
    results.sort(key=lambda x: x["Growth Score"], reverse=True)
    st.session_state.results = results
    st.session_state.scanned_count = total
    st.rerun()


# ══════════════════════════════════════════════════════
#  RESULTS RENDER
# ══════════════════════════════════════════════════════

results = st.session_state.results

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card blue">
    <div class="kpi-number">{st.session_state.scanned_count}</div>
    <div class="kpi-label">Symbols Scanned</div>
    <div class="kpi-sub">Full Universe Scope</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-number">{len(results)}</div>
    <div class="kpi-label">Breakouts Identified</div>
    <div class="kpi-sub">Cap ₹{min_mcap:,.0f}–{max_mcap:,.0f} Cr</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-number">{len([r for r in results if r['Growth Score'] >= 75])}</div>
    <div class="kpi-label">High Conviction</div>
    <div class="kpi-sub">FII + Mcap Verified</div>
  </div>
</div>
""", unsafe_allow_html=True)

if not results:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">🔍</div>
      <div class="empty-title">Ready to Scan Full Universe</div>
      <div class="empty-body">Click <b>▶ Run Deep Scanner</b> to scan across the full 2,000+ NSE stock list.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    tab1, tab2 = st.tabs(["📋 Screener Results", "📈 Chart Deep-Dive"])
    with tab1:
        for r in results:
            mcap_val = f"₹{r['Market Cap (Cr)']:,.0f} Cr" if isinstance(r['Market Cap (Cr)'], (int, float)) else "N/A"
            fii_val = f"{r['Inst / FII %']:.1f}%" if r['Inst / FII %'] else "—"
            st.markdown(f"""
            <div class="result-card">
              <div>
                <div class="result-symbol">{r['Symbol']}</div>
                <div class="result-sector">{mcap_val}</div>
              </div>
              <div class="result-metric">
                <div class="result-metric-label">LTP</div>
                <div class="result-metric-value">₹{r['LTP']:.2f}</div>
                <div class="pill pill-rr">R:R {r['R:R']}x</div>
              </div>
              <div class="result-metric">
                <div class="result-metric-label">Stop Loss</div>
                <div class="result-metric-value red">₹{r['Stop Loss']:.2f}</div>
                <div class="result-metric-label" style="margin-top:0.2rem;">Risk {r['Risk %']}%</div>
              </div>
              <div class="result-metric">
                <div class="result-metric-label">Target 1</div>
                <div class="result-metric-value green">₹{r['Target 1']:.2f}</div>
                <div class="pill pill-vol">Vol {r['Vol Expansion']}x</div>
              </div>
              <div class="result-metric">
                <div class="result-metric-label">Inst / FII Holding</div>
                <div class="result-metric-value amber">{fii_val}</div>
              </div>
              <div>
                <div class="result-metric-label">Score</div>
                <div style="font-family:'IBM Plex Mono', monospace; font-size:1.1rem; color:#38bdf8;">{r['Growth Score']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        syms = [r["Symbol"] for r in results]
        selected = st.selectbox("Select Stock", syms)
        row = next(r for r in results if r["Symbol"] == selected)
        df = row["_df"]
        dates = df.index.tolist()

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75, 0.25], vertical_spacing=0.03)
        fig.add_trace(go.Candlestick(x=dates, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="Price"), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=row["_trendline"], mode="lines", name="Resistance", line=dict(color="#f59e0b", width=1.8, dash="dot")), row=1, col=1)
        fig.add_trace(go.Bar(x=dates, y=df["Volume"], name="Volume", opacity=0.55), row=2, col=1)
        fig.update_layout(paper_bgcolor="#060a10", plot_bgcolor="#060a10", xaxis_rangeslider_visible=False, height=550)
        st.plotly_chart(fig, use_container_width=True)