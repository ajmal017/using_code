import pandas as pd
from mpl_finance import *
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from matplotlib import rc
import numpy as np
rc('font', family="Batang")


ticker1 = 'AAPL'

df = pd.read_excel('./db/0. nasdaq100 earnings.xlsx')
df['Date'] = df['Date'].dt.strftime("%Y-%m-%d")
df.set_index('Date', inplace=True)
df = df.iloc[:,1:]
df.dropna(how='all', inplace=True)
df['Surprise'] = round((df['Actual'] / df['Consensus'] -1) * 100, 1)
df = df[df['Ticker']==ticker1]
print(df)


# TODO minus surprise fix    / groupby


read_ticker1 = './db/' + ticker1 + '.csv'
raw_data1 = pd.read_csv(read_ticker1)

raw_data1.set_index('Date', inplace=True)
merge1 = pd.merge(raw_data1, df, left_index=True, right_index=True, how='left')
merge1 = merge1.fillna(method='ffill', limit=3)
merge1 = merge1.fillna(method='bfill', limit=3)
merge1 = merge1.dropna(axis=0, how='any')
merge1.drop(columns=['Ticker', 'Time'], inplace=True)
print(merge1)


fig, ax = plt.subplots(figsize=(12,7))
candlestick2_ohlc(ax,merge1.iloc[:,0], merge1.iloc[:,1], merge1.iloc[:,2],
                  merge1.iloc[:,3], width=0.6, colorup='g', colordown='r', alpha=0.75)

ax.set_ylabel(ticker1, color='g')
ax.tick_params('y', colors='r')

# tick setting

xtick_value = pd.Series(merge1['Fiscal'])
xtick_value.reset_index(drop=True, inplace=True)
xtick_interval = round(len(xtick_value) / 10, 0)
position = np.arange(0,len(xtick_value),xtick_interval)
xticks = xtick_value[position]
plt.xticks(np.arange(0,len(xtick_value),xtick_interval),xticks, rotation=45)

fig.tight_layout()

savename = './data/2.' + ticker1 + '_earnings.csv'
merge1.to_csv(savename)
out_path = './charts/' + '{}_earnings.png'.format\
    (ticker1)
plt.savefig(out_path)
plt.show()
