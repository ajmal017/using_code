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
ticker1 = 'KORU'
ticker2 = 'YINN'
ticker3 = 'TQQQ'
ticker4 = 'CWEB'
ticker5 = 'CHAU'

# ticker3 has only 1 column, so modify the code other way.


# date format = %Y-%m-%d

start_date = "2020-01-01"
end_date = "2020-02-15"


# file path
read_ticker1 = './ib_db/' + ticker1 + '_20200215_1M_1day' + '.csv'
read_ticker2 = './ib_db/' + ticker2 + '_20200215_1M_1day' + '.csv'
read_ticker3 = './ib_db/' + ticker3 + '_20200215_1M_1day' + '.csv'
read_ticker4 = './ib_db/' + ticker4 + '_20200215_1M_1day' + '.csv'
read_ticker5 = './ib_db/' + ticker5 + '_20200215_1M_1day' + '.csv'


raw_data1 = pd.read_csv(read_ticker1)
raw_data2 = pd.read_csv(read_ticker2)
raw_data3 = pd.read_csv(read_ticker3)
raw_data4 = pd.read_csv(read_ticker4)
raw_data5 = pd.read_csv(read_ticker5)


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

# set data to make chart


raw_data1.set_index('Date', inplace=True)
chart11 = raw_data1.loc[st:et].apply(lambda x: x / x[0])
chart1 = chart11.iloc[:,3]
raw_data2.set_index('Date', inplace=True)
chart22 = raw_data2.loc[st:et].apply(lambda x: x / x[0])
chart2 = chart22.iloc[:,3]
raw_data3.set_index('Date', inplace=True)
chart33 = raw_data3.loc[st:et].apply(lambda x: x / x[0])
chart3 = chart33.iloc[:,3]
raw_data4.set_index('Date', inplace=True)
chart44 = raw_data4.loc[st:et].apply(lambda x: x / x[0])
chart4 = chart44.iloc[:,3]
raw_data5.set_index('Date', inplace=True)
chart55 = raw_data5.loc[st:et].apply(lambda x: x / x[0])
chart5 = chart55.iloc[:,3]



# ticker3 has only 1 column and monthly data,  so modify the code other way.

#
# if '1.' in ticker3:
#     raw_data3.set_index('Date', inplace=True)
#     chart33 = raw_data3.loc[st:et].apply(lambda x: x / x[0])
#     chart3 = chart33.iloc[:, 3]
#
# else:
#     chart33 = pd.Series(raw_data1.index)
#     merge1 = pd.merge(raw_data3, chart33, how='outer')
#     merge1.sort_values(by=['Date'], ascending=True, inplace=True)
#     merge1 = merge1.ffill()
#     merge1.set_index('Date', inplace=True)
#     chart3 = merge1.loc[st:et].apply(lambda x: x / x[0])
#     chart3 = chart3.iloc[:,0]

max_value = max(chart1.max(), chart2.max(), chart3.max(), chart4.max(), chart5.max())*1.1
min_value = min(chart1.min(), chart2.min(), chart3.min(), chart4.min(), chart5.min())*0.9
print(max_value)
print(min_value)

fig, ax1 = plt.subplots()
ax1.plot(chart1.index, chart1, 'r-', label = ticker1)
ax1.set_xlabel('Date')
ax1.set_ylabel(ticker1,color='r')
ax1.tick_params('y', colors='r')
plt.legend(loc='upper left')


ax2 = ax1.twinx()
ax2.plot(chart2.index, chart2, 'b-', label = ticker2)
ax2.set_ylabel(ticker2, color='b')
ax2.tick_params('y', colors='b')
plt.legend(loc='upper right')

ax3 = ax1.twinx()
ax3.plot(chart3.index, chart3, 'k-', label = ticker3)
ax3.set_ylabel(ticker3, color='k', labelpad=15)
plt.legend(loc='lower right')

ax4 = ax1.twinx()
ax4.plot(chart4.index, chart4, 'g-', label = ticker4)
plt.legend(loc='lower left')

ax5 = ax1.twinx()
ax5.plot(chart5.index, chart5, 'y-')
ax5.set_ylabel(ticker5, color='y', labelpad=30)

ax1.set_ylim(bottom=min_value, top=max_value)
ax2.set_ylim(bottom=min_value, top=max_value)
ax3.set_ylim(bottom=min_value, top=max_value)
ax4.set_ylim(bottom=min_value, top=max_value)
ax5.set_ylim(bottom=min_value, top=max_value)

ax3.xaxis.set_major_locator(ticker.MultipleLocator(xtick_interval))
fig.tight_layout()

out_path = './charts/' + '{}_{}_{}_{}_{}norm.png'.format\
    (ticker1, ticker2, ticker3, sd.strftime("%y%m"), ed.strftime("%y%m"))
plt.savefig(out_path)
plt.show()