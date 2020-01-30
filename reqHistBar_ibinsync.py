from ib_insync import *
import pandas as pd
import datetime as dt
# util.startLoop()  # uncomment this line when in a notebook

symbol1 = "AAPL"
sectype = "STK"
exchange1 = "SMART"
enddatetime_temp = '20200130 00:00:00'
duration1 = '3 Y'
barsize1 = '2 hours'

##for timezone setting
et1 = dt.datetime.strptime(enddatetime_temp, "%Y%m%d %H:%M:%S")
et2 = et1.astimezone(dt.timezone.utc) - dt.timedelta(hours=5)
enddatetime1 = dt.datetime.strftime(et2, "%Y%m%d %H:%M:%S")
dates = dt.datetime.strftime(et1, "%Y%m%d")

ib = IB()
ib.connect('127.0.0.1', 7496, 0)
contract = Contract()
contract.symbol = symbol1
contract.secType = sectype
contract.exchange = exchange1
contract.currency = "USD"


bars = ib.reqHistoricalData(
    contract, endDateTime= enddatetime1, durationStr=duration1,
    barSizeSetting=barsize1, whatToShow='TRADES', useRTH=1)

# convert to pandas dataframe:
df = util.df(bars)
df.columns = df.columns.str.capitalize()
df.set_index('Date', inplace=True)
print(df)


savename = './ib_db/' + '{}_{}_{}_{}'.format(symbol1, dates, duration1.replace(' ', ''), barsize1.replace(' ', '')) + '.csv'

df.to_csv(savename)
