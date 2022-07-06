import requests
from bs4 import BeautifulSoup
import re
import inspect
from random import choice, randint
from .utils import phone_b64_parse
import time
import os
from MainParser.models import Ad
import threading
from datetime import datetime, timedelta
from .avito_cookies import cookies
import logging

import random
l = list(cookies.items())
random.shuffle(l)
d = dict(l)
cookies = d


user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0']

FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO)
avito = logging.FileHandler('logs/avito.log')
avito.setFormatter(logging.Formatter(FORMAT))

logger = logging.getLogger('avito')
logger.addHandler(avito)
logger.propagate = False


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'u=2t9do3b0.1hnw16s.11ehufk22s4g0; v=1650647156; luri=moskva; buyer_location_id=637640; sx=H4sIAAAAAAAC%2F1TMS3KDMAwA0LtozUL%2BSLK5DZbtAmWmUKhpwnD3rLLIBd4FVj2bQEgWySYpfhhSMCFhccmoC9Bf0KAHj0fD%2FPVEHNVITDux6tra33LS9L1BBwV6w4TiHAneHTAzaxaukSOx51gkFRezEKpKjm9Z%2Fkc7ol%2B3c9Mqx%2Fx7Olv3wc9cH9Py8yGziff9CgAA%2F%2F9m58hXtQAAAA%3D%3D; dfp_group=57; abp=0; _gcl_au=1.1.2002214504.1650647160; _ga_9E363E7BES=GS1.1.1650647159.1.1.1650647221.59; _ga=GA1.1.1827810015.1650647160; _gid=GA1.2.710741973.1650647160; SEARCH_HISTORY_IDS=1; _ym_uid=1650647162280574338; _ym_d=1650647162; adrdel=1; adrcid=ALi8LuuRlgWzogaIa_YtjUw; cto_bundle=xvBFnV9kTFp2T3FtZlNJRVVNbzc3VzRBVlV2Z24lMkJ5T2tCVlRRVlpZNTM3VjBZZktMUm1nJTJGSmRZUGlMM3JzNEZqUk1QcHpncSUyRmI3ZFBFNDlvV2hxWnJCVVRkJTJGTmUyOUNJa2hISVVkb2V6bkhBbkdWeEF3aUNPRmo0d2hUNzNZdmU1JTJCR2tqVWp5JTJCcHpmRiUyRkJPZzgwblBubVQlMkJ1TlVSRlZVVk51UjBPWUV2VkhDOHgwTThPeUpTSlNyV1lDYnBWWjNyZU1jaGxYcTNhWkJKb2dwV2VHN0tGWURoUSUzRCUzRA; _ym_visorc=w; _ym_isad=2; buyer_laas_location=637640; showedStoryIds=129-128-125-124-122-121-120-116-115-113-112-111-108-105-104-103-99-98-97-96-94-88-83-78-71; f=5.8696cbce96d2947c36b4dd61b04726f14f0aa6d4f7157ca44f0aa6d4f7157ca44f0aa6d4f7157ca44f0aa6d4f7157ca42668c76b1faaa3582668c76b1faaa3582668c76b1faaa3584f0aa6d4f7157ca402b7af2c19f2d05c02b7af2c19f2d05c0df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac7b0d53c7afc06d0b8b1472fe2f9ba6b99364cc9ca0115366f03bdfa0d1f878520f7bd04ea141548c956cdff3d4067aa559b49948619279117b0d53c7afc06d0b2ebf3cb6fd35a0ac71e7cb57bbcb8e0ff0c77052689da50ddc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1a0df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686adecb8388123cde3fb9ec93e8150cb32f702c730c0109b9fbb1ef6e77b994771b7ecad4a27389d318fd21ab7cd585086e04d908c0130110a21a9e7a66faf989bc1e2415097439d404746b8ae4e81acb9fa786047a80c779d5146b8ae4e81acb9fa8d3db3389eefdd068edb85158dee9a6671e7cb57bbcb8e0f3e08c616a2d267c39b0c17aee5a3f60bbc289eafbcfd72a4575d77d5fd32c277',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'If-None-Match': 'W/"39e6a5-3opLKVOxQIPnUrjCLDLZBx3huAg"',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

