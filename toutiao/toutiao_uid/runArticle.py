import StartArticle
import pymysql
import time
def mysqldb():
        connection = pymysql.connect(host='localhost',
                                     user='yaosichao',
                                     password='yao65138170',
                                     db='tgene',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
        
def startjob(target_rounds):
            sql = "select uid,mid from following where crawled=0 and mid!=0 order by rand() limit %s;"%(target_rounds)
            connection=mysqldb()
            cursor = connection.cursor()
            cursor.execute(sql)
            row1 = cursor.fetchall()
            i = 2
            for row in row1:
                uid = row['uid']
                media_id = row['mid']
                a = StartArticle.article(uid,media_id)
                a.get_newurl()
              #  sql2 = "update following set crawled=crawled+1 where uid='%s';"%(uid)
              #  cursor.execute(sql2)
             #   connection.commit()
                print("wait No%s people 5s"%i)
                i+=1
                time.sleep(5)
            connection.close()
startjob(6000)