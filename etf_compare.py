import pandas as pd
from glob import glob
import re
import seaborn as sns
import matplotlib.pyplot as plt
from functools import reduce

path = r'./db/'
filenames = glob(path + 'xl*.csv')
filename = []

for i in range(len(filenames)):
    filename.append(re.sub('\W', '', filenames[i]))
    filename[i] = filename[i].replace('csv', '').replace('db', '')
print(filename)
load_name = './db/' + pd.Series(filename) + '.csv'

dfs = (pd.read_csv(f, index_col=0, usecols=[0,4]) for f in load_name)
df = pd.concat(dfs, ignore_index=False, join='inner', axis=1)
df.columns = filename
correl = df.corr(method='pearson')

print(df)

sns.heatmap(correl)
plt.show()

#
# for i in filename:
#     globals()[str(i)] = dfs[i]
#
# print(ZSL)
#
# print(df)
