import pandas as pd
from bs4 import BeautifulSoup
import requests


df = pd.read_csv('Lists/2015_jeju_test.tsv', sep='\t',encoding='utf8')


def search(keyword1,keyword2,keyword3, category, city, name):
    sd= "20150101"
    ed= "20191231"
    query= keyword1 +"+"+ "%7c" + "+" +keyword2 + "+" + "%7c"+ "+" +keyword3 + '+"' + city + '"+"' + name +'"'
    url= "https://search.naver.com/search.naver?where=post&query={}&date_from={}&date_to={}&date_option=8&qvt=0".format(query,sd,ed)
    url1=makeURL(keyword1,sd,ed,city,name)
    url2=makeURL(keyword2,sd,ed,city,name)
    url3=makeURL(keyword3,sd,ed,city,name)
    total= [request(url),request(url1),request(url2),request(url3)]
    print(total[0])
    return total
def makeURL(keyword,sd,ed,city,name):
    query= keyword +'+"' + city + '"+"' + name +'"'
    return "https://search.naver.com/search.naver?where=post&query={}&date_from={}&date_to={}&date_option=8&qvt=0".format(query,sd,ed)

def request(url):
    req = requests.get(url)
    print(url)
        # 정상적인 request 확인
    if req.ok:        
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        total= soup.select( 'div.section_head > span.title_num')
        try :
            total =  total[0].text.split(' ')[2]
            total = total.replace(',','').strip()
            total = int(total[:-1])
            print(total)
            return total
        except:
            return 0
    return 0 

if __name__ == '__main__':
    category=[]
    a=[]
    b=[]
    c=[]
    keyword0= "편리성(화장실,도로변,주차장)"
    keyword1= "화장실"
    keyword2= "도로변"
    keyword3= "주차장"
        
    for data in df['name']:
        if len(data) <=2:
            data= "카페 "+data 
        total = search(keyword1,keyword2,keyword3,keyword0,"제주",data)
        category.append(total[0])
        a.append(total[1])
        b.append(total[2])
        c.append(total[3])
    df[keyword0] = category
    df[keyword1] = a
    df[keyword2] = b
    df[keyword3] = c

    category=[]
    a=[]
    b=[]
    c=[]
    keyword0= "기능(시그니처,다양한메뉴,친절한)"
    keyword1= "시그니처"
    keyword2= "다양한메뉴"
    keyword3= "친절한"
        
    for data in df['name']:
        if len(data) <=2:
            data= "카페 "+data 
        total = search(keyword1,keyword2,keyword3,keyword0,"제주",data)
        category.append(total[0])
        a.append(total[1])
        b.append(total[2])
        c.append(total[3])
    df[keyword0] = category
    df[keyword1] = a
    df[keyword2] = b
    df[keyword3] = c
    
    category=[]
    a=[]
    b=[]
    c=[]
    keyword0= "여가(오름,바다,빵)"
    keyword1= "오름"
    keyword2= "바다"
    keyword3= "빵"
        
    for data in df['name']:
        if len(data) <=2:
            data= "카페 "+data 
        total = search(keyword1,keyword2,keyword3,keyword0,"제주",data)
        category.append(total[0])
        a.append(total[1])
        b.append(total[2])
        c.append(total[3])
    df[keyword0] = category
    df[keyword1] = a
    df[keyword2] = b
    df[keyword3] = c
    
    category=[]
    a=[]
    b=[]
    c=[]
    keyword0= "분위기(예쁜,분위기,음악)"
    keyword1= "예쁜"
    keyword2= "분위기"
    keyword3= "음악"
        
    for data in df['name']:
        if len(data) <=2:
            data= "카페 "+data 
        total = search(keyword1,keyword2,keyword3,keyword0,"제주",data)
        category.append(total[0])
        a.append(total[1])
        b.append(total[2])
        c.append(total[3])
    df[keyword0] = category
    df[keyword1] = a
    df[keyword2] = b
    df[keyword3] = c
    df.to_csv("Lists/result_test.csv", encoding='utf-8-sig')
    
