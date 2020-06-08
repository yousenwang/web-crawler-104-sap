import numpy as np
import pandas as pd
import csv
from datetime import datetime

#keyword104 = "SAP"
#source = f'104人力銀行_{keyword104}_companies_duplicate.csv'

def remove_duplicate(source):
    df = pd.DataFrame()
    with open(source, newline='', encoding='utf-8-sig',) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            df = df.append(row, ignore_index=True)
    print(df.columns)
    print(df.shape)
    df['創建時間'] = pd.to_datetime(df['創建時間'], format='%Y/%m/%d %H:%M')#, errors='coerce')
    df['更改時間'] = pd.to_datetime(df['更改時間'], format='%Y/%m/%d %H:%M')#, errors='coerce')

    #print (df[df['創建時間'].isnull()])
    df.loc[df['更改時間'].isnull(), '更改時間'] = df['創建時間']
    res = pd.DataFrame()
    #print(len(set(df["公司名稱"])))
    count = 0
    for company_name in set(df["公司名稱"]):
        company = df.loc[df.公司名稱 == company_name]
        #print(company.shape)
        latest = max(company.創建時間)
        oldest = min(company.創建時間)
        #print(company)
        if latest.to_datetime64() != oldest.to_datetime64():
            #print(latest, oldest)
            latest_row = company[company.創建時間 == latest]
            oldest_row = company[company.創建時間 == oldest]
            #print(latest_row.values.tolist())
            #print(oldest_row.values.tolist())
            # change the created time to old one.
            df.at[latest_row.index[0], '創建時間'] = df.at[oldest_row.index[0], '創建時間']
            df.at[latest_row.index[0], '業務'] = df.at[oldest_row.index[0], '業務']
            df.at[latest_row.index[0], '類型'] = df.at[oldest_row.index[0], '類型']
            df.at[latest_row.index[0], '備註'] = df.at[oldest_row.index[0], '備註']
            company1 = df.loc[df.公司名稱 == company_name]
            updated_row = company1.loc[company1.更改時間 == latest]
        else:
            company1 = df.loc[df.公司名稱 == company_name]
            updated_row = company1
        # use modified time since created time is already changed to the oldest time.
        # we can't use created time here anymore.
        #print("update:")
        #print(updated_row)
        res = pd.concat([res, updated_row], axis=0)

    print(res.shape)
    path = f"./{source}"
    res.to_csv(path, index=False, header=True,encoding='utf-8-sig')
    print(path)
    print(count)