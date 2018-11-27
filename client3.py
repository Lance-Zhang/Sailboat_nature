# socket client
from PID import PID
import socket
import time
ip_port=('192.168.31.63',7786)

# 封装协议（对象）
s = socket.socket()

# 向服务端建立连接
s.connect(ip_port)

pid = PID(0.2,0.1,0)

print('conected')

while True:
    # 设定方向
    pid.SetPoint = float(input('目標角度>>: ').strip())
    try:
        while True:
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
    
# 结束连接
s.close()
