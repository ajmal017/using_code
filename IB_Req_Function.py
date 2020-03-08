from ib_insync import *
import pandas as pd
import datetime as dt
import time
# util.startLoop()  # uncomment this line when in a notebook

# DOW  s: INDU, e: CME / NASDAQ s: COMP e: NASDAQ / SPX s: SPX e: CBOE / DAX s: DAX e: DTB c: EUR

# for specific STOCK (and ticker1 == US_STOCK). for indices, use ticker1

NASDAQ = {'symbol1': 'COMP', 'sectype': 'IND', 'exchange1': 'NASDAQ', 'currency': 'USD'}
DOW = {'symbol1': 'INDU', 'sectype': 'IND', 'exchange1': 'CME', 'currency': 'USD'}
SPX500 = {'symbol1': 'SPX', 'sectype': 'IND', 'exchange1': 'CBOE', 'currency': 'USD'}
DAX = {'symbol1': 'DAX', 'sectype': 'IND', 'exchange1': 'DTB', 'currency': 'EUR'}
tickers = ['NASDAQ', 'DOW', 'SPX500', 'DAX', 'US_STOCK']
dicts = {'NASDAQ': NASDAQ, 'DOW': DOW, 'SPX': SPX500, 'DAX': DAX}


def request(ticker2, enddatetime=None, duration=None, barsize=None, usecols=None,
            primaryexchange="", index_col=None):
    if enddatetime == None:
        enddatetime = (dt.datetime.today() + dt.timedelta(days=1)).strftime('%Y%m%d 00:00:00')
    if duration == None:
        duration1 = '1 Y'
    if barsize == None:
        barsize1 = '1 day'

    US_STOCK = {'symbol1': ticker2, 'sectype': 'STK', 'exchange1': 'SMART', 'currency': 'USD'}

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
        contract, endDateTime= enddatetime, durationStr=duration,
        barSizeSetting=barsize, whatToShow='TRADES', useRTH=1)

    # convert to pandas dataframe:
    df = util.df(bars)
    ib.disconnect()
    time.sleep(0.3)
    df.columns = df.columns.str.capitalize()
    if index_col == 'Date':
        df.set_index(index_col, inplace=True)
        df.index = pd.to_datetime(df.index)
    if usecols != None:
        return df[usecols]
    else:
        return df

