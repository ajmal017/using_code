import IB_Req_Function
from ib_insync import *
import pandas as pd

SPX500 = IB_Req_Function.request('SPX500', enddatetime= '20050302 00:00:00', duration='20 Y', barsize='1 day', index_col='Date')
SPX500.index = pd.to_datetime(SPX500.index)


ib = IB()
ib.connect('127.0.0.1', 7496, 0)


SPX500.to_csv('US5001.csv')