class AvitoParser:
    title = ['title-root.*', 'iva-item-title.*', 'title-listRedesign.*', 'text-text-LurtD.*', 'text-size-s.*',
             'text-bold.*']
    description = ['iva-item-description.*', 'iva-item-text.*', 'text-text-LurtD', 'text-size-s.*']
    price = ['price-text-.*', 'text-text-.*', 'text-size-s-.*']
    link = ['link-link-.*', 'link-design-default-.*', 'title-root.*', 'iva-item-title-.*', 'title-listRedesign-.*']
    address = ['geo-address.*', 'text-text.*', 'text-size.*']

    def __init__(self):
        all_attributes = inspect.getmembers(AvitoParser, lambda a: not (inspect.isroutine(a)))
        self.user_attrs = {a[0]: a[1] for a in all_attributes if not (a[0].startswith('__') and a[0].endswith('__'))}
        self.user_attrs_compiled = {k: [re.compile(vv) for vv in v] for k, v in self.user_attrs.items()}

        self.cookie_counter = 0

        self.session = requests.session()
        self.session.headers.update(headers)
        self.session.cookies.update(list(cookies.values())[self.cookie_counter])
        print(list(cookies.values())[self.cookie_counter])
        print( list(cookies.keys())[self.cookie_counter])
        
        self.session.proxies.update({'https': list(cookies.keys())[self.cookie_counter]})
        #self.session.get('https://avito.ru')

        # self.session.get('https://avito.ru')
        self.url = 'https://www.avito.ru/moskva/kvartiry/sdam-ASgBAgICAUSSA8gQ?s=104&user=1'
        self.url = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?s=104&user=1'

    def get_ads(self):
        self.cookie_counter += 1
        self.cookie_counter %= len(cookies)

        self.session.headers.update(headers)

        self.session.proxies.update({'https': list(cookies.keys())[self.cookie_counter].replace('https', 'http')})

        print('------')
        print(f'Using {list(cookies.keys())[self.cookie_counter]}')
        
        ip = self.session.get('https://api.ipify.org').content.decode('utf8')
        self.session.cookies.update(list(cookies.values())[self.cookie_counter])
        print('My public IP address is: {}'.format(ip))
        print('------')
        try:
            page = self.session.get(self.url)
            print(page)
        except:
            return []
            
        soup = BeautifulSoup(page.text, 'html.parser')
        res = {}
        for k, v in self.user_attrs_compiled.items():
            res[k] = soup.find_all(lambda x: self._reg_equal(v, x.get('class')))

        ress = [dict() for _ in range(len(res['title']))]
        for k, v in res.items():
            for id, j in enumerate(v):
                if k == 'link':
                    ress[id][k] = j.get('href')
                    ress[id]['id'] = ress[id]['link'].split('_')[-1]
                else:
                    ress[id][k] = j.getText().replace(u'\xa0', u' ')
        ress = [
                    i
                    for i in ress
                    if not soup.find("div", {"id": "i" + i["id"]}).find_all(
                        lambda x: x.name == "i"
                        and re.compile(r"style-vas-icon-.+").search(str(x.get("class")))
                    )
                ]
        return ress

    def get(self, url):
        return self.session.get(url)

    # Check if all regexp are in second array
    def _reg_equal(self, regs, cls):
        if cls and regs:
            return all(any(r.match(c) for c in cls) for r in regs)
        else:
            return False

    def previous_proxy(self):
        return list(cookies.keys())[self.cookie_counter]


def run():
    start_time = datetime.now()
    proxy_stat = {x: {'ddos': 0, 'good': 0} for x in list(cookies.keys())}
    total_ads = [0]

    ap = AvitoParser()
    ads = ap.get_ads()
    if len(ads) == 0:
        proxy_stat[ap.previous_proxy()]['ddos'] += 1
        print("DDOS")

    time.sleep(1)
    print()
    while True:
        if datetime.now() > start_time + timedelta(hours=2):
            start_time = datetime.now()
            logger.info('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            logger.info(f"Total ads: {total_ads[0]}")
            for proxy, statistic in proxy_stat.items():
                logger.info(f"{proxy} - DDOS:{statistic['ddos']}, GOOD: {statistic['good']}")
            proxy_stat = {x: {'ddos': 0, 'good': 0} for x in list(cookies.keys())}
            total_ads = [0]
        print(123)
        last_ads = ap.get_ads()
        if len(ads) == 0:
            print("DDOS")
            proxy_stat[ap.previous_proxy()]['ddos'] += 1
            time.sleep(5)
            continue

        proxy_stat[ap.previous_proxy()]['good'] += 1
        for i, ad in enumerate(last_ads):

            def get_phone_and_save(ap, ad):
                phone = ''
                for i in range(2):
                    try:
                        from urllib.parse import unquote
                        json = ap.session.get(
                            f"https://m.avito.ru/api/1/items/{ad['link'].split('_')[-1]}/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir").json()
                        phone = unquote(
                            re.findall(r'ru\.avito://1/phone/call\?number=(.*)', json['result']['action']['uri'])[0])
                        print(phone)
                        proxy_stat[ap.previous_proxy()]['good'] += 1
                        total_ads[0] += 1

                        if Ad.objects.filter(link=ad['link']):
                            return
                            
                        Ad(date=datetime.now(), site='av', title=ad['title'], address=ad['address'], price=ad['price'],
                           phone=phone, city='Москва', person='', link=ad['link']).save()
                        return
                    except Exception as e:
                        print('ddos')
                        time.sleep(1)
                        proxy_stat[ap.previous_proxy()]['ddos'] += 1
                    

            if Ad.objects.filter(link=ad['link']):
                continue

            print(ad)            
            threading.Thread(target=get_phone_and_save, args=(ap, ad)).start()
            time.sleep(3)
        time.sleep(3)
# d = ap.get_ads()
# for id, i in enumerate(d):
# #     print('-------')
#     print(i)
#     b64str = 'data:image/png;base64,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'
#     # try:
#     while True:
#         try:
#             ap.session.get(f'https://avito.ru{i["link"]}')
#             time.sleep(3)
#             b64str = ap.get(f"https://www.avito.ru/web/1/items/phone/{i['link'].split('_')[-1]}").json()['image64']
#             print(phone_b64_parse(b64str))
#             break
#         except:
#             print('ebat huevo vyrubai!!!!!!')
#
#             exit(0)
#             # ap.session = requests.session()
#             # ap.session.headers.update(headers)
#             time.sleep(3)
#         time.sleep(5)
# except:
#     continue
# time.sleep(1)
