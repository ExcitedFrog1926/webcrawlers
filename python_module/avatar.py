#-*-coding:utf8-*-
__author__ = 'kira'
from lxml import etree
import requests
import urllib.request
import urllib.parse
import re


ranking_333_single_url = 'http://cubingchina.com/results/rankings?region=China&event=333&gender=all&type=single'

def get_all_player_homepage(ranking_url):
    ranking_page = requests.get(ranking_url)

    page_selector = etree.HTML(ranking_page.text)

    person_homepage = page_selector.xpath('//tr/td[3]/a/@href')

    person_homepage_whole = []

    for each in person_homepage:
        person_homepage_whole.append('http://cubingchina.com'+ each)

    # print(person_homepage_whole)
    return person_homepage_whole

def cubing_personalpage_info(person_homepage_url):

    homepage = requests.get(person_homepage_url)

    page_selector = etree.HTML(homepage.text)

    person_avatar = page_selector.xpath('//img[@class="user-avatar"]/@src')

    print(person_avatar)

    person_info_value = page_selector.xpath('//span[@class="info-value"]/text()')

    name = re.findall('\((.*?)\)',person_info_value[0],re.S)

    if(person_avatar):
        file_dic = 'avatar/' + name[0] + '.jpg'
        pic_data = urllib.request.urlopen(person_avatar[0]).read()
        file = open(file_dic,'ab+')
        file.write(pic_data)
        file.close()


person_homepage_set = get_all_player_homepage(ranking_333_single_url)

for each in person_homepage_set:
    cubing_personalpage_info(each)

