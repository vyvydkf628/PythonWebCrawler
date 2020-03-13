# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from konlpy.tag import Twitter
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv

search_word = "제주 갈등"  # 검색어 지정
title_list = []
 
def get_titles(start_num, end_num):
    #start_num ~ end_num까지 크롤링
    while 1:
        if start_num > end_num:
            break
        print(start_num)
        url = "https://search.naver.com/search.naver?where=news&query={}&pd=5&start={}".format(search_word,start_num)
        req = requests.get(url)
 
        # 정상적인 request 확인
        if req.ok:
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            f= open('write.csv','w')
            
            wr = csv.writer(f)


            
            # 뉴스제목 뽑아오기
            titles = soup.select(
                'ul.type01 > li > dl > dt > a'
            )
            texts = soup.select(
                'ul.type01 > li > dl > dd'
            )
            
            for index,text in enumerate(texts,1):
                if(len(titles)<=index):
                    break
                title = titles[index]['title'].encode('utf-8')
                url = titles[index]['href'].encode('utf-8','ignore')
                FROM =texts[index*2].text.split(' ')[0].encode('utf-8','ignore')
                date =texts[index*2].text.split(' ')[2].encode('utf-8','ignore')
                body =texts[index*2+1].text.encode('utf-8','ignore')
                wr.writerow([index,date,FROM,title,body,url])
                print(title)
                print(url)
                print(date)
                print(body)

                print(texts[index*2].text.split(' ')[0])
                print(texts[index*2+1].text)
                print("-------------------")
            f.close() 
            # list에 넣어준다
            for title in titles:
                title_list.append(title['title'])
        start_num += 10
    print(title_list)
 
def make_wordcloud(word_count):
    twitter = Twitter()
 
    sentences_tag = []
    #형태소 분석하여 리스트에 넣기
    for sentence in title_list:
        morph = twitter.pos(sentence)
        sentences_tag.append(morph)
        print(morph)
        print('-' * 30)
 
    print(sentences_tag)
    print('\n' * 3)
 
    noun_adj_list = []
    #명사와 형용사만 구분하여 이스트에 넣기
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun', 'Adjective']:
                if word.encode('utf-8','ignore') not in ['제주','갈등','제','수']:
                    
                    noun_adj_list.append(word)
                
                    
 
    #형태소별 count
    counts = Counter(noun_adj_list)
    tags = counts.most_common(word_count)
    print(tags)
 
    #wordCloud생성
    #한글꺠지는 문제 해결하기위해 font_path 지정
    wc = WordCloud(font_path='‪C://indows/Fonts/NanumSquareB.ttf', background_color='white', width=800, height=600)
    print(dict(tags))
    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()
 
if __name__ == '__main__':
    
    #1~200번게시글 까지 크롤링
    get_titles(5,10)
    #단어 30개까지 wordcloud로 출력
    make_wordcloud(30)
