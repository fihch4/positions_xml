#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import datetime
from config import *
import re
import xml.etree.ElementTree as ET


def xml_proxy_get_data(get_url):
    try:
        r = requests.get(get_url)
        return r
    except Exception as e:
        print(f"Error: {e}")
        return "Error"


with open('keys.txt', encoding='utf-8', mode='r') as f:
    lines = f.readlines()

for i in lines:
    res = re.split(';', i)
    key = res[0]
    domain = res[1]
    group: str = res[2]
    region = res[3]
    if '\n' in region:
        region = region.replace('\n', '')
    print(f"Domain: {domain} - Ключевое слово: {key} - Регион: {region} - Кластер: {group}")
    request_url = xml_proxy_url + '&query=' + str(key) + '&' + region + xml_proxy_other_url
    r = xml_proxy_get_data(request_url)
    if r != "Error":
        root = ET.fromstring(r.text)
        position = 1
        domain_url = None
        url_key = None
        for i in root.findall('.//doc/'):
            if i.tag == 'url':
                url_key = i.text.lower()
            if i.tag == 'domain':
                domain_url = i.text.lower()
            if domain_url and url_key is not None:
                print(
                    f"Дата: {datetime.datetime.now().date()} Домен: {domain_url} - URL: {url_key} - "
                    f"Позиция: {position} - "
                    f"Ключ: {key} - Кластер: {group} - Регион: {regions_dictionary[region]}")
                if domain in domain_url:
                    print(f"Наш домен на позиции: {position}")
                domain_url = None
                url_key = None
                position += 1
