# NSE Breakout Scanner — Complete A-Z Guide

> **What this tool does:** It scans NSE stocks every time you press Run, fits a downward-sloping resistance trendline to recent weekly swing highs, and flags only the stocks whose latest weekly close broke above that line with a 1.5× volume surge — filtered by fundamental quality and scored 0–100 for multi-bagger potential.

---

## Part 1 — One-time Setup (do this once)

### Step 1 · Check your Python version

Open **Terminal** (macOS/Linux) or **Command Prompt / PowerShell** (Windows).

```
python --version
```

You need **Python 3.10 or higher**. If you get `3.9.x` or lower, download the latest Python from https://python.org/downloads and install it. If `python` isn't recognised, try `python3`.

---

### Step 2 · Create a project folder

```bash
# macOS / Linux
mkdir ~/nse-scanner
cd ~/nse-scanner

# Windows
mkdir C:\nse-scanner
cd C:\nse-scanner
```

---

### Step 3 · Copy the two files into that folder

Copy both files into the folder you just created:

- `app.py`
- `requirements.txt`

Your folder should look like:

```
nse-scanner/
├── app.py
└── requirements.txt
```

---

### Step 4 · Create a virtual environment

A virtual environment keeps these packages isolated from your system Python. Always do this.

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

Your terminal prompt will now show `(venv)` at the start. That confirms it's active.

---

### Step 5 · Install all dependencies

```bash
pip install -r requirements.txt
```

This installs: `streamlit`, `yfinance`, `pandas`, `numpy`, `scipy`, `plotly`, and `requests`.

It will take 1–3 minutes. You'll see a stream of progress lines — that's normal.

If you get a `pip: command not found` error, use `pip3` instead.

---

### Step 6 · (Optional) Install nselib for full NSE universe

The app works without `nselib` — it falls back to its own curated list of ~100 growth stocks. But if you want to scan the full Nifty 500, install it:

```bash
pip install nselib
```

`nselib` occasionally has breaking changes. If it fails to install, skip it — the app handles that automatically.

---

## Part 2 — Running the App

### Step 7 · Launch Streamlit

Make sure your virtual environment is active (you should see `(venv)` in the prompt), then:

```bash
streamlit run app.py
```

Streamlit will print something like:

```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

Your browser should open automatically. If it doesn't, open it manually and go to:

```
http://localhost:8501
```

---

### Step 8 · Stop the app

Press `Ctrl + C` in the terminal.

---

### Step 9 · Run it again next time

Every time you want to use the scanner after the first setup:

```bash
# Activate the environment first
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate.bat         # Windows

