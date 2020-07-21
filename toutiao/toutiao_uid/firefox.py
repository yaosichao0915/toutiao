import time
import re
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import httplib2
import random
from bs4 import BeautifulSoup
#最多10000条
#从一个大v出发，找1w粉丝，1w粉丝的关注全要，再从这1w粉丝的关注中抽取部分，作为种子，再找粉丝，再要关注
#一个followed池 作为种子往外找
#一个following池 作为最终值 去重
class scrap_uid(object):
    def __init__(self,uid,driver,follow_type,need_file='N'):
        self.page=1
        self.uid=uid
        self.uid_list=[]
        self.need_file=need_file
        self.follow_type=follow_type
        self.mark_time = time.time()
        self.file = './Proxy-IP.txt' 
        self.proxy_list = self.get_iplist()
        self.retry = 0
        self.url = 'https://www.toutiao.com/c/user/relation/%s/?tab=%s'%(self.uid,self.follow_type)      
     #   self.url='https://www.toutiao.com/c/user/relation/63955695731/?tab=following#mid=1607589748621315'
        self.driver=driver
      #  self.driver.get(self.url)
   
        
    def get_iplist(self):
        self.proxy_list = []
        ip_list = []
        with open(self.file, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                self.proxy_list.append('https://'+line.strip())
            return(self.proxy_list) 
            
    def get_random_ip(self):
        if time.time()-self.mark_time > 900:
            self.proxy_list=self.get_iplist()
            self.mark_time=time().time()
        proxy_ip = random.choice(self.proxy_list)
        proxies = {'https': proxy_ip}
        return proxies
        
    def get_newurl(self,cursor="0"):
        print ("page %s"%self.page)
       # print (cursor)
        script = "return TAC.sign('%s'+''+'%s')"%(self.uid,cursor)
        
        sig = self.driver.execute_script(script)
     #   print(script)
        #new_cursor in response
     #   print(sig)
        new_url="https://www.toutiao.com/c/user/%s/?user_id=%s&cursor=%s&count=400&_signature=%s"%(self.follow_type,self.uid,cursor,sig)
      #  new_url = "https://www.toutiao.com/c/user/following/?user_id=63955695731&cursor=0&count=20&_signature=OgUAVBAYYYYv27sk6rgwMzoFAE"
        print(new_url)
        time.sleep(10)
        self.page+=1
        res = self.get_content(new_url)   
# 还是要检测user-agent的版本        
    def get_content(self,new_url):
    #X-Forwarded-For
    #X-Real-IP
        headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding':'gzip,deflate,br',
                'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connection':'keep-alive',
                'Cookie':'csrftoken=3c2e91119ed38fbeb2801cf0f2a51239; tt_webid=6593486956754126343; __tasessionId=ya9o25ugs1535165811866; UM_distinctid=1656f034d0e16c-07d3dccecf5931-4c312b7b-384000-1656f034d0f492; CNZZDATA1259612802=13182784-1535163245-%7C1535163245; uuid="w:3a12f73daa84445c8004734b98cdf49f"',
                'Host':'www.toutiao.com',
                'Content-Type': 'application/json',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
                'X-Forwarded-For':'203.122.133.12',
                'X-Real-IP':'203.122.133.12',
                'HTTP_CLIENT_IP':'203.122.133.12',
    }
        proxies = self.get_random_ip()
       # print(proxies)
       # proxies={'https': '119.251.244.131:8080'}
        try:
          #  r = requests.get(new_url,headers=headers,proxies=proxies,timeout=10)
            r = requests.get(new_url,headers=headers,timeout=10)
            #ip = requests.get('http://httpbin.org/ip',headers=headers,proxies=proxies,timeout=2)
            #print (ip.status_code)
            hjson = r.json()
            self.parse_content(hjson)
            if hjson['has_more']==False:
                return 0
                
            self.get_newurl(str(hjson['cursor']))
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print ('connect error')
            self.retry+=1
            print(self.retry)
            self.get_content(new_url)
        except:
            self.retry+=1
            print(self.retry)
            self.get_content(new_url)
    def parse_content(self,content):
        for data in content['data']:
            if self.need_file=='Y':
                with open('%s.txt'%self.follow_type,'a+') as f:
                    f.write("%s-%s\n"%(data['user_id'],data['media_id']))
            else:
                self.uid_list.append(str(data['user_id'])+'-'+str(data['media_id']))
        print("done")
    def startjobs(self):
        self.get_newurl()
        return(self.uid_list)
    
if __name__ == "__main__":
    start_time = time.time()
    
   # uid="63955695731"   
    uid="103509373298"
    caps = DesiredCapabilities.FIREFOX
    #caps['loggingPrefs'] = {'browser': 'ALL'}
    fireFoxOptions = webdriver.FirefoxOptions()
    profile = webdriver.FirefoxProfile()
    fireFoxOptions.add_argument("--headless")
    fireFoxOptions.add_argument("--disable-gpu")
  #  user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
    profile.set_preference("general.useragent.override",user_agent)
    profile.set_preference('network.proxy.type', 1)
  #  profile.set_preference('network.proxy.http','118.190.95.35')
   # profile.set_preference('network.proxy.http_port',9001)
    ip ="119.251.244.131:8080"
    print(ip.split(':')[0])
    profile.set_preference('network.proxy.http',ip.split(':')[0])
    profile.set_preference('network.proxy.http_port',int(ip.split(':')[1]))
    profile.set_preference('network.proxy.ssl', '157.65.28.91')
    profile.set_preference('network.proxy.ssl_port',3128)
    profile.update_preferences()
    driver = webdriver.Firefox(capabilities=caps,firefox_profile=profile,firefox_options=fireFoxOptions)
    driver.get('https://httpbin.org/get?show_env=1')
    print(driver.page_source)
   # driver.get("http://httpbin.org/ip")
  #  print(driver.page_source)
   # driver.get("http://httpbin.org/ip")
  #  driver.get("http://icanhazip.com/")
   # print(driver.page_source)
   # print(self.driver.page_source)
    a = scrap_uid(uid,driver,'following','Y')
    a.startjobs()