#encoding = utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re

def getcomment(url):
    commentable = pd.DataFrame({"detail":"","time":"","username":"","userlevel":""},index=[])
    driver.get(url)
    driver.find_element_by_id('comment_tab').click()
    time.sleep(0.5)
    while True:
        try:
            commentable = pd.merge(commentable,parse(driver.page_source),how='outer')
            if(conti(driver.page_source)):
                pagedown()
            else:
                break
        except:
            return commentable
    return commentable

def parse(src):
    soupcomment = BeautifulSoup(src,'lxml')
    comment=soupcomment.select('.comment_items')
    temp = pd.DataFrame({"detail":"","time":"","username":"","userlevel":""},index=[])
    for c in comment:
        detail=c.select('.describe_detail')[0].text
        if len(c.select('.clearfix')[0].select('span')):
            time=c.select('.clearfix')[0].select('span')[0].text
        else:
            time=None
        username=c.select('.name')[0].text
        userlevel=c.select('.level')[0].text
        temp = temp.append(pd.Series([detail,time,username,userlevel],index=['detail','time','username','userlevel']),ignore_index=True)
    return temp

def pagedown():
    driver.find_element_by_css_selector("a.btn.next").click()
    time.sleep(0.8)

def conti(src):
    soup = BeautifulSoup(src,'lxml')
    if(len(soup.select('.btn.next'))):
        return True
    else:
        return False

urls = pd.read_excel('C:\\Users\\TENAG\\Documents\\GitHub\\dangdang\\分类总表.xlsx')
rbooklist = urls[['bookname','booklink']]
for i in range(len(rbooklist)):
    rbooklist.at[i,'booklink'] = re.match(r'http://product.dangdang.com/(.*)\.html',rbooklist.at[i,'booklink']).group()
    rbooklist.at[i,'bookname'] = re.sub(r'/','_',rbooklist.at[i,'bookname'])
rawindex = rbooklist['booklink'].drop_duplicates().index
temp = rbooklist.iloc[rawindex]
data ={}
data['bookname'] = temp.bookname.values
data['booklink'] = temp.booklink.values
data['rawindex'] = rawindex
booklist = pd.DataFrame(data,index=range(len(temp)),columns=['bookname','booklink','rawindex'])
#booklist.to_excel('去重书单.xlsx')

service_args = []
service_args.append('--load-images=no')
service_args.append('--disk-cache=yes')
#service_args.append('--ignore-ssl-errors=true')
driver = webdriver.PhantomJS(executable_path='C:\\ProgramData\\Anaconda3\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',service_args=service_args)
os.chdir('C:\\Users\\TENAG\\Documents\\GitHub\\dangdang\\图书及其评论')

for i in range(len(booklist)-1,-1,-1):
    if(i%6==0):
        driver.quit()
        time.sleep(10)
        driver = webdriver.PhantomJS(executable_path='C:\\ProgramData\\Anaconda3\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',service_args=service_args)
    try:
        com = getcomment(booklist.at[i,'booklink'])
        com.to_excel(str(booklist.at[i,'rawindex'])+'-'+booklist.at[i,'bookname']+'.xlsx')
        print(str(i)+'-完成')
    except:
        print(str(i)+'------获取出错')

driver.quit()