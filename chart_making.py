from mpl_finance import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from datetime import datetime as dt
import datetime
import matplotlib.dates as dates

ticker1 = 'DIS'
path = './ib_db/' + 'DIS_20200205_3Y_1day' + '.csv'
interval_num = 15


raw_data = pd.read_csv(path)

start_date = "2017-01-01"
end_date = "2020-01-25"

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
xlabel1 = pd.Series(chart1.index)
print(xlabel1)
xtick_interval = int((ed - sd).days / interval_num)
xticklen = pd.Series(np.arange(0,len(xlabel1), xtick_interval)).astype(int)
xticklen[interval_num-1] = 0
xticklen.sort_values(inplace=True)
xticklen.reset_index(drop=True, inplace=True)
xlabel2 = xlabel1[xticklen]
print(xtick_interval)
print(xticklen)
print(xlabel2)

fig, ax = plt.subplots(figsize=(12,7))
candlestick2_ohlc(ax,chart1.iloc[:,0], chart1.iloc[:,1], chart1.iloc[:,2],
                  chart1.iloc[:,3], width=0.6, colorup='g', colordown='r', alpha=0.75)


ax.set_ylabel(ticker1, color='g')
plt.xticks(ticks=xticklen, labels=xlabel2)
ax.tick_params('y', colors='r')
ax.xaxis.set_major_locator(ticker.MultipleLocator(xtick_interval))
ax.tick_params('x', labelsize='small', labelrotation=45)
ax.grid(which='major', axis='both', color='gray', dashes=(2, 4), linewidth=0.5)
plt.margins(x=0, y=None, tight=True)

fig.tight_layout()
plt.show()