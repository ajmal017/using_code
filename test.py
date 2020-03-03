import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_finance import *
import FinanceDataReader as fdr
from pandas.core.common import SettingWithCopyWarning
import warnings
import datetime as dt
import IB_Req_Function

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# use ticker1 variable for plot label.
ticker1 = 'NASDAQ'
observation_period = -100
today1 = dt.datetime.today()
today_ = today1.strftime("%y%m%d")

MA_num = [5, 10, 120, 200, 967]

SMA_data = IB_Req_Function.request('NASDAQ')
for g in range(len(MA_num)):
    SMA_data[str(MA_num[g]) + 'MA'] = SMA_data['Close'].rolling(MA_num[g]).mean()

print(SMA_data)
# # want to draw SMA lines,  use longer period of data.
# # set raw_  at first,  and slicing data to raw_data
#
# SMA_raw = pd.read_csv(path_for_SMA, index_col='Date')
# SMA_data = pd.DataFrame(index=SMA_raw.index)
# for g in range(len(MA_num)):
#     SMA_data[str(MA_num[g]) + 'MA'] = SMA_raw['Close'].rolling(MA_num[g]).mean()
#
# # SMA day-1 to show breaking intra-day or not
# SMA_data['Date_day'] = ''
# for i in range(1, 20):
#     SMA_data['Date_day'][-i-1] = SMA_data.index[-i]
# SMA_data.set_index('Date_day', inplace=True)
#
#
# # extract days from hourly or minutely data
# raw_data = pd.read_csv(path_for_candle)
# raw_data_date = pd.to_datetime(raw_data['Date'])
# raw_data['Date_day'] = raw_data_date.dt.strftime("%Y-%m-%d")
# raw_data.set_index('Date_day', inplace=True)
#
#
# # merging
# merge1 = pd.merge(raw_data, SMA_data, left_index=True, right_index=True, how='left')
# merge1 = merge1.fillna(method='bfill', limit=12)
# merge1.reset_index(inplace=True)
# print(merge1)
#
# # visualize candle
# fig, ax = plt.subplots(figsize=(14,9))
# candlestick2_ohlc(ax, merge1['Open'], merge1['High'], merge1['Low'], merge1['Close'],
#                   width=0.2, colorup='g', colordown='r')
#
#
# # visualize SMA data. using specific color by MAs
# # MA_5 = ax.plot(merge1['5MA'], linewidth=0.5, color='saddlebrown', label='5MA')
# # MA_10 = ax.plot(merge1['10MA'], linewidth=0.5, color='teal', label='10MA')
# MA_120 = ax.plot(merge1['120MA'], linewidth=0.5, color='b', label='120MA')
# MA_200 = ax.plot(merge1['200MA'], linewidth=0.5, color='r', label='200MA')
# # MA_200w = ax.plot(merge1['967MA'], linewidth=0.5, color='pink', label='200W-MA')
#
#
# # date setting for candlestick2_ohlc
# # https://wikidocs.net/4766
#
# index_to_datetime = pd.Series(pd.to_datetime(merge1['Date_day']))
# month_day_index = index_to_datetime.dt.strftime("%m-%d")
# unique_day = np.unique(month_day_index, return_index=True)
# day_list = list(unique_day[1])
# name_list = list(unique_day[0])
#
# ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
# ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))
#
#
# #
# # # annotate 120MA
# ax.annotate(int(merge1.iloc[-1, -3]), color='b', fontsize=7,
#                      xy=(merge1.index[-1]+1, merge1.iloc[-1, -3]+2))
# #
# # #
# # # annotate 200MA
# ax.annotate(int(merge1.iloc[-1, -2]), color='r', fontsize=7,
#                      xy=(merge1.index[-1]+1, merge1.iloc[-1, -2]))
# #
# # # annotate 200week MA
# # ax.annotate(int(SMA_data.iloc[-1, 3]), color='pink', fontsize=7,
# #                      xy=(SMA_data.index[-1]+1, SMA_data.iloc[-1, 3]))
# #
# #
# # annotate last_price
# ax.annotate(merge1.iloc[-1, 5], color='k', fontsize=9,
#                      xy=(merge1.index[-1]+1, merge1.iloc[-1, 5]), label='Current')
# #
# # axes setting
# ax.set_ylabel(ticker1, color='g')
# ax.yaxis.tick_right()
#
# # grid
# ax.grid(which='major', axis='both', color='gray', dashes=(2, 4), linewidth=0.2)
#
# # Beautify the x-labels
# plt.legend()
# plt.title("5mins candle with SMA")
# plt.tight_layout()
# plt.savefig('./charts/' + ticker1 + str(today_) + 'daily_SMA.png')
# plt.show()
