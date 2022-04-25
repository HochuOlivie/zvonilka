import requests
import time

for i in range(13):
    s = requests.session()
    print(s.get('https://avito.ru'))
    print(s.get('https://avito.ru/favicon.ico'))
    print(s.get('https://avito.ru'))
    print(dict(s.cookies))
    time.sleep(5)