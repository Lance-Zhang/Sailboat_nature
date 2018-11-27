# boatclass
from boatclass import sailboat
##import RPi.GPIO as GPIO
##import pigpio
##import os
# soceet server
import socket
#ina219
from ina219 import INA219, DeviceRangeError
from time import sleep
# IMU
import logging
import sys
import time
import numpy as np
import xlwt
import datetime
# import matplotlib.pyplot as plt
from Adafruit_BNO055 import BNO055

#creat an object newboat
newboat = sailboat(21,20,1500,1500,16,26,80,62)
newboat.initialization()
last_angle=62

# 依照上socket流程图，实现一个功能，客户端输入什么，就把输入的转为大写
# soceet server
ip_port=('192.168.31.63',7786)
# 封装协议（对象)
s = socket.socket()
# 绑定ip，端口
s.bind(ip_port)
# 启动监听
s.listen(5)  # 挂起连接数，  允许最多处理5个请求

# ina219
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 3.19
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

# IMU

# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
##print('Software version:   {0}'.format(sw))
##print('Bootloader version: {0}'.format(bl))
##print('Accelerometer ID:   0x{0:02X}'.format(accel))
##print('Magnetometer ID:    0x{0:02X}'.format(mag))
##print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
##
##print('Reading BNO055 data, press Ctrl-C to quit...')
stime = np.array([])
sHeading = np.array([])

