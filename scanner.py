import requests, os
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
THRESHOLD = 12
PAGES = 8

def send(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
        json={"chat_id": CHAT_ID, "text": msg, "parse_mode":"Markdown"}, timeout=10)

for page in range(1, PAGES+1):
    coins = requests.get(
        f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page={page}&order=market_cap_desc",
        timeout=10).json()
    for c in coins:
        if not c.get('atl'): continue
        dist = (c['current_price'] - c['atl']) / c['atl'] * 100
        if dist <= THRESHOLD:
            send(f"🚨 {c['symbol'].upper()} +{dist:.1f}% above ATL\nNow ${c['current_price']} ATL ${c['atl']} Rank #{c['market_cap_rank']}")
