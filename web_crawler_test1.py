#爬取5頁的職缺內容,將各個職缺內容存到csv檔
import requests
import bs4
import csv
import random,time
url_A ='https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=SAP&order=15&asc=0&page='
url_B = '&mode=s&jobsource=2018indexpoc'

all_job_datas=[]
for page in range(1,50+1):
    url = url_A+str(page)+url_B
    print(url)
    htmlFile = requests.get(url)
    ObjSoup=bs4.BeautifulSoup(htmlFile.text,'lxml')
    jobs = ObjSoup.find_all('article',class_='js-job-item')                 #搜尋所有職缺  
       
    for job in jobs:
        job_name=job.find('a',class_="js-job-link").text                    #職缺內容
        job_company=job.get('data-cust-name')                               #公司名稱
        job_loc=job.find('ul', class_='job-list-intro').find('li').text     #地址
        job_pay=job.find('span',class_='b-tag--default').text               #薪資
        job_url=job.find('a').get('href')                                   #網址
        job_data={'職缺內容':job_name,'公司名稱':job_company,
                         '地址':job_loc,'薪資':job_pay,'網址':job_url}
        all_job_datas.append(job_data)
    time.sleep(random.randint(1,3))


fn='104人力銀行SAP.csv'                                             #取CSV檔名
columns_name=['職缺內容','公司名稱','地址','薪資','網址']                     #第一欄的名稱
with open(fn,'w',newline='') as csvFile:               #定義CSV的寫入檔,並且每次寫入完會換下一行
    dictWriter = csv.DictWriter(csvFile,fieldnames=columns_name)            #定義寫入器
    dictWriter.writeheader()       
    for data in all_job_datas:
        dictWriter.writerow(data)