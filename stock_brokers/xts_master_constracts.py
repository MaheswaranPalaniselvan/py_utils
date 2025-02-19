import requests
import pandas as pd
exchanges = ['NSEFO',"NSECM", "NSECD", "MCXFO", "BSECM", "BSEFO"]
r = requests.post("https://developers.symphonyfintech.in/apimarketdata/instruments/master", data={"exchangeSegmentList": exchanges})
columns = ['ExchangeSegment', 'ExchangeInstrumentID', 'InstrumentType', 'Name', 'Description',
               'Series', 'NameWithSeries', 'InstrumentID', 'PriceBand.High', 'PriceBand.Low',
               'FreezeQty', 'TickSize', 'LotSize', 'Multiplier', 'UnderlyingInstrumentId',
               'UnderlyingIndexName', 'ContractExpiration', 'StrikePrice', 'OptionType',
               'displayName', 'PriceNumerator', 'PriceDenominator', "Extra"]

rows = [row.split("|") for row in r.json()['result'].split('\n') if row.strip()]
df = pd.DataFrame(rows, columns=columns)
print(df.head())