original_heading=0
while True:
    # 等待连接
    print('waiting')
    conn, addr = s.accept()  # accept方法等待客户端连接，直到有客户端连接后，会返回连接线（conn）、连接地址（addr）
    #Select Mode
    try:
        while True:
            recv_data=conn.recv(1024)  # 接收conn连接线路，并指定缓存该线路的1024
            recv_data=(str(recv_data,encoding='utf8').split(' '))
            Mode=recv_data[0]
            print(Mode)
            time.sleep(0.5)
            if Mode == 'Mode0':
                
                heading, roll, pitch= bno.read_euler()
                print(heading,roll,pitch)
                #time.sleep(0.5)

            elif Mode == 'Mode1':
                print('Auto')
                #
                newboat.motorruning(20,1500)
                newboat.motorruning(21,1500)
                newboat.servoturning(16,80)
                newboat.servoturning(26,62)
                #
                wb= xlwt.Workbook()
                ws=wb.add_sheet('Test')
                #write head of the table
                ws.write(0,0,'heading');ws.write(0,1,'roll');ws.write(0,2,'pitch');ws.write(0,3,'Bus Voltage');ws.write(0,4,'Bus Current');ws.write(0,5,'Power');ws.write(0,6,'Shunt Voltage');ws.write(0,7,'Time-hour');ws.write(0,8,'Time-minute');ws.write(0,9,'Time-second');
                i=1
                try:
                    while True:
                        # Read the Euler angles for heading, roll, pitch (all in degrees).
                        heading, roll, pitch= bno.read_euler()
                        real_heading=heading
                        if heading != 0 and i <= 2:
                            original_heading = heading
                            print(original_heading)
                        #heading from 0 to 180, -180 to 0
                        heading=heading-original_heading  # IMU的角度-初始值
                        if heading>180:
                            heading = heading - 360
                        elif heading<-180:
                            heading = heading + 360

                        ##            try:
                        # 接收消息
                        pidoutput=float(recv_data[1])
                        print('Pid Output：%s' % pidoutput)
                        pidSetPoint=recv_data[2]
                        pidSetPoint=float(pidSetPoint)
                        
                        #大角度开电机
                        deltaangle = heading-pidSetPoint
                        if deltaangle>180:
                            deltaangle = deltaangle -360
                        elif deltaangle<-180:
                            deltaangle = deltaangle +360

                        if deltaangle>20:
                            if newboat.getspeed()[1] != 1550:
                                newboat.motorruning(20,1560)#right
                                newboat.motorruning(21,1500)
                        elif deltaangle<-20:
                            if newboat.getspeed()[0] != 1550:
                                newboat.motorruning(21,1560)#left
                                newboat.motorruning(20,1500)
                        else:
                            newboat.motorruning(20,1500)
                            newboat.motorruning(21,1500)
                        
                        #转舵
                        if pidoutput>0:
                            if pidoutput<12:
                                angle=round(pidoutput)
                                if abs(angle-last_angle)>=1:
                                    newboat.servoturning(26,62-3.3*angle)
                                    last_angle=angle
                            else:
                                angle=12
                                if abs(angle-last_angle)>=1:
                                    newboat.servoturning(26,62-3.3*angle)
                                    last_angle=angle
                        elif pidoutput<0:
                            if pidoutput>-12:
                                angle=round(pidoutput)
                                if abs(angle-last_angle)>=1:
                                    newboat.servoturning(26,62-3.3*angle)
                                    last_angle=angle
                            else:
                                angle=-12
                                if abs(angle-last_angle)>=1:
                                    newboat.servoturning(26,62-3.3*angle)
                                    last_angle=angle
                                    
                        # 发送消息
                        send_data=heading
                        print("IMU angle：%s" % send_data)
                        print('Angles:',newboat.getangle())
                        conn.send(bytes(str(send_data),encoding='utf8'))  # 使用conn线路，发送消息
            ##            except Exception:  # 如果客户端主动断开，则server退出该循环等待下一条连接
            ##                time.sleep(1)
            ##                wb.save('2example34.xls')
            ##                break
                        # Print everything out.
                        ws.write(i,0,'{0:0.2F}'.format(heading))
                        ws.write(i,1,'{0:0.2F}'.format(real_heading))
                        ws.write(i,2,'{0:0.2F}'.format(62-2*pidoutput))
                        ws.write(i,3,'{0:0.2f}V'.format(ina.voltage()))
                        ws.write(i,4,'{0:0.2f}mA'.format(ina.current()))
                        ws.write(i,5,'{0:0.2f}mW'.format(ina.power()))
                        ws.write(i,6,'{0:0.2f}mV'.format(ina.shunt_voltage()))
                        t=datetime.datetime.now()
                        ws.write(i,7,str(t.hour))
                        ws.write(i,8,str(t.minute))
                        ws.write(i,9,str(t.second))
                        print('(Voltage, Current): (',round(ina.voltage(),3),',', round(ina.current(),3),')')
                        i+=1
                        newTime = time.clock()
                        stime = np.append(stime,newTime)
                        sHeading = np.append(sHeading,heading)
                        time.sleep(0.5)
                
                except KeyboardInterrupt:
                    #plt.plot(stime,sHeading,'ro')
                    #print('Plotting Graph...')
                    time.sleep(1)
                    print('Saving data...')
                    wb.save('%s .xls' % t)
                    #plt.show()
                    # 结束进程
                    newboat.motorruning(20,1500)
                    newboat.motorruning(21,1500)
                    newboat.servoturning(16,80)
                    newboat.servoturning(26,62)
                    
            elif Mode == 'Mode2':
                print('Manual')
                while True:
                    Cammand=recv_data[1]
                    if len(Cammand)==1:
                        speed1=1500
                        speed2=1500
                        if Cammand=='a':
                            speed1=1560
                            speed2=1560
                            print('run')
                        elif Cammand=='s':
                            speed1+=2
                        elif Cammand=='x':
                            speed1-=2
                        elif Cammand=='d':
                            speed2+=2
                        elif Cammand=='c':
                            speed2-=2
                        elif Cammand=='w':
                            speed1=1560
                        elif Cammand=='e':
                            speed2=1560
                        else:
                            speed1=1500
                            speed2=1500
                        time.sleep(0.02)
                        newboat.motorruning(21,speed1)
                        newboat.motorruning(20,speed2)
                        print('MoterSpeed1'+str(speed1))
                        print('MoterSpeed2'+str(speed2))
                    else:
                        sailangle=70
                        rudderangle=62
                        if Cammand[0]=='s':
                            sailangle=float(Cammand[1:])
                            newboat.servoturning(16,sailangle)
                        elif Cammand[0]=='r':
                            rudderangle=float(Cammand[1:])
                            newboat.servoturning(26,rudderangle)          
                        print('sail'+str(sailangle))
                        print('rudder'+str(rudderangle))
       
    except KeyboardInterrupt:
        #plt.plot(stime,sHeading,'ro')
        #print('Plotting Graph...')
        time.sleep(1)
        #wb.save('%s .xls' % t)
        #plt.show()
        # 结束进程
        newboat.motorruning(20,1500)
        newboat.motorruning(21,1500)
        conn.close() # 中断线路
