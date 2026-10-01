import requests, os
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
THRESHOLD = 12 # % above ATL

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode":"Markdown"}, timeout=10)
    except: pass

# 1. Get Binance listed coins
print("Fetching Binance list...")
binance = requests.get("https://api.binance.com/api/v3/exchangeInfo", timeout=10).json()
binance_coins = set()
for s in binance['symbols']:
    if s['status'] == 'TRADING' and s['quoteAsset'] in ['USDT','BTC','FDUSD']:
        binance_coins.add(s['baseAsset'].upper())
print(f"Binance coins: {len(binance_coins)}")

# 2. Scan only those
for page in range(1, 6): # 1250 coins is enough, all binance coins are inside top 1250
    coins = requests.get(
        f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page={page}&order=market_cap_desc",
        timeout=15).json()
    for c in coins:
        sym = c['symbol'].upper()
        if sym not in binance_coins: # NOT on Binance -> skip
            continue
        if not c.get('atl'): continue
        dist = (c['current_price'] - c['atl']) / c['atl'] * 100
        if dist <= THRESHOLD:
            msg = f"🚨 *Binance* {c['name']} ({sym}) is +{dist:.1f}% from ATL\nPrice: ${c['current_price']} | ATL: ${c['atl']} | Rank #{c['market_cap_rank']}"
            send(msg)
            print(msg)
