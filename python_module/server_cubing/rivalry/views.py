from django.shortcuts import render, redirect
from django.http import HttpResponse
from json_response import JsonResponse as JsonHttpResponse
import requests
from lxml import etree

def vs(request):
    a = []
    p1_id = request.GET['p']
    p2_id = request.GET['ap']
    item_name = request.GET['item']
    item_class = 'event-icon' + ' event-icon-' + item_name
    pk_page_url = 'http://cubingchina.com/results/battle/' + p1_id + '-' +p2_id
    page_data = requests.get(pk_page_url)
    page_selector = etree.HTML(page_data.text)
    path = '//span[@class="' + item_class + '"]'
    battle_data =page_selector.xpath(path)[0]
    a[0] = battle_data.xpath('../../following-sibling::tr[14]/td[3]/text()')
    # a[1] = battle_data.xpath('../../following-sibling::tr[14]/td[4]/text()')

    return HttpResponse(a[0])
