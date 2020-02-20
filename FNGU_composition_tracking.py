import pandas as pd

raw_df = pd.read_excel('etf_components.xlsx', sheet_name='FNGU')
Symbol = raw_df['Symbol']
Symbol.dropna(inplace=True)
print(Symbol)

load_name = './db/' + Symbol + '.csv'

# load data from database (of each symbols) and concat close data

df_from_each_file = (pd.read_csv(f, index_col=0, usecols=['Date', 'Close']) for f in load_name)
df = pd.concat(df_from_each_file, ignore_index=False, join='inner', axis=1)
df.columns = Symbol

# quarterly rebalancing weight , 10% each

df_norm = df.loc['2020-01-02':].apply(lambda x: x / x[0] * 10)
weight_now = df_norm.apply(lambda x: x / df_norm.sum(axis=1) * 100)
weight_now.to_csv('FNGU_weight_now.csv')
print(weight_now)