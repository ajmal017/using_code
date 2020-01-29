from ib_insync import *
import pandas as pd
import datetime as dt
# util.startLoop()  # uncomment this line when in a notebook

symbol1 = "AAPL"
sectype = "STK"
exchange1 = "SMART"
enddatetime_temp = '20200128 00:00:00'
duration1 = '20 Y'
barsize1 = '1 day'

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


mark = ib.reqFundamentalData(contract, 'ReportsOwnership')
print(mark)
print(type(mark))

# df.to_csv('savename.csv')
