#  -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import collections
import xlsxwriter
import time
import lxml

# 获取标题序号和pdf链接
def get_dict(time_format):
    url = 'http://epaper.cs.com.cn/zgzqb/html/%s/nbs.D110000zgzqb_A01.htm' % time_format
    cookie_str = r'JSESSIONID=113FE58CD3C9CB060A0B7B9AF00A9B9F; user_guid=rBBUHly+K+qgawnD90plAg==;username=gildata0001'
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 	Chrome/73.0.3683.103 Safari/537.36'}
    resp = requests.get(url, headers=headers, cookies=cookies)
    c = collections.OrderedDict()
    d = {}
    # print(resp.content.decode('utf-8'))
    print(resp.status_code)
    if resp.status_code == int(404):
        print("该日未披露")
    soup = BeautifulSoup(resp.content, 'lxml')
    div4_list = re.findall(r'<a href="nw.D110000zgzqb.*?</a>', str(soup))
    for each1 in div4_list:
        if each1:
            if '基金' in each1:
                a = each1.replace('<br/>', '').split('>')[1][:-3]
                c[a] = each1[36:].split('.')[0]
                d[a] = "http://epaper.cs.com.cn/zgzqb" + each1.split('"')[1]
    time1_format = re.sub(r'[-/]', '', time_format)
    workbook = xlsxwriter.Workbook('%s中证报补充公告.xlsx' % time1_format)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for key in (c):
        h1=key
        worksheet.write(row, col, c[key])
        worksheet.write(row, col + 1, h1)
        worksheet.write(row, col + 2, d[h1])
        row += 1
    workbook.close()

    print("已完成！")

time_format = input("请输入查询日期：XXXX-XX/XX的形式\n")
while (time_format > time.strftime('%Y-%m/%d', time.localtime(time.time()))):
    time_format = input("请重新输入查询日期：XXXX-XX/XX的形式\n")

if __name__ == "__main__":
    get_dict(time_format)
