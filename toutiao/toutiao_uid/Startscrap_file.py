import time
import random
from firefox import scrap_uid
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#following 关注 
#followed 粉丝
class grabNewList(object):
    def __init__(self):
        self.ToFollowed = self.get_list('followed')
        self.ToFollowing = self.get_list('following')
        caps = DesiredCapabilities.FIREFOX
        caps['loggingPrefs'] = {'browser': 'ALL'}
        fireFoxOptions = webdriver.FirefoxOptions()
        profile = webdriver.FirefoxProfile()
        #fireFoxOptions.add_argument("--headless")
        #fireFoxOptions.add_argument("--disable-gpu")
        self.driver = webdriver.Firefox(capabilities=caps,firefox_profile=profile,firefox_options=fireFoxOptions)
    
    def get_list(self,follow_type):
        list = []
        ip_list = []
        with open("%s.txt"%follow_type, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                list.append(line.strip())
            return(list)

    def appendin(self,uid_list,follow_type):
        file = self.get_list(follow_type)
        for uid in uid_list:
            if uid not in file:
                with open('%s.txt'%follow_type,'a+') as f:
                    f.write("%s\n"%(uid))
                    
    def start(self,follow_type,target_rounds):
        rounds=0
        if follow_type=='following':
            file_type='followed'
        else: file_type='following'
        file = self.get_list(file_type)
        target = random.sample(file,target_rounds)
        
        for uid in target:
            print(uid)
            a=scrap_uid(uid.split('-')[0],self.driver,follow_type)
            uid_list = a.startjobs()
            print('find %s '%(len(uid_list)))
            self.appendin(uid_list,follow_type)
            rounds+=1
            print ('finished %s set'%rounds)
                

if __name__ == "__main__":
    start_time = time.time()
    a = grabNewList()
    #a.start('followed',10)
    a.start('following',1000)
    
    
