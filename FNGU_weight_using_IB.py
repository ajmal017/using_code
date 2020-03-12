import pandas as pd
import IB_Req_Function

raw_df = pd.read_excel('0. etf_components.xlsx', sheet_name='FNGU')
tickers = list(raw_df['Symbol'].dropna().values)

df_from_each_file = (IB_Req_Function.request(f, duration='3 M', barsize='1 day', index_col = 'Date',
                                             usecols=['Close'], enddatetime="20200310 00:00:00")
                     for f in tickers)
df = pd.concat(df_from_each_file, ignore_index=False, join='inner', axis=1)
df.columns = tickers

# quarterly rebalancing weight , 10% each
#
df_norm = df.loc['2020-01-02':].apply(lambda x: x / x[0] * 10)
weight_now = df_norm.apply(lambda x: x / df_norm.sum(axis=1) * 100)
weight_now.to_csv('./data/FNGU_weight_now.csv')
print(weight_now)