# https://github.com/farhadab/sec-edgar-financials
import pandas as pd
from edgar.stock import Stock
import sys
import os
from functools import reduce

ticker1 = 'AAPL'
stock = Stock(ticker1)

years = [2017, 2018, 2019, 2020]
quarters = [1,2,3,4]
period = 'quarterly'  # or 'annual', which is the default

# main

file_names = list(ticker1 + '_' + str(q)+'Q'+str(y)[2:] for y in years for q in quarters)
print(file_names)


# make list of dataframes
dfs = []
load_name = './test/' + pd.Series(file_names) + '.csv'
for i in range(len(file_names)):
    try:
        dfs.append(pd.read_csv(load_name[i], index_col=0))
    except: pass

index1 = pd.read_csv('./test/' + ticker1 + '_index.csv', usecols=[1])

dfs.insert(0, index1)
df_merged = [index1]
for i in range(len(dfs)-1):
    df_merged.append(pd.merge(df_merged[0], dfs[i+1], how='left', on='Label'))

for i in range(len(df_merged)):
    df_merged[i].set_index('Label', inplace=True)
#
# print(df_merged)
df_concat = pd.concat(df_merged, axis=1)
# print(df_concat)
df_concat.to_csv('dd.csv')


#
# # for i in range(len(df.Name)):
# #     df['Label'][i] = ''.join(
# #         ' ' + char if char.isupper() else char.strip() for char in df['Name'][i]).strip()
