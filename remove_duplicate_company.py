import numpy as np
import pandas as pd
import csv
from datetime import datetime

keyword104 = "SAP"
source = f'104人力銀行_{keyword104}_companies_draft.csv'

df = pd.DataFrame()
with open(source, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        df = df.append(row, ignore_index=True)
df['創建時間'] = pd.to_datetime(df['創建時間'], format='%Y/%m/%d %H:%M')
df['更改時間'] = pd.to_datetime(df['更改時間'], format='%Y/%m/%d %H:%M')
df.loc[df['更改時間'].isnull(), '更改時間'] = df['創建時間']
res = pd.DataFrame()
for company_name in set(df["公司名稱"]):
    company = df.loc[df.公司名稱 == company_name]
    latest = max(company['創建時間'])
    oldest = min(company['創建時間'])
    if latest.to_datetime64() != oldest.to_datetime64():
        latest_row = company.loc[company['創建時間'] == latest]
        oldest_row = company.loc[company['創建時間'] == oldest]
        df.at[latest_row.index[0], '創建時間'] = df.at[oldest_row.index[0], '創建時間']
        df.at[latest_row.index[0], '業務'] = df.at[oldest_row.index[0], '業務']
        df.at[latest_row.index[0], '類型'] = df.at[oldest_row.index[0], '類型']
    ### Need to get the lastest modified df again!!! ###
    company = df.loc[df.公司名稱 == company_name]
    # use modified time since created time is already changed to the oldest time.
    # we can't use modified time here anymore.
    updated_row = company.loc[company['更改時間'] == latest]
    res = pd.concat([res, updated_row], axis=0)

print(res.shape)
out = f'104人力銀行_{keyword104}_companies_draft_out.csv'
path = f"./{out}"
res.to_csv(path, index=False, header=True,encoding='utf-8-sig')
print(path)
