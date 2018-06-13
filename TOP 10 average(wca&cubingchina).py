__author__ = 'Jacob Zhou'
from lxml import etree
import requests
import math
import xlwt
import re

#
# get name of TOP 10 from cubingchina


def cubingchina_rank_name(url):

    homepage = requests.get(url)
    page_selector = etree.HTML(homepage.text)
    person_list = page_selector.xpath(
        '//div[@id="yw1"]/table/tbody/tr[position()<12]')

    person_name_list = [0] * 10
    looptimes = 1
    while (looptimes <= 10):
        person_name = person_list[looptimes].xpath('td[3]//text() ')
        person_name_list[looptimes - 1] = person_name
        looptimes = looptimes + 1
    return person_name_list


# get name of TOP 10 from WCA
def WCA_rank_name(url):
    homepage = requests.get(url)
    page_selector = etree.HTML(homepage.text)
    person_name_list = page_selector.xpath(
        '//div[@class="table-responsive"]/table/tbody/tr[position()<11]//td[@class="name"]//text()')
    return person_name_list


#
# get WCA ID of TOP 10 from cubingchina
def cubingchina_get_WCA_ID(url):

    # get person_list
    homepage = requests.get(url)
    page_selector = etree.HTML(homepage.text)
    person_list = page_selector.xpath(
        '//div[@id="yw1"]/table/tbody/tr[position()<12]')
    # get WCA ID
    person_WCA_ID_list = [0] * 10
    looptimes = 1
    while (looptimes <= 10):
        personalpage_url = person_list[looptimes].xpath('td[3]//@href')
        personal_page = requests.get(''.join(personalpage_url))
        personalpage_selector = etree.HTML(personal_page.text)
        person_WCA_ID = personalpage_selector.xpath(
            '//div[@class="row"]/div[4]/span[2]//text()')
        person_WCA_ID_list[looptimes - 1] = person_WCA_ID
        looptimes = looptimes + 1
    return person_WCA_ID_list


# get WCA ID of TOP 10 from WCA
def WCA_get_WCA_ID(url):
    homepage = requests.get(url)
    page_selector = etree.HTML(homepage.text)
    person_WCA_ID_list = page_selector.xpath(
        '//div[@class="table-responsive"]/table/tbody/tr[position()<11]//td[@class="wca-id"]//span[@class="wca-id"]/a//text()')
    return person_WCA_ID_list


#
# get 10 average from cubingchina
def cubingchina_get_average(url, WCA_ID, event):

    looptimes = 0
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('dede', cell_overwrite_ok=True)
    sheet.write(0, 0, 'NAME')
    sheet.write(0, 12, 'AVERAGE')
    sheet.write(0, 13, 'S.D.')
    while (looptimes < 10):
        # get single WCA ID
        single_WCA_ID = WCA_ID[looptimes][0]
        single_person_name = re.findall(
            '\((.*?)\)', cubingchina_rank_name(url)[looptimes][0], re.S)[0]
        print(single_person_name + ' , ' + single_WCA_ID)
        sheet.write(looptimes + 1, 0, single_person_name)
        # get average list
        WCA_ID_url = 'https://www.worldcubeassociation.org/persons/' + \
            single_WCA_ID + '?event=' + event
        homepage = requests.get(WCA_ID_url)
        page_selector = etree.HTML(homepage.text)
        raw_average_list = page_selector.xpath(
            '//div[@id="results-by-event"]//tbody[@class="event-' + event + '"]')
        raw_average_list = raw_average_list[0].xpath(
            'tr[@class="result"]/td[6]//text()')
        average_list = [0] * 10
        average_num = 0
        # get recent 10 & normalize
        for average in raw_average_list:
            if ("DNF" in average):
                continue
            else:
                if (average_num < 10):
                    if (':' in average_list[average_num]):

                        average_list[average_num] = float(average.strip())
                        average_num = average_num + 1
                else:
                    break
        print(average_list)
        num = 0
        while (num < 10):
            sheet.write(looptimes + 1, num + 1,
                        float('%.2f' % average_list[num]))
            num = num + 1
        # 计算平均值和标准差
        avg = sum(average_list) / (10 - average_list.count(0))
        average_num = 0
        avg_list = [0] * 10
        while (average_num < (10 - average_list.count(0))):
            avg_list[average_num] = math.pow(
                average_list[average_num] - avg, 2)
            average_num = average_num + 1
        SD = math.sqrt(sum(avg_list) / (10 - average_list.count(0) - 1))
        print('Average: ' + str('%.3f' % avg) +
              '  ,  ' + 'S.D.： ' + str('%.3f' % SD))
        sheet.write(looptimes + 1, 12, float('%.3f' % avg))
        sheet.write(looptimes + 1, 13, float('%.3f' % SD))

        looptimes = looptimes + 1
    book.save('../10 average of TOP 10/DATA of ' + event + '.xls')


