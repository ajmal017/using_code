from mpl_finance import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from datetime import datetime as dt
import datetime
import matplotlib.dates as dates

ticker1 = 'AAPL'
path = './data/' + ticker1 + '.csv'

raw_data = pd.read_csv(path)

start_date = "2000-01-01"
end_date = "2020-01-15"

# to skip the days not in data
sd = dt.strptime(start_date,"%Y-%m-%d")
st = dt.strftime(sd,"%Y-%m-%d")
ed = dt.strptime(end_date,"%Y-%m-%d")
et = dt.strftime(ed,"%Y-%m-%d")


while st not in raw_data['Date'].values:
    sd += datetime.timedelta(days=1)
    st = dt.strftime(sd,"%Y-%m-%d")
    print(sd)
else: pass

while et not in raw_data['Date'].values:
    ed -= datetime.timedelta(days=1)
    et = dt.strftime(ed,"%Y-%m-%d")
    print(ed)
else: pass


raw_data1 = raw_data.set_index('Date')
chart1 = raw_data1.loc[st:et]


fig, ax = plt.subplots(figsize=(12,7))
candlestick2_ohlc(ax,chart1.iloc[:,0], chart1.iloc[:,1], chart1.iloc[:,2],
                  chart1.iloc[:,3], width=0.6, colorup='g', colordown='r', alpha=0.75)

ax.set_xlabel('Date')
ax.set_ylabel(ticker1, color='g')
ax.tick_params('y', colors='r')
ax.plot(index=chart1.index)
plt.legend(loc='upper left')

xtick_interval = (ed - sd).days / 6
ax.xaxis.set_major_locator(ticker.MultipleLocator(xtick_interval))
fig.tight_layout()
plt.show()