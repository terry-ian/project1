# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 16:31:45 2018

@author: terry_ian
"""

from flask import Flask, request, abort

from linebot import (
LineBotApi, WebhookHandler
)
from linebot.exceptions import (
InvalidSignatureError
)
from linebot.models import (
MessageEvent, TextMessage, TextSendMessage,
)

from weatherbot import LineBot 
weather_line_bot = LineBot()
from linebot.models import *
import random
import datetime
import difflib 
import jieba
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from pandas.core.frame import DataFrame
import pandas
########################################################################################################################
deepThought = ChatBot("deepThought")
deepThought.set_trainer(ChatterBotCorpusTrainer)
# 使用中文语料库训练它
deepThought.train("chatterbot.corpus.chinese.greetings")
deepThought.train("chatterbot.corpus.chinese.conversations")
deepThought.train("chatterbot.trivia.chinese") # 语料库


#台銀匯率網址
dfs = pandas.read_html('http://rate.bot.com.tw/xrt?Lang=zh-TW')
#取dsf的list 資料
currency = dfs[0]
#只取前五欄
currency = currency.ix[:,0:5]
#重新命名欄位名稱 u-utf
currency.columns = [u'幣別',u'現金匯率-本行買入',u'現金匯率-本行賣出',u'現金匯率-本行買入',u'現金匯率-本行賣出']
#幣別值有重複字 利用正規式取英文代號
#\s 代表非空白字元
currency[u'幣別'] = currency[u'幣別'].str.extract('(.+\s+\s)')
price=pandas.DataFrame(currency,columns=['幣別','現金匯率-本行買入','現金匯率-本行賣出','現金匯率-本行買入','現金匯率-本行賣出'])

#電影
def movie():
    target_url = 'https://movies.yahoo.com.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.movielist_info h1 a')):
        if index == 20:
            return content       
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

#新聞
def apple_news2():
    target_url = 'https://tw.appledaily.com/new/realtime'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for index, data in enumerate(soup.select('div.item a')):
        if index ==10:           
            return content
        print(data)  
        title = data.find('img')['alt']
        link =  data['href']
        link2 = 'https:'+ data.find('img')['data-src']
        content+='{}\n{}\n{}\n'.format(title,link,link2)
    return content

######################################################################################################################
app = Flask(__name__)

line_bot_api = LineBotApi('THcbNW71Q9XNcAAamM/x9mc3h9ZU32FjrEr7QX+Kk4lIbzGwtHpxX+qWXRL1z+QgFzLW7hsxPQOHSGCb3wUizePYFleTuBjUYCuAktr/oakSGf+IZPmtrn0lC7wZi6YVmAab0ahSzZ5G6TJYeJFI7AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b3358afe260626a99ecdcb11b5d6f6cd')

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(4000)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(msg)
    msg = msg.encode('utf-8')
    mytext = ",".join(jieba.cut(event.message.text, cut_all=False))
    if mytext.find('terry') >= 0:
        print("文字get")
        message = TextSendMessage(text='好帥好帥好帥帥')
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('你好') >= 0:
        print("文字get")
        message = TextSendMessage(text='你好我是terry的智能客服')
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('網站')>= 0 or mytext.find('網頁')>= 0 or mytext.find('黑屏')>= 0:
        print("文字get")
        message = TextSendMessage(text='您好! 你可以參考 https://www.bbin.support/problem/unableOpenSite.html')
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('遊戲')>= 0 :
        print("文字get")
        message = TextSendMessage(text='您好! 你可以參考 https://www.bbin.support/problem/unablePlayGame.html')
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('緩慢')>= 0 or mytext.find('慢') >= 0:
        print("文字get")
        message = TextSendMessage(text='您好! 你可以參考 https://www.bbin.support/problem/visitsSlow.html')
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('早安') >= 0:
        print("文字get")
        message = TextSendMessage(text='早安呀! 非常感謝你的問好')
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('午安') >= 0:
        print("文字get")
        message = TextSendMessage(text='午安呀! 中餐吃過了嗎')
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('晚安') >= 0:
        print("文字get")
        message = TextSendMessage(text='晚安呀! 祝你有個好眠')
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('貼圖') >= 0:
        print("貼圖get")
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=random.randint(1,10)))
    elif mytext.find('時間')>= 0 or mytext.find('日期')>= 0 or mytext.find('年')>= 0 or mytext.find('月')>= 0 or mytext.find('幾號') >= 0:          
        print("文字get")
        theTime = datetime.datetime.now()
        theTime=str(theTime)
        message = TextSendMessage(text=theTime)
        line_bot_api.reply_message(event.reply_token, message)    
    elif mytext.find('天氣') >= 0:          
        print("文字get")
        message = TextSendMessage(text=str(weather_line_bot.getResponse(event.message.text)))
        line_bot_api.reply_message(event.reply_token, message)    
    elif mytext.find('電影') >= 0:
        print("文字get")
        a=movie()
        message = TextSendMessage(text=a)
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('新聞') >= 0:
        print("文字get")
        a=apple_news2()
        message = TextSendMessage(text=a)
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('正妹') >= 0: 
        print("正妹get")
        b=random.randint(1,5)
        phototext=['86dXT2s','uQOHkaE','Qou99G2','BwX1xJU','yDiYoyF']
        message = ImageSendMessage(
                original_content_url='https://i.imgur.com/'+phototext[b]+'.jpg',
                preview_image_url='https://i.imgur.com/'+phototext[b]+'.jpg'
                )
        line_bot_api.reply_message(event.reply_token, message)        
    elif mytext.find('帥哥') >= 0: 
        print("帥哥get")
        b=random.randint(1,7)
        phototext=['tbdgegX','JHWYf6z','h30cFkc','0eqM8d1','cyUtm23','Lpeytzj','ZYQLzrn','OrKe3w2']
        message = ImageSendMessage(
                original_content_url='https://i.imgur.com/'+phototext[b]+'.jpg',
                preview_image_url='https://i.imgur.com/'+phototext[b]+'.jpg'
                )
        line_bot_api.reply_message(event.reply_token, message)
    elif mytext.find('匯率') >= 0 :
        print("文字get")
        if mytext.find('美金')>= 0 : j=0
        if mytext.find('港幣')>= 0 : j=1
        if mytext.find('英鎊') >= 0: j=2
        if mytext.find('澳幣')>= 0 : j=3
        if mytext.find('加拿大幣')>= 0 : j=4
        if mytext.find('新加坡幣')>= 0 : j=5
        if mytext.find('瑞士法郎')>= 0 : j=6
        if mytext.find('日圓')>= 0 : j=7
        if mytext.find('南非幣')>= 0 : j=8
        if mytext.find('瑞典幣')>= 0 : j=9
        if mytext.find('紐元')>= 0 : j=10
        if mytext.find('泰幣')>= 0 : j=11
        if mytext.find('菲國比索')>= 0 : j=12
        if mytext.find('印尼幣')>= 0 : j=13
        if mytext.find('歐元')>= 0 : j=14
        if mytext.find('韓元')>= 0 : j=15
        if mytext.find('越南盾')>= 0 : j=16
        if mytext.find('馬來幣')>= 0 : j=17
        if mytext.find('人民幣')>= 0 : j=18

        message = TextSendMessage(text='今天'+price.values[j,0]+'匯率為' + '現金匯率-本行買入'+price.values[j,1]+'現金匯率-本行賣出'+price.values[j,2]+'現金匯率-本行買入'+price.values[j,3]+'現金匯率-本行賣出'+price.values[j,4])
        line_bot_api.reply_message(event.reply_token, message)
    else : 
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
        print("解釋get")
        #message = TextSendMessage(text='我聽不太懂你說的，可以換個方式說唷')
        #line_bot_api.reply_message(event.reply_token, message)
        
        message = TextSendMessage(text=str(deepThought.get_response(event.message.text)))
        line_bot_api.reply_message(event.reply_token, message)
if __name__ == "__main__":
    app.run(debug=False,port=3000)
