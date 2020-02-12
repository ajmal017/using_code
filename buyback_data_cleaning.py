import pandas as pd

df = pd.read_excel('./data/corporate event.xlsx')
buyback = df[df['Action Type'] == 'Stock Buyback'].iloc[:, [1,3,7,9]]
buyback.set_index('Effective Date', inplace=True)
cols = ['Ticker', 'Amount', 'Outstanding Shares']
buyback.columns=cols
buyback['Ticker'] = buyback['Ticker'].str.replace('US Equity', '').str.strip()
buyback['Outstanding Shares'] = buyback['Outstanding Shares'].str.replace('Current Share Out:', '').str.strip()
buyback['Amount'] = buyback['Amount'].str.replace(' Amount to be bought: ', '').str.strip()
print(buyback)