# get 10 average from WCA
def WCA_get_average(url, WCA_ID, event):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('dede', cell_overwrite_ok=True)
    sheet.write(0, 0, 'NAME')
    sheet.write(0, 12, 'AVERAGE')
    sheet.write(0, 13, 'S.D.')
    looptimes = 0
    while (looptimes < 10):
        # get single WCA ID
        single_WCA_ID = WCA_ID[looptimes]
        single_person_name = WCA_rank_name(url)[looptimes]
        print(single_person_name + ' , ' + single_WCA_ID)
        sheet.write(looptimes + 1, 0, single_person_name)
        # get average list
        WCA_ID_url = 'https://www.worldcubeassociation.org/persons/' + \
            single_WCA_ID + '?event=' + event
        homepage = requests.get(WCA_ID_url)
        page_selector = etree.HTML(homepage.text)
        raw_average_list = page_selector.xpath(
            '//div[@id="results-by-event"]//tbody[@class="event-' + event + '"]')
        raw_average_list = raw_average_list[0].xpath(
            'tr[@class="result"]/td[6]//text()')
        average_list = [0] * 10
        average_num = 0
        # get recent 10 & normalize
        for average in raw_average_list:
            if ("DNF" in average):
                continue
            else:
                if (average_num < 10):
                    average_list[average_num] = float(average.strip())
                    average_num = average_num + 1
                else:
                    break
        print(average_list)
        num = 0
        while (num < 10):
            sheet.write(looptimes + 1, num + 1,
                        float('%.2f' % average_list[num]))
            num = num + 1
        # 计算平均值和标准差
        avg = sum(average_list) / (10 - average_list.count(0))
        average_num = 0
        avg_list = [0] * 10
        while (average_num < (10 - average_list.count(0))):
            avg_list[average_num] = math.pow(
                average_list[average_num] - avg, 2)
            average_num = average_num + 1
        SD = math.sqrt(sum(avg_list) / (10 - average_list.count(0) - 1))
        print('Average: ' + str('%.3f' % avg) +
              '  ,  ' + 'S.D.： ' + str('%.3f' % SD))
        sheet.write(looptimes + 1, 12, float('%.3f' % avg))
        sheet.write(looptimes + 1, 13, float('%.3f' % SD))

        looptimes = looptimes + 1
    book.save('../10 average of TOP 10/DATA of ' + event + '.xls')


##########################################################################
# final output , from cubing china
def cubingchina_result_operate(competitors, event):
    cubingchina_get_average(competitors + '?sort=' + event,
                            cubingchina_get_WCA_ID(competitors + '?sort=' + event), event)


# final output , from WCA
def WCA_result_operate(comp_competitors, event):
    WCA_get_average(comp_competitors + '/psych-sheet/' + event,
                    WCA_get_WCA_ID(comp_competitors + '/psych-sheet/' + event), event)

##### Choose function here #####
#cubingchina_result_operate('https://cubingchina.com/competition/China-Championship-2017/competitors' , '333')

if __name__ == '__main__':
    WCA_result_operate(
        'https://www.worldcubeassociation.org/competitions/WC2017/registrations', '333')

# event = 222 ; 333 ; 444 ; 555 ; 666 ; 777 ; 333bf ; 333fm ; 333oh ;
# 333ft ; minx ; pyram ; clock ; skewb ; sq1 ; 444bf ; 555bf ; 333mbf
