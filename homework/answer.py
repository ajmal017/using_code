import pandas as pd
raw_data = pd.read_excel('nasdaq100.xlsx')
from pandas.core.common import SettingWithCopyWarning
import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
