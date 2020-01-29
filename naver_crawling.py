import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
from tqdm import tqdm
import numpy as np

read_csv = pd.read_csv('./db/0.korean_db_metadata.csv', encoding='CP949')
tickers = read_csv['Symbol']
names = read_csv['Name']
df_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]

count = '3000'
print(tickers)

for i in tqdm(range(len(tickers))):
    code = tickers[i][-6:]
    name = names[i]
    raw_data = []
    url = f'https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count={count}&requestType=0'
    r = urllib.request.urlopen(url)
    xml_data = r.read().decode('EUC-KR')
    root = ET.fromstring(xml_data)
    for index, each in enumerate(root.findall('.//item')):


        temp = each.attrib['data'].split('|')
        raw_data.append({"Date":temp[0], "Open":temp[1], "High":temp[2], "Low":temp[3],
                         "Close":temp[4], "Volume":temp[5], "Adj Close":temp[4]})


        # print(raw_data)
    data1 = pd.DataFrame(raw_data, columns=df_cols)
    data1['Date'] = pd.to_datetime(data1['Date'])
    data1.set_index('Date', inplace=True)
    data1 = round(data1.astype(int), -1)
    data1.replace(to_replace=0, value=np.NaN, inplace=True)
    data1.fillna(method='ffill', inplace=True)

    savename = './db/' + name + '.csv'
    data1.to_csv(savename)