# Then launch
streamlit run app.py
```

---

## Part 3 — Using the App (screen by screen)

### The Sidebar — configure before running

The sidebar on the left controls everything the scanner looks for. Set these **before** clicking Run.

| Control | What it does | Recommended starting value |
|---|---|---|
| **Min Risk : Reward** | Only shows setups where Target ÷ Risk ≥ this number | 3.0 |
| **Min Sales CAGR 3Y (%)** | Only shows companies whose revenue grew at least this fast per year over 3 years | 10% |
| **Min PAT CAGR 3Y (%)** | Same but for net profit after tax | 10% |
| **Min FII QoQ Change (%)** | Minimum quarter-on-quarter increase in Foreign Institutional Investor shareholding | 0% (start open) |
| **Min DII QoQ Change (%)** | Same for Domestic Institutional Investors | 0% (start open) |
| **Sector filter** | Restrict results to one sector, or keep "All" | All |
| **Use compact list** | Checked = scans ~100 curated growth stocks (fast, ~2 min). Unchecked = tries to fetch full NSE equity list via nselib (slow, 10–20 min) | Checked |
| **Max symbols to scan** | Cap on how many symbols to process | 40 |

**Click "▶ Run Deep Scanner"** when ready.

---

### Tab 1 — Screener & Leaderboard

**KPI row (top 4 cards):**

- **Symbols Scanned** — total tickers processed this run
- **Breakouts Found** — passed both technical conditions (trendline break + volume)
- **High-Conviction** — of those, how many scored ≥ 60/100
- **Avg Growth Score** — average composite score across all results

**Card view vs Table view:**

Click the two buttons just below the KPIs to switch.

- **Card view** shows each result as a rich row: symbol, sector pill, entry price, stop-loss, target, R:R badge, volume surge badge, sales CAGR, FII change, and a scored progress bar. Sorted highest score first.
- **Table view** shows all 17 columns in a sortable dataframe. Click any column header to sort. Scroll right to see all columns.

**Colour coding in the table:**
- Growth Score green = 70+, amber = 45–69, red = below 45

**Export CSV** saves all results to `nse_breakout_results.csv` in your Downloads.

---

### Tab 2 — Chart Deep-Dive

Select any stock from the dropdown (populated with your breakout results).

**Trade panel (5 boxes across the top):**
- **Entry** — last weekly close, the breakout price
- **Stop Loss** — lowest low of the 3 candles before breakout (capped at 8% below entry)
- **Target 1 (1:3)** — Entry + (3 × Risk). This is where you take profits if the 1:3 ratio is met
- **Target 2 (52W High)** — the prior 52-week swing high, a natural resistance / secondary target
- **R:R Ratio** — confirmed ratio for this setup

**The chart:**
- **Candles** — green = up week, red = down week
- **Amber dotted line** — the fitted downward resistance trendline across recent swing highs. The breakout happened when the last candle closed above this line
- **Red dashed** — your stop-loss level
- **Green dashed** — Target 1
- **Pale green dotted** — Target 2
- **Bottom panel** — volume bars (green/red matching candle direction) with the 10-week SMA in blue. The breakout candle's bar should be visibly taller than the SMA line

---

### Tab 3 — Fundamentals

Select any stock from the dropdown.

**Left panel — Financial Metrics:**

Each metric has a colour-coded badge:
- 🟢 Green = strong (above the good threshold)
- 🟡 Amber = moderate
- 🔴 Red = weak / concerning

| Metric | Green threshold |
|---|---|
| Sales CAGR 3Y | ≥ 20% |
| PAT CAGR 3Y | ≥ 20% |
| Revenue Growth TTM | ≥ 15% |
| Earnings Growth TTM | ≥ 15% |
| ROCE | ≥ 20% |
| ROE | ≥ 20% |
| Debt / Equity | ≤ 0.5× |

**Right panel — Radar chart:**

A pentagon showing 5 dimensions scaled 0–100:
- Sales CAGR (scaled: 40% CAGR = 100 pts)
- PAT CAGR (same scale)
- ROCE (scaled: 30% = 100 pts)
- ROE (same scale)
- Low Leverage (100 = zero debt, 50 = D/E 1.0, 0 = D/E 2+)

A large, wide pentagon = strong all-round fundamentals. A lopsided shape shows where the weakness is.

**Institutional Accumulation card:**

Shows FII and DII quarter-on-quarter shareholding change (positive = institutions are buying more), plus the composite Growth Score with a visual bar.

---

## Part 4 — Understanding the Scores and Signals

### How the breakout is detected

1. The app fetches 2 years of weekly OHLCV data for each symbol.
2. It finds **swing highs** — weekly candle highs that are higher than the 5 candles on either side.
3. It fits a **linear trendline** through those swing highs using least-squares regression. If the slope is flat or upward, it's skipped — the scanner only flags **downward resistance**.
4. **Breakout condition:** the previous week's close was at or below the trendline, and the current week's close is above it.
5. **Volume condition:** the current week's volume is at least 1.5× the 10-week average. This filters out low-conviction breaks.

### How R:R is calculated

```
Entry     = current weekly close (breakout candle)
Stop Loss = max(lowest low of last 3 candles, entry × 0.92)
Risk      = Entry − Stop Loss
Target 1  = Entry + (3 × Risk)
R:R       = (Target 1 − Entry) ÷ Risk   → should be ≥ 3.0
```

### How the Growth Score (0–100) is built

| Component | Max pts | How it's earned |
|---|---|---|
| Institutional accumulation | 30 | FII + DII both positive; more pts for larger combined increase |
| PAT + Sales CAGR | 30 | Both > 20% = full 30; either > 15% = 18; either > 8% = 10 |
| Sector tailwind | 20 | Sector is in: EMS, Defence, Renewable Energy, Railways, Infrastructure, Specialty Chemicals, Capital Goods, Technology |
| Balance sheet | 20 | ROCE or ROE > 20% = 10 pts; D/E < 0.8 = 10 pts (financials/NBFCs D/E exempt) |

---

## Part 5 — Troubleshooting

### "No module named streamlit" or similar

Your virtual environment isn't active. Run:
```bash
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate.bat   # Windows
```
Then try `streamlit run app.py` again.

### App opens but scanner finds 0 results

This is expected behaviour — the conditions are strict. Try:
1. Lower the Min R:R to 2.0
2. Set Sales CAGR and PAT CAGR sliders to 0
3. Set sector to "All"
4. Increase Max symbols to scan (more symbols = more chances)

If you still get 0, it means no stock in the scanned universe broke its weekly resistance trendline with volume expansion this week. That's a real signal — the market may be in a low-breakout phase.

### Slow scanning

Each symbol makes 2 network calls (OHLCV + fundamentals). For 40 symbols expect ~2 minutes. For 100 symbols expect ~5 minutes. This is normal and unavoidable with free APIs.

To speed it up:
- Keep "Use compact list" checked
- Lower Max symbols to 20–30
- Results are cached for 30–60 minutes — re-running without restarting the app is fast

### yfinance data errors / partial data

yfinance occasionally returns empty or malformed data for some NSE tickers. The app silently skips any symbol that fails rather than crashing. You may see fewer results than expected — this is normal.

### "debtToEquity" showing very large values

yfinance reports `debtToEquity` as a percentage in some versions (e.g., 45 meaning 45%, not 45×). The app divides by 100 to normalise. If a D/E value looks wrong, verify it on Screener.in for the same stock.

### nselib not available / import error

This is fine. The app catches the import error and uses its hardcoded universe. You don't need to install `nselib` for the app to work.

### Browser doesn't open automatically

Go to `http://localhost:8501` manually in any browser.

