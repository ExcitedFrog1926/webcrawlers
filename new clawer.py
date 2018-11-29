#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 18-11-29
# @Author  : Jacob_Zhou (zzh839985914@gmail.com)
# @Link    : https://github.com/Jacob0817
# @Version : $Id$

import os               #
from lxml import etree  # 文档解析
import requests         # http请求
import xlwt             # 写入Excel
import re               # 正则匹配


class cc_rank_name:

    def __init__(self, competition):
        self.competition = competition

    def _list(self, full_url):
        self.full_url = full_url
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
        # 构建浏览器请求头
        homepage = requests.get(self.full_url, headers=header)  # 向服务器发送请求
        page_selector = etree.HTML(homepage.text)    # 获取页面
        p_list = page_selector.xpath(
            '//div[@id="competitors"]/table/tbody/tr[position()<12]')  # 选择器正则定位tr元素地址
        p_name_list = [0] * 10   # 初始化一个长度为10的数组，保存姓名
        for looptimes in range(1, 11):
            p_name = p_list[looptimes].xpath(
                'td[2]//text() ')  # 遍历tr元素，获得元素中第二个td元素文本内容
            p_name_list[looptimes - 1] = p_name
            # 将获得的文本内容存入数组
        return p_name_list

    def event(self, event):
        self.event = event
        url = "https://cubingchina.com/competition/" + \
            self.competition + "/competitors?sort=" + self.event
        name_list = self._list(url)
        # 将爬取的姓名保存到name数组
        return name_list


if __name__ == '__main__':
    rank = cc_rank_name("Suzhou-University-Rubiks-Cube-Open-2018")
    rank_list = rank.event("444")
    print(rank_list)
