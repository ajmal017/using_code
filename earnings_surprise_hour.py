from mpl_finance import *
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rc
import numpy as np
import warnings
from pandas.core.common import SettingWithCopyWarning
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import IndexFormatter
from itertools import compress, cycle
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


def pos_neg(num):
    if num > 0:
        return True
    else:
        return False


ticker1 = 'AMZN'
surp_thres = 20

# bar data by 2hours, get data with IB api

read_ticker1 = './ib_db/' + 'AMZN_20200201_3Y_2hours' + '.csv'
raw_data1 = pd.read_csv(read_ticker1)
raw_data_date = pd.to_datetime(raw_data1['Date'])
raw_data1['Date_day'] = raw_data_date.dt.strftime("%Y-%m-%d")
raw_data1.set_index('Date_day', inplace=True)

# cleaning data of earnings calendar

df = pd.read_csv('./data/cleaned_earning_calendar.csv')
df = df[df['Ticker'] == ticker1]
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

df.dropna(how='all', inplace=True)
df['Act'] = ''
df['Con'] = ''
df['Real-Con'] = ''
df['SurpShock'] = ''

# Surprise or Shock? calculate

for i in range(len(df)):
    df['Act'][i] = pos_neg(df['Actual'][i])
    df['Con'][i] = pos_neg(df['Consensus'][i])

for i in range(len(df)):
    if df['Act'][i] == 1 and df['Con'][i] == 0:
        df['Real-Con'][i] = 100
    elif df['Act'][i] == 0 and df['Con'][i] == 1:
        df['Real-Con'][i] = -100
    elif df['Act'][i] == 0 and df['Con'][i] == 0:
        df['Real-Con'][i] = -round((df['Actual'][i] / df['Consensus'][i] - 1) * 100, 2)
    elif df['Act'][i] == 1 and df['Con'][i] == 1:
        df['Real-Con'][i] = round((df['Actual'][i] / df['Consensus'][i] - 1) * 100, 2)

df['Actual'] = round(df['Actual'], 2)
df['Consensus'] = round(df['Consensus'], 2)


for i in range(len(df)):
    if df['Real-Con'][i] > surp_thres:
        df['SurpShock'][i] = 'Surprise'
    elif df['Real-Con'][i] > - surp_thres:
        df['SurpShock'][i] = 'in-line'
    else:
        df['SurpShock'][i] = 'Shock'


# merging

merge1 = pd.merge(raw_data1, df, left_index=True, right_index=True, how='left')
merge1 = merge1.fillna(method='ffill', limit=8)
print(merge1)
merge_col = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Actual', 'Consensus', 'Real-Con',
             'SurpShock', 'Calendar']
merge2 = merge1[merge_col]
merge2 = merge2.dropna(axis=0, how='any')
merge2.set_index('Date', inplace=True)
merge2.sort_values(by=['Date'], ascending=True, inplace=True)
print(merge2)

# tick, label value setting

xtick_value = pd.Series(merge2['Calendar'])
xtick_value.reset_index(drop=True, inplace=True)
xtick_interval = round(len(xtick_value) / len(xtick_value.unique()), 0)
position = np.arange(0, len(xtick_value), xtick_interval)
xticks = xtick_value[position]
xtick_sub = pd.Series(merge2['SurpShock'])
xtick_sub.reset_index(drop=True, inplace=True)

# xtick_sub compressing
# make specific interval difference between data
# https://www.geeksforgeeks.org/python-interval-initialization-in-list/

num_values = list(range(len(xtick_sub)))
N = 3
K = int(xtick_interval)
func = cycle([True] * N + [False] * (K - N))
res = list(compress(num_values, func))
null_list = [''] * (len(xtick_sub) - len(res))
for j in range(len(res)):
    qw = res[j]
    null_list.insert(qw, xtick_sub[qw])
xticks_sub = null_list


# plotting

# candlestick function

fig, ax = plt.subplots(figsize=(12, 7))
candlestick2_ohlc(ax, merge2.iloc[:, 0], merge2.iloc[:, 1], merge2.iloc[:, 2],
                  merge2.iloc[:, 3], width=0.6, colorup='g', colordown='r', alpha=0.75)

# setting tick, label, grid

ax.set_ylabel(ticker1, color='g')
ax.tick_params('y', colors='r')
ax.tick_params('x', which='minor', direction='in', pad=-10, labelsize=8, colors='b')
plt.xticks(np.arange(0, len(xtick_value), xtick_interval), xticks, rotation=45)
ax.xaxis.set_minor_locator(MultipleLocator(3))
ax.xaxis.set_minor_formatter(IndexFormatter(xticks_sub))
ax.grid(which='major', axis='x', color='k', linewidth=0.5)
ax.grid(which='minor', axis='x', color='gray', dashes=(2, 4), linewidth=0.5)
legend_text = 'in-line: between' + '[-' + str(surp_thres) + ':' + str(surp_thres) + ']'
plt.legend([legend_text], loc='upper left', handlelength=0,
           fontsize='small', fancybox=True)
fig.tight_layout()

# save to file as png format

out_path = './charts/' + '{}_earnings_hourly.png'.format(ticker1)
plt.savefig(out_path)

plt.show()


# TODO: set date and left index = False