import requests
import pymysql
import get_as_cp
import time
from sshtunnel import SSHTunnelForwarder
class article(object):
    def __init__(self,uid,media_id,server,connection):
        #self.server,self.connection=self.mysqldb() 
        self.server,self.connection=server,connection        
        self.uid = uid
        self.media_id =media_id
        self.behot_time=0
        self.retry = 0
        self.rounds = 0
        self.count = 0
       # self.mark_time = time.time()
       # self.file = './Proxy-IP.txt' 
       # self.proxy_list = self.get_iplist()
    def mysqldb(self):
        server = SSHTunnelForwarder(
        ssh_address_or_host=('116.228.207.126', 26),  # 指定ssh登录的跳转机的address
        ssh_username='yaosichao',  # 跳转机的用户
        ssh_password='yao65138170',  # 跳转机的密码
        remote_bind_address=('127.0.0.1', 3306))
        server.start()
        connection = pymysql.connect(host='127.0.0.1',
                                     user='yaosichao',
                                     password='yao65138170',
                                     db='tgene',
                                     port=server.local_bind_port,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return (server,connection)

    def get_newurl(self):
        as_cp = get_as_cp.get_as_cp()
        next_url = 'https://www.toutiao.com/pgc/ma/?page_type=1&max_behot_time=%s&uid=%s&media_id=%s&output=json&is_json=1&count=400&from=user_profile_app&version=2&as=%s&cp=%s'%(self.behot_time,self.uid,self.media_id,as_cp['as'],as_cp['cp'])
        print(next_url)
        r = self.get_content(next_url)
        if r == 0:
            sql = "update following set crawled=%s where uid='%s';"%(self.count*20,self.uid)
            self.connection.cursor().execute(sql)
         #   self.connection.close()
         #   self.server.stop()
            print ("people crawled success")
        if r == 1:
            #self.connection.close()
            #self.server.stop()
            print ("people crawled error")
        
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
        }
       # proxies = self.get_random_ip()
           # print(proxies)
        #proxies={'http': 'http://61.135.217.7:80'}
        
        try:
           # r = requests.get(new_url,headers=headers,proxies=proxies,timeout=2)
            r = requests.get(new_url,headers=headers,timeout=10)
                #ip = requests.get('http://httpbin.org/ip',headers=headers,proxies=proxies,timeout=2)
            res = r.json()
          #  print(res['data'])
            self.behot_time=res['next']['max_behot_time']
            r = self.parse(res)            
            if r == 0 :
                print('parse scuess')
            else:
                print('parse error!!!')
                return 1
            self.count+=1
            if res['has_more']==0:
                return 0
            print ("finished %s"%self.count)
            
            if self.count > 100:
                print('out')
                return 0
            print ("wait 5 s")
            time.sleep(0.5)            
            new_url = self.get_newurl()
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print ('connect error!!!')
        except Exception as e:
            print (e)
            return 1
            
      #      self.retry+=1
      #      print("重试%s"%self.retry)
      #      self.get_content(new_url)
           
    def parse(self,content):  
        if content['data'] == [] and self.behot_time==0:
            return 1
        for article in content['data']:
            label=[]
            if 'has_video' not in article:
                continue
            if article['has_video']==False:
                if 'total_read_count' not in article:
                    continue
                else:
                    count = article['total_read_count']
            else:
                count = article['detail_play_effective_count']
            if count<10000:
                    continue
            uid=self.uid
            item_id=article['item_id']
            title=article['title']
            impression_count=article['impression_count']
            total_read_count=count
            datetime=article['datetime'].split(' ')[0]
            label='-'.join(article['label'])
            keywords=article['keywords'].replace(',',"-")
            tag=article['tag']
            content_cntw=article['content_cntw']
            repin_count=article['repin_count']
            share_count=article['share_count']
            comment_count=article['comment_count']
            print(uid,item_id,title,impression_count,total_read_count,datetime)
            sql = "REPLACE INTO article (uid,item_id,title,impression_count,total_read_count,datetime,label,keywords,tag,content_cntw,repin_count,share_count,comment_count) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(uid,item_id, pymysql.escape_string(title),impression_count,total_read_count,datetime, pymysql.escape_string(label), pymysql.escape_string(keywords), pymysql.escape_string(tag),content_cntw,repin_count,share_count,comment_count)
          #  print(sql)
            self.connection.cursor().execute(sql)
            self.connection.commit()
        return 0    
    def startjob(self,target_rounds):
            sql = "select uid,mid from following where crawled=0 and mid!=0 order by rand() limit %s;"%(target_rounds)
            cursor = self.connection.cursor()
            cursor.execute(sql)
            row1 = cursor.fetchall()
            for row in row1:
                self.rounds= 0 
                self.uid = row['uid']
                self.media_id = row['mid']
                self.get_newurl()
                sql2 = "update following set crawled=crawled+1 where uid='%s';"%(self.uid)
                cursor.execute(sql2)
            self.connection.commit()
            self.connection.close()

if __name__ == "__main__":
    uid = '67631291543'
    media_id='1577066607177742'
    a = article(uid,media_id)
    url='https://www.toutiao.com/pgc/ma/?page_type=1&max_behot_time=1533871476&uid=63955695731&media_id=1607589748621315&output=json&is_json=1&count=400&from=user_profile_app&version=2&as=A1F58BC866B7C4E&cp=5B86470C640E9E1'
    a.get_newurl()