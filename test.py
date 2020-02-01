import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
from pandas.core.common import SettingWithCopyWarning
import matplotlib.ticker as mtick
from cycler import cycler
import matplotlib.cm as cm
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


ticker1 = 'TSLA'
file1 = 'TSLA_20200201_3Y_2hours'

# cleaning data of earning season

df = pd.read_excel('0. nasdaq100.xlsx')
df = df[df['Ticker'] == ticker1]
df['Date_day'] = df['Date'].dt.strftime("%Y-%m-%d")
df.set_index('Date_day', inplace=True)
df = df.iloc[:, 1:]
df.dropna(how='all', inplace=True)
df['Act'] = ''
df['Con'] = ''
df['Real-Con'] = ''
df['SurpShock'] = ''

# Fiscal string cleaning. 'Q'n YY -> YY'Q'n


for i in range(len(df)):
    df['Fiscal'][i] = df['Fiscal'][i].strip()
    sp1, sp2 = df['Fiscal'][i].split(' ')
    df['Fiscal'][i] = sp2 + sp1

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
        df['Real-Con'][i] = '+ Surp'
    elif df['Act'][i] == 0 and df['Con'][i] == 1:
        df['Real-Con'][i] = '- Shock'
    elif df['Act'][i] == 0 and df['Con'][i] == 0:
        df['Real-Con'][i] = -round((df['Actual'][i] / df['Consensus'][i] - 1) * 100, 1)
    elif df['Act'][i] == 1 and df['Con'][i] == 1:
        df['Real-Con'][i] = round((df['Actual'][i] / df['Consensus'][i] - 1) * 100, 1)

# 3 types surprise / consensus / shock

for i in range(len(df)):
    if df['Real-Con'][i] == '+ Surp':
        df['SurpShock'][i] = 'Surprise'
    elif df['Real-Con'][i] == '- Shock':
        df['SurpShock'][i] = 'Shock'
    elif df['Real-Con'][i] > 15:
        df['SurpShock'][i] = 'Surprise'
    elif df['Real-Con'][i] > -15:
        df['SurpShock'][i] = 'in-line'
    else:
        df['SurpShock'][i] = 'Shock'



# bar data by 2hours

read_ticker1 = './ib_db/' + file1 + '.csv'
raw_data1 = pd.read_csv(read_ticker1)
raw_data_date = pd.to_datetime(raw_data1['Date'])
raw_data1['Date_day'] = raw_data_date.dt.strftime("%Y-%m-%d")
raw_data1.set_index('Date_day', inplace=True)

# merging

merge1 = pd.merge(raw_data1, df, left_index=True, right_index=True, how='left')
merge1 = merge1.fillna(method='ffill', limit=12)
merge_col = ['Date_x', 'Fiscal', 'Open', 'Real-Con']
merge2 = merge1[merge_col]
merge2 = merge2.dropna(axis=0, how='any')
merge2.set_index('Date_x', inplace=True)
merge2.sort_values(by=['Date_x'], ascending=True, inplace=True)
merge2['Fis_Earn'] = merge2['Fiscal'].astype(str) + '  ' + merge2['Real-Con'].astype(str)


# normalizing each Quarter, using groupby, apply

def normalizing(df):
    df['Open'] = (df['Open'] / df['Open'][0] -1) *100
    return df


merge2 = merge2.groupby('Fis_Earn').apply(normalizing)
merge2.to_csv('ddd.csv')

# plot color setting
colormap = plt.nipy_spectral()
colornum = int(len(pd.Series(merge2['Fiscal'].unique())))
# colors = [colormap(i) for i in np.linspace(0, 1, colornum)]

print(colornum)
print(type(colornum))