from mpl_finance import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from datetime import datetime as dt
import datetime
from dateutil.relativedelta import relativedelta
from matplotlib import rc
rc('font', family="Batang")

# tickers
ticker1 = '롯데케미칼'
ticker2 = 'X'
ticker3 = 'POSCO'

# file path
read_ticker1 = './db/' + ticker1 + '.csv'
read_ticker2 = './db/' + ticker2 + '.csv'
read_ticker3 = './db/' + ticker3 + '.csv'

raw_data1 = pd.read_csv(read_ticker1)
raw_data2 = pd.read_csv(read_ticker2)
raw_data3 = pd.read_csv(read_ticker3)


# date format = %Y-%m-%d
start_date1 = "2016-01-01"
end_date1 = "2018-06-01"
start_date2 = "2015-06-01"
end_date2 = "2018-01-01"
start_date3 = "2015-06-01"
end_date3 = "2018-01-01"

# to skip the days not in data
sd1 = dt.strptime(start_date1,"%Y-%m-%d")
st1 = dt.strftime(sd1,"%Y-%m-%d")
ed1 = dt.strptime(end_date1,"%Y-%m-%d")
et1 = dt.strftime(ed1,"%Y-%m-%d")

sd2 = dt.strptime(start_date2,"%Y-%m-%d")
st2 = dt.strftime(sd2,"%Y-%m-%d")
ed2 = dt.strptime(end_date2,"%Y-%m-%d")
et2 = dt.strftime(ed2,"%Y-%m-%d")

sd3 = dt.strptime(start_date3,"%Y-%m-%d")
st3 = dt.strftime(sd3,"%Y-%m-%d")
ed3 = dt.strptime(end_date3,"%Y-%m-%d")
et3 = dt.strftime(ed3,"%Y-%m-%d")


while st1 not in raw_data1['Date'].values:
    sd1 += datetime.timedelta(days=1)
    st1 = dt.strftime(sd1,"%Y-%m-%d")
    print(sd1)
else: pass

while et1 not in raw_data1['Date'].values:
    ed1 += datetime.timedelta(days=1)
    et1 = dt.strftime(ed1,"%Y-%m-%d")
    print(ed1)
else: pass

while st2 not in raw_data2['Date'].values:
    sd2 += datetime.timedelta(days=1)
    st2 = dt.strftime(sd2,"%Y-%m-%d")
    print(sd2)
else: pass

while et2 not in raw_data2['Date'].values:
    ed2 += datetime.timedelta(days=1)
    et2 = dt.strftime(ed2,"%Y-%m-%d")
    print(ed2)
else: pass

while st3 not in raw_data3['Date'].values:
    sd3 += datetime.timedelta(days=1)
    st3 = dt.strftime(sd3,"%Y-%m-%d")
    print(sd3)
else: pass

while et3 not in raw_data3['Date'].values:
    ed3 += datetime.timedelta(days=1)
    et3 = dt.strftime(ed3,"%Y-%m-%d")
    print(ed3)
else: pass


xtick_interval = (ed1 - sd1).days / 6

## set data to make chart

raw_data1.set_index('Date', inplace=True)
chart1 = raw_data1.loc[st1:et1].apply(lambda x: x / x[0])
raw_data2.set_index('Date', inplace=True)
chart2 = raw_data2.loc[st2:et2].apply(lambda x: x / x[0])
raw_data3.set_index('Date', inplace=True)
chart3 = raw_data3.loc[st3:et3].apply(lambda x: x / x[0])

max_value = max(chart1.iloc[:,3].max(), chart2.iloc[:,3].max(), chart3.iloc[:,3].max())*1.1
min_value = min(chart1.iloc[:,3].min(), chart2.iloc[:,3].min(), chart3.iloc[:,3].min())*0.9
print(max_value)
print(min_value)

fig, ax1 = plt.subplots()
ax1.plot(chart1.index, chart1.iloc[:,3], 'k-', label = ticker1)
ax1.set_ylabel(ticker1,color='k')
ax1.yaxis.set_ticks_position('right')
ax1.tick_params('y', colors='k')
plt.legend(loc='upper left')



ax2 = ax1.twiny()
ax2.plot(chart2.index, chart2.iloc[:,3], 'b-', label = ticker2)
ax2.set_xlabel(ticker2, color='b')
ax2.xaxis.set_label_coords(0.7, 1.16)
ax2.tick_params('x', colors='blue')
plt.legend(loc='upper right')

ax3 = ax1.twiny()
ax3.plot(chart3.index, chart3.iloc[:,3], 'r-', label = ticker3)
ax3.set_xlabel(ticker3, color='r', labelpad=15)
ax3.tick_params(axis='x', which='major', colors='r', pad=15)
plt.legend(loc='lower right')

ax1.set_ylim(bottom=min_value, top=max_value)
ax2.set_ylim(bottom=min_value, top=max_value)
ax3.set_ylim(bottom=min_value, top=max_value)

ax1.xaxis.set_major_locator(ticker.MultipleLocator(xtick_interval))
ax2.xaxis.set_major_locator(ticker.MultipleLocator(xtick_interval))
ax3.xaxis.set_major_locator(ticker.MultipleLocator(xtick_interval))
fig.tight_layout()

out_path = './charts/' + '{0}_{1}_{2}_{3}_{4}_{5}_norm.png'.format\
    (ticker1, sd1.strftime("%y%m"), ticker2, sd2.strftime("%y%m"), ticker3, sd3.strftime("%y%m"))
plt.savefig(out_path)
plt.show()