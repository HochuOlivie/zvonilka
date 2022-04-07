import requests
from bs4 import BeautifulSoup
import re
import inspect
from random import choice, randint
from .utils import phone_b64_parse
import time
import os
from MainParser.models import Ad

from datetime import datetime


cookies = {
    'u': '2t92zh5n.1mxle60.s1woe35wpgg0',
    'buyer_laas_location': '637640',
    'buyer_location_id': '641780',
    'sx': 'H4sIAAAAAAAC%2F1TQS7ajIBAA0L0wdgBCFVZ2w6dAgq3RtBo6x733KO%2BdbOAO7ltIHpwGmyR7aSGCHwjYmgFd4EhDEre3OMRNFC7j%2BhrWls96zzylaZn0VlXzcpqrF51gcVNoyIDUSl6dQEQM0WIiJECDxNazpmhBhmAjfWS3Z3sH3vWL%2FuE51TDuqbY%2FucQyu619yT3B1Qni1h4ulHs0ZpHVnDnU83nm4UNma3EM%2BdjReP08noVo3fU6PjC8gjx%2BSY1gNV6diMmrPkVtvFSQGJLrEZS04BSoaH%2FkWZ%2Bm0dJ4G%2F3Bf%2Fs6l1TzthzVZM31u0Hjdf0PAAD%2F%2F9LkfFRiAQAA',
    'showedStoryIds': '116-113-112-111-108-105-104-103-99-98-97-96-94-88-83-78-71',
    'luri': 'novosibirsk',
    'f': '5.7402d030492fb99536b4dd61b04726f1a816010d61a371dda816010d61a371dda816010d61a371dda816010d61a371ddbb0992c943830ce0bb0992c943830ce0bb0992c943830ce0a816010d61a371dd2668c76b1faaa358c08fe24d747f54dc0df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac7b0d53c7afc06d0b8b1472fe2f9ba6b99364cc9ca0115366f03bdfa0d1f878520f7bd04ea141548c956cdff3d4067aa559b49948619279117b0d53c7afc06d0b2ebf3cb6fd35a0ac71e7cb57bbcb8e0ff0c77052689da50ddc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1a0df103df0c26013a03c77801b122405c868aff1d7654931c9d8e6ff57b051a58d53a34211e148d88000f4c8f0ee6a421938bf52c98d70e5c939e7a4bd30d5db9bda62c2f2d8bd858d21ab7cd585086e04d908c0130110a21a9e7a66faf989bc1e2415097439d404746b8ae4e81acb9fa786047a80c779d5146b8ae4e81acb9fa99d4b279dec4605da291fc3f0bfffdd52da10fb74cac1eabd1d953d27484fd81666d5156b5a01ea6',
    'ft': '"TrqF/tHLa/qpoKu2IYRX606SFz9E4IZBTCwoDMy+bS5SlGwLRmYvTAteA5D959rY6sIK8zzR2KOFHOk2wAJIShs7/NINqL1VvMVjrot6Iivmsw6kjYABc5mrr9Q7quN58/nC1xHo7ZcnwO/F1Wayg2E0cY5R/+CO6RNmKkg8EaeWN5a8rtG3dG2uGnSSMpPd"',
    'v': '1649362799',
    'dfp_group': '4',
    'SEARCH_HISTORY_IDS': '1',
}

