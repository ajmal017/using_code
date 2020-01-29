from ib_insync import *
import pandas as pd
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7496, 0)
contract = Contract()
contract.symbol = "COMP"
contract.secType = "IND"
contract.exchange = "NASDAQ"
contract.currency = "USD"

bars = ib.reqHistoricalData(
    contract, endDateTime='20100128 00:00:01', durationStr='10 Y',
    barSizeSetting='1 hour', whatToShow='TRADES', useRTH=1)

# convert to pandas dataframe:
df = util.df(bars)
print(df)
df.to_csv('dddd.csv')
