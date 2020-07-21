import time
import random
from firefox import scrap_uid
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pymysql.cursors
#following 关注 
#followed 粉丝
class grabNewList(object):
    def __init__(self):
        self.connection=self.mysqldb()
        caps = DesiredCapabilities.FIREFOX
        fireFoxOptions = webdriver.FirefoxOptions()
        profile = webdriver.FirefoxProfile()
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        profile.set_preference("general.useragent.override",user_agent)
        profile.set_preference('network.proxy.type', 1)      
        ip=self.get_random_ip()
       # ip ="118.190.95.35:9001"
        print(ip)
    #    profile.set_preference('network.proxy.http',ip.split(':')[0])
    #    profile.set_preference('network.proxy.http_port',int(ip.split(':')[1]))
    #    profile.set_preference('network.proxy.ssl',ip.split(':')[0])
    #    profile.set_preference('network.proxy.ssl_port',int(ip.split(':')[1]))
        profile.update_preferences()
        fireFoxOptions.add_argument("--headless")
        fireFoxOptions.add_argument("--disable-gpu")
        self.driver = webdriver.Firefox(capabilities=caps,firefox_profile=profile,firefox_options=fireFoxOptions)
        self.driver.set_page_load_timeout(10)
        self.driver.set_script_timeout(10)
        try:
            self.driver.get("https://www.toutiao.com/c/user/relation/63955695731/?tab=following#mid=1607589748621315")
           # self.driver.get("https://www.toutiao.com/c/user/following/?user_id=50241899175&cursor=0&count=400&_signature=VPzS9RAdD3uIxdD2CqN.21T80u")
            #d = self.driver.page_source
            #print(d)
        except:
            self.driver.quit()
            exit("proxy error")
        
    def get_random_ip(self):
        proxy_list = []
        file='./Proxy-IP.txt'
        with open(file, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                proxy_list.append(line.strip())
        return(random.choice(proxy_list)) 
            
    def firefox(self):
        caps = DesiredCapabilities.FIREFOX
        fireFoxOptions = webdriver.FirefoxOptions()
        profile = webdriver.FirefoxProfile()
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        profile.set_preference("general.useragent.override",user_agent)
        profile.set_preference('network.proxy.type', 1)
        ip = self.get_random_ip()
        profile.set_preference('network.proxy.http',ip.split(':')[0])
        profile.set_preference('network.proxy.http_port',ip.split(':')[1])
        profile.set_preference('network.proxy.ssl',ip.split(':')[0])
        profile.set_preference('network.proxy.ssl_port',ip.split(':')[1])
        profile.update_preferences()
        fireFoxOptions.add_argument("--headless")
        fireFoxOptions.add_argument("--disable-gpu")
        driver = webdriver.Firefox(capabilities=caps,firefox_profile=profile,firefox_options=fireFoxOptions)
       # driver.delete_all_cookies()
       # driver.add_cookie({'__tasessionId': '0m2brheyo1535558497801','tt_webid': '6593313127348454926'})
        return driver
        
        
    def mysqldb(self):
        connection = pymysql.connect(host='localhost',
                                     user='yaosichao',
                                     password='yao65138170',
                                     db='tgene',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
        
    def get_list(self,follow_type,target_rounds):
        uid_list=[]
        sql = "select * from %s where visited=0 order by rand() limit %s;"%(follow_type,target_rounds)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        row1 = cursor.fetchall()
        for row in row1:
            uid_list.append(row['uid'])
        return(uid_list)

    def appendin(self,query_id,uid_list,follow_type,file_type):
        for uid in uid_list:
           # sql = "REPLACE INTO %s (uid,mid) values(%s,%s);"%(follow_type,uid.split('-')[0],uid.split('-')[1])
            sql="INSERT INTO %s (uid,mid) values(%s,%s) ON DUPLICATE KEY UPDATE mid=%s"%(follow_type,uid.split('-')[0],uid.split('-')[1],uid.split('-')[1])
            self.connection.cursor().execute(sql)
        sql = "update %s set visited=visited+1 where uid='%s';"%(file_type,query_id)
        self.connection.cursor().execute(sql)
        self.connection.commit()            
        
    def start(self,follow_type,target_rounds):
        rounds=0
        if follow_type=='following':
            file_type='followed'
        else: file_type='following'
        target = self.get_list(file_type,target_rounds)
        
        for uid in target:
            time.sleep(1)
            print(uid)
            a=scrap_uid(uid,self.driver,follow_type)
            uid_list = a.startjobs()
            print('find %s '%(len(uid_list)))
            if len(uid_list)>0:
                self.appendin(uid,uid_list,follow_type,file_type)
            rounds+=1
            print ('finished %s set'%rounds)
          #  driver.quit()

    def closeconnection(self):
        self.connection.close()
        self.driver.quit()

if __name__ == "__main__":
    start_time = time.time()
    a = grabNewList()
    a.start('followed',50)
    a.start('following',300)
    a.closeconnection()
    print("finished time %s seconds"%(time.time()-start_time))
    
