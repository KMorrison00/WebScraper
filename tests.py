import Scraper as s
import pandas as pd
import time
from pubproxpy import Level, Protocol, ProxyFetcher
from selenium import webdriver
import requests


USER_AGENTS = \
        ['Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    ,'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    , 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    , 'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    , 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    ,  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    , 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
    , 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    , 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    , 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    , 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36']

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome(options=options)
#
# # user_agent = cycle(USER_AGENTS)
#
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': USER_AGENTS[5]})

# driver.close()

def get_proxies():
    proxy_fetcher = ProxyFetcher(level=Level.ELITE, protocol=Protocol.HTTP, countries="CA")
    proxies = proxy_fetcher.get()
    url = "http://httpbin.org/ip"
    print(proxies)
    working_proxies = []
    for proxy in proxies:
        getter = {"http": proxy, "https":proxy}
        try:
            response = requests.post(url, proxies=getter)
            print(response.elapsed.total_seconds())
            if response.elapsed.total_seconds() < 15:
                return proxy
            working_proxies.append(proxy)
        except requests.exceptions.ProxyError:
            proxies.remove(proxy)
    working_proxies.sort()
    return working_proxies[0]