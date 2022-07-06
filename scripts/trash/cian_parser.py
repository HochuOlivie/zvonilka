import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import inspect
import time
from datetime import datetime, timedelta
from .cian_cookies import cookies
from MainParser.models import Ad
import logging

FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
logging.basicConfig(level=logging.INFO)
cian = logging.FileHandler('logs/cian.log')
cian.setFormatter(logging.Formatter(FORMAT))

logger = logging.getLogger('cian')
logger.addHandler(cian)
logger.propagate = False

headers = {
    'authority': 'www.cian.ru',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Opera GX";v="85"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.65',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.cian.ru/',
    'accept-language': 'ru-RU,ru;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'cookie': '__cf_bm=vjX4fXMAkrQQOj72KL5RIFLYvXxQA6rF91xTw_xzkSs-1649608462-0-ARTxP+u4PZQe5LfAQXWC3DpoZDoPa4Czm8G9ldLvlCavamDuViBMjne+0OlXb4+BHwFre2LWXGVMreO1AXLgWHw=; _CIAN_GK=ad09d1d7-d870-4167-9849-5d2a56ceb81d; _gcl_au=1.1.799167971.1649608463; anti_bot="2|1:0|10:1649608483|8:anti_bot|40:eyJyZW1vdGVfaXAiOiAiMTk0Ljg3Ljk0LjQzIn0=|7658adc25d94861dffb6a8339001b9cc0ca5fed21f46ba49cf4124e3613bf64f"; session_region_id=1; adb=1; login_mro_popup=1; uxfb_usertype=searcher; sopr_utm=%7B%22utm_source%22%3A+%22direct%22%2C+%22utm_medium%22%3A+%22None%22%7D; sopr_session=3bacc1a0955048e5; _ga=GA1.2.1291009391.1649608495; _gid=GA1.2.1122705383.1649608495; _dc_gtm_UA-30374201-1=1; _ym_uid=1649608495222256227; _ym_d=1649608495; _ym_isad=2; uxs_uid=27923a50-b8ec-11ec-be3e-ada3716650b3; _ym_visorc=b',
}


class AvitoParser:
    title = ['.*row.*']
    link = ['.*link--eoxce']
    address = ['.*labels.*']

    def __init__(self):
        all_attributes = inspect.getmembers(AvitoParser, lambda a: not (inspect.isroutine(a)))
        self.user_attrs = {a[0]: a[1] for a in all_attributes if not (a[0].startswith('__') and a[0].endswith('__'))}
        self.user_attrs_compiled = {k: [re.compile(vv) for vv in v] for k, v in self.user_attrs.items()}
        self.cookie_counter = 0

        self.session = requests.session()
        self.session.headers.update(headers)
        self.session.cookies.update(list(cookies.values())[self.cookie_counter])
        self.session.proxies.update({'https': list(cookies.keys())[self.cookie_counter]})

        # self.url = 'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&sort=creation_date_desc&type=4'
        self.url = 'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&offer_type=flat&region=1&sort=creation_date_desc&totime=3600&type=4'

    def get_ads(self):

        self.cookie_counter += 1
        self.cookie_counter %= len(cookies)
        self.session.cookies.update(list(cookies.values())[self.cookie_counter])
        self.session.proxies.update({'https': list(cookies.keys())[self.cookie_counter]})
        print(f"Using {list(cookies.keys())[self.cookie_counter]}")
        try:
            page = self.session.get(self.url)
        except Exception as e:
            print(e)
            return []

        soup = BeautifulSoup(page.text, 'html.parser')
        res = {}
        for k, v in self.user_attrs_compiled.items():
            res[k] = soup.find_all(lambda x: self._reg_equal(v, x.get('class')))

        ress = []
        for k, v in res.items():
            for id, j in enumerate(v):
                if k == 'title' and j.find('span', recursive=False):
                    ress.append({k: j.getText().replace(u'\xa0', u' ')})

        phones = re.findall(r'''"phones":.{"countryCode":"(\d+)","number":"(\d+)"}''', page.text)

        #noviy code s ttelephnami
        info = re.findall(r'''window\._cianConfig\['frontend-serp'] = (.*);[\n.]?</script>''', page.text)
        if not info:
            return []
        import json
        info = json.loads(info[0])

        phones = []
        ids = []
        
        offers = info[-1]['value']['results']['offers']
        print(len(offers))
        for offer in offers:
            try:
                phone = '+' + offer['phones'][0]['countryCode'] + offer['phones'][0]['number']
                id = offer['id']
            except:
                phone = ''
                id = offer['id']
            phones.append(phone)
            ids.append(id)
        #-----------------------
        print(phones)
        description = soup.find_all('div', {'data-name': 'Description'})
        for i in range(len(ress)):
            ress[i]['description'] = description[i].getText()

        price = soup.find_all('span', {'data-mark': 'MainPrice'})
        for i in range(len(ress)):
            ress[i]['price'] = price[i].getText()

        for k, v in res.items():
            for id, j in enumerate(v):
                if k == 'link':
                    ress[id][k] = j.get('href').replace(u'\xa0', u' ')
                    for i1, id1 in enumerate(ids):
                        if str(id1) in ress[id][k]:
                            ress[id]['phone'] = phones[i1]
                            break
                    else:
                        ress[id]['phone'] = ''
                elif k != 'title':
                    ress[id][k] = j.getText().replace(u'\xa0', u' ')
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

    while True:

        if datetime.now() > start_time + timedelta(hours=2):
            start_time = datetime.now()
            logger.info('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
            logger.info(f"Total ads: {total_ads[0]}")
            for proxy, statistic in proxy_stat.items():
                logger.info(f"{proxy} - DDOS:{statistic['ddos']}, GOOD: {statistic['good']}")
            proxy_stat = {x: {'ddos': 0, 'good': 0} for x in list(cookies.keys())}
            total_ads = [0]

        last_ads = ap.get_ads()
        if len(last_ads) == 0:
            print("DDOS")
            proxy_stat[ap.previous_proxy()]['ddos'] += 1
            time.sleep(30)
            continue

        for i, ad in enumerate(last_ads):
            ad_db = Ad.objects.filter(link=ad['link'])
            if ad_db:
                continue

            total_ads[0] += 1
            proxy_stat[ap.previous_proxy()]['good'] += 1
            print(ad)
            
            if ad['phone'] == '+74954760059':
                continue
                
            Ad(date=datetime.now(), site='ci', title=ad['title'], address=ad['address'], price=ad['price'],
               phone=ad['phone'], city='Москва', person='', link=ad['link']).save()
        time.sleep(2 * 60)

# output = open('offers.xlsx', 'wb')
# output.write(response.content)
# output.close()
#
# print(pd.read_excel('offers.xlsx'))
