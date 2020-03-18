import FinanceDataReader as fdr
import matplotlib.pyplot as plt

df = fdr.DataReader('US500', start='1990-01-01', end=None)
df['Close'].plot()

plt.show()


