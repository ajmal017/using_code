# https://github.com/farhadab/sec-edgar-financials
import pandas as pd
from edgar.stock import Stock
import sys
import os
import itertools
from functools import reduce

ticker1 = 'AAPL'
stock = Stock(ticker1)

year = 2019
quarter = 2
period = 'quarterly'  # or 'annual', which is the default

# using defaults to get the latest annual, can simplify to stock.get_filing()
filing = stock.get_filing(period, year, quarter)

# financial reports (contain data for multiple years)
income_statements = filing.get_income_statements()
balance_sheets = filing.get_balance_sheets()
cash_flows = filing.get_cash_flows()

print(income_statements)
