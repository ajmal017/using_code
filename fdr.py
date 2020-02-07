import FinanceDataReader as fdr
import matplotlib.pyplot as plt

df = fdr.DataReader('BTC/USD', start='2015-01-01', end=None)
df['Close'].plot()

plt.show()