user_agents = [ 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0' ]

headers = {
    'User-Agent': choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Content-Type': 'text/html; charset=utf-8',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'u=2t92xywk.nkb3i6.uywl1y4q6bg0; v=1649087796; luri=moskva; buyer_location_id=637640; sx=H4sIAAAAAAAC%2FwTAUQ6DIAwG4Lv8z3uQgrblNi0p0YWXbYkmM9zd70bOHmTSSZeVy5bU3FRStGzqpXXUGycqDrr%2Bl%2FPeR3yWYf57H77r%2BJqwcDvxQqCmrWjitRDN%2BQQAAP%2F%2FkvYURVsAAAA%3D; SEARCH_HISTORY_IDS=1; f=5.8696cbce96d2947c36b4dd61b04726f1a816010d61a371dda816010d61a371dda816010d61a371dda816010d61a371ddbb0992c943830ce0bb0992c943830ce0bb0992c943830ce0a816010d61a371dd2668c76b1faaa358c08fe24d747f54dc0df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac7b0d53c7afc06d0b8b1472fe2f9ba6b99364cc9ca0115366f03bdfa0d1f878520f7bd04ea141548c956cdff3d4067aa559b49948619279117b0d53c7afc06d0b2ebf3cb6fd35a0ac71e7cb57bbcb8e0ff0c77052689da50ddc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1a0df103df0c26013a03c77801b122405c868aff1d7654931c9d8e6ff57b051a5860ccc977364de1549ec93e8150cb32f7938bf52c98d70e5c939e7a4bd30d5db9bda62c2f2d8bd858d21ab7cd585086e04d908c0130110a21a9e7a66faf989bc1e2415097439d404746b8ae4e81acb9fa786047a80c779d5146b8ae4e81acb9fa638b1237dc2c97678edb85158dee9a662da10fb74cac1eabd1d953d27484fd81666d5156b5a01ea6; ft="1b7Vm4zWdCTB+nfOfuDJpgaEL1Ls3lVw0ZmJvpclMIE6uKRWWFEX8OKZQR9j6a84ek9o6X+xmi1DCgHXsxelBX1aZeTpBwdHTTQvCEg8BvaJwOFzxM2LtmBGIMdLNBsFqsC3c3kEAouwzb6ag6V09nYhSvvO88sVG3jxwc2Gv/PjtTF9U3PrUVLouF7kcHon"; dfp_group=3; buyer_from_page=catalog',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'If-None-Match': 'W/"479f01-sUkV2VRz2QYMSCHXyUrLBLU8eUQ"',
}


class AvitoParser:
    title = ['title-root.*', 'iva-item-title.*', 'title-listRedesign.*', 'text-text-LurtD.*', 'text-size-s.*',
             'text-bold.*']
    description = ['iva-item-description.*', 'iva-item-text.*', 'text-text-LurtD', 'text-size-s.*']
    price = ['price-text-.*', 'text-text-.*', 'text-size-s-.*']
    link = ['link-link-.*', 'link-design-default-.*', 'title-root.*', 'iva-item-title-.*', 'title-listRedesign-.*']

    def __init__(self):
        all_attributes = inspect.getmembers(AvitoParser, lambda a: not (inspect.isroutine(a)))
        self.user_attrs = {a[0]: a[1] for a in all_attributes if not(a[0].startswith('__') and a[0].endswith('__'))}
        self.user_attrs_compiled = {k: [re.compile(vv) for vv in v] for k, v in self.user_attrs.items()}

        self.session = requests.session()
        self.session.headers.update(headers)
        self.session.cookies.update(cookies)
        self.session.get('https://avito.ru')
        time.sleep(10)
        # self.session.get('https://avito.ru')
        self.url = 'https://www.avito.ru/moskva/kvartiry/?s=104&user=1'

    def get_ads(self):
        page = self.session.get(self.url)
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
        return ress

    def get(self, url):
        return self.session.get(url)

    # Check if all regexp are in second array
    def _reg_equal(self, regs, cls):
        if cls and regs:
            return all(any(r.match(c) for c in cls) for r in regs)
        else:
            return False


def run():
    ap = AvitoParser()
    n = 20
    ads = ap.get_ads()
    if len(ads) == 0:
        print("DDOS")
        return
        
    last_ad_id = [ads[x]['id'] for x in range(n)]
    last_ad_id.reverse()

    time.sleep(5)
    print()
    while True:

        
        last_ads = ap.get_ads()
        if len(ads) == 0:
            print("DDOS")
            return

        for i, ad in enumerate(last_ads):
            if ad['id'] in last_ad_id:
                break

            if i < n:
                del last_ad_id[0]
                last_ad_id.append(ad['id'])

            print(ad)
            time.sleep(3)
            if False:                
                ap.session.get(f'https://avito.ru{ad["link"]}')
                b64str = ap.get(f"https://www.avito.ru/web/1/items/phone/{ad['link'].split('_')[-1]}").json()['image64']
                phone = phone_b64_parse(b64str)
            else:
                phone = ''
            print(f"Phone: {phone}")
            Ad(date=datetime.now(), site='av', title=ad['titlle'], address='', price=0, phone=phone, city='', person='', link=ad['link']).save()

        time.sleep(5)
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

