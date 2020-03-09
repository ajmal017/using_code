import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_finance import *
import FinanceDataReader as fdr
from pandas.core.common import SettingWithCopyWarning
import warnings
import datetime as dt
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
today1 = dt.datetime.today()
today_ = today1.strftime("%y%m%d")

import IB_Req_Function

# Variables. ticker1 can be USSTOCKs, major_indices
ticker1 = 'NASDAQ'
barsize1 = "1 week"
duration1 = "5 Y"
MA_num = [5, 10, 120, 200]


# make SMA_data
SMA_data = IB_Req_Function.request(ticker1, duration='10 Y', barsize='1 week', usecols=['Date', 'Close'])
for g in range(len(MA_num)):
    SMA_data[str(MA_num[g]) + 'MA'] = SMA_data['Close'].rolling(MA_num[g]).mean()

SMA_data['Date_day'] = pd.to_datetime(SMA_data['Date'].shift(-1)).dt.strftime("%Y-%m-%d")
SMA_data.set_index('Date_day', inplace=True)
SMA_data.drop(columns=['Date', 'Close'], inplace=True)


# # extract days from hourly or minutely data
raw_data = IB_Req_Function.request(ticker1, usecols=['Date', 'Open', 'High', 'Low', 'Close'],
                                   duration=duration1, barsize=barsize1)

raw_data['Date_day'] = pd.to_datetime(raw_data['Date']).dt.strftime("%Y-%m-%d")
raw_data.set_index('Date_day', inplace=True)

# merging
merge1 = pd.merge(raw_data, SMA_data, left_index=True, right_index=True, how='left')
merge1.reset_index(drop=True, inplace=True)
print(merge1)

# visualize candle
fig, ax = plt.subplots(figsize=(14,9))
candlestick2_ohlc(ax, merge1['Open'], merge1['High'], merge1['Low'], merge1['Close'],
                  width=1, colorup='g', colordown='r')

## visualize SMA data. using specific color by MAs. and annotate
#
## 5MA
# MA_5 = ax.plot(merge1['5MA'], linewidth=0.4, color='saddlebrown', label='5MA')
# ax.annotate(int(merge1.iloc[-1, -5]), color='saddlebrown', fontsize=10,
#                      xy=(merge1.index[-1]+1, merge1.iloc[-1, -5]+2))
#
#
# 10MA
MA_10 = ax.plot(merge1['10MA'], linewidth=0.4, color='teal', label='10MA')
ax.annotate(int(merge1.iloc[-1, -3]), color='teal', fontsize=10,
                     xy=(merge1.index[-1]+1, merge1.iloc[-1, -3]+2))


# 120MA
MA_120 = ax.plot(merge1['120MA'], linewidth=0.4, color='b', label='120MA')
ax.annotate(int(merge1.iloc[-1, -2]), color='b', fontsize=10,
                     xy=(merge1.index[-1]+1, merge1.iloc[-1, -2]+2))

# 200MA
MA_200 = ax.plot(merge1['200MA'], linewidth=0.5, color='r', label='200MA')
ax.annotate(int(merge1.iloc[-1, -1]), color='r', fontsize=10,
                     xy=(merge1.index[-1]+1, merge1.iloc[-1, -1]))


# # annotate last_price
ax.annotate(round(merge1.iloc[-1, 5],2), color='k', fontsize=10,
                     xy=(merge1.index[-1]+1, merge1.iloc[-1, 5]), label='Current')


# # x_axis - date setting for candlestick2_ohlc
# # https://wikidocs.net/4766
#
# date index extract as month-day / hours-minutes

index_to_datetime = pd.to_datetime(merge1['Date'])
month_day_index = index_to_datetime.dt.strftime("'%y-%m")

# set major ticks

day_list1 = list(np.arange(0, len(merge1), step=int(len(merge1)/10)))
name_list1 = list(month_day_index.iloc[day_list1])#

#  axes setting
ax.yaxis.tick_right()
ax.xaxis.set_major_locator(mticker.FixedLocator(day_list1))
ax.xaxis.set_major_formatter(mticker.FixedFormatter(name_list1))

# # grid
ax.grid(which='major', axis='x', color='dimgrey', dashes=(1,1), linewidth=0.4)
ax.grid(which='major', axis='y', color='k', dashes=(1,1), linewidth=0.4)

# # legend, title, layout
plt.legend(loc=2)
plt.title(ticker1 + ' ' + barsize1 + " candle with SMA")
plt.tight_layout()
plt.margins(x=0.01)
# # plt.savefig('./charts/' + ticker1 + str(today_) + 'daily_SMA.png')
plt.show()
