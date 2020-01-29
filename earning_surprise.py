import pandas as pd
from mpl_finance import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import datetime
import matplotlib.dates as matdates
from matplotlib import rc
rc('font', family="Batang")


ticker1 = 'AAPL'

df = pd.read_excel('./db/0. nasdaq100 earnings.xlsx')
df['Date'] = df['Date'].dt.strftime("%Y-%m-%d")
df.set_index('Date', inplace=True)
df = df.iloc[:,1:]
df.dropna(how='all', inplace=True)
df['Surprise'] = round((df['Actual'] / df['Consensus'] -1) * 100, 1)
df = df[df['Ticker']==ticker1]
print(df)


start_date = "2015-04-01"
end_date = "2020-01-05"
read_ticker1 = './db/' + ticker1 + '.csv'
raw_data1 = pd.read_csv(read_ticker1)

# to skip the days not in data
sd = datetime.datetime.strptime(start_date,"%Y-%m-%d")
st = datetime.datetime.strftime(sd,"%Y-%m-%d")
ed = datetime.datetime.strptime(end_date,"%Y-%m-%d")
et = datetime.datetime.strftime(ed,"%Y-%m-%d")


while st not in raw_data1['Date'].values:
    sd += datetime.timedelta(days=1)
    st = datetime.datetime.strftime(sd,"%Y-%m-%d")
    print(sd)
else: pass

while et not in raw_data1['Date'].values:
    ed -= datetime.timedelta(days=1)
    et = datetime.datetime.strftime(ed,"%Y-%m-%d")
    print(ed)
else: pass


raw_data1.set_index('Date', inplace=True)
merge1 = pd.merge(raw_data1, df, left_index=True, right_index=True, how='left')
print(merge1)
merge1 = merge1.fillna(method='ffill', limit=3)
merge2 = merge1.dropna(axis=0, how='any')
merge2.drop(columns=['Ticker', 'Time'], inplace=True)
print(merge2)
savename = './data/' + ticker1 + '.csv'
merge2.to_csv(savename)
