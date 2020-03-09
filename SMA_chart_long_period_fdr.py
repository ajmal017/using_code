import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_finance import *
import FinanceDataReader as fdr
from pandas.core.common import SettingWithCopyWarning
import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# use ticker1 variable for plot label.
# https://github.com/FinanceData/FinanceDataReader/wiki/Users-Guide

ticker1 = 'NASDAQ'  # all uppers

tickers = {
    'WTI':'CL', 'KOSPI':'KS11', 'KOSDAQ':'KQ11','VIX':'VIX','GOLD':'GC', 'SILVER':'SI',
    'US10Y':'US10YT=X', 'KR10Y':'KR10YT=RR', 'BITCOIN':'BTC/USD', 'DOW':'DJI', 'GAS':'NG',
    'NASDAQ':'IXIC', 'S&P500':'US500', 'NIKKEI':'JP225', 'DAX':'DE30', 'KR1Y':'KR1YT=RR',
    'KR3Y':'KR3YT=RR', 'US1M':'US1MT=X', 'US3M':'US3MT=X', 'US1Y':'US1YT=X', 'US3Y':'US3YT=X',
    'US30Y':'US30YT=X', 'KR30Y':'KR30YT=RR', 'US6M':'US6MT=X'
}
MA_num = [5, 120, 200, 967]
observe_days = 300
if ticker1 in tickers:
    ticker = tickers[ticker1]
else:
    ticker = ticker1

raw_ = fdr.DataReader(ticker, '2015')

# convert date to num for using
raw_data = raw_.iloc[-observe_days:, :]
raw_data.index = pd.to_datetime(raw_data.index)
raw_data['Datetonum'] = [mdates.date2num(d) for d in raw_data.index]

# Re-arrange data so that each row contains values of a day for candlestick's quote:
# 'date','open','high','low','close'.
quote = [tuple(x) for x in raw_data[['Datetonum', 'Open', 'High', 'Low', 'Close']].values]

# SMA_data  using rolling in pandas
SMA_data_ = pd.DataFrame(index=raw_.index)
for g in range(len(MA_num)):
    SMA_data_[str(MA_num[g]) + 'MA'] = raw_['Close'].rolling(MA_num[g]).mean()
SMA_data = SMA_data_.iloc[-observe_days:, :]

# visualize candle
fig, ax = plt.subplots(figsize=(14,9))
candlestick_ohlc(ax, quote, width=0.7, colorup='g', colordown='r')

# visualize SMA data. using specific color by MAs

# 120MA visualize and annotate
MA_120 = ax.plot(SMA_data.iloc[:, 1], linewidth=0.5, color='b', label='120MA')
if ticker1[:2] not in ['KR', 'US']:
    ax.annotate(int(SMA_data.iloc[-1, 1]), color='b', fontsize=7, xy=(SMA_data.index[-1], SMA_data.iloc[-1, 1]+2))
else :
    ax.annotate(round(SMA_data.iloc[-1, 1], 2), color='b', fontsize=7, xy=(SMA_data.index[-1], SMA_data.iloc[-1, 1]+2))


# 200MA visualize and annotate
MA_200 = ax.plot(SMA_data.iloc[:, 2], linewidth=0.5, color='r', label='200MA')
if ticker1[:2] not in ['KR', 'US']:
    ax.annotate(int(SMA_data.iloc[-1, 2]), color='r', fontsize=7, xy=(SMA_data.index[-1], SMA_data.iloc[-1, 2]+2))
else :
    ax.annotate(round(SMA_data.iloc[-1, 2], 2), color='r', fontsize=7, xy=(SMA_data.index[-1], SMA_data.iloc[-1, 2]+2))


# 200w-MA visualize and annotate
# MA_200w = ax.plot(SMA_data.iloc[:, 3], linewidth=0.5, color='pink', label='200W-MA')
# ax.annotate(int(SMA_data.iloc[-1, 3]), color='pink', fontsize=7,
#                      xy=(SMA_data.index[-1], SMA_data.iloc[-1, 3]))


# annotate last_price
if ticker1[:2] not in ['KR', 'US']:
    ax.annotate(int(raw_data['Close'][-1]), color='k', fontsize=9,
                xy=(raw_data.index[-1], raw_data['Close'][-1]), label='Current')
else:
    ax.annotate(round(raw_data['Close'][-1], 2), color='k', fontsize=9,
                xy=(raw_data.index[-1], raw_data['Close'][-1]), label='Current')

# axes setting
ax.yaxis.tick_right()
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax.xaxis.set_minor_locator(mticker.AutoLocator())

# grid
ax.grid(which='major', axis='y', color='gray', dashes=(2, 4), linewidth=0.5)
ax.grid(which='major', axis='x', color='k', dashes=(1, 1), linewidth=0.8)

# Beautify the x-labels
plt.title(ticker1)
plt.legend()
plt.gcf().autofmt_xdate()
if ticker1[:2] not in ['KR', 'US']:
    plt.tight_layout()
plt.savefig('./charts/' + ticker1 + 'SMA.png')
plt.show()
