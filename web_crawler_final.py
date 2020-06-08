"""
Author: You Sen Wang (Ethan)
Started Date: 04/06/2020
Email: 
Ethan_Wang@infofab.com
yousenwang@gmail.com
Please read the README.md before using it.
"""

import requests
import bs4
from bs4 import BeautifulSoup as bs
import datetime
import csv
import random, time
start_page = 1
num_of_pages = 1
keyword104 = 'SAP'
head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'} 
my_params = {'ro':'0', # 限定全職的工作，如果不限定則輸入0
             'keyword':keyword104, # 想要查詢的關鍵字
             #'area':'6001001000', # 限定在台北的工作
             #'isnew':'90', # 只要最近三個月有更新的過的職缺
             #'jobsource' : '2018indexpoc'
             'mode':'s',
             'kwop': '7',
             'order':'15'} 
#fn=f'104人力銀行_{keyword104}_positions_draft.csv'  
fn=f'104人力銀行_{keyword104}_positions.csv'  
url = 'https://www.104.com.tw/jobs/search/?'
# companies_out = f'104人力銀行_{keyword104}_companies_draft.csv'
companies_out = f'104人力銀行_{keyword104}_companies.csv'
company_url = 'https://www.104.com.tw/cust/list/index?'
companies_columns=[
    '備註',
    '公司名稱',
    '創建時間',
    '員工人數',
    '地址',
    '更改時間',
    '業務',
    '產業類別',
    '網址',
    '資本額',
    '類型'
    ]

def get_company_data(company):
    comp_dat = company.find_all('span')
    company_data = {
        '備註': "",
        '公司名稱' : company.h1.a.text,
        '創建時間' : str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M")),
        '員工人數' : comp_dat[3].text.strip('員工人數：'),
        '地址' : comp_dat[0].text,
        '更改時間' : str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M")),
        '業務' : "",
        '產業類別' : comp_dat[1].text,
        '網址' : company.h1.a.get('href'),
        '資本額' : comp_dat[2].text.strip('資本額：'),
        '類型': "",
    }
    return company_data

jobs_columns=[
    '職缺內容',
    '公司名稱',
    '地址',
    '薪資',
    '網址',
    '抓取時間'
    ]

def get_job_data(job):
    job_fetch_time = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    job_name=job.find('a',class_="js-job-link").text
    job_company=job.get('data-cust-name')
    job_loc=job.find('ul', class_='job-list-intro').find('li').text
    job_pay=job.find('span',class_='b-tag--default').text               #薪資
    urls = job.find_all('a')
    job_url = 'https:' + urls[0].get("href")
    #company104_url = 'https:' + urls[1].get("href")
    job_data = {
        '職缺內容':job_name,
        '公司名稱':job_company,
        '地址':job_loc,
        '薪資':job_pay,
        '網址':job_url,
        '抓取時間': job_fetch_time
    }
    return job_data

import os.path
def save_to_csv(file_name, col_name, all_data, encoding=None):
    write_headers = True
    if os.path.isfile(file_name):
        write_headers = False
    #try:
    with open(file_name,'a+', newline='', encoding=encoding) as csvFile:               #定義CSV的寫入檔,並且每次寫入完會換下一行
        dictWriter = csv.DictWriter(csvFile, fieldnames=col_name, delimiter=",")            #定義寫入器
        if write_headers:
            dictWriter.writeheader()
            print(f"write headers to {file_name}.")   
        for dat in all_data:
            try:
                dictWriter.writerow(dat)
            except UnicodeEncodeError:
                print(dat)
                #dictWriter.writerow({k:v.encode("utf-8") for k,v in dat.items()})
                pass
    csvFile.close()
    print(f"New rows/data are written in {file_name}.")
all_job_data = []
all_comp_data = []
comp_not_found_count = 0
for page in range(start_page, num_of_pages+1):
    print(("*" * 20) + f"page: {page}" + ("*" * 20))
    my_params['page'] = str(page)
    res = requests.get(url, my_params, headers=head)

    soup = bs(res.text, 'html.parser')
    jobs = soup.find_all('article',class_='js-job-item')

    for job in jobs:
        print("-" *100)
        job_data = get_job_data(job)
        company_name = job_data['公司名稱']
        # Check to see if we already search the company before.
        if any(job_dat['公司名稱'] == company_name for job_dat in all_job_data):
            print(f"{company_name} already exists, skip.")
        else:
            company_param = {
                "keyword": str(company_name),
                'mode':'s'
                }
            company_req =  requests.get(company_url, company_param, headers=head)
            comp_soup = bs(company_req.text, 'html.parser')
            #print(comp_soup.body.prettify())
            companies = comp_soup.body.find_all('article', class_='items')
            comp_found = False
            for company in companies:
                if company_name == company.h1.a.text:
                    company_data = get_company_data(company)
                    all_comp_data.append(company_data) 
                    print(f"{companies_out} will append: {company_data['公司名稱']}")
                    comp_found = True
            if not comp_found:
                comp_not_found_count+=1
                print(f'unable to get {company_name}\' data.')
        all_job_data.append(job_data)
        print(f"{fn} will append: {job_data['職缺內容']}")
    time.sleep(random.randint(1,3))
save_to_csv(fn, jobs_columns, all_job_data)
save_to_csv(companies_out, companies_columns, all_comp_data, 'utf-8-sig')

print(f"num_jobs: {len(all_job_data)}")
print(f"num_companies: {len(all_comp_data)}")
print(f'num companies info not found: {comp_not_found_count}')
print("checking whether there is a duplciate with previous date.....")
from _remove_duplicate_company import remove_duplicate
remove_duplicate(source=companies_out)