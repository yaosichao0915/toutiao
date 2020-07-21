import requests
import pymysql
import get_as_cp
class article(object):
    def __init__(self):
        self.connection=self.mysqldb()
        self.uid = '63955695731'
        self.media_id='1607589748621315'
        self.behot_time=0
    def mysqldb(self):
        connection = pymysql.connect(host='localhost',
                                     user='yaosichao',
                                     password='yao65138170',
                                     db='tgene',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    def get_newurl(self):
        as_cp = get_as_cp.get_as_cp()
        next_url = 'https://www.toutiao.com/pgc/ma/?page_type=1&max_behot_time=%s&uid=%s&media_id=%s&output=json&is_json=1&count=400&from=user_profile_app&version=2&as=%s&cp=%s'%(self.behot_time,self.uid,self.media_id,as_cp['as'],as_cp['cp'])
        self.get_content(next_url)
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
        proxies={'http': 'http://61.135.217.7:80'}
        
        try:
            r = requests.get(new_url,headers=headers,proxies=proxies,timeout=2)
                #ip = requests.get('http://httpbin.org/ip',headers=headers,proxies=proxies,timeout=2)
            res = r.json()
           # print(res['data'])
            self.parse(res)
            if res['has_more']==0:
                return 0
            self.behot_time=res['next']['max_behot_time']
            new_url = self.get_newurl()
        except:
            pass
    def parse(self,content):
        for article in content['data']:
            label=[]
            if 'has_video' not in article:
                continue
            if article['has_video']==False:
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
            sql = "REPLACE INTO article (uid,item_id,title,impression_count,total_read_count,datetime,label,keywords,tag,content_cntw,repin_count,share_count,comment_count) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(uid,item_id,title,impression_count,total_read_count,datetime,label,keywords,tag,content_cntw,repin_count,share_count,comment_count)
          #  print(sql)
            self.connection.cursor().execute(sql)
            self.connection.commit()

if __name__ == "__main__":
    a = article()
    url='https://www.toutiao.com/pgc/ma/?page_type=1&max_behot_time=1533871476&uid=63955695731&media_id=1607589748621315&output=json&is_json=1&count=400&from=user_profile_app&version=2&as=A1F58BC866B7C4E&cp=5B86470C640E9E1'
    a.get_newurl()