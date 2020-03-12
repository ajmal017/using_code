import pandas as pd
import matplotlib.pyplot as plt

import FinanceDataReader as fdr

WTI1 = fdr.DataReader('CL', '1980')
WTI2 = fdr.DataReader('CL', '2001')

WTI = pd.concat([WTI1, WTI2], axis=0)
WTI.drop_duplicates(inplace=True)
WTI.index = pd.to_datetime(WTI.index)

WTI = WTI.loc['1994-01-02':'2019-10-02']

oil_production1 = pd.read_excel('./data/oil production.xlsx', sheet_name='Sheet3')
oil_production1.drop(axis=1, index=[0,1,2,3,4,39,40], inplace=True)
oil_production1.index = pd.to_datetime(oil_production1['Month'])
oil_production1['Major'] = oil_production1['World'] - oil_production1['ETC']
production_change2 = pd.Series((oil_production1['Major'].pct_change() * 100).rolling(12).sum())
production_change2.index = oil_production1.index
oil_production1.drop(columns=['Month', 'World', 'ETC', 'Major'], inplace=True)
oil_production1 = oil_production1[['Saudi Arabia', 'Russia', 'US', 'Brazil', 'UK', 'Iran', 'Iraq', 'Norway', 'Venezuela', 'Qatar', 'Kuwait', 'Mexico']]


y1= []
labels2=[]
for i in range(len(oil_production1.columns)):
    y1.append(oil_production1.iloc[:,i])
    labels2.append(oil_production1.columns[i])
print(y1, labels2, production_change2)


window = 100

Roll_Max = WTI['Close'].rolling(window, min_periods=1).max()
Daily_Drawdown = WTI['Close']/Roll_Max - 1.0

# Plot the results

fig, [ax5, ax1, ax2, ax3] = plt.subplots(4,1, figsize=(15,10))
plt.subplots_adjust(hspace = 0.5)

ax1.plot(WTI['Close'])
ax1.axhline(y=40, color='k', linestyle='-', linewidth=0.5)
ax2.stackplot(oil_production1.index , y1, labels=labels2)
ax2.legend(loc='upper left', ncol=3, fontsize=7)
ax3.plot(Daily_Drawdown)
ax3.axhline(y=-0.2, color='r', linestyle='-', linewidth=0.5)
ax3.axhline(y=-0.4, color='firebrick', linestyle='-', linewidth=0.5)
ax4 = ax2.twinx()
ax4.plot(production_change2, color='k', linewidth=4)
ax4.axhline(y=0, color='k', linewidth=2, linestyle='dotted')
ax4.axhline(y=5, color='k', linewidth=2, linestyle='dotted')
ax5.plot(WTI['Close'])
ax5.set_yscale("log")

ax1.title.set_text("WTI")
ax5.title.set_text("Log Scale")
ax3.title.set_text("MDD, line with -20%")

print(WTI['Close'], oil_production1)
plt.tight_layout()
plt.savefig('WTIrolling.png')
plt.show()

