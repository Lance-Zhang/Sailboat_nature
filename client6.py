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
pid.SetPoint = 60
print('conected')

#大角度开电机
def motor(heading,setting,C_LM,C_RM):
    deltaangle = heading-setting
    if deltaangle>180:
        deltaangle = deltaangle -360
    elif deltaangle<-180:
        deltaangle = deltaangle +360

    if deltaangle>60:
        if C_RM != 1560:
            C_RM = 1560#right
            C_LM = 1500
    elif deltaangle<-60:
        if C_LM != 1560:
            C_LM = 1560#left
            C_RM = 1500
    else:
        C_LM = 1500
        C_RM = 1500
    return C_LM, C_RM

def pidrudder(pidoutput,C_R):
    pidoutput=round(pidoutput,2)
    if pidoutput>0:
        if pidoutput<6:
            C_R_aim=62-6.6*pidoutput
            if abs(C_R_aim-C_R)>=1:
                C_R=62-6.6*pidoutput
        else:
            pidoutput=6
            C_R_aim=62-6.6*pidoutput
            if abs(C_R_aim-C_R)>=1:
                C_R=62-6.6*pidoutput
    elif pidoutput<0:
        if pidoutput>-6:
            C_R_aim=62-6.6*pidoutput
            if abs(C_R_aim-C_R)>=1:
                C_R=62-6.6*pidoutput
        else:
            pidoutput=-6
            C_R_aim=62-6.6*pidoutput
            if abs(C_R_aim-C_R)>=1:
                C_R=62-6.6*pidoutput
    return int(C_R)

def tailwind(x_now,x_left,heading,setting,C_LM,C_RM,pidoutput,C_R):
    if x_now < x_left and setting == -120:
        setting = 120
        print('Backward 2')
    C_S = 60
    C_R = pidrudder(pidoutput,C_R)
    C_LM, C_RM = motor(heading,setting,C_LM,C_RM)
    return setting, C_S, C_R, C_LM, C_RM

def tacking(heading,setting,x_now,x_init,x_right):
    changingangle=10
    C_LM=1500
    C_RM=1500
    C_R=62
    #rudder & close motor(by angle) 
    if setting==60:
        if heading>=changingangle:#condition to change rudder
            C_R=102
            C_LM=1500
            C_RM=1500
            print('正常右tacking')
        elif heading<changingangle:
            C_R=22
            print('刚刚右tacking')
    elif setting==-60:
        if heading<=-changingangle:
            C_R=22
            C_LM=1500
            C_RM=1500
            print('正常左tacking')
        else:
            C_R=102
            print('刚刚左tacking')

    #open motor (by location)
    if x_now>=x_right:
        setting=-60
        C_RM=1560
    elif x_now <= x_init:
        setting=60
        C_LM=1560
    C_S=80
    print('heading'+str(heading))
    return setting, C_S, C_R, C_LM, C_RM

def selfsail(x_now,y_now,x_init,x_right,x_left,y_down,y_up,heading,setting,C_LM,C_RM,C_R,pidoutput,sailmode):
    # 逆风折线
    #sailmode = 1 # tacking mode
    if y_now > y_up and sailmode == 1:
        sailmode = 0
        setting=-120
        print('Backward 1')
    elif y_now < y_down and sailmode == 0:
        sailmode = 1
        setting = 60

    if sailmode == 1:
        setting, C_S, C_R, C_LM, C_RM = tacking(heading,setting,x_now,x_init,x_right)
    elif sailmode ==0:
        setting, C_S, C_R, C_LM, C_RM = tailwind(x_now,x_left,heading,setting,C_LM,C_RM,pidoutput,C_R)

    return setting, C_S, C_R, C_LM, C_RM, sailmode
    
while True:
    Mode = input('選擇模式>>: ')
    send_data = str(Mode)
    s.send(bytes(str(send_data),encoding='utf8'))
    print('Mode:',Mode)
    if Mode == 'Mode1':
        x_init = int(input('x_initial>>:'))
        y_down = int(input('y_initial>>:'))
        x_right = x_init + 230
        x_left = x_init - 460
        y_up = y_down + 600
        #print(x_init,x_r,x_l,y_init,y_u)
        C_LM = 1500 # Left Moter
        C_RM = 1500 # Right Moter
        C_R = 62 # Rudder
        C_S = 80 # Sail
        Initialization = 1
        sailmode = 1
        try:
            while True:
                # 设定方向
                cursor = db.cursor()
                cursor.execute("SELECT * FROM data WHERE id=1")
                data = cursor.fetchone()
                x = int(data[5])#实时获取船x坐标
                y = int(data[4])#实时获取船y坐标
                print('location: x'+str(x)+' y'+str(y))

                if Initialization == 1:
                    Initialization = 0
                else:
                    pid.SetPoint, C_S, C_R, C_LM, C_RM, sailmode = selfsail(x,y,x_init,x_right,x_left,y_down,y_up,feedback,pid.SetPoint,C_LM,C_RM,C_R,pid.output,sailmode)

                # 发送消息
                send_data = str(C_LM)+' '+str(C_RM)+' '+str(C_R)+' '+str(C_S)
                s.send(bytes(str(send_data),encoding='utf8'))
                print('Command:',str(send_data))
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

