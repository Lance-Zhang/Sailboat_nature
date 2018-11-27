import pymysql
import time

db = pymysql.connect("192.168.0.105","root","root","star")
cursor = db.cursor()
cursor.execute("SELECT * FROM data WHERE id=1")
    
while True:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data WHERE id=1")
    data = cursor.fetchone()
    x = int(data[5])#实时获取船x坐标
    y = int(data[4])#实时获取船y坐标
    print(data)
    time.sleep(0.5)

db.close()
