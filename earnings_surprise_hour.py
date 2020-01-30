import pandas as pd
from mpl_finance import *
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from matplotlib import rc
import numpy as np
import warnings
from pandas.core.common import SettingWithCopyWarning
from matplotlib.ticker import MultipleLocator

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

rc('font', family="Batang")


def pos_neg(num):
    if num > 0:
        return True
    else:
        return False

ticker1 = 'TSLA'


# cleaning data of earning season

df = pd.read_excel('./db/0. nasdaq100 earnings.xlsx')
df = df[df['Ticker']==ticker1]
df['Date_day'] = df['Date'].dt.strftime("%Y-%m-%d")
df.set_index('Date_day', inplace=True)
df = df.iloc[:,1:]
df.dropna(how='all', inplace=True)
df['Act'] = ''
df['Con'] = ''
df['Real-Con'] = ''


# Fiscal string cleaning. 'Q'n YY -> YY'Q'n


for i in range(len(df)):
    df['Fiscal'][i] = df['Fiscal'][i].strip()
    sp1, sp2 = df['Fiscal'][i].split(' ')
    df['Fiscal'][i] = sp2 + sp1


# real-con column setting


for i in range(len(df)):
    df['Act'][i] = pos_neg(df['Actual'][i])
    df['Con'][i] = pos_neg(df['Consensus'][i])


for i in range(len(df)):
    if df['Act'][i]==1 and df['Con'][i] == 0:
        df['Real-Con'][i] = 100
    elif df['Act'][i]==0 and df['Con'][i] == 1:
        df['Real-Con'][i] = -100
    elif df['Act'][i]==0 and df['Con'][i] == 0:
        df['Real-Con'][i] = -round((df['Actual'][i] / df['Consensus'][i] -1) * 100,2)
    elif df['Act'][i]==1 and df['Con'][i] == 1:
        df['Real-Con'][i] = round((df['Actual'][i] / df['Consensus'][i] -1) * 100,2)

df['Actual'] = round(df['Actual'], 2)
df['Consensus'] = round(df['Consensus'], 2)


# bar data by 2hours

read_ticker1 = './ib_db/' + 'TSLA_20200131_3Y_2hours' + '.csv'
raw_data1 = pd.read_csv(read_ticker1)
raw_data_date = pd.to_datetime(raw_data1['Date'])
raw_data1['Date_day'] = raw_data_date.dt.strftime("%Y-%m-%d")
raw_data1.set_index('Date_day', inplace=True)


# merging

merge1 = pd.merge(raw_data1, df, left_index=True, right_index=True, how='left')
merge1 = merge1.fillna(method='ffill', limit=8)
merge_col = ['Date_x', 'Open', 'High', 'Low', 'Close', 'Volume', 'Actual', 'Fiscal', 'Consensus', 'Real-Con']
merge2 = merge1[merge_col]
merge2 = merge2.dropna(axis=0, how='any')
merge2.set_index('Date_x', inplace=True)
merge2.sort_values(by=['Date_x'], ascending=True, inplace=True)
print(merge2)

# tick, label value setting

xtick_value = pd.Series(merge2['Fiscal'])
xtick_value.reset_index(drop=True, inplace=True)
xtick_interval = round(len(xtick_value) / 12, 0)
position = np.arange(0,len(xtick_value),xtick_interval)
xticks = xtick_value[position]


# plotting

fig, ax = plt.subplots(figsize=(12,7))
candlestick2_ohlc(ax,merge2.iloc[:,0], merge2.iloc[:,1], merge2.iloc[:,2],
                  merge2.iloc[:,3], width=0.6, colorup='g', colordown='r', alpha=0.75)

ax.set_ylabel(ticker1, color='g')
ax.tick_params('y', colors='r')
plt.xticks(np.arange(0,len(xtick_value),xtick_interval),xticks, rotation=45)
ax.xaxis.set_minor_locator(MultipleLocator(4))
ax.grid(which='major', axis='x', color='k', linewidth=0.5)
ax.grid(which='minor', axis='x', color='gray', dashes=(2,4), linewidth=0.5)
fig.tight_layout()
out_path = './charts/' + '{}_earnings_hourly.png'.format(ticker1)
plt.savefig(out_path)
plt.show()