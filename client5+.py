# socket client
from PID import PID
import socket
import time
import pymysql
db = pymysql.connect("192.168.0.105","root","root","star")

cursor = db.cursor()
cursor.execute("SELECT * FROM data WHERE id=1")
data = cursor.fetchone()
#
ip_port=('192.168.31.63',7786)

# 封装协议（对象）
s = socket.socket()

# 向服务端建立连接
s.connect(ip_port)

##x_int = data[5]#实时获取船x坐标
##y_int = data[4]#实时获取船y坐标
##x_ter = x_ini - 400
##y_ter = y_ini + 600
##print(x_int,y_int,x_ter,y_ter)


pid = PID(0.2,0.1,0)
pid.SetPoint = 40
print('conected')

def selfsail(x_now,y_now,x_initial,x_right,x_left,y_down,y_up,SetPoint):
    # 逆风折线
    if (x_now >= x_right) and int(SetPoint) == 40:
        SetPoint = -40
        print('逆风折线 -40°')
    elif (x_now <= x_initial) and SetPoint == -40:
        SetPoint = 40
        print('逆风折线 +40°')
    
    if y_now > y_up and (SetPoint == 40 or SetPoint == -40):
        SetPoint = -120
        print('顺风第一段 -120°')
    if x_now < x_left and SetPoint == -120:
        SetPoint = 120
        print('顺风第二段 +120°')
    if y_now < y_down and SetPoint == 120:
        SetPoint = 40
        print('重新开始逆风折线 +40°')
    return SetPoint
    
while True:
    Mode = input('選擇模式>>: ')
    send_data = str(Mode)
    s.send(bytes(str(send_data),encoding='utf8'))
    print('Mode:',Mode)
    if Mode == 'Mode1':
        x_int = int(input('x_initial>>:'))
        y_int = int(input('y_initial>>:'))
        x_r = x_int + 230
        x_l = x_int - 460
        y_u = y_int + 600
        print(x_int,x_r,x_l,y_int,y_u)
        try:
            while True:
                # 设定方向
                cursor = db.cursor()
                cursor.execute("SELECT * FROM data WHERE id=1")
                data = cursor.fetchone()
                x = int(data[5])#实时获取船x坐标
                y = int(data[4])#实时获取船y坐标
                print('location: x'+str(x)+' y'+str(y))
                pid.SetPoint = selfsail(x,y,x_int,x_r,x_l,y_int,y_u,pid.SetPoint)
                # 发送消息
                send_data = str(round(pid.output,4))+' '+str(pid.SetPoint)
                s.send(bytes(str(send_data),encoding='utf8'))
                print('PID.output:',str(send_data))
                #if send_data == 'exit': break  # 如果输入exit，则退出
                
                # 接收消息
                recv_data = s.recv(1024) #接受船角度信息
                feedback = float(str(recv_data,encoding='utf8'))
                pid.update(feedback)
                print('IMU angle:',feedback)
        except KeyboardInterrupt:
            time.sleep(0.5)

    elif Mode == 'Mode2':
        try:
            while True:
                # 设定方向
                data = input('Cammand>>: ').strip()
                # 发送消息
                send_data = str(data)
                s.send(bytes(str(send_data),encoding='utf8'))
        except KeyboardInterrupt:
            time.sleep(0.5)
    
# 结束连接
s.close()

