import pandas as pd
import numpy as np

raw_data = pd.read_excel('./data/buybacks.xlsx', header=0, index_col=0, na_values=[0,np.nan])
raw_data.dropna(how='all', axis=0, inplace=True)
raw_data.fillna('00.00M', inplace=True)


# Million , Billion  cleaning

def digit_measure(string):
    digit1, digit2 = string.split(sep='.')
    if digit2[-1]=='M' and len(digit2) ==3:
        digit = str(digit1) + digit2[:2] + '0000'
    elif digit2[-1]=='M' and len(digit2) ==4:
        digit = str(digit1) + digit2[:3] + '000'
    elif digit2[-1]=='B' and len(digit2) ==3:
        digit = str(digit1) + digit2[:2] + '0000000'
    elif digit2[-1]=='B' and len(digit2) ==4:
        digit = str(digit1) + digit2[:3] + '000000'
    else: digit = 0
    return digit


tickers = raw_data.columns
buybacks = pd.DataFrame()
for i in range(len(tickers)):
    buybacks[tickers[i]] = raw_data.iloc[:,i].transform(lambda x: digit_measure(x))
buybacks = buybacks.apply(pd.to_numeric)
buybacks['Sum(Bil.$)'] = buybacks.apply(np.sum, axis=1)
buybacks = round(buybacks.transform(lambda x: x/1000000000),2)
print(buybacks)
buybacks.to_excel('./data/buybacks_cleaned.xlsx')



