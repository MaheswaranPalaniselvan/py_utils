from Connect import XTSConnect

creds = {
    "MARKET_API_KEY": "MARKET_API_KEY",
    "MARKET_API_SECRET": "MARKET_API_SECRET",
    "INTRAATIVE_API_SECRET": "INTRAATIVE_API_SECRET",
    "INTRAATIVE_API_KEY": "INTRAATIVE_API_KEY",
    "userID": "userID",
    "source": "WEBAPI",
}

MARKET_API_KEY = creds['MARKET_API_KEY']
MARKET_API_SECRET = creds['MARKET_API_SECRET']
INTRAATIVE_API_SECRET = creds['INTRAATIVE_API_SECRET']
INTRAATIVE_API_KEY = creds['INTRAATIVE_API_KEY']
userID = creds['userID']
source = creds['source']

xt = XTSConnect(INTRAATIVE_API_KEY, INTRAATIVE_API_SECRET, source)
intractive_response = xt.interactive_login()
print(intractive_response)
mkd = XTSConnect(MARKET_API_KEY, MARKET_API_SECRET, source)
market_response = mkd.marketdata_login()
print(market_response)
intractivetoken = intractive_response.get("result", {}).get("token", "Intractive Token didn't fetched")
marketoken = market_response.get("result", {}).get("token", "MarketAPI Token didn't fetched")

print(f"{intractivetoken=}")
print(f"{marketoken=}")