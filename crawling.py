import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import sys

start = 1
result_df = pd.DataFrame()
news_title = []
dates = []
keyword = '코로나'


for i in range(2017, 2023):
  for j in range(1, 13):
    for k in range(1, 32):
      if i==2017 and j<=4:
        continue
      if i==2017 and j==5 and k<=12:
        continue
      if i==2022 and j==5 and k>=7: 
        continue
      if i==2022 and j>=6: 
        continue
      start = 1
      front = str(i)+'.'+str('%02d' %j)+'.'+str('%02d' %k)
      end = str(i)+str('%02d' %j)+str('%02d' %k)
      while True:
        try:
          url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='+keyword+'&sort=2&photo=3&field=0&pd=3&ds='+front+'&de='+front+'&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from'+end+'to'+end+',a:all&start='+str(start)
          headers = {'User-Agent': 'Mozilla/5.0'}
          response = requests.get(url)
          soup = BeautifulSoup(response.text, 'lxml')
          news_title  = [title['title'] for title in soup.find_all('a', attrs={'class': 'news_tit'})]
          dates = [date.get_text() for date in soup.find_all('span', attrs={'class':'info'})]
          news_date = []
          for date in dates:
            if re.search(r'\d+.\d+.\d+.', date) != None: ## 자료형 날짜로 바꾸기
              news_date.append(date)
          
          df = pd.DataFrame({'기사작성일':news_date, '기사제목' : news_title})
          print(df)
          if df.empty:
            break
          result_df = pd.concat([result_df, df], ignore_index=True)
          start +=10
          #print(result_df)

          if start ==4001:
            ##print(news_date[0]) 
            break

        except:
          print(start)
          break
  
result_df.to_csv(keyword+'.csv',index=None)
