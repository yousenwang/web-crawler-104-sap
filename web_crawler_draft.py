#%%
import sys
# !{sys.executable} -m pip install requests
# #%%
# !{sys.executable} -m pip install bs4
#%%
import requests
import csv
import random, time
from bs4 import BeautifulSoup

#%%
my_params = {'ro':'0', # 限定全職的工作，如果不限定則輸入0
             'keyword':'SAP', # 想要查詢的關鍵字
             #'area':'6001001000', # 限定在台北的工作
             #'isnew':'90', # 只要最近三個月有更新的過的職缺
             'mode':'s',
             'kwop': '7',
             'order':'15'} 

num_of_pages = 10
# %%
url_A ='https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=SAP&order=15&asc=0&page='
url_B = '&mode=s'#&jobsource=2018indexpoc'
url = 'https://www.104.com.tw/jobs/search/?'
all_job_datas=[]
for page in range(1,num_of_pages+1):
    #url = url_A+str(page)+url_B
    my_params['page'] = str(page)
    source_html = requests.get(url, my_params).text
    soup = BeautifulSoup(source_html,'lxml')
    jobs = soup.find_all('article',class_='js-job-item')                 #搜尋所有職缺  
    # a job is an article
    for job in jobs:
        job_url='https:' + job.find('a').get('href')
        print(f'!!!!!!!!!! {job_url} !!!!!!!!')
        job_html = requests.get(job_url).text
        soup2 = BeautifulSoup(job_html, 'html.parser')
        print(soup2.prettify())
        job_data = {
            '公司名稱':soup2.find('a', {'class':'cn'}).text,
            '工作職稱':content.attrs['title'],
            '工作內容':soup2.find('p').text,
            '職務類別':bind(soup2.findAll('dd', {'class':'cate'})[0].findAll('span')),
            '工作待遇':soup2.find('dd', {'class':'salary'}).text.split('\n\n',2)[0].replace(' ',''),
            '工作性質':soup2.select('div > dl > dd')[2].text,
            '上班地點':soup2.select('div > dl > dd')[3].text.split('\n\n',2)[0].split('\n',2)[1].replace(' ',''),
            '管理責任':soup2.select('div > dl > dd')[4].text,
            '出差外派':soup2.select('div > dl > dd')[5].text,
            '上班時段':soup2.select('div > dl > dd')[6].text,
            '休假制度':soup2.select('div > dl > dd')[7].text,
            '可上班日':soup2.select('div > dl > dd')[8].text,
            '需求人數':soup2.select('div > dl > dd')[9].text,
            '接受身份':soup2.select('div.content > dl > dd')[10].text,
            '學歷要求':soup2.select('div.content > dl > dd')[12].text,
            '工作經歷':soup2.select('div.content > dl > dd')[11].text,
            '語文條件':soup2.select('div.content > dl > dd')[14].text,
            '擅長工具':soup2.select('div.content > dl > dd')[15].text,
            '工作技能':soup2.select('div.content > dl > dd')[16].text,
            '其他條件':soup2.select('div.content > dl > dd')[17].text,
            '公司福利':soup2.select('div.content > p')[1].text,
            '科系要求':soup2.select('div.content > dl > dd')[13].text,
            '聯絡方式':soup2.select('div.content')[3].text.replace('\n',''),
            '連結路徑':'https://' + content.attrs['href'].strip('//')}
        all_job_datas.append(job_data)
    time.sleep(random.randint(1,3))
fn='104人力銀行SAP_test.csv'                                             #取CSV檔名
columns_name=['公司名稱','工作職稱','工作內容','職務類別','工作待遇','工作性質','上班地點','管理責任','出差外派',
'上班時段','休假制度','可上班日','需求人數','接受身份','學歷要求','工作經歷','語文條件','擅長工具',
'工作技能','其他條件','公司福利','科系要求','聯絡方式','連結路徑']
#第一欄的名稱
with open(fn,'w',newline='') as csvFile:               #定義CSV的寫入檔,並且每次寫入完會換下一行
    dictWriter = csv.DictWriter(csvFile,fieldnames=columns_name)            #定義寫入器
    dictWriter.writeheader()       
    for data in all_job_datas:
        dictWriter.writerow(data)