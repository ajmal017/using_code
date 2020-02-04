import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


ticker1 = 'DIS'
file1 = 'DIS_20200205_3Y_2hours'
ffil_days = 3
# cleaning data of earning season

df = pd.read_csv('./data/cleaned_earning_calendar.csv')
df = df[df['Ticker'] == ticker1]
df.set_index('Date', inplace=True)
df.dropna(how='all', inplace=True)
df['Act'] = ''
df['Con'] = ''
df['EPS.Real-Con'] = ''
df['Rev.Real-Con'] = round((df['RevActual'] / df['RevConsensus'] -1) * 100, 1)


# real-con column setting


def pos_neg(num):
    if num > 0:
        return True
    else:
        return False


for i in range(len(df)):
    df['Act'][i] = pos_neg(df['Actual'][i])
    df['Con'][i] = pos_neg(df['Consensus'][i])

for i in range(len(df)):
    if df['Act'][i] == 1 and df['Con'][i] == 0:
        df['EPS.Real-Con'][i] = '+ Surp'
    elif df['Act'][i] == 0 and df['Con'][i] == 1:
        df['EPS.Real-Con'][i] = '- Shock'
    elif df['Act'][i] == 0 and df['Con'][i] == 0:
        df['EPS.Real-Con'][i] = -round((df['Actual'][i] / df['Consensus'][i] - 1) * 100, 1)
    elif df['Act'][i] == 1 and df['Con'][i] == 1:
        df['EPS.Real-Con'][i] = round((df['Actual'][i] / df['Consensus'][i] - 1) * 100, 1)


# bar data by 2hours

read_ticker1 = './ib_db/' + file1 + '.csv'
raw_data1 = pd.read_csv(read_ticker1)
raw_data_date = pd.to_datetime(raw_data1['Date'])
raw_data1['Date_day'] = raw_data_date.dt.strftime("%Y-%m-%d")
raw_data1.set_index('Date_day', inplace=True)

# merging  and  before market  //  after close

merge1 = pd.merge(raw_data1, df, left_index=True, right_index=True, how='left')

# if merge1['relasetime'] before market, bfill and ffill , after market -> ffill only
count1 = merge1['releasetime'].value_counts()
count=count1.index[0]
if count != 'After Close':
    merge1 = merge1.fillna(method='bfill', limit=(ffil_days-2) * 4)
    merge1 = merge1.fillna(method='ffill', limit=(ffil_days-1) * 4)

else:
    merge1 = merge1.fillna(method='ffill', limit=ffil_days * 4)


# merged data cleaning

merge_col = ['Date', 'Calendar', 'Open', 'EPS.Real-Con', 'Rev.Real-Con']
merge2 = merge1[merge_col]
merge2 = merge2.dropna(axis=0, how='any')
merge2.set_index('Date', inplace=True)
merge2.sort_values(by=['Date'], ascending=True, inplace=True)
merge2['Fis_Earn'] = merge2['Calendar'].astype(str) + ': EPS  ' + merge2['EPS.Real-Con'].astype(str) + '% ' \
                     'Rev ' + merge2['Rev.Real-Con'].astype(str) + '%'


# normalizing each Quarter, using groupby, apply

def normalizing(df):
    df['Open'] = (df['Open'] / df['Open'][3] -1) *100
    return df


merge2 = merge2.groupby('Fis_Earn').apply(normalizing)
merge2.to_csv('ddd.csv')


## make line chart

# color setting
sns.set_palette('Paired')
colornum = int(len(pd.Series(merge2['Calendar'].unique())))
colors = sns.color_palette(n_colors=colornum)

# plotting

fig, ax = plt.subplots(figsize=(12,7))
merge2.groupby('Fis_Earn')['Open'].plot(legend=True, linewidth=1.5)

# set ticks
np_xticks = pd.Series(np.arange(-ffil_days,+(ffil_days+1)*3+1) *2)
xticks = 'T' + np_xticks.astype(str) + 'h'
plt.xticks(ticks=np.arange(0,(ffil_days+1)*4), labels=xticks)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

# set label
ax.set_xlabel('hours after earnings')
ax.set_ylabel('price movement')

# set color
ax.set_prop_cycle('color', colors)

# set legend
plt.legend(title="Actual-Consensus(%)", loc='best', handlelength=1.5, ncol=3,
           fontsize='small', fancybox=True, markerfirst=False)
plt.title(ticker1)

# save to file as png format

out_path = './charts/' + '{}_earnings_surprise.png'.format(ticker1)
plt.savefig(out_path)


plt.show()

# for i, g in mer1.groupby('Fiscal'):
#     globals()['df_' + str(i)] = g
