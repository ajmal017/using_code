# https://github.com/farhadab/sec-edgar-financials
import pandas as pd
from edgar.stock import Stock
import sys
import os
from functools import reduce

ticker1 = 'AAPL'
stock = Stock(ticker1)

years = [2017, 2018, 2019, 2020]
quarters = [1, 2, 3, 4]
period = 'quarterly'  # or 'annual', which is the default

file_names = []
# main

for y in years:
    for q in quarters:

        year = y  # can use default of 0 to get the latest
        quarter = q  # 1, 2, 3, 4, or default value of 0 to get the latest
        # using defaults to get the latest annual, can simplify to stock.get_filing()
        filing = stock.get_filing(period, year, quarter)

        # financial reports (contain data for multiple years)
        income_statements = filing.get_income_statements()
        balance_sheets = filing.get_balance_sheets()
        cash_flows = filing.get_cash_flows()

        all_statements = [income_statements, balance_sheets, cash_flows]

        # quarter name
        quarter_name = str(quarter) + 'Q' + str(year)[2:]

        # iterate to make each IS,BS, CF files
        for i, sheet in enumerate(all_statements):
            file_path = './test/' + ticker1 + str(i) + quarter_name + '.csv'

            # get excel file with sys.stdout changing

            sys.stdout = open(file_path, 'w', encoding='unicode_escape')
            print(sheet)

            # reset sys.stdout

            sys.stdout = sys.__stdout__

            # data cleaning

            read_csv = pd.Series(pd.read_csv(file_path, encoding='unicode_escape').columns)
            raw_string = read_csv.str.cat(sep=',')
            raw_list = pd.Series(raw_string.split("us-gaap_"))
            raw_df = raw_list.str.split("': ", expand=True)

            # select columns : label and value

            df = raw_df.iloc[:, [0, 2, 3]]
            df.columns = ['Name', 'Label', quarter_name]
            df = df.iloc[range(int(len(df) / 2 + 1))]
            for i in range(len(df.Name)):
                df['Label'][i] = ''.join(
                    ' ' + char if char.isupper() else char.strip() for char in df['Name'][i]).strip()
            df.drop(0, axis=0, inplace=True)
            df.reset_index(drop=True, inplace=True)

            # extract only numeric value
            df[quarter_name] = df[quarter_name].str.extract(r'([-+]?\d+.\d+)')
            df.to_csv(file_path)

            # print(df)

        # concat all statements

        for i, sheet in enumerate(all_statements):
            file_path = './test/' + ticker1 + str(i) + quarter_name + '.csv'
            globals()['df_' + str(i)] = pd.read_csv(file_path, index_col=0)
            os.remove(file_path)
        concat_df = pd.concat([df_0, df_1, df_2], ignore_index=True)


        # print(concat_df)

        final_file_path = './test/' + ticker1 + '_' + quarter_name + '.csv'
        file_names.append(ticker1 + '_' + quarter_name)
        concat_df.to_csv(final_file_path)


# finally merge by quarters

load_name = './test/' + pd.Series(file_names) + '.csv'
dfs = (pd.read_csv(f, index_col=0) for f in load_name)

df_merged = reduce(lambda left,right: pd.merge(left,right, on=['Label', 'Name'], how='outer'), dfs)
df_merged.set_index('Label', inplace=True)
df_merged.to_csv('./test/' + ticker1 + '_financial_data' + '.csv')