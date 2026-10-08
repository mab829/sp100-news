import os, json, time, urllib.request, urllib.parse
from datetime import date, timedelta, datetime, timezone

# Approximate S&P 100 constituents; edit this list to track any set of stocks.
TICKERS = """AAPL ABBV ABT ACN ADBE AIG AMD AMGN AMT AMZN AVGO AXP BA BAC BK BKNG BLK BMY BRK.B C CAT CHTR CL CMCSA
COF COP COST CRM CSCO CVS CVX DE DHR DIS DUK EMR FDX GD GE GILD GM GOOG GOOGL GS HD HON IBM INTC INTU ISRG JNJ JPM
KO LIN LLY LMT LOW MA MCD MDLZ MDT MET META MMM MO MRK MS MSFT NEE NFLX NKE NVDA ORCL PEP PFE PG PM PYPL QCOM RTX
SBUX SCHW SO SPG T TGT TMO TMUS TSLA TXN UBER UNH UNP UPS USB V VZ WFC WMT XOM""".split()

KEY = os.environ["FINNHUB_API_KEY"]
PER_TICKER = 5
today = date.today()
params = {"from": str(today - timedelta(days=2)), "to": str(today), "token": KEY}

quotes = {}
for t in TICKERS:
    try:
        url = "https://finnhub.io/api/v1/quote?" + urllib.parse.urlencode({"symbol": t, "token": KEY})
        with urllib.request.urlopen(url, timeout=20) as r:
            q = json.load(r)
        if q.get("c"):
            quotes[t] = {"c": q["c"], "d": q.get("d"), "dp": q.get("dp")}
    except Exception as e:
        print(f"{t}: quote failed ({e})")
    time.sleep(1.1)
print(f"Got {len(quotes)} quotes")

seen, items = set(), []
for t in TICKERS:
    url = "https://finnhub.io/api/v1/company-news?" + urllib.parse.urlencode({**params, "symbol": t})
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            news = json.load(r)
    except Exception as e:
        print(f"{t}: failed ({e})")
        continue
    for n in sorted(news, key=lambda x: x.get("datetime", 0), reverse=True)[:PER_TICKER]:
        if n["id"] in seen:
            continue
        seen.add(n["id"])
        items.append({"ticker": t, "headline": n["headline"], "summary": n.get("summary", ""),
                      "source": n.get("source", ""), "url": n["url"], "time": n["datetime"]})
    time.sleep(1.1)  # stay under the free-tier rate limit (60 calls/min)

items.sort(key=lambda x: x["time"], reverse=True)
with open("news.json", "w") as f:
    json.dump({"updated": datetime.now(timezone.utc).isoformat(), "quotes": quotes, "items": items}, f)
print(f"Wrote {len(items)} items")
