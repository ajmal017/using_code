import pandas as pd

raw_data = pd.read_excel('./data/buybacks.xlsx', index_col=0)
raw_data.dropna(how='all', axis=0, inplace=True)
raw_data.fillna(0, inplace=True)


def digit_measure(string):
    if len(string) > 3:
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

# print(range(1,len(raw_data.iloc[0,:])))
# print(len(raw_data))

for i in range(len(raw_data)):
    for j in range(1,len(raw_data.iloc[0,:])):
        raw_data.iloc[i,j] = digit_measure(raw_data.iloc[i,j])
#
# print(raw_data)



