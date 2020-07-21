
import requests
import httplib2
import time
from requests.adapters import HTTPAdapter
import ssl
import urllib3
import certifi
ssl._create_default_https_context=ssl._create_unverified_context
headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding':'gzip,deflate,br',
                'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connection':'keep-alive',
                'Cookie':'csrftoken=3c2e91119ed38fbeb2801cf0f2a51239; tt_webid=6593486956754126343; __tasessionId=ya9o25ugs1535165811866; UM_distinctid=1656f034d0e16c-07d3dccecf5931-4c312b7b-384000-1656f034d0f492; CNZZDATA1259612802=13182784-1535163245-%7C1535163245; uuid="w:3a12f73daa84445c8004734b98cdf49f"',
             #   'Host':'www.toutiao.com',
                'Content-Type': 'application/json',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
                
    }
#proxies={'https': 'https://58.57.83.220:10800'}
#proxies={'https': 'https://219.141.153.41:80'}
proxies = {'https':'https://202.107.195.217:80'}
proxies = {'https':'80.52.238.30:36127'}

new_url = 'https://www.toutiao.com/c/user/3772023195/#mid=3772086105'

new_url = 'https://httpbin.org/get?show_env=1'
#new_url = 'https://httpbin.org/ip'
#new_url = 'https://www.toutiao.com/c/user/following/?user_id=103509373298&cursor=0&count=400&_signature=9VupXxAQrucpYqtcQKkmE.VbqU'


#r = requests.get(new_url,headers=headers,proxies=proxies,timeout=10,verify=False,allow_redirects=True)
r = requests.get(new_url,proxies=proxies,headers=headers,verify=False)

print (r.text)
 #/etc/pki/tls/certs/ca-bundle.crt
'''

import requests, os
os.environ['HTTP_PROXY'] = '112.25.60.32:8080'
os.environ['HTTPS_PROXY'] = '202.107.195.217:80'
try:
    text = requests.get('https://httpbin.org/get?show_env=1').text # request https address
except Exception as e:
    print(e)
    print('connect failed')
print(text) 
'''