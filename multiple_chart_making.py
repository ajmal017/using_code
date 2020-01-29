from mpl_finance import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from datetime import datetime as dt
import datetime
import matplotlib.dates as matdates
from matplotlib import rc
rc('font', family="Batang")

# tickers
ticker1 = 'HD'
ticker2 = 'MSFT'
ticker3 = 'PLD'

# file path
read_ticker1 = './db/' + ticker1.upper() + '.csv'
read_ticker2 = './db/' + ticker2.upper() + '.csv'
read_ticker3 = './db/' + ticker3.upper() + '.csv'

raw_data1 = pd.read_csv(read_ticker1)
raw_data2 = pd.read_csv(read_ticker2)
raw_data3 = pd.read_csv(read_ticker3)


# date format = %Y-%m-%d
start_date = "2018-01-01"
end_date = "2020-01-15"

# to skip the days not in data
sd = dt.strptime(start_date,"%Y-%m-%d")
st = dt.strftime(sd,"%Y-%m-%d")
ed = dt.strptime(end_date,"%Y-%m-%d")
et = dt.strftime(ed,"%Y-%m-%d")


while st not in raw_data1['Date'].values:
    sd += datetime.timedelta(days=1)
    st = dt.strftime(sd,"%Y-%m-%d")
    print(sd)
else: pass

while et not in raw_data1['Date'].values:
    ed -= datetime.timedelta(days=1)
    et = dt.strftime(ed,"%Y-%m-%d")
    print(ed)
else: pass

xtick_interval = (ed - sd).days / 6

## set data to make chart

raw_data1.set_index('Date', inplace=True)
chart1 = raw_data1.loc[st:et]
raw_data2.set_index('Date', inplace=True)
chart2 = raw_data2.loc[st:et]
raw_data3.set_index('Date', inplace=True)
chart3 = raw_data3.loc[st:et]


fig, ax1 = plt.subplots()
ax1.plot(chart1.index, chart1.iloc[:,3], 'r-', label = ticker1)
ax1.set_xlabel('Date')
ax1.set_ylabel(ticker1,color='r')
ax1.tick_params('y', colors='r')
plt.legend(loc='upper left')



ax2 = ax1.twinx()
ax2.plot(chart2.index, chart2.iloc[:,3], 'b-', label = ticker2)
ax2.set_ylabel(ticker2, color='b')
ax2.tick_params('y', colors='b')
plt.legend(loc='upper right')

ax3 = ax1.twinx()
ax3.plot(chart3.index, chart3.iloc[:,3], 'k-', label = ticker3)
ax3.set_ylabel(ticker3, color='k', labelpad=5)
ax3.tick_params('y', pad=30)
plt.legend(loc='lower right')


ax3.xaxis.set_major_locator(ticker.MultipleLocator(xtick_interval))
fig.tight_layout()

out_path = './charts/' + '{}_{}_{}_{}.png'.format\
    (ticker1, ticker2, ticker3, sd.strftime("%y%m"))
plt.savefig(out_path)

plt.show()