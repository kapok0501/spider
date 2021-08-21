# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 16:25
# @Author  : kapok
# @File    : douban.py
# @Software: PyCharm
#
import re
import requests
from bs4 import BeautifulSoup
import pandas

# 书名、评分、评价数量、简述

def get_book_top250():
    datas = []

    for page in range(0,250,25):
        url = f'https://book.douban.com/top250?start={page}'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67"
        }
        res = requests.get(url,headers=headers).content

        soup = BeautifulSoup(res,'html.parser')
        indent_items = soup.find('div',class_='indent').find_all('tr',class_='item')
        for indent_item in indent_items:
            book_name = indent_item.find('div',class_='pl2').find('a').get('title')
            score = indent_item.find('span',class_='rating_nums').string
            pl_num = re.split('\n', indent_item.find('span',class_='pl').string)[1].replace(' ', '')
            if "inq" in str(indent_item):
                comment = indent_item.find('span',class_='inq').string
            else:
                comment = '暂无commnet'
            datas.append({
                "book_name": book_name,
                "score": score,
                "pl_num": pl_num,
                "comment": comment
            })
    df = pandas.DataFrame(datas)
    df.to_excel("douban_book_top250.xlsx")


if __name__=='__main__':
    get_book_top250()