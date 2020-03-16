from ib_insync import *
import pandas as pd
import datetime as dt
# util.startLoop()  # uncomment this line when in a notebook

# use symbol2 for specific STOCK (and ticker1 == US_STOCK). for indices, use ticker1

ticker2 = 'SPX500'
enddatetime1 = "20050305 00:00:00"
duration1 = '30 Y'
barsize1 = '1 day'
primaryexchange = ""

# DOW  s: INDU, e: CME / NASDAQ s: COMP e: NASDAQ / SPX s: SPX e: CBOE / DAX s: DAX e: DTB c: EUR
NASDAQ = {'symbol1':'COMP', 'sectype':'IND', 'exchange1':'NASDAQ', 'currency':'USD'}
DOW = {'symbol1':'INDU', 'sectype':'IND', 'exchange1':'CME', 'currency':'USD'}
SPX500 = {'symbol1':'SPX', 'sectype':'IND', 'exchange1':'CBOE', 'currency':'USD'}
DAX = {'symbol1':'DAX', 'sectype':'IND', 'exchange1':'DTB', 'currency':'EUR'}
US_STOCK = {'symbol1':ticker2, 'sectype':'STK', 'exchange1':'SMART', 'currency':'USD'}
dicts = {'NASDAQ': NASDAQ, 'DOW': DOW, 'SPX500': SPX500, 'DAX': DAX}
tickers = ['NASDAQ', 'DOW', 'SPX500', 'DAX', US_STOCK]
if ticker2 not in tickers:
    ticker1 = US_STOCK
else:
    ticker1 = dicts[ticker2]


# request data from IB api part. package = ib_insync
ib = IB()
ib.connect('127.0.0.1', 7496, 0)
contract = Contract()
contract.symbol = ticker1['symbol1']
contract.secType = ticker1['sectype']
contract.exchange = ticker1['exchange1']
contract.currency = ticker1['currency']
contract.primaryExchange = primaryexchange

bars = ib.reqHistoricalData(
    contract, endDateTime= enddatetime1, durationStr=duration1,
    barSizeSetting=barsize1, whatToShow='TRADES', useRTH=1)

# convert to pandas dataframe:
df = util.df(bars)
df.columns = df.columns.str.capitalize()
df.set_index('Date', inplace=True)
print(df)


savepath = './ib_db/' + '{}_{}_{}_{}'.format\
    (ticker1['symbol1'], enddatetime1[:8], duration1.replace(' ', ''), barsize1.replace(' ', '')) + '.csv'

df.to_csv(savepath)
