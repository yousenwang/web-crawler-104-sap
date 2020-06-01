"""
Author: You Sen Wang (Ethan)
Started Date: 04/06/2020
Email: 
Ethan_Wang@infofab.com
yousenwang@gmail.com
Please read the README.md before using it.
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebPage
import warnings
warnings.filterwarnings("ignore")
import requests
import bs4
from bs4 import BeautifulSoup as bs
import datetime
import csv
import random, time
start_page = 3
num_of_pages = 3
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
fn=f'104人力銀行_{keyword104}_positions.csv'  
url = 'https://www.104.com.tw/jobs/search/?'
companies_out = f'104人力銀行_{keyword104}_companies.csv'
company_url = 'https://www.104.com.tw/cust/list/index?'
companies_columns=[
    '公司名稱',
    '員工人數',
    '地址',
    '創建時間',
    '業務',
    '產業類別',
    '網址',
    '資本額',
    '類型',
    '更改時間'
    ]

def get_company_data(company):
    comp_dat = company.find_all('span')
    company_data = {
        '公司名稱' : company.h1.a.text,
        '員工人數' : comp_dat[3].text.strip('員工人數：'),
        '地址' : comp_dat[0].text,
        '創建時間' : str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M")),
        '業務' : "",
        '產業類別' : comp_dat[1].text,
        '網址' : company.h1.a.get('href'),
        '資本額' : comp_dat[2].text.strip('資本額：'),
        '類型': "",
        '更改時間' : str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M")),
    }
    return company_data

jobs_columns=[
    '職缺內容',
    '公司名稱',
    '地址',
    '薪資',
    '網址',
    '抓取時間',
    '需求人數',
    '職務類別1',
    '職務類別2',
    '職務類別3'
    ]

def get_job_data(job):
    job_urls = job.find_all('a')
    job_url = 'https:' + job_urls[0].get("href")
    print(job_url)
    print("URL!")
    client_response = Client(job_url)
    html_source = client_response.mainFrame().toHtml()
    comp_soup = bs(html_source, 'html.parser')
    del client_response
    job_fetch_time = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    job_header = comp_soup.body.find('div', class_="job-header__title")
    job_name = job_header.h1.get('title')
    job_company = job_header.div.a.get('title')
    job_type=[type_i.text for type_i in comp_soup.body.find_all('div', class_='trigger')]
    job_info = [row for row in comp_soup.find_all('div', class_="col p-0 job-description-table__data")]
    get_info = lambda row : row.find('p', class_="t3 mb-0").text.strip(" ")
    
    try:
        job_data = {
        '職缺內容': job_name,
        '公司名稱': job_company,
        '地址' : get_info(job_info[3]),
        '需求人數' : get_info(job_info[9]),
        '職務類別1': job_type[0],
        '職務類別2': job_type[1],
        '職務類別3': job_type[2],
        '抓取時間': job_fetch_time,
        '網址': job_url
        }
    except IndexError:
        print(job_url)
        print("*"*10 + "out of index" + "*"*10)
        job_data = {
        '職缺內容': job_name,
        '公司名稱': job_company,
        '地址' : get_info(job_info[3]),
        '需求人數' : get_info(job_info[9]),
        '職務類別1': job_type[0],
        '職務類別2': job_type[1],
        '職務類別3': "",
        '抓取時間': job_fetch_time,
        '網址': job_url
        } 
    return job_data

import os.path
def save_to_csv(file_name, col_name, all_data, encoding=None):
    write_headers = True
    if os.path.isfile(file_name):
        write_headers = False
    #try:
    with open(file_name,'a+', newline='', encoding=encoding) as csvFile:               #定義CSV的寫入檔,並且每次寫入完會換下一行
        dictWriter = csv.DictWriter(csvFile, fieldnames=col_name)            #定義寫入器
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
    
class Client(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()
    def on_page_load(self):
        self.app.quit()

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