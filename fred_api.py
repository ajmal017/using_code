from fredapi import Fred
fred = Fred(api_key='6e2c6245f074967fbc4fadf157442863')
import pandas as pd

## https://datascienceschool.net/view-notebook/54411c71f041487aba00a3ddcd17e5d8/

# housing = fred.search("housing", limit=10)
# print(housing)

series_name = 'CSUSHPINSA'

data = fred.get_series(series_name)
data = pd.DataFrame(data)
data.reset_index(drop=False, inplace=True)
data.columns=['Date', '']
data.set_index('Date', inplace=True)
savename = './db/1.fred.' + series_name + '.csv'
data.to_csv(savename)
print(data)