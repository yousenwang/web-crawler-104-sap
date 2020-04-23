"""
Author: You Sen Wang (Ethan)
Started Date: 04/06/2020
Email: yousenwang@gmail.com
"""

#%%
# import sys
# !{sys.executable} -m pip install requests
# #%%
# !{sys.executable} -m pip install bs4
#%%
import requests
import csv
import random, time
from bs4 import BeautifulSoup
import datetime
num_of_pages = 
#%%
my_params = {'ro':'0', # 限定全職的工作，如果不限定則輸入0
             'keyword':'SAP', # 想要查詢的關鍵字
             #'area':'6001001000', # 限定在台北的工作
             #'isnew':'90', # 只要最近三個月有更新的過的職缺
             #'jobsource' : '2018indexpoc'
             'mode':'s',
             'kwop': '7',
             'order':'15'} 

# %%
url = 'https://www.104.com.tw/jobs/search/?'
fn=f'104人力銀行SAP.csv'                                             #取CSV檔名
columns_name=[
    '職缺內容',
    '公司名稱',
    '地址',
    '薪資',
    '網址',
    '抓取時間'
    ]
all_job_datas=[]
for page in range(1,num_of_pages+1):
    #url = url_A+str(page)+url_B
    print(f"page: {page}")
    my_params['page'] = str(page)
    source_html = requests.get(url, my_params).text
    soup = BeautifulSoup(source_html,'lxml')
    jobs = soup.find_all('article',class_='js-job-item')                 #搜尋所有職缺  
    # a job is an article
    for job in jobs:
        # print(job.prettify())
        job_name=job.find('a',class_="js-job-link").text                    #職缺內容
        job_company=job.get('data-cust-name')                               #公司名稱
        job_loc=job.find('ul', class_='job-list-intro').find('li').text     #地址
        job_pay=job.find('span',class_='b-tag--default').text               #薪資
        job_url='https:' + job.find('a').get('href')                        #網址
        job_fetch_time = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        job_data = {
            '職缺內容':job_name,
            '公司名稱':job_company,
            '地址':job_loc,
            '薪資':job_pay,
            '網址':job_url,
            '抓取時間': job_fetch_time}
        all_job_datas.append(job_data)
    time.sleep(random.randint(1,3))

print(f"n: {len(all_job_datas)}")

#, encoding='utf-8' 
# add this to open for company_count.py to work

try:
    with open(fn,'a+', newline='') as csvFile:               #定義CSV的寫入檔,並且每次寫入完會換下一行
        dictWriter = csv.DictWriter(csvFile, fieldnames=columns_name)            #定義寫入器
        # dictWriter.writeheader()       
        for data in all_job_datas:
            dictWriter.writerow(data)
        csvFile.close()
except UnicodeEncodeError:
    pass

