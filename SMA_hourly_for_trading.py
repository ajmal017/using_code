import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from mpl_custom import *
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
barsize1 = "30 mins"
MA_num = [5, 10, 120, 200, 967]


# make SMA_data
SMA_data = IB_Req_Function.request(ticker1, duration='5 Y', barsize='1 day', usecols=['Date', 'Close'])
for g in range(len(MA_num)):
    SMA_data[str(MA_num[g]) + 'MA'] = SMA_data['Close'].rolling(MA_num[g]).mean()

SMA_data['Date_day'] = pd.to_datetime(SMA_data['Date'].shift(-1)).dt.strftime("%Y-%m-%d")
SMA_data.set_index('Date_day', inplace=True)
SMA_data.drop(columns=['Date', 'Close'], inplace=True)
SMA_data = SMA_data.iloc[-20:]


# extract days from hourly or minutely data
raw_data = IB_Req_Function.request(ticker1, usecols=['Date', 'Open', 'High', 'Low', 'Close'],
                                   duration='2 W', barsize=barsize1)
raw_data['Date_day'] = raw_data['Date'].dt.strftime("%Y-%m-%d")
raw_data['Change'] = round(raw_data['Close'].pct_change() * 100, 1).astype(str) + "%"
raw_data['Mid'] = (raw_data['High'] + raw_data['Low']) / 2
raw_data.set_index('Date_day', inplace=True)

# merging
merge1 = pd.merge(raw_data, SMA_data, left_index=True, right_index=True, how='left')
merge1.reset_index(drop=True, inplace=True)
print(merge1)

# visualize candle
fig, ax = plt.subplots(figsize=(10,7))
candlestick2_ohlc(ax, merge1['Open'], merge1['High'], merge1['Low'], merge1['Close'])

# # visualize SMA data. using specific color by MAs. and annotate

# # 5MA
# MA_5 = ax.plot(merge1['5MA'], linewidth=0.4, color='saddlebrown', label='5MA')
# ax.annotate(int(merge1.iloc[-1, -5]), color='saddlebrown', fontsize=10,
#                      xy=(merge1.index[-1]+1, merge1.iloc[-1, -5]+2))
#
#
# # 10MA
# MA_10 = ax.plot(merge1['10MA'], linewidth=0.4, color='teal', label='10MA')
# ax.annotate(int(merge1.iloc[-1, -4]), color='teal', fontsize=10,
#                      xy=(merge1.index[-1]+1, merge1.iloc[-1, -4]+2))


# 120MA
MA_120 = ax.plot(merge1['120MA'], linewidth=0.4, color='b', label='120MA')
ax.annotate(int(merge1.iloc[-1, -3]), color='b', fontsize=10,
                     xy=(merge1.index[-1]+1, merge1.iloc[-1, -3]+2))

# 200MA
MA_200 = ax.plot(merge1['200MA'], linewidth=0.5, color='r', label='200MA')
ax.annotate(int(merge1.iloc[-1, -2]), color='r', fontsize=10,
                     xy=(merge1.index[-1]+1, merge1.iloc[-1, -2]))

# 200w MA
# MA_200w = ax.plot(merge1['967MA'], linewidth=0.5, color='pink', label='200W-MA')
# ax.annotate(int(merge1.iloc[-1, -1]), color='r', fontsize=10,
#                      xy=(merge1.index[-1]+1, merge1.iloc[-1, -1]))


# annotate last_price
ax.annotate(round(merge1.iloc[-1, 4],2), color='k', fontsize=11,
                     xy=(merge1.index[-1]+1, merge1.iloc[-1, 4]), label='Current')

for i, txt in enumerate(merge1['Change']):
    if raw_data['Close'].pct_change()[i] > 0.01 or raw_data['Close'].pct_change()[i] < -0.01:
        ax.annotate(txt, (merge1.index[i]-0.9, merge1['Mid'][i]), fontsize=7, fontweight='bold')



# x_axis - date setting for candlestick2_ohlc
# https://wikidocs.net/4766

# date index extract as month-day / hours-minutes

index_to_datetime = pd.to_datetime(merge1['Date'])
month_day_index = index_to_datetime.dt.strftime("%m-%d")
minutes_index = index_to_datetime.dt.strftime("%H:%M")
# set major ticks

unique_day = np.unique(month_day_index, return_index=True)
day_list = list(unique_day[1])
name_list = list(unique_day[0])

# set minor ticks
minutes_to_extract = ["10:00", "15:30"]
summertime_extract = ["09:00", "14:30"]
minorticks_index= []
minorticks_values = []
for i, values in enumerate(minutes_index):
    if i < 104:
        if values in minutes_to_extract:
            minorticks_index.append(i)
            minorticks_values.append(values)

    else:
        if values in summertime_extract:
            minorticks_index.append(i)
            minorticks_values.append(values)


# axes setting
ax.yaxis.tick_right()
ax.xaxis.set_major_locator(mticker.FixedLocator(day_list))
ax.xaxis.set_major_formatter(mticker.FixedFormatter(name_list))
ax.xaxis.set_minor_locator(mticker.FixedLocator(minorticks_index))
ax.xaxis.set_minor_formatter(mticker.FixedFormatter(minorticks_values))
ax.tick_params(which='minor', axis='x', labelrotation=90, pad=14, labelsize=8)


# grid
ax.grid(which='major', axis='x', color='dimgrey', linewidth=1)
ax.grid(which='major', axis='y', color='k', dashes=(1,1), linewidth=0.8)
ax.grid(which='minor', axis='both', color='grey', dashes=(2, 4), linewidth=0.5)


# legend, title, layout
plt.legend()
plt.title(ticker1 + ' ' + barsize1 + " candle with SMA" + "\n annotate on >1% change since previous Close")
plt.tight_layout()
plt.margins(x=0.01)
plt.savefig('./charts/' + ticker1 + str(today_) + 'daily_SMA.png')
plt.show()
