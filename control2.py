import logging
import sys
import time
import numpy as np
import xlwt
import datetime
#import matplotlib.pyplot as plt
from Adafruit_BNO055 import BNO055
#ina219
from ina219 import INA219, DeviceRangeError
from time import sleep
#
from boatclass import sailboat
import RPi.GPIO as GPIO
import pigpio
import os
newboat = sailboat(21,20,1500,1500,16,26,100,60)
#newboat.initialization
#
# 依照上socket流程图，实现一个功能，客户端输入什么，就把输入的转为大写

# soceet server

import socket
ip_port=('192.168.31.63',7786)

# 封装协议（对象)
s = socket.socket()

# 绑定ip，端口
s.bind(ip_port)

# 启动监听
s.listen(5)  # 挂起连接数，  允许最多处理5个请求
#

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 3.19
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)
#

wb= xlwt.Workbook()
ws=wb.add_sheet('Test')
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
#write head of the table
ws.write(0,0,'heading');ws.write(0,1,'roll');ws.write(0,2,'pitch');ws.write(0,3,'Bus Voltage');ws.write(0,4,'Bus Current');ws.write(0,5,'Power');ws.write(0,6,'Shunt Voltage');ws.write(0,7,'Time-hour');ws.write(0,8,'Time-minute');ws.write(0,9,'Time-second');
i=1
while True:
    # 等待连接
    print('waiting')
    conn, addr = s.accept()  # accept方法等待客户端连接，直到有客户端连接后，会返回连接线（conn）、连接地址（addr）
    try:
        while True:
            # Read the Euler angles for heading, roll, pitch (all in degrees).
            heading, roll, pitch= bno.read_euler()
            if i == 1:
                original_heading = heading
                print(original_heading)
            heading=heading-original_heading  # IMU的角度-初始值
            if heading>180:
                heading = heading - 360
            elif heading<-180:
                heading = heading + 360
##            try:
            # 接收消息
            recv_data=conn.recv(1024)  # 接收conn连接线路，并指定缓存该线路的1024
            recv_data=float(str(recv_data,encoding='utf8'))
            print('接收消息类型：%s' % recv_data)
            if recv_data>0:
                newboat.motorruning(21,min(1560,1549+recv_data))
            elif recv_data<0:
                newboat.motorruning(20,min(1560,1549-recv_data))
            print(newboat.getspeed())
            # 发送消息
            send_data=heading
            print("发送消息内容：%s" % send_data)
            conn.send(bytes(str(send_data),encoding='utf8'))  # 使用conn线路，发送消息
##            except Exception:  # 如果客户端主动断开，则server退出该循环等待下一条连接
##                time.sleep(1)
##                wb.save('2example34.xls')
##                break
            # Print everything out.
            ws.write(i,0,'{0:0.2F}'.format(heading))
            ws.write(i,1,'{0:0.2F}'.format(recv_data))
            ws.write(i,2,'{0:0.2F}'.format(1550+abs(recv_data)))
            ws.write(i,3,'{0:0.2f}V'.format(ina.voltage()))
            ws.write(i,4,'{0:0.2f}mA'.format(ina.current()))
            ws.write(i,5,'{0:0.2f}mW'.format(ina.power()))
            ws.write(i,6,'{0:0.2f}mV'.format(ina.shunt_voltage()))
            t=datetime.datetime.now()
            ws.write(i,7,str(t.hour))
            ws.write(i,8,str(t.minute))
            ws.write(i,9,str(t.second))
            i+=1
            newTime = time.clock()
            stime = np.append(stime,newTime)
            sHeading = np.append(sHeading,heading)
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        #plt.plot(stime,sHeading,'ro')
        #print('Plotting Graph...')
        time.sleep(1)
        wb.save('2example34.xls')
        #plt.show()
        # 结束进程
        conn.close() # 中断线路
