
import requests
from hyper.contrib import HTTP20Adapter
import time


url = 'https://avito.ru/'

p = {
    'http://': "kit:17628312D@193.104.57.4:9999",
    'https://': "kit:17628312D@193.104.57.4:9999"
    }
    

headers2 = {
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'image',
    'Referer': 'https://www.avito.ru/',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9',
}


headers3 = {
    'Cookie': 'u=2t9d2q0i.1gd50e9.1ohfqfgwqhe0; v=1650562554',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9'
    
}
headers3 = {
    'Host': 'www.avito.ru',
    'Cookie': 'u=2t9d33vo.1gd50e9.nfbf0fuyjsg0; v=1650568524',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="100"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9',
}


s = requests.session()
#s.headers.update(headers2)
#s.get(url)
#s.get(url + 'favicon.ico')
#print(s.cookies)
#print(f'u={s.cookies["u"]}; v=s.cookies["v"]')
#time.sleep(1)
headers3 = {
    'Host': 'www.avito.ru',
    #'Cookie': f'u={s.cookies["u"]}; v={s.cookies["v"]}',
    #'Cookie': 'u=2t9dlley.19lrycn.v5104gl1ig00; v=1650606058',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="100"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9',
}
cookies = {'buyer_laas_location': '659020', 'buyer_location_id': '659020', 'dfp_group': '61', 'luri': 'tyumen', 'sx': 'H4sIAAAAAAAC%2FwTAUQrCMAwG4Lv8zz50cflDehtNKgyliEJXGbu73wGSjDQ%2BnK5c6c3u7eppWiIsHfXAQMUtVctnvucunbL%2Fhm59fF%2FSy7Y8Z%2BCChrpQC311kfP8BwAA%2F%2F9pZprAWwAAAA%3D%3D', 'u': '2t9dlrp5.1gd50e9.u98y4ejpaaw0', 'v': '1650608521'}

#s.mount('https://', HTTP20Adapter())
print(requests.get('https://avito.ru', headers=headers3, proxies=p, cookies=cookies))
