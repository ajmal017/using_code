import FinanceDataReader as fdr
ss = fdr.DataReader('IXIC', '2010')
print(ss, type(ss.index))
