import yfinance as yf
from pandas_datareader import data as pdr
from datetime import datetime
import pandas as pd
from tqdm import tqdm


#tickers = yf.Tickers('msft aapl goog')

#tickers.aapl.history(period="1mo")


# yf.download(tickers:"a b c", period = "1d, 1mo, 1y, max, ytd", interval = "1h, 1m, 1d, 1mo", group_by, auto_adjust,
# prepost=Bool, threads=Bool)
# data = yf.download("SPY AAPL MSFT AMD", period = "5y", interval = "1d", auto_adjust=True)

yf.pdr_override()
now = datetime.now()
ticker1 = "^DJI"
start_date = "1980-11-28"
end_date = "2020-02-14"
date_now = datetime.strftime(now, "%Y%m%d")

# for multiple stock tickers from csv

if ticker1 == "":
    read_csv = pd.read_csv('./db/0.etf_db_metadata.csv')
    tickers = read_csv['Symbol']
    tickers = pd.Series(tickers)
    tickers.drop_duplicates(inplace=True)
    tickers.reset_index(drop=True, inplace=True)
    tickers.sort_values(ascending=True, inplace =True)
    print(tickers)
    for i in tqdm(range(len(tickers))):
        ticker2 = tickers[i].replace('.', '-')
        data = pdr.get_data_yahoo(ticker2, start=start_date, end=end_date)
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        data = pd.DataFrame(data)
        data = round(data, 2)
        savename = './db/' + ticker2 + '.csv'
        data.to_csv(savename)

# get one simply

else:
    data = pdr.get_data_yahoo(ticker1, start=start_date, end=end_date)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data = pd.DataFrame(data)
    data = round(data, 2)
    savename = './db/' + ticker1 + '.csv'
    data.to_csv(savename)