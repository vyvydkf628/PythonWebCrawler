# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime,timedelta
import re

search_word = "제주 갈등"  # 검색어 지정

def get_data():
    #start_num ~ end_num까지 크롤링
    start_num=1
    f= open('write.csv','w',encoding='euc_kr', newline='')
            
    wr = csv.writer(f)
    
    wr.writerow(["날짜","출처","제목","본문 요약 ","URL"])
    i=0

    ## 시작 일자 선택
    ssd= datetime(2018,12,31)

    ## 4주 간격으로 데이터 검색
    eed=ssd + timedelta(weeks=4)
    ## 종료 일자 선택
    end="2019.12.31"

    
    ssd=ssd+ timedelta(days=1)
    
    while 1:
        ## 날짜 데이터 네이버 검색 쿼리형식에 맞게 수정
        sd= ssd.strftime("%Y-%m-%d").split('-')
        sd= sd[0]+'.'+sd[1]+'.'+sd[2]
            
        ed= eed.strftime("%Y-%m-%d").split('-')
        ed= ed[0]+'.'+ed[1]+'.'+ed[2]
        if ed>end:
            print("SUC")
            ed=end
                
        url = "https://search.naver.com/search.naver?where=news&query={}&pd=3&ds={}&de={}&start={}".format(search_word,sd,ed,start_num)
        req = requests.get(url)
        
        # 정상적인 request 확인
        if req.ok:        
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            total= soup.select( 'div.title_desc > span')
            total =  total[0].text.split(' ')[2]
            total = total.replace(',','').strip()
            total = int(total[:-1])
            print(total)
            start_num=1
            end_num=total
            print(sd)
            
            print(sd,ed)
            while 1:
                if start_num > end_num:
                    break
                print(start_num)
                url = "https://search.naver.com/search.naver?where=news&query={}&pd=3&ds={}&de={}&start={}&sort=2&related=0&photo=0".format(search_word,sd,ed,start_num)
                req = requests.get(url)
                
                # 정상적인 request 확인
                if req.ok:
                    html = req.text
                    soup = BeautifulSoup(html, 'html.parser')
                    


                    
                    # 뉴스제목 뽑아오기
                    titles = soup.select(
                        'ul.type01 > li > dl > dt > a'
                    )
                    texts = soup.select(
                        'ul.type01 > li > dl'
                    )
                    texts1 = soup.select(
                        'ul.type01 > li > dl > dd.txt_inline'
                    )

                    for index,text in enumerate(texts,1):
                        i=i+1
                        if(len(titles)<=index):
                            break
                        title = titles[index]['title']
                        url = titles[index]['href']
                        FROM =texts1[index].text.split(' ')[0]
                        date =texts1[index].text.split(' ')[2]
                        print(date)
                        x=2
                        while(date=="" or date=="선정"):
                           x=x+1
                           date=texts1[index].text.split(' ')[x]
                           print(date,"NULL!!!")
                        if "면" in date:
                            date=texts1[index].text.split(' ')[4]
                            print(date,"suc")
                        x=3
                        while(date==""):
                           x=x+1
                           date=texts1[index].text.split(' ')[x]
                           print(date,"NULL!!!")    
                        if "시간" in date:
                            now = datetime.now()
                            date= "{}.{}.{}.".format(now.year,now.month,now.day)
                            print(date,"suc11")
                        if "일" in date:
                            now = datetime.now()
                            now=now + timedelta(days=-int(date[0]))
                            date= "{}.{}.{}.".format(now.year,now.month,now.day)
                            print(date,"suc day")
                        
                        body =texts[index].find_all('dd')[1].text
                        try:
                            wr.writerow([date,FROM,title,body,url])
                        except:
                            print("error")
                       
                     
                              
                start_num += 10                       


            




            ssd=ssd + timedelta(weeks=4)
            eed=eed + timedelta(weeks=4)
            if ed==end:
                break
        


    f.close()
 
if __name__ == '__main__':
    
    #1~14000번게시글 까지 크롤링
    get_data()
