import pymysql.cursors
def readdata():
    
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='65138170',
                                 db='toutiao',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
    
def get_list(follow_type):
        list = []
        ip_list = []
        with open("%s.txt"%follow_type, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                list.append(line.strip())
            return(list)
connection = readdata()
list=get_list('followed')
cursor = connection.cursor()
for i in list:  
    sql = "REPLACE INTO followed (uid,mid) values(%s,%s)"%(i.split('-')[0],i.split('-')[1])
    cursor.execute(sql)
connection.commit()
connection.close()
