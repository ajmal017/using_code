from ib_insync import *
import pandas as pd
import datetime as dt
# util.startLoop()  # uncomment this line when in a notebook

# use symbol2 for specific STOCK (and ticker1 == US_STOCK). for indices, use ticker1
symbol2 = 'AAPL'
enddatetime_temp = '20200305 00:00:00'
duration1 = '2 W'
barsize1 = '5 mins'
# DOW  s: INDU, e: CME / NASDAQ s: COMP e: NASDAQ / SPX s: SPX e: CBOE / DAX s: DAX e: DTB c: EUR
NASDAQ = {'symbol1':'COMP', 'sectype':'IND', 'exchange1':'NASDAQ', 'currency':'USD'}
DOW = {'symbol1':'INDU', 'sectype':'IND', 'exchange1':'CME', 'currency':'USD'}
SPX500 = {'symbol1':'SPX', 'sectype':'IND', 'exchange1':'CBOE', 'currency':'USD'}
DAX = {'symbol1':'DAX', 'sectype':'IND', 'exchange1':'DTB', 'currency':'EUR'}
US_STOCK = {'symbol1':symbol2, 'sectype':'STK', 'exchange1':'SMART', 'currency':'USD'}

# tickers = [NASDAQ, DOW, SPX500, DAX, US_STOCK]
ticker1 = NASDAQ

symbol1 = ticker1['symbol1']
sectype = ticker1['sectype']
exchange1 = ticker1['exchange1']
currency = ticker1['currency']
primaryexchange = ""


# for timezone setting
et1 = dt.datetime.strptime(enddatetime_temp, "%Y%m%d %H:%M:%S")
et2 = et1.astimezone(dt.timezone.utc) - dt.timedelta(hours=5)
enddatetime1 = dt.datetime.strftime(et2, "%Y%m%d %H:%M:%S")
dates = dt.datetime.strftime(et1, "%Y%m%d")

# request data from IB api part. package = ib_insync
ib = IB()
ib.connect('127.0.0.1', 7496, 0)
contract = Contract()
contract.symbol = symbol1
contract.secType = sectype
contract.exchange = exchange1
contract.currency = currency
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
    (symbol1, dates, duration1.replace(' ', ''), barsize1.replace(' ', '')) + '.csv'

df.to_csv(savepath)
