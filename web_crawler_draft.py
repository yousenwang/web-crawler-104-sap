import requests
import bs4
import csv
import random,time

my_params = {'ro':'1', # 限定全職的工作，如果不限定則輸入0
             'keyword':'SAP', # 想要查詢的關鍵字
             #'area':'6001001000', # 限定在台北的工作
             'isnew':'30', # 只要最近一個月有更新的過的職缺
             'mode':'l'} # 清單的瀏覽模式

url = requests.get('https://www.104.com.tw/jobs/search/?' , my_params, headers = headers).url