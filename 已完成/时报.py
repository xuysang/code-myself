#  -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import lxml
import requests
import re
import collections
import xlsxwriter
import time
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
r = requests.get('http://epaper.stcn.com/paper/zqsb/html/epaper/index/index.htm', headers=headers)
print("响应状态码：", r.status_code)
soup = BeautifulSoup(r.content, 'lxml')
div_list = soup.find_all(class_="pdf")
b=[]
c = collections.OrderedDict()
d = collections.OrderedDict()
e = collections.OrderedDict()
for each in div_list:
    x = str(each.find('a')).split('/')[7]
    b.append(x)
    if x:
        url = each.find('a')['href']
        e[x] = url.replace("../../..", "http://epaper.stcn.com/paper/zqsb")  # e的字典是大序号和对应的pdf链接

div2_list = soup.find_all('dl')
for each1 in div2_list:
    i = str(each1.find('a').text).split('版')[0]
    sub_str = re.sub(u"[^\u0030-\u0039\u0041-\u005a\u0061-\u007a]", "", i)
    name = each1.find_all('li')
    c[sub_str] = name

for key in c:   
    for value in c[key]:
        value1 = value.text
        if '基金' in value1:
            d[value1] = key

# time1_format = re.sub(r'[-/]', '', time_format)
workbook = xlsxwriter.Workbook('时报补充公告.xlsx' )
worksheet = workbook.add_worksheet()
row = 0
col = 0
for key in (d):
    h = d[key]
    worksheet.write(row, col, h)
    worksheet.write(row, col + 1, key)
    worksheet.write(row, col + 2, e[h])
    row += 1
workbook.close()

print("已完成！")

'''
            d[value] = key  # d就是以标题为键，序号为值的字典
            key_new.append(key)

name = div2_list.text.replace(' ', '').split()
    c[i] = name  # c是个字典，key是对应的每个大序号，值是大序号下面小标题的集合列表
'''
