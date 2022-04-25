import requests

cookies = {
    'u': '2t9d2go3.cn0cq9.1hgs6lngmysw',
    'v': '1650557683',
}

p = {
    'http': "http://kit:17628312D@45.141.103.113:9999/",
    'https': "https://kit:17628312D@45.141.103.113:9999/"
}

headers = {
    'authority': 'www.avito.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'u=2t9d2fsj.cn0cq9.1li70doki5w00; v=1650556987',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
}

response = requests.get('https://www.avito.ru/', headers=headers, cookies=cookies, proxies=p)
print(response)