import requests
import pandas as pd
import re
import os
import json
from bs4 import BeautifulSoup
from wxpy import get_wechat_logger

def get_book_id(string):
    return re.search('http://product.dangdang.com/(.*?)\.html',string).group(1)

booklist = pd.read_excel('去重书单.xlsx')
booklist['bookid'] = booklist['booklink'].apply(get_book_id)
base = 'http://product.dangdang.com/index.php?r=callback%2Fcomment-list'
logger = get_wechat_logger()

def get_comment_page(bookid,pn):
    try:
        response = requests.get(base+'&productId='+bookid+'&mainProductId='+bookid+'&mediumId=0'+'&pageIndex='+str(pn)+'&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0')
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        print('获取'+bookid+'评论第'+str(pn)+'页出错！')
        logger.warning('获取'+bookid+'评论第'+str(pn)+'页出错！')
        return None

def get_page_number(cp):
    if(cp):
        data = json.loads(cp)
        if data and 'data' in data.keys():
            pages = data.get('data').get('summary').get('pageCount')
            return int(pages)
        else:
            print('获取评论页数失败！')
            logger.warning('获取评论页数失败！')
            return None
    else:
        print('评论首页加载不成功！')
        logger.warning('评论首页加载不成功！')
        return None

def parse_comment_page(cp):
    if(cp):
        data = json.loads(cp)
        if data and 'data' in data.keys():
            soup = BeautifulSoup(data.get('data').get('html'),'lxml')
            clist = soup.select('.comment_items')
            temp = pd.DataFrame({"describe_detail":"","time":"","username":"","userlevel":""},index=[])
            for c in clist:
                try:
                    time=c.select('.starline')[0].select('span')[0].text
                    describe_detail = c.select('.describe_detail')[0].text.strip()
                    username = c.select('.name')[0].text
                    userlevel = c.select('.level')[0].text
                    temp = temp.append(pd.Series([describe_detail,time,username,userlevel],index=['describe_detail','time','username','userlevel']),ignore_index=True)
                except:
                    continue
            return temp
        else:
            print('解析评论页面失败！')
            logger.warning('解析评论页面失败！')
            return None
    else:
        print('页面加载不成功！')
        logger.warning('页面加载不成功！')
        return None

def main():
    os.chdir('C:\\Users\\TENAG\\Documents\\GitHub\\dangdang\\图书评论Swift')
    for i in range(0,len(booklist)):
        homepage = get_comment_page(booklist.at[i,'bookid'],1)
        pages = get_page_number(homepage)
        commentable = pd.DataFrame({"describe_detail":"","time":"","username":"","userlevel":""},index=[])
        for j in range(pages):
            cp = get_comment_page(booklist.at[i,'bookid'],j+1)
            try:
                commentable = pd.merge(commentable,parse_comment_page(cp),how='outer')
            except ValueError:
                continue
        commentable.to_excel(str(booklist.at[i,'rawindex'])+'-'+booklist.at[i,'bookname']+'.xlsx')
        print(str(i)+'-完成')
        logger.warning(str(i)+'-完成')

if __name__=='__main__':
    main()