### Port 8501 already in use

```bash
streamlit run app.py --server.port 8502
```
Then open `http://localhost:8502`.

---

## Part 6 — Updating the Stock Universe

The fallback list (`FALLBACK_UNIVERSE`) in `app.py` is a hand-curated set of ~100 growth-oriented NSE stocks. To add or remove stocks, open `app.py` in any text editor and edit the list starting around line 80:

```python
FALLBACK_UNIVERSE = [
    "DIXON", "KAYNES", ...   # add "YOURSYMBOL" here
]
```

Use the NSE symbol exactly as it appears on NSE India (without `.NS`). For example: `TATAMOTORS`, `ICICIBANK`, `INFY`.

---

## Part 7 — Data Sources & Limitations

| Data | Source | Limitation |
|---|---|---|
| OHLCV prices | Yahoo Finance (yfinance) | 15-min delay; some tickers inconsistent |
| Fundamentals | Yahoo Finance Ticker.info | Not always up-to-date; some fields missing |
| Sales / PAT CAGR | Calculated from yfinance annual financials | Max 4 years available; approximate |
| FII / DII change | Approximated from yfinance major_holders | **Synthetic QoQ delta** — not the actual SEBI filing data. Treat as indicative only |

**For production-grade FII/DII data:** replace the `fetch_fundamentals` FII/DII block with a scraper targeting Screener.in, Trendlyne, or the NSE shareholding pattern XML endpoint.

---

## Quick-Reference Cheat Sheet

```
1.  cd ~/nse-scanner
2.  source venv/bin/activate
3.  streamlit run app.py
4.  Browser: http://localhost:8501
5.  Sidebar → set filters → Run Deep Scanner
6.  Tab 1 → browse results (card or table view)
7.  Tab 2 → pick a stock → inspect chart + trade levels
8.  Tab 3 → check fundamentals radar + score breakdown
9.  Export CSV if needed
10. Ctrl+C to stop
```

---

*NSE Breakout Scanner · For research purposes only · Not financial advice · Not SEBI registered*
