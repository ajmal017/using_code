import FinanceDataReader as fdr
import pandas as pd
import pytz
import re
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
import datetime


# get list of ticker and name of us stocks

df_snp = fdr.StockListing('S&P500')
df_nasdaq = fdr.StockListing('NASDAQ')
df_concat = pd.concat([df_snp, df_nasdaq], axis=0, join='outer')
df_concat.rename(columns={'Symbol':'Ticker'},inplace=True)


raw_data = pd.read_excel('./data/earning_evt_from_2017.xlsx')
raw_data.drop(['이름', '시간', '서프라이즈', '잠정실적'], axis=1, inplace=True)
cols = ['Ticker', 'DateTime', 'Actual', 'Consensus', 'RevActual', 'RevConsensus']
raw_data.columns=cols

# cleaning Ticker
Tickers = []
for ticker in raw_data['Ticker']:
    tickers = ticker.replace(' US', '')
    Tickers.append(tickers)
raw_data['Ticker'] = Tickers

# merge and get name from ticker, using fdr
df = pd.merge(raw_data, df_concat[['Ticker', 'Name', 'Sector', 'Industry']], on = 'Ticker', how = 'left')
df.drop_duplicates(['Ticker', 'DateTime'], inplace=True)

df.set_index('DateTime', inplace=True)
df.sort_index(ascending=True, inplace=True)
df = df[['Ticker', 'Name', 'Actual', 'Consensus', 'RevActual', 'RevConsensus', 'Sector', 'Industry']]


# calendar Quarter
cy = pd.Series(df.index.get_level_values(0)) - datetime.timedelta(days=90)
cy_y = cy.astype(str).str.slice(2,4)
cy_q = cy.dt.quarter
ccf = list(cy_y.astype(str) + "Q" + cy_q.astype(str))
df.insert(2, "Calendar", ccf, True)

# UTC setting and convert to EST
df['UTC'] = df.index.tz_localize(pytz.utc)
df.index = df.index.tz_localize(pytz.utc).tz_convert(pytz.timezone('US/Eastern'))

# split datetimeIndex to date, time. and multi-indexing
df.index = pd.MultiIndex.from_arrays([df.index.date, df.index.time], names=['Date','Time'])

df['releasetime'] = ''
for i in range(len(df)):
    reltime = int(re.split('\W', str(df['UTC'][i]))[3])
    if reltime >= 20:
        df['releasetime'][i] = 'After Close'
    else:
        df['releasetime'][i] = 'Before Open'

df.to_csv('./data/cleaned_earning_calendar.csv')


print(df)
