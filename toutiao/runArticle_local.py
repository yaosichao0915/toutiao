import StartArticle
import pymysql
import time
from sshtunnel import SSHTunnelForwarder
def mysqldb():
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
        
def startjob(target_rounds):
            starttime=time.time()
            sql = "select uid,mid from following where crawled=0 and mid!=0 order by rand() limit %s;"%(target_rounds)
            server,connection=mysqldb()
            cursor = connection.cursor()
            cursor.execute(sql)
            row1 = cursor.fetchall()
            i = 2
            for row in row1:
                uid = row['uid']
                media_id = row['mid']
                a = StartArticle.article(uid,media_id,server,connection)
                a.get_newurl()
              #  sql2 = "update following set crawled=crawled+1 where uid='%s';"%(uid)
              #  cursor.execute(sql2)
             #   connection.commit()
                print("wait No%s people 5s"%i)
                i+=1
                time.sleep(1)
            connection.close()
            server.stop()
            print("runtime %s"%(time.time()-starttime))
startjob(100)