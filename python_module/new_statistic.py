#-*-coding:utf8-*-
__author__ = 'kira'
from lxml import etree
import os
import requests
import json
import time
import re
time_start = time.time()
import urllib.request
import urllib.parse
#  import urllib for python2
whole_list = []

if not os.path.exists('resources/person'):
    os.makedirs('resources/person')


# person_homepage_url = 'http://cubingchina.com/results/person/2010WANG53'
def cubing_personalpage_info(person_homepage_url):
    homepage = requests.get(person_homepage_url)
    page_selector = etree.HTML(homepage.text)
    person_info_value = page_selector.xpath('//span[@class="info-value"]/text()')

    PersonInfo = {}
    CurrentPersonRecord = {}
    PersonReocrdBreaking = {}

    PersonInfo['name'] = person_info_value[0]
    PersonInfo['region'] = person_info_value[1].replace(' ','')
    PersonInfo['competition_num'] = person_info_value[2]
    PersonInfo['wcaid'] = person_info_value[3]
    PersonInfo['gender'] = person_info_value[4]
    PersonInfo['career'] = person_info_value[5]
    PersonInfo['cubing_page'] = person_homepage_url

    current_person_reocrd = page_selector.xpath('//div[@id="yw0"]')
    person_reocrd_breaking = page_selector.xpath('//div[@id="yw4"]')
    if(current_person_reocrd):
        event_list = current_person_reocrd[0].xpath('table/tbody/tr')

        CurrentPersonRecord['num'] = len(event_list)
        CurrentPersonRecord['event_name'] = []
        CurrentPersonRecord['event_detail'] = {}

        for each in event_list:
            event_name_sign = each.xpath('td[1]/a/@href') and each.xpath('td[1]/a/@href')[0] or ''
            event_name = each.xpath('td[1]/a/span/text()') and each.xpath('td[1]/a/span/text()')[0] or ''

            single_NR_ranking =each.xpath('td[2]//text()') and each.xpath('td[2]//text()')[0] or ''
            single_CR_ranking =each.xpath('td[3]//text()') and each.xpath('td[3]//text()')[0] or ''
            single_WR_ranking =each.xpath('td[4]//text()') and each.xpath('td[4]//text()')[0] or ''
            single_result =each.xpath('td[5]//text()') and each.xpath('td[5]//text()')[0] or ''

            average_result =each.xpath('td[6]//text()') and each.xpath('td[6]//text()')[0] or ''
            average_NR_ranking =each.xpath('td[9]//text()') and each.xpath('td[9]//text()')[0] or ''
            average_CR_ranking =each.xpath('td[8]//text()') and each.xpath('td[8]//text()')[0] or ''
            average_WR_ranking =each.xpath('td[7]//text()') and each.xpath('td[7]//text()')[0] or ''

            competition_glod_number =each.xpath('td[10]//text()') and each.xpath('td[10]//text()')[0] or ''
            competition_silver_number =each.xpath('td[11]//text()') and each.xpath('td[11]//text()')[0] or ''
            competition_bronze_number =each.xpath('td[12]//text()') and each.xpath('td[12]//text()')[0] or ''

            solves_attempts = each.xpath('td[13]//text()') and each.xpath('td[13]//text()')[0] or ''

            CurrentPersonRecord['event_name'].append(''.join(event_name))    # .join  将数组变成字符串        用event_name[0]当event name 为空的时候报错
            CurrentPersonRecord['event_detail'][event_name] = {}
            CurrentPersonRecord['event_detail'][event_name]['event_name_sign']= event_name_sign

            CurrentPersonRecord['event_detail'][event_name]['single_NR_ranking']= single_NR_ranking
            CurrentPersonRecord['event_detail'][event_name]['single_CR_ranking']= single_CR_ranking
            CurrentPersonRecord['event_detail'][event_name]['single_WR_ranking']= single_WR_ranking
            CurrentPersonRecord['event_detail'][event_name]['single_result']= single_result

            CurrentPersonRecord['event_detail'][event_name]['average_result']= average_result
            CurrentPersonRecord['event_detail'][event_name]['average_NR_ranking']= average_NR_ranking
            CurrentPersonRecord['event_detail'][event_name]['average_CR_ranking']= average_CR_ranking
            CurrentPersonRecord['event_detail'][event_name]['average_WR_ranking']= average_WR_ranking

            CurrentPersonRecord['event_detail'][event_name]['competition_glod_number']= competition_glod_number
            CurrentPersonRecord['event_detail'][event_name]['competition_silver_number']= competition_silver_number
            CurrentPersonRecord['event_detail'][event_name]['competition_bronze_number']= competition_bronze_number

            CurrentPersonRecord['event_detail'][event_name]['solves_attempts'] = solves_attempts
    else:
        print('选手不存在个人最好成绩')

    def get_top5(list):
        top5_list = []
        for each in list:
            if int(list[each])<=200 :
                top5_list.append(each)

        if len(top5_list)>=5:
            del top5_list[:]
            for each in list:
                if int(list[each])<=100 :
                    top5_list.append(each)

        if len(top5_list)>=5:
            del top5_list[:]
            for each in list:
                if int(list[each])<=50 :
                    top5_list.append(each)

        if len(top5_list)>=5:
            del top5_list[:]
            for each in list:
                if int(list[each])<=30 :
                    top5_list.append(each)
        return top5_list

    single_ranking_list ={}
    for each in CurrentPersonRecord['event_detail']:
        single_ranking_list[each] = CurrentPersonRecord['event_detail'][each]['single_NR_ranking']

    skilled_item = get_top5(single_ranking_list)

    PersonInfo['skilled_item'] = skilled_item and skilled_item or ''

    if(person_reocrd_breaking):
        title = person_reocrd_breaking[0].xpath('parent::div/h2')
        if(title):
            WR_breaking = person_reocrd_breaking[0].xpath('table//td[1]/text()') and  person_reocrd_breaking[0].xpath('table//td[1]/text()')[0] or ''
            CR_breaking = person_reocrd_breaking[0].xpath('table//td[2]/text()') and  person_reocrd_breaking[0].xpath('table//td[2]/text()')[0] or ''
            NR_breaking = person_reocrd_breaking[0].xpath('table//td[3]/text()') and  person_reocrd_breaking[0].xpath('table//td[3]/text()')[0] or ''
            PersonReocrdBreaking['WR_breaking'] = WR_breaking
            PersonReocrdBreaking['CR_breaking'] = CR_breaking
            PersonReocrdBreaking['NR_breaking'] = NR_breaking
        else:
            print('该选手并未打破记录')
    else:
        print('该选手并未打破记录')
    # print(PersonInfo)
    # print(CurrentPersonRecord)
    # print(PersonReocrdBreaking)


    name = PersonInfo['name'].split(" (")
    # name = re.findall('\((.*?)\)',PersonInfo['name'],re.S)
    whole_list.append(name[0])

    with open('resources/person/whole_list.json','w') as f:
        f.write(json.dumps({'whole_list':whole_list}))

    filename ='resources/person/' + name[0] + '.json'
    filedata = {'PersonInfo':PersonInfo,'CurrentPersonRecord':CurrentPersonRecord,'PersonReocrdBreaking':PersonReocrdBreaking}
    with open(filename,'w') as f:
        f.write(json.dumps(filedata))

    # person_avatar = page_selector.xpath('//img[@class="user-avatar"]/@src')
    # if(person_avatar):
    #     file_dic = '../resources/avatar/' + name[0] + '.jpg'
    #     pic_data = urllib.request.urlopen(person_avatar[0]).read()    #for python2
    #     file = open(file_dic,'ab+')
    #     file.write(pic_data)
    #     file.close()
    return PersonInfo,CurrentPersonRecord,PersonReocrdBreaking

competition_page_url = 'http://ac2016.cubingchina.com/competitors'   # ac2016 competitors
def cubing_competition_page(competition_page_url):
    homepage = requests.get(competition_page_url)
    page_selector = etree.HTML(homepage.text)

    person_list = page_selector.xpath('//div[@id="yw1"]/table/tbody')

    person_name = person_list[0].xpath('tr[@class="odd"]/td[3]//text() | tr[@class="even"]/td[3]//text() ')
    person_page_url = person_list[0].xpath('tr[@class="odd"]/td[3]/a/@href | tr[@class="even"]/td[3]/a/@href ')
    # print(person_page_url)
    # print(len(person_page_url))
    with open('resources/all_player_url.json','w') as f:
            f.write(json.dumps(person_page_url))
    return person_page_url


person_page_url = cubing_competition_page(competition_page_url)


for each in range(len(person_page_url)):
    try:
        (PersonInfo, CurrentPersonRecord, PersonReocrdBreaking) = cubing_personalpage_info(person_page_url[each])
        print('finish',each)
    except:
        num_present = each
        print(each)

# cubing_personalpage_info('http://cubingchina.com/results/person/2010WANG53')


time_end = time.time()
time_period = time_end-time_start
print(time_period)