import pandas as pd
import FinanceDataReader as fdr
from mpl_finance import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

tickers = ['IXIC', 'USD/KRW']
data_from = '2015'
MA_num = [5, 10, 20, 60, 120, 200]
quotes = []
SMA_datas = []
axes_ = []

for i in range(len(tickers)):
    globals()['raw_data' + str(i)] = fdr.DataReader(tickers[i], data_from)

    # candle stick use datetime as float. so convert using date2num
    globals()['raw_data' + str(i)]['Date'] = \
        [mdates.date2num(d) for d in globals()['raw_data' + str(i)].index]

    # extract Close data only for calculate MA
    globals()['data' + str(i)] = globals()['raw_data' + str(i)]['Close']

    # Re-arrange data so that each row contains values of a day for candlestick's quote:
    # 'date','open','high','low','close'.
    quotes.insert(i,[tuple(x) for x in globals()['raw_data' + str(i)]
    [['Date', 'Open', 'High', 'Low', 'Close']].values])

    # make MAs as columns
    globals()['SMA' + str(i)] = pd.DataFrame()
    for g in range(len(MA_num)):
        globals()['SMA' + str(i)][str(MA_num[g]) + 'MA'] = \
            globals()['data' + str(i)].rolling(MA_num[g]).mean()
    SMA_datas.append(globals()['SMA' + str(i)])

fig, axs = plt.subplots(nrows=len(tickers), sharex=True, figsize=(12, 7))
for i in range(len(tickers)):
    candlestick_ohlc(axs[i], quotes[i], width=1, colorup='g', colordown='r')
    axs[i].plot(SMA_datas[i], linewidth=0.2)
    axs[i].xaxis_date()
    axs[i].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

plt.gcf().autofmt_xdate()  # Beautify the x-labels
plt.autoscale(tight=True)

plt.show()
