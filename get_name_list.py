#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-06-14 18:05
# @Author  : Jacob Zhou (zzh839985914@gmail.com)
# @Link    : ${link}
# @Version : $Id$

import os
from lxml import etree
import requests

# get names of first 10 person on competitors list
# CubingChina-->


def cb_rank_name(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    homepage = requests.get(url, headers=header)
    page_selector = etree.HTML(homepage.text)
    person_list = page_selector.xpath(
        '//div[@id="yw1"]/table/tbody/tr[position()<12]/td[3]//text()')
    return person_list

# WCA-->


def WCA_rank_name(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    homepage = requests.get(url, headers=header)
    page_selector = etree.HTML(homepage.text)
    person_name_list = page_selector.xpath(
        '//div[@class="table-responsive"]/table/tbody/tr[position()<11]//td[@class="name"]//text()')
    return person_name_list


if __name__ == "__main__":
    print(cb_rank_name(
        "https://cubingchina.com/competition/China-Championship-2018/competitors?sort=333"))
    print(WCA_rank_name(
        'https://www.worldcubeassociation.org/competitions/SouthAmericanChampionship2018/registrations/psych-sheet/333'))
