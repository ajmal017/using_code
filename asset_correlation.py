##TODO correlation bewtween assets

import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from functools import reduce

# tickers

raw_data1_ = fdr.DataReader('US500', '2006-01-04')
raw_data2_ = fdr.DataReader('US10YT=X', '2003')
SPX = raw_data1_['Close']
US10Y = raw_data2_['Close'].get(raw_data1_.index)

SPX_change = SPX.pct_change().rolling(250, min_periods=1).sum() * 100
US10Y_change = US10Y.diff().rolling(250, min_periods=1).sum()

# date format = %Y-%m-%d
start_date = "2015-01-01"
end_date = "2020-01-15"


def autocorrelation_test(inputSeries):
    print("auto correlation: %f" % inputSeries.autocorr(lag=30))


def rolling_correlation(data_1, data_2, window):
    rol_cor = data_1.rolling(window, min_periods=1).corr(data_2)
    print(rol_cor)
    return rol_cor


correl_ = rolling_correlation(SPX, US10Y, 250) * -1
correl = correl_.loc[start_date:end_date]

correl.to_csv('dd.csv')

fig, [ax1,ax2,ax3] = plt.subplots(nrows=3)
ax1.plot(correl)
ax2.plot(SPX_change.loc[start_date:end_date])
ax3.plot(US10Y_change.loc[start_date:end_date])
# # ax1.plot(spread1.index, spread1, 'r-', label=ticker1 + '-' + ticker2)
# # ax1.set_xlabel('Date')
# # ax1.set_ylabel(ticker1 + '-' + ticker2, color='r')
# # ax1.tick_params('y', colors='r')
# # plt.legend(loc='upper left')
# #
# # ax1.xaxis.set_major_locator(ticker.MultipleLocator(xtick_interval))
# # fig.tight_layout()
# #
plt.show()
