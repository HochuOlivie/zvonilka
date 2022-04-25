from requests import get
import requests

p = {
    'http': "http://kit:17628312D@45.141.103.113:9999/",
    'https': "https://kit:17628312D@45.141.103.113:9999/"
    }
s = requests.session()
s.proxies.update(p)

ip = s.get('https://api.ipify.org').content.decode('utf8')
print('My public IP address is: {}'.format(ip))