# -*- coding: utf-8 -*-
"""
@File    : get_html_xpath.py
@Time    : 2022/12/28 23:17
@Author  : 欧振宇
"""
import requests
from lxml import etree
from requests.adapters import HTTPAdapter


class GetHtmlXpath:

    def __init__(self, user_agent, referer):
        self.s = requests.Session()
        self.s.mount('http://', HTTPAdapter(max_retries=3))
        self.s.mount('https://', HTTPAdapter(max_retries=3))
        self.headers = {
            'User-Agent': user_agent,
            "Referer": referer
        }

    def get_html_path(self, url, xpath):
        response = self.s.get(url=url, headers=self.headers, timeout=60)
        response.encoding = response.apparent_encoding
        page_sub_text = response.text
        tree_sub = etree.HTML(page_sub_text)
        return tree_sub.xpath(xpath)

    def download_html(self,url):
        content = self.s.get(url=url, headers=self.headers, timeout=60).content
        return content
