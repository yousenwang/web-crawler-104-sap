#%%
import pandas as pd
import numpy as np
from collections import Counter, OrderedDict

#%%
source = './104人力銀行SAP.csv'
pd_data = pd.read_csv(source, encoding = 'utf-8')
n = pd_data.shape[0]
counter = Counter(pd_data["公司名稱"])

sorted_counter = sorted(counter.items(),key=lambda i:i[1], reverse=True)

n_threshold = -1
companies = [k[0] for k in sorted_counter if k[1] > n_threshold]
companies_count = [k[1] for k in sorted_counter if k[1] > n_threshold]

col_names = ["name", "count"]
dat = np.transpose(np.array([companies, companies_count]))
df = pd.DataFrame(dat, columns=col_names)
print(df.head(5))
path = './companies_name_and_count.csv'
try:
    df.to_csv(path, encoding='big5', index=False)
except UnicodeEncodeError:
    pass
print(path)

n_threshold = 4
companies = [k[0] for k in sorted_counter if k[1] > n_threshold]
companies_count = [k[1] for k in sorted_counter if k[1] > n_threshold]
top_n = len(companies_count)

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
import datetime
time_produced = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
plt.figure(figsize=(19.2 * 1, 10.8 / 1.3 * 4))
#plt.yscale('log', nonposy='clip')
#plt.tight_layout()
plt.xticks(range(len(companies_count)), companies, rotation='vertical')
plt.bar(range(len(companies_count)), companies_count, align='center')
plt.ylim(bottom=min(companies_count))
plt.title(f'Companies that hire SAP positions. \n Sample size(n): {n}, Top n: {top_n}')
plt.ylabel('position count')
plt.xlabel('companies name')
pic_name = f'SAP_company_list_{time_produced}.jpg'
plt.savefig(pic_name)
print(f"{pic_name} was produced.")