#-*-coding:utf8-*-
__author__ = 'hanzhao'


from  lxml import etree
import requests

url = 'http://cubingchina.com/results/battle/2010WANG53-2013LINK01'
homepage = requests.get(url)
page_selector = etree.HTML(homepage.text)
person_info_value = page_selector.xpath('//span[@class="event-icon event-icon-333"]')[0]
print(person_info_value)
aa = person_info_value.xpath('../../following-sibling::tr[14]/td[3]/text()')
aa = person_info_value.xpath('../../following-sibling::tr[14]/td[4]/text()')
print aa