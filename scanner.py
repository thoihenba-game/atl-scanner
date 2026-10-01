import requests, os
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
THRESHOLD = 15

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode":"Markdown"}, timeout=10)
    except: pass

BLACKLIST_SYMBOLS = {"USDT","USDC","FDUSD","USDS","USDE","USD1","RLUSD","U","BFUSD","XUSD","DAI","TUSD","USDP","PYUSD","GUSD","FRAX","USDD"}
BLACKLIST_IDS = {"tether","usd-coin","first-digital-usd","ethena-usde","ripple-usd","united-stables","bfusd","straitsx-xusd","dai","true-usd","paxos-standard","paypal-usd","frax","usdd"}

print("Scanning real bottoms only...")
API = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&order=market_cap_desc&page="

for page in range(1, 6):
    coins = requests.get(API+str(page), timeout=15).json()
    for c in coins:
        sym = c['symbol'].upper()
        if sym in BLACKLIST_SYMBOLS: continue
        if c['id'] in BLACKLIST_IDS: continue
        if "usd" in c['id'] and c['current_price'] > 0.8: continue
        if c['current_price'] > 0.9 and c['current_price'] < 1.2: continue
        if not c.get('atl'): continue
        dist = (c['current_price'] - c['atl']) / c['atl'] * 100
        if dist <= THRESHOLD:
            if c.get('ath') and c['current_price'] > c['ath'] * 0.5: continue
            msg = f"🚨 {c['name']} ({sym}) +{dist:.1f}% from ATL Price ${c['current_price']} ATL ${c['atl']} Rank #{c['market_cap_rank']}"
            send(msg)
            print(msg)
print("Done")
