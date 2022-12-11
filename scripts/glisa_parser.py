import requests
from bs4 import BeautifulSoup
import re
from MainParser.models import Ad
from datetime import datetime, timedelta
from django.utils import timezone
import time

cookies = {
    'rapidshopref': 'http%3A%2F%2Fxn--80afpl5a.xn--p1ai%2F%25D0%25B2%25D0%25BE%25D0%25B9%25D1%2582%25D0%25B8%2F',
    'rapidshoplogin': 'ceb187409f19d79391ec9c7310258a6c',
    'rapidshopemail': 'egorkin.ivan64%40gmail.com',
    'user_code': 'grf_21052_5310531',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'rapidshopref=http%3A%2F%2Fxn--80afpl5a.xn--p1ai%2F%25D0%25B2%25D0%25BE%25D0%25B9%25D1%2582%25D0%25B8%2F; rapidshoplogin=ceb187409f19d79391ec9c7310258a6c; rapidshopemail=egorkin.ivan64%40gmail.com; user_code=grf_21052_5310531',
    'Upgrade-Insecure-Requests': '1',
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

req_amount = 0
while True:
    if req_amount > 3000:
        exit(0)
        
    try:
        url = 'http://глиса.рф/личныйкабинет/adlist/0/'
        try:
            page = session.get(url)
            req_amount += 1

            if req_amount % 10000 == 0:
                print(f"Working! Amount req: {req_amount}")
        except Exception as e:
            print(f"[REQUEST] {e}")
            continue
            
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

        continue
    except Exception as e:
        print(f"[TOTAL] {e}")
