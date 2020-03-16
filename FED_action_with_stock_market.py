##TODO FED action and stock

import yfinance
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from adjustText import adjust_text

FED_rate = pd.read_csv('./data/FED_target_rate.csv', index_col='Date', squeeze=True)
FED_rate.index = pd.to_datetime(FED_rate.index)
_FED2010 = FED_rate['2010-01-01':]
print(_FED2010)
action_date = []
action = []
rate = []
cut_date = []
cut_date_pre = []
cut_rate = []
raise_date = []
raise_rate = []
weekday = []

for i in range(1, len(FED_rate)):
    if FED_rate.iloc[i-1] -0.25 > FED_rate.iloc[i]:
        action_date.append(FED_rate.index[i])
        cut_date.append(FED_rate.index[i])
        cut_date_pre.append(FED_rate.index[i] - datetime.timedelta(days=1))
        action.append('Cut '+ str(FED_rate.iloc[i] - FED_rate.iloc[i-1]) + 'bp')
        rate.append(FED_rate.iloc[i])
        cut_rate.append(FED_rate.iloc[i] - FED_rate.iloc[i-1])
        weekday.append(FED_rate.index[i].dayofweek)

for i in range(1, len(_FED2010)):
    if _FED2010.iloc[i - 1] > _FED2010.iloc[i] >= _FED2010.iloc[i - 1] - 0.25:
        action_date.append(_FED2010.index[i])
        cut_date.append(_FED2010.index[i])
        cut_date_pre.append(_FED2010.index[i] - datetime.timedelta(days=1))
        action.append('Cut '+ str(_FED2010.iloc[i] - _FED2010.iloc[i-1]) + 'bp')
        rate.append(_FED2010.iloc[i])
        cut_rate.append(_FED2010.iloc[i] - _FED2010.iloc[i-1])
        weekday.append(_FED2010.index[i].dayofweek)

print(cut_date)

FED_rate = FED_rate.to_frame()

action_date = pd.to_datetime(action_date)
cut_date = pd.to_datetime(cut_date)
raise_date = pd.to_datetime(raise_date)

pd_action = pd.DataFrame({'Action': action, 'Date': action_date}).set_index('Date')
pd_cut = pd.DataFrame({'Cut': cut_rate, 'Cut_date':cut_date, 'Cut_date_pre':cut_date_pre,
                       'Date': cut_date, 'Rate':rate}).set_index('Date')
pd_raise = pd.DataFrame({'Raise': raise_rate, 'Date': raise_date}).set_index('Date')


cut_1980 = pd_cut.loc['1980-01-01':'1989-12-31']
cut_1990 = pd_cut.loc['1990-01-01':'1999-12-31']
cut_2000 = pd_cut.loc['2000-01-01':'2004-12-31']
cut_2005 = pd_cut.loc['2005-01-01':'2009-12-31']
cut_2010 = pd_cut.loc['2010-01-01':]

print(cut_2010, pd_cut)



merge1 = FED_rate.merge(pd_action, how='left', left_index=True, right_index=True)\
    .merge(pd_cut,  how='left', left_index=True, right_index=True)\
    .merge(pd_raise,  how='left', left_index=True, right_index=True)


stock_data_ = yfinance.download('^GSPC', start='1980-01-01')
stock_data = stock_data_['Close']

# merge2 = pd.merge(stock_data, merge1, how='left', left_index=True, right_index=True)

stock_with_cut = pd.merge(stock_data, pd_cut, how='left', left_index=True, right_index=True)
stock_with_cut['Cut_date_pre'].fillna(method='ffill', limit=100, inplace=True)


def normalizing1(df):
    df['Close'] = (df['Close'] / df['Close'][1] -1) *100
    df['Close'][0] = np.NaN
    return df

def normalizing(df):
    df['Close'] = (df['Close'] / df['Close'][0] -1) *100
    return df



cut_groupby = stock_with_cut.groupby('Cut_date_pre')
merge2 = cut_groupby.apply(normalizing1)
for2010 = cut_groupby.apply(normalizing)
_1980 = merge2.loc['1980-01-01':'1989-12-31']
_1990 = merge2.loc['1990-01-01':'1999-12-31']
_2000 = merge2.loc['2000-01-01':'2004-12-31']
_2005 = merge2.loc['2005-01-01':'2009-12-31']
_2010 = merge2.loc['2010-01-01':]

fig, [ax1, ax2, ax3, ax4] = plt.subplots(nrows=4, figsize=(16.5,9.5))
ax1.plot(_1990['Close'])
ax2.plot(_2000['Close'])
ax3.plot(_2005['Close'])
ax4.plot(_2010['Close'])


ax1.axhline(y=0, color='k', linewidth=0.3, alpha=0.8)
ax1.axhline(y=-10, color='k', linewidth=0.3, alpha=0.8)
ax1.axhline(y=-20, color='k', linewidth=0.3, alpha=0.8)

for i in range(len(cut_1990)):
    ax1.axvline(x=cut_1990.index[i], color='gray', linewidth=0.3)
for i, text in enumerate(cut_1990['Cut_date']):
    ax1.annotate(text.strftime("%m-%d"), xy=(cut_1990.index[i]+datetime.timedelta(days=3), -20), rotation=90, fontsize=7)

ax2.axhline(y=0, color='k', linewidth=0.3, alpha=0.8)
ax2.axhline(y=-10, color='k', linewidth=0.3, alpha=0.8)
ax2.axhline(y=-20, color='k', linewidth=0.3, alpha=0.8)

for i in range(len(cut_2000)):
    ax2.axvline(x=cut_2000.index[i], color='gray', linewidth=0.3)
for i, text in enumerate(cut_2000['Cut_date']):
    ax2.annotate(text.strftime("%m-%d"), xy=(cut_2000.index[i]+datetime.timedelta(days=2), -20), rotation=90, fontsize=7)


ax3.axhline(y=0, color='k', linewidth=0.3, alpha=0.8)
ax3.axhline(y=-10, color='k', linewidth=0.3, alpha=0.8)
ax3.axhline(y=-20, color='k', linewidth=0.3, alpha=0.8)

for i in range(len(cut_2005)):
    ax3.axvline(x=cut_2005.index[i], color='gray', linewidth=0.3)
for i, text in enumerate(cut_2005['Cut_date']):
    ax3.annotate(text.strftime("%m-%d"), xy=(cut_2005.index[i]+datetime.timedelta(days=2), -20), rotation=90, fontsize=7)


ax4.axhline(y=0, color='k', linewidth=0.3, alpha=0.8)
ax4.axhline(y=-10, color='k', linewidth=0.3, alpha=0.8)
ax4.axhline(y=-20, color='k', linewidth=0.3, alpha=0.8)

for i in range(len(cut_2010)):
    ax4.axvline(x=cut_2010.index[i], color='gray', linewidth=0.3)
for i, text in enumerate(cut_2010['Cut_date']):
    ax4.annotate(text.strftime("%m-%d"), xy=(cut_2010.index[i], -20), rotation=90, fontsize=7)


ax1.set_title("S&P500 performance after >=50bp cut, max=100days \n (every cut for 2010s)")
plt.tight_layout()

plt.show()