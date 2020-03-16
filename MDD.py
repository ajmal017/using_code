import pandas as pd
import matplotlib.pyplot as plt
import FinanceDataReader as fdr

# using yfinance, NQ = ^IXIC , SPX = ^GSPC  and use 'Adj Close'

NQ = fdr.DataReader('IXIC', '2005')
SPX = fdr.DataReader('US500', '2005')
KOSPI = fdr.DataReader('KS11', '2005')
KOSDAQ = fdr.DataReader('KQ11', '2005')

ticker = KOSDAQ

ticker.index = pd.to_datetime(ticker.index)





## https://quant.stackexchange.com/questions/18094/how-can-i-calculate-the-maximum-drawdown-mdd-in-python
# We are going to use a trailing 252 trading day window
window = 800

# Calculate the max drawdown in the past window days for each day in the series.
# Use min_periods=1 if you want to let the first 252 days data have an expanding window
Roll_Max = ticker['Close'].rolling(window, min_periods=1).max()
Daily_Drawdown = ticker['Close']/Roll_Max - 1.0

# Next we calculate the minimum (negative) daily drawdown in that window.
# Again, use min_periods=1 if you want to allow the expanding window
Max_Daily_Drawdown = Daily_Drawdown.rolling(window, min_periods=1).min()

print(NQ, type(NQ.index), Daily_Drawdown, Max_Daily_Drawdown)


# Plot the results

fig, [ax1, ax2, ax3] = plt.subplots(3,1, figsize=(15,9))
plt.subplots_adjust(hspace = 0.5)

ax1.plot(ticker['Close'])
ax1.axhline(y=40, color='k', linestyle='-', linewidth=0.5)
ax2.plot(ticker['Close'])
ax2.set_yscale("log")
ax3.plot(Daily_Drawdown)
ax3.axhline(y=-0.2, color='r', linestyle='-', linewidth=0.5)
ax3.axhline(y=-0.4, color='firebrick', linestyle='-', linewidth=0.5)

ax1.title.set_text("KOSDAQ")
ax2.title.set_text("Log Scale")
ax3.title.set_text("MDD, line with -20%")


plt.tight_layout()
plt.savefig('KOSDAQ.png')
plt.show()