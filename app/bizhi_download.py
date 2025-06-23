# -*- coding: utf-8 -*-
"""
@File    : StringDemo.py
@Time    : 2020/11/22 22:34
@Author  : 欧振宇
Copyright (c) 2020/11/22, 作者版权所有.
"""
import os
from util.get_html_xpath import GetHtmlXpath
from util.mysql_util import MySqlUtil

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
referer = 'https://www.xiu09.top'
html = 'https://www.xiu09.top/XiuRen/'
request = GetHtmlXpath(user_agent, referer)
db = MySqlUtil("127.0.0.1", 3306, "test", "utf8", "root", "root")
pwd = r'E:\欧振宇\壁纸'


def get_home_html():
    # 获取主页所有壁纸URL
    url = request.get_html_path(html, '/html/body/div[3]/div[2]/div/ul/li/a/@href')
    # 获取业务所有壁纸title
    url_title = request.get_html_path(html, '/html/body/div[3]/div[2]/div/ul/li/a/@title')
    html_dict = dict(zip(url, url_title))
    list = []
    # 遍历URL、title
    for v, k in html_dict.items():
        url = referer + v
        val = (referer, url, k)
        list.append(val)
    sql = 'insert into  download_page_home(`host`,`url`,`url_title`) values (%s,%s,%s)'
    db.insert_db(sql, list)


def get_sub_html(n):
    sql = 'select id,url,url_title from download_page_home where is_download = 0 and id = {}'.format(n)
    data = db.select_db(sql)
    page_id = data[0]['id']
    url = data[0]['url']
    url_title = data[0]['url_title']
    # 获取每页url
    sub_urls = request.get_html_path(url, '/html/body/div[3]/div/div/div[4]/div/div/a/@href')
    # sub_urls = ['/XiuRen/2025/202516892_9.html', '/XiuRen/2025/202516892_10.html', '/XiuRen/2025/202516892_11.html', '/XiuRen/2025/202516892_12.html', '/XiuRen/2025/202516892_13.html', '/XiuRen/2025/202516892_14.html', '/XiuRen/2025/202516892_15.html', '/XiuRen/2025/202516892_16.html', '/XiuRen/2025/202516892_17.html', '/XiuRen/2025/202516892_18.html', '/XiuRen/2025/202516892_19.html', '/XiuRen/2025/202516892_20.html', '/XiuRen/2025/202516892_21.html', '/XiuRen/2025/202516892_22.html', '/XiuRen/2025/202516892_23.html', '/XiuRen/2025/202516892_24.html', '/XiuRen/2025/202516892_25.html', '/XiuRen/2025/202516892_26.html']
    # 获取壁纸页数
    url_num = len(sub_urls) - 1
    # url_num = 27
    sql = 'insert into download_page_detail(`page_id`,`host`,`url`,`url_title`,`url_num`,`sub_url`,`sub_page_url`,`page_name`)' \
          'values(%s,%s,%s,%s,%s,%s,%s,%s)'
    j = 0
    for i in sub_urls:
        list = []
        if j < url_num:
            sub_url = referer + i
            sub_page_urls = request.get_html_path(sub_url, '/html/body/div[3]/div/div/div[3]/div/p/img/@src')
            for i in sub_page_urls:
                sub_page_url = 'https://www.xiu09.top' + i
                page_name = i.split('/')[4]
                val = (page_id, referer, url, url_title, url_num, sub_url, sub_page_url, page_name)
                list.append(val)
        else:
            break
        db.insert_db(sql, list)
        j = j + 1
    update_sql = 'update download_page_home set is_download = 1 where id = {}'.format(n)
    db.update_db(update_sql)


def download_html_page(url, img_pwd, page_name):
    img_data = request.download_html(url)
    if not os.path.exists(img_pwd):
        os.mkdir(img_pwd)
    with open(img_pwd + '\\' + page_name, 'wb') as fp:
        fp.write(img_data)
        print(page_name + '下载成功!')


if __name__ == '__main__':
    # get_home_html()
    # get_sub_html(32)
    sql = 'select id,sub_page_url,url_title,page_name from download_page_detail where page_id = 32 and is_download = 0'
    datas = db.select_db(sql)
    for data in datas:
        id = data['id']
        url = data['sub_page_url']
        page_name = data['page_name']
        url_title = data['url_title']
        img_pwd = pwd + '\\' + url_title
        download_html_page(url, img_pwd, page_name)
        update_sql = 'update download_page_detail set is_download = 1 where id = {}'.format(id)
        db.update_db(update_sql)
