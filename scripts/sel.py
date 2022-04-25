from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from seleniumwire import webdriver
from avito_cookies import cookies


f = open('proxies.py', 'w')
f.write(f'cookies = {{')

for prs in reversed(cookies.keys()):
    print(prs)
    try:
        options = Options()
        options.headless = True
        #"https://kit:17628312D@91.245.227.152:9999": {
        myProxy = prs
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            'sslProxy': myProxy,
            'noProxy': ''})
        #options.proxy = proxy
        optionsw = {
           'proxy': {
                'http': myProxy,
                'https': myProxy,
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        driver = webdriver.Firefox(executable_path='./geckodriver', options=options, seleniumwire_options=optionsw)
        try:
            driver.get("https://avito.ru")
        except:
            pass
        time.sleep(1)
        driver.set_page_load_timeout(3)
        try:
            driver.get("https://avito.ru")
        except:
            pass

        c = {}
        for cookie in driver.get_cookies():
            c[cookie['name']] = cookie['value']
        f = open('proxies.py', 'w')
        print(f'"{myProxy}": {c},')
        f.write(f'"{myProxy}": {c},')
    except Exception as e:
        print(e)
f.write('}')