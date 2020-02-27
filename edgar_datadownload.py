# https://github.com/farhadab/sec-edgar-financials
import pandas as pd
from edgar.stock import Stock
import sys
import os
import itertools
from functools import reduce

ticker1 = 'ADBE'
stock = Stock(ticker1)

years = [2017, 2018, 2019, 2020]
quarters = [1, 2, 3, 4]
period = 'quarterly'  # or 'annual', which is the default

file_names = []
index_cols = []
# main

for y, q in itertools.product(years, quarters):
    try:
        year = y  # can use default of 0 to get the latest
        quarter = q  # 1, 2, 3, 4, or default value of 0 to get the latest
        # using defaults to get the latest annual, can simplify to stock.get_filing()
        filing = stock.get_filing(period, year, quarter)

        # financial reports (contain data for multiple years)
        income_statements = filing.get_income_statements()
        balance_sheets = filing.get_balance_sheets()
        cash_flows = filing.get_cash_flows()

        all_statements = [income_statements, balance_sheets, cash_flows]
        sheet_name = ['IS', 'BS', 'CF']
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

            ## data cleaning

            read_csv = pd.Series(pd.read_csv(file_path, encoding='unicode_escape').columns)
            raw_ = read_csv.str.cat(sep=',')

            # get first datetime, to avoid get values of last year, last quarter values
            find_str_index = raw_[300:].find(""'date'"")
            raw_string = raw_[:300+find_str_index]
            raw_list = pd.Series(raw_string.split("us-gaap_"))
            raw_df = raw_list.str.split("': ", expand=True)

            # select columns : label and value

            df = raw_df.iloc[:, [0, 3]]
            df.columns = ['Label', quarter_name]
            df.Label = sheet_name[i]+ '_' + df['Label']
            # df = df.iloc[range(int(len(df) / 2 + 1))]
            df.drop(0, axis=0, inplace=True)
            df.set_index('Label', inplace=True)

            # extract only numeric value
            df[quarter_name] = df[quarter_name].str.extract(r'([-+]?\d+.\d+)')
            df.to_csv(file_path)

            # print(df)

        # concat all statements

        for i, sheet in enumerate(all_statements):
            file_path = './test/' + ticker1 + str(i) + quarter_name + '.csv'
            globals()['df_' + str(i)] = pd.read_csv(file_path, index_col=0)
            os.remove(file_path)
        concat_df = pd.concat([df_0, df_1, df_2], ignore_index=False)



        final_file_path = './test/' + ticker1 + '_' + quarter_name + '.csv'
        file_names.append(ticker1 + '_' + quarter_name)
        concat_df.to_csv(final_file_path)

        # make full index_values (preliminary , to clean merge)
        index_values = pd.Series(concat_df.index)
        for item in index_values.unique():
            index_cols.append(item)

    except: pass


# load full index

index1 = pd.DataFrame(pd.Series(index_cols).unique())
index1.columns=['Label']
index1.to_csv('./test/' + ticker1 + '_index.csv')




# # for i in range(len(df.Name)):
# #     df['Label'][i] = ''.join(
# #         ' ' + char if char.isupper() else char.strip() for char in df['Name'][i]).strip()
