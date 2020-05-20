import numpy as np
import pandas as pd
import csv

keyword104 = "SAP"
source = f'104人力銀行_{keyword104}_companies_with_sales.csv'

#df = pd.DataFrame()
type_dict = {}
salesperson_dict = {}

out = f'104人力銀行_{keyword104}_companies.csv'
out_pd = pd.read_csv(out)


with open(source, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print(row)
        #print(row["公司名稱"])
        
        if row["類型"] != "":
            type_dict[row["公司名稱"]] = row["類型"]
        if row["業務"] != "":
            salesperson_dict[row["公司名稱"]] = row["業務"]
        #df = df.append(row, ignore_index=True)
print(len(type_dict))

print(salesperson_dict)
print(len(salesperson_dict))
# print(df.head())
# print(df.tail())
# print(df.shape)


print(out_pd.head())
print(out_pd.shape)
out_pd["類型"] = np.nan
out_pd["業務"] = np.nan
for comp, comp_type in type_dict.items():
    out_pd.at[out_pd[out_pd["公司名稱"] == comp].index,"類型"] = comp_type
for comp, salesperson in salesperson_dict.items():
    out_pd.at[out_pd[out_pd["公司名稱"] == comp].index,"業務"] = salesperson

    

print(out_pd.shape)
path = f"./{out}"
out_pd.to_csv(path, index=False, header=True, encoding='utf-8-sig')
print(path)