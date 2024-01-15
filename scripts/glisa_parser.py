import requests
from bs4 import BeautifulSoup
import re
from MainParser.models import Ad
from datetime import datetime, timedelta
from django.utils import timezone
import time

cookies = {
    'user_rnd': 'grf_1705324054_0',
    '_ga': 'GA1.2.373876291.1705324056',
    '_gid': 'GA1.2.1440359982.1705324056',
    '_ym_uid': '1705324056275299195',
    '_ym_d': '1705324056',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    'rapidshopref': 'https%3A%2F%2Fxn--80afpl5a.xn--p1ai%2F',
    'rapidshoplogin': '8297d8a343692c1dca1202873a1e901c',
    'rapidshopemail': 'Amaks996%40mail.ru',
    'user_code': 'grf_23071_1232410',
    '_gat': '1',
    '_ga_9TY92ZQNZT': 'GS1.2.1705324056.1.1.1705324145.0.0.0',
}


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'user_rnd=grf_1705324054_0; _ga=GA1.2.373876291.1705324056; _gid=GA1.2.1440359982.1705324056; _ym_uid=1705324056275299195; _ym_d=1705324056; _ym_isad=1; _ym_visorc=w; rapidshopref=https%3A%2F%2Fxn--80afpl5a.xn--p1ai%2F; rapidshoplogin=8297d8a343692c1dca1202873a1e901c; rapidshopemail=Amaks996%40mail.ru; user_code=grf_23071_1232410; _gat=1; _ga_9TY92ZQNZT=GS1.2.1705324056.1.1.1705324145.0.0.0',
    'Referer': 'https://xn--80afpl5a.xn--p1ai/%D0%BB%D0%B8%D1%87%D0%BD%D1%8B%D0%B9%D0%BA%D0%B0%D0%B1%D0%B8%D0%BD%D0%B5%D1%82/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def _reg_equal(reg, cls):
    if cls:
        rc = re.compile(reg)
        return rc.match(cls)


session = requests.session()
session.headers.update(headers)
session.cookies.update(cookies)

start = timezone.localtime(timezone.now())
print(f'Start: {start}')

TABLE_XPATH = '//*[@id="content"]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody'

req_amount = 0
while True:
    if req_amount > 3000:
        exit(0)
        
    try:
        url = 'https://xn--80afpl5a.xn--p1ai/%D0%BB%D0%B8%D1%87%D0%BD%D1%8B%D0%B9%D0%BA%D0%B0%D0%B1%D0%B8%D0%BD%D0%B5%D1%82/adlist/73565/'
        try:
            page = session.get(url, verify=False)
            req_amount += 1

            if req_amount % 10000 == 0:
                print(f"Working! Amount req: {req_amount}")
        except Exception as e:
            print(f"[REQUEST] {e}")
            continue

        print("Parsing...")
        soup = BeautifulSoup(page.content, 'lxml')

        titles = soup.find_all(lambda x: _reg_equal(r'name_\d+', x.get('id')))
        links = [title.get('href') for title in titles]
        titles = [title.getText().strip() for title in titles]

        phones = soup.find_all(lambda x: str(x.get('href')).startswith('tel:'))
        phones = [phone.getText() for phone in phones]

        addresses = soup.find_all(lambda x: str(x.get('id')).startswith('c_details_'))

        addresses = [address.findAll(text=True, recursive=False)[-1] for address in addresses]

        rows = soup.find_all(lambda x: re.compile('crow_\d+').match(str(x.get('id'))) if x else False)
        prices = [row.find(lambda x: x.name == 'td' and x.get('align') == 'right') for row in rows]
        prices = [price.getText().strip().replace('\xa0', u'') for price in prices]

        
        for i in zip(titles, prices, links, addresses, phones):            
            try:
                ads = Ad.objects.filter(link=i[2])
                if ads:
                    continue
            except Exception as e:
                print(f"[BD] {e}")
                continue

            print(datetime.now().strftime("%H:%M:%S"), i[3])

            Ad(site='ci', title=i[0], address=i[3], price=i[1],
                   phone=i[4], city='Москва', link=i[2], full_link=i[2]).save()

    except Exception as e:
        print(f"[TOTAL] {e}")

    finally:
        time.sleep(0.2)
