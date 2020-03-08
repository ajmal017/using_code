from ib_insync import *
import pandas as pd
from pandas.core.common import SettingWithCopyWarning
import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

ib = IB()
ib.connect('127.0.0.1', 7496, 0)

account1 = ib.accountSummary()
account2 = ib.portfolio()
account3 = ib.executions()
df1 = util.df(account1)
df2 = util.df(account2)
df3 = util.df(account3)
liquidity = int(pd.to_numeric(df1[df1['tag'] == 'NetLiquidationByCurrency'].iloc[0,2]))
cash = round(pd.to_numeric(df1[df1['tag'] == 'CashBalance'].iloc[0, 2]) / liquidity * 100, 1)


df2['contract'] = df2['contract'].astype(str)
symbol_start = df2['contract'].str.find('symbol=') + 8
symbol_end = df2['contract'].str.find("', right")

df2['symbol'] = ''
for i in range(len(df2)):
    df2['symbol'][i] = df2['contract'][i][symbol_start.iloc[i]:symbol_end.iloc[i]]

df_= df2[['position', 'averageCost', 'marketPrice', 'marketValue', 'unrealizedPNL', 'realizedPNL']]
df_['Size'] = df_['marketValue'] / liquidity * 100
df_['Unreal. P&L'] = df_['unrealizedPNL'] / df2['marketValue'] * 100
df_['Realized P&L'] = df_['realizedPNL'] / df2['marketValue'] * 100
df_['Daily Move'] = ''
df_.insert(0, 'Symbol', df2['symbol'])

df = df_[['Symbol', 'Size', 'averageCost', 'marketPrice', 'Daily Move', 'Unreal. P&L', 'Realized P&L']]
df.columns = ['Symbol', 'Size', 'Avg. Price', 'Last Price', 'Daily Move', 'Unreal. P&L', 'Realized P&L']
df = round(df, 1)

if df3 is not None:
    df3 = df3[['side', 'shares', 'price']]
    df3['Size'] = df3['shares'] * df3['price'] / liquidity * 100

print(df, "\n net liquid: ", liquidity, "\n action: ", df3, "\n daily Unreal PNL: ",
      round((df_['unrealizedPNL'] / liquidity * 100).sum(), 1) , "\n daily Realized PNL: ",
      round((df_['realizedPNL'] / liquidity * 100).sum(), 1) , "\n Cash: ", cash)
