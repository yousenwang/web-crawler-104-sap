import numpy as np
import pandas as pd
import csv

keyword104 = "SAP"
source = f'104人力銀行_{keyword104}_companies.csv'

df = pd.DataFrame()
with open(source, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        df = df.append(row, ignore_index=True)

print(df.head())
print(df.tail())
print(df.shape)
df['抓取時間'] = pd.to_datetime(df['抓取時間'], format='%m/%d/%Y %H:%M')
res = pd.DataFrame()
for company_name in set(df["公司名稱"]):
    company = df.loc[df.公司名稱 == company_name]
    latest = max(company['抓取時間'])
    latest_row = company.loc[company['抓取時間'] == latest]
    res = pd.concat([res, latest_row], axis=0)

print(res.shape)
path = f"./{source}"
res.to_csv(path, index=False, header=True, encoding='utf-8-sig')
print(path)
