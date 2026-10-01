import requests, os
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
THRESHOLD = 15  # only real bottoms

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode":"Markdown"}, timeout=10)
    except: pass

# FINAL STABLECOIN BLACKLIST
BLACKLIST_SYMBOLS = {"USDT","USDC","FDUSD","USDS","USDE","USD1","RLUSD","U","BFUSD","XUSD","DAI","TUSD","USDP","PYUSD","GUSD","FRAX","USDD","USDG","EURC","EURS"}
BLACKLIST_IDS = {"tether","usd-coin","first-digital-usd","ethena-usde","usd-coin-2","ripple-usd","united-stables","bfusd","straitsx-xusd","dai","true-usd","paxos-standard","paypal-usd","frax","usdd"}

print("Scanning... skipping stablecoins")
for page in range(1, 6):
    coins = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=250&page={page}&order=market_cap_desc", timeout=15).
