#  -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import lxml
import requests
import re
import collections
import xlsxwriter
import time
import os

time_format = input("请输入查询日期：XXXX-XX/XX的形式\n")
while (time_format > time.strftime('%Y-%m/%d', time.localtime(time.time()))):
    time_format = input("请重新输入查询日期：XXXX-XX/XX的形式\n")

time1_format = re.sub(r'[-/]', '', time_format)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
r = requests.get('http://epaper.zqrb.cn/html/%s/node_2.htm' % time_format, headers=headers)
print("响应状态码：", r.status_code)

while r.status_code == int(404):
    print("该天未披露公告")
    time_format = input("请重新输入查询日期：XXXX-XX/XX的形式\n")
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    r = requests.get('http://epaper.zqrb.cn/html/%s/node_2.htm' % time_format, headers=headers)

print("请稍等.....")
soup = BeautifulSoup(r.content, 'lxml')

div_list = soup.find_all('h2')
b = []
all = []
c = {}
c = collections.OrderedDict()
key_new = []
d = {}
d = collections.OrderedDict()
e = {}
e = collections.OrderedDict()
for eachead in div_list:
    title_name = eachead.text.strip()
    sub_str = re.sub(u"[^\u0030-\u0039\u0041-\u005a\u0061-\u007a]", "", title_name)
    if sub_str:
        str = sub_str
        b.append(str)  # b是大序号
    url = eachead.span.find('a')['href']
    e[str] = url.replace("../../..", "http://epaper.zqrb.cn")  # e的字典是大序号和对应的pdf链接

for i in b:
    div2_list = soup.find(id=i)
    name = div2_list.text.replace(' ', '').split()
    c[i] = name  # c是个字典，key是对应的每个大序号，值是大序号下面小标题的集合列表

for key in c:
    for value in c[key]:
        if '基金' in value:
            d[value] = key  # d就是以标题为键，序号为值的字典
            key_new.append(key)
            # print('title: %s, body: %s' % (key,value))

time1_format = re.sub(r'[-/]', '', time_format)
workbook = xlsxwriter.Workbook('%s日报补充公告.xlsx' % time1_format)
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
filename = os.path.join('D:\pycharm\fund','%s补充公告.xlsx'%time1_format)
if os.path.exists(filename):
    print("已完成！")

import pdb
pdb.set_trace()
# 下载标题、序号以及文件 'class_='vote_content12px'
'''
