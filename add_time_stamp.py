# import csv
# import datetime
time_stamp = "2020/04/07 05:35:00 PM"
col_name = "抓取時間"
# source = './104人力銀行SAP0407.csv'
input_file = "104人力銀行SAP0407.csv"
output_file = "104人力銀行SAP.csv"

from _csvhandler import (add_column_in_csv)

add_column_in_csv(input_file, output_file, lambda row, line_num: row.append(time_stamp), col_name)