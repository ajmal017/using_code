import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from datetime import datetime as dt
import datetime
import seaborn as sns
from matplotlib import rc
from statsmodels.tsa.stattools import adfuller
from functools import reduce
rc('font', family="Batang")

# tickers
ticker1 = '삼성전자'
ticker2 = '삼성전자우'

# file path
read_ticker1 = './db/' + ticker1.upper() + '.csv'
read_ticker2 = './db/' + ticker2.upper() + '.csv'

raw_data1 = pd.read_csv(read_ticker1)
raw_data2 = pd.read_csv(read_ticker2)


# date format = %Y-%m-%d
start_date = "2017-01-01"
end_date = "2020-01-15"

# to skip the days not in data
sd = dt.strptime(start_date,"%Y-%m-%d")
st = dt.strftime(sd,"%Y-%m-%d")
ed = dt.strptime(end_date,"%Y-%m-%d")
et = dt.strftime(ed,"%Y-%m-%d")


while (st not in raw_data1['Date'].values) or (st not in raw_data2['Date'].values):
    sd += datetime.timedelta(days=1)
    st = dt.strftime(sd,"%Y-%m-%d")
    print(sd)
else: pass

while (et not in raw_data1['Date'].values) or (et not in raw_data2['Date'].values):
    ed += datetime.timedelta(days=1)
    et = dt.strftime(ed,"%Y-%m-%d")
    print(ed)
else: pass

# convert to yield

raw_data1.set_index('Date', inplace=True)
data1 = raw_data1.loc[st:et, 'Close']
chart1 = data1 / data1[0] - 1
raw_data2.set_index('Date', inplace=True)
data2 = raw_data2.loc[st:et, 'Close']
chart2 = data2 / data2[0] - 1


spread1 = chart1 - chart2
spread1.dropna(inplace=True)
print(spread1)


def print_adfuller(inputSeries):
    result = adfuller(inputSeries)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

print_adfuller(spread1)

def divide_time_test(inputSeries):
    X = inputSeries.values
    split = round(len(X) / 2)
    X1, X2 = X[0:split], X[split:]
    mean1, mean2 = X1.mean(), X2.mean()
    var1, var2 = X1.var(), X2.var()
    print('mean1=%f, mean2=%f' % (mean1, mean2))
    print('variance1=%f, variance2=%f' % (var1, var2))

divide_time_test(spread1)

def autocorrelation_test(inputSeries):
    print("auto correlation: %f" % inputSeries.autocorr(lag=30))

def correlation_test(data_1, data_2):
    merge_data = [data_1, data_2]
    cor_data = reduce(lambda left, right: pd.merge(left, right, on='Date'), merge_data)
    cor = cor_data.corr(method="pearson").iloc[0,1]
    print("Correlation: %f" % cor)

autocorrelation_test(spread1)
correlation_test(chart1,chart2)


xtick_interval = (ed - sd).days / 6

fig, ax1 = plt.subplots()
ax1.plot(spread1.index, spread1, 'r-', label = ticker1 + '-' + ticker2)
ax1.set_xlabel('Date')
ax1.set_ylabel(ticker1 + '-' + ticker2 ,color='r')
ax1.tick_params('y', colors='r')
plt.legend(loc='upper left')

ax1.xaxis.set_major_locator(ticker.MultipleLocator(xtick_interval))
fig.tight_layout()


plt.show()