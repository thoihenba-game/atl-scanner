import requests, os, time
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
THRESHOLD = 15  # increased to 15% for real bottoms

STABLES = set(["tether","usd-coin","first-digital-usd","dai","true-usd","frax","usdd","paxos-standard","gemini-dollar","usdp","usde","ethena-usde","paypal-usd","binance-usd","liquity-usd","magic-internet-money","alchemix-usd","fei-usd"])

def send(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
        json={"chat_id": CHAT_ID, "text": msg, "parse_mode":"Markdown"}, timeout=10)

print("Getting Binance list...")
binance_ids = set()
try:
    data = requests.get("https://api.coingecko.com/api/v3/exchanges/binance/tickers", timeout=15).json()
    for t in data.get('tickers', []):
        if t.get('coin_id'):
            binance_ids.add(t['coin_id'])
    print(f"Binance IDs: {len(binance_ids)}")
except: pass

for page in range(1, 6):
    coins = requests.get(
        f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page={page}&order=market_cap_desc",
        timeout=15).json()
    for c in coins:
        # FILTER 1: Skip stablecoins
        if c['id'] in STABLES: continue
        if c['symbol'].lower() in ['usdt','usdc','fdusd','dai','busd']: continue
        if c['current_price'] > 0.9 and c['atl'] > 0.5: continue  # stablecoin price logic

        # FILTER 2: Binance only
        if binance_ids and c['id'] not in binance_ids: continue
        
        # FILTER 3: Real bottom (ATL must be real crash, not 5% down)
        if not c.get('atl'): continue
        dist = (c['current_price'] - c['atl']) / c['atl'] * 100
        if dist <= THRESHOLD:
            # FILTER 4: Must be at least 50% down from ATH to be real bottom
            ath_dist = (c['current_price'] - c['ath']) / c['ath'] * 100 if c.get('ath') else -99
            if ath_dist > -50: continue  # skip if not 50% down from ATH
            
            msg = f"🚨 *{c['name']} ({c['symbol'].upper()})* is near ATL\n+{dist:.1f}% from ATL | {ath_dist:.0f}% from ATH\nPrice ${c['current_price']} | ATL ${c['atl']} | Rank #{c['market_cap_rank']}"
            send(msg)
            print(msg)
