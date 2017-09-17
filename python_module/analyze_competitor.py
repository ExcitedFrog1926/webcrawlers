#-*-coding:utf8-*-
__author__ = 'kira'
# this module is a function set, generate different competitors name_list such classify by regin or gender and so on
# output file just include  competitor's name, display name, number





from lxml import etree
import requests
import json
import time
import re
time_start = time.time()
import urllib.request
import urllib.parse


def get_all_english_and_native_name(url):

        homepage = requests.get(url)
        page_selector = etree.HTML(homepage.text)

        person_list = page_selector.xpath('//div[@id="yw1"]/table/tbody')

        person_name = person_list[0].xpath('tr[@class="odd"]/td[3]//text() | tr[@class="even"]/td[3]//text() ')
        print(len(person_name))
        person_eng_and_native = {}
        for name in person_name:
            if("(" in name):
                person_native_name = re.findall('\((.*?)\)',name,re.S)[0]
                person_english_name = name.split(" (")[0]
                person_eng_and_native[person_english_name] = person_native_name
            else:
                person_eng_and_native[name] = name
        print(len(person_eng_and_native))
        with open('../resources/person_classify/all_players_name_mapping.json','w') as f:
            f.write(json.dumps(person_eng_and_native))
get_all_english_and_native_name('http://ac2016.cubingchina.com/competitors')



def get_english_name(name):
        if("(" in name):
            person_english_name = name.split(" (")[0]
            return person_english_name
        else:。

            return name



url_sort_by_country = 'http://ac2016.cubingchina.com/competitors?sort=country_id.desc'
def classify_by_country(sort_url):

    regin_dic = {}
    regin_list = []

    homepage = requests.get(sort_url)
    page_selector = etree.HTML(homepage.text)

    person_list = page_selector.xpath('//div[@id="yw1"]/table/tbody')

    person_name = person_list[0].xpath('tr[@class="odd"]/td[3]//text() | tr[@class="even"]/td[3]//text() ')



    # person_page_url = person_list[0].xpath('tr[@class="odd"]/td[3]/a/@href | tr[@class="even"]/td[3]/a/@href ')

    person_regin = person_list[0].xpath('tr[@class="odd"]/td[5]//text() | tr[@class="even"]/td[5]//text()')
    for each in range(len(person_regin)):
        if('中国' in person_regin[each]):
            pass
        else:
            if(person_regin[each] in regin_dic):
                regin_dic[person_regin[each]].append(get_english_name(person_name[each]))
            else:
                regin_dic[person_regin[each]] = []
                regin_dic[person_regin[each]].append(get_english_name(person_name[each]))
    # print(regin_dic)

    with open('../resources/person_classify/regin.json','w') as f:
        f.write(json.dumps(regin_dic))
# classify_by_country(url_sort_by_country)






def classify_all_item(url):

    def classify_by_item(item,url_front):
        event_dict = {
                '二阶':'222',
                '三阶':'333',
                '四阶':'444',
                '五阶':'555',
                '六阶':'666',
                '七阶':'777',
                '三盲':'333bf',
                '单手':'333oh',
                '最少步':'333fm',
                '多盲':'333mbf',
                '五魔方':'minx',
                '金字塔':'pyram',
                'SQ1':'sq1',
                '魔表':'clock',
                '斜转':'skewb',
                '四盲':'444bf',
                '五盲':'555bf'
                }
        event_dict_transfer = {
                '222':'二阶',
                '333':'三阶',
                '444':'四阶',
                '555':'五阶',
                '666':'六阶',
                '777':'七阶',
                '333bf':'三盲',
                '333oh':'单手',
                '333fm':'最少步',
                '333mbf':'多盲',
               'minx': '五魔方',
               'pyram': '金字塔',
               'sq1': 'SQ1',
                'clock':'魔表',
               'skewb': '斜转',
                '444bf':'四盲',
                '555bf':'五盲'
                }
        url_all = ''
        item_fix = ''
        if(item in event_dict):
            item_fix = event_dict[item]
            url_all = url_front + item_fix
        elif(item in event_dict_transfer):
            item_fix = item
            url_all = url_front + item_fix



        loop_len = {'222':50,
                '333':50,
                '444':50,
                '555':50,
                '666':40,
                '777':40,
                '333bf':40,
                '333oh':40,
                '333fm':30,
                '333mbf':20,
               'minx': 30,
               'pyram': 40,
               'sq1': 40,
                'clock':30,
               'skewb': 40,
                '444bf':26,
                '555bf':19}

        homepage = requests.get(url_all)
        page_selector = etree.HTML(homepage.text)

        person_list = page_selector.xpath('//div[@id="yw1"]/table/tbody')

        person_name = person_list[0].xpath('tr[@class="odd"]/td[3]//text() | tr[@class="even"]/td[3]//text() ')

        list = []
        for index in range(loop_len[item_fix]):
            list.append(get_english_name(person_name[index]))

        file_name = '../resources/person_classify/' + item_fix + '.json'
        with open(file_name,'w') as f:
            f.write(json.dumps(list))

    event_list = ['222','333','444','555','666','777','333bf','333oh','333fm','333mbf','minx','pyram','sq1','clock','skewb','444bf','555bf']

    for each in event_list:
        classify_by_item(each,url)
# classify_all_item('http://ac2016.cubingchina.com/competitors?sort=')



time_end = time.time()
time_period = time_end-time_start
print(time_period)