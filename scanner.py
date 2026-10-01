import requests, os
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
THRESHOLD = 12

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode":"Markdown"}, timeout=10)
    except: pass

# 1. Get Binance list - using data-api which works on GitHub
try:
    url = "https://data-api.binance.vision/api/v3/exchangeInfo"
    binance = requests.get(url, timeout=15).json()
    binance_coins = set(s['baseAsset'].upper() for s in binance['symbols'] if s['status']=='TRADING')
    print(f"Binance coins loaded: {len(binance_coins)}")
except Exception as e:
    print(f"Binance API fail {e}, using backup list")
    # Backup - top Binance coins
    binance_coins = set(["BTC","ETH","BNB","SOL","XRP","DOGE","ADA","AVAX","SHIB","DOT","TRX","LINK","MATIC","LTC","BCH","UNI","XLM","ETC","ATOM","HBAR","FIL","APT","ARB","OP","NEAR","SUI","PEPE","BONK","FLOKI","WIF","FET","RNDR","INJ","TIA","SEI","JUP","ENA","W","PYTH","STRK"])

# 2. Scan
for page in range(1, 6):
    try:
        coins = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page={page}&order=market_cap_desc",
            timeout=15).json()
    except: continue
    
    for c in coins:
        sym = c['symbol'].upper()
        if sym not in binance_coins: continue
        if not c.get('atl'): continue
        dist = (c['current_price'] - c['atl']) / c['atl'] * 100
        if dist <= THRESHOLD:
            msg = f"🚨 *Binance* {c['name']} ({sym}) +{dist:.1f}% from ATL\nPrice ${c['current_price']} ATL ${c['atl']}"
            send(msg)
            print(msg)

print("Done")
