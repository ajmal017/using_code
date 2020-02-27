from pyalgotrade.technical import ma
from pyalgotrade import plotter
from pyalgotrade.barfeed import csvfeed

feed = csvfeed.GenericBarFeed('DAY')
fileName = "C:/python_final/using_codes/db/AAPL.csv"
feed.addBarsFromCSV("AAPL", fileName)

sma = ma.SMA()