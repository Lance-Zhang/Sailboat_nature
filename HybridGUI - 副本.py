from tkinter import *
import socket   
import time
import sys


class HybridSailBoat:

    def __init__(self):

        window = Tk()
        window.title('Hybrid Sail Boat')
        
        self.speedR = 1500
        self.speedL = 1500

        self.shift_tag = 0
        self.control_tag = 0

        # left part: keyboard
        self.canvas = Canvas(window, width = 245, height = 400, highlightthickness=0)
        self.canvas.pack()
        #self.canvas.grid()
        #self.canvas.flag=True
        #self.canvas.transparent=False
        #self.canvas.top= self.canvas.winfo_toplevel()
        self.canvas.grid(row = 0, column = 0)

        # Bind keys
        self.canvas.bind('<w>', self.dirF)
        self.canvas.bind('<a>', self.dirL)
        self.canvas.bind('<d>', self.dirR)
        self.canvas.bind('<s>', self.stop)
        self.canvas.bind('<W>', self.speedupF)
        self.canvas.bind('<A>', self.speedupL)
        self.canvas.bind('<D>', self.speedupR)
        self.canvas.bind('<S>', self.back)
        self.canvas.bind('<Control-w>', self.speeddownF)
        self.canvas.bind('<Control-a>', self.speeddownL)
        self.canvas.bind('<Control-d>', self.speeddownR)

        self.canvas.bind('<KeyRelease-w>', self.releaseW)
        self.canvas.bind('<KeyRelease-a>', self.releaseA)
        self.canvas.bind('<KeyRelease-s>', self.releaseS)
        self.canvas.bind('<KeyRelease-d>', self.releaseD)
        self.canvas.bind('<KeyRelease-W>', self.releaseShiftW)
        self.canvas.bind('<KeyRelease-A>', self.releaseShiftA)
        self.canvas.bind('<KeyRelease-D>', self.releaseShiftD)
        self.canvas.bind('<KeyRelease-S>', self.releaseShiftS)
        # self.canvas.bind('<KeyRelease-Control>', self.releaseControl)

        # w
        self.canvas.create_rectangle(ori_x,ori_y,ori_x+length,ori_y+length,fill="black",outline="grey",width=5)
        # s
        self.canvas.create_rectangle(ori_x,ori_y+length,ori_x+length,ori_y+length+length,fill="black",outline="grey",width=5)
        # a 
        self.canvas.create_rectangle(ori_x-length,ori_y+length,ori_x,ori_y+length+length,fill="black",outline="grey",width=5)
        # d
        self.canvas.create_rectangle(ori_x+length,ori_y+length,ori_x+length+length,ori_y+length+length,fill="black",outline="grey",width=5)
        # shift
        self.canvas.create_rectangle(10,180,150,230,fill="black",outline="grey",width=5)
        # control
        self.canvas.create_rectangle(10,240,150,290,fill="black",outline="grey",width=5)
        
        # w text
        self.canvas.create_text(ori_x+30,ori_y+30,text="W",fill="#66CCFF",font="Normal -25 bold", tags = 'w')
        # s text
        self.canvas.create_text(ori_x+30,ori_y+length+30,text="S",fill="#66CCFF",font="Normal -25 bold", tags = 's')
        # a text
        self.canvas.create_text(ori_x-30,ori_y+length+30,text="A",fill="#66CCFF",font="Normal -25 bold", tags = 'a')
        # d text
        self.canvas.create_text(ori_x+length+30,ori_y+length+30,text="D",fill="#66CCFF",font="Normal -25 bold", tags = 'd')
        # shift text
        self.canvas.create_text(80,205,text="Shift",fill="#66CCFF",font="Normal -25 bold", tags = 'shift')
        # control text
        self.canvas.create_text(80,265,text="Ctrl",fill="#66CCFF",font="Normal -25 bold", tags = 'control')

        self.canvas.focus_set()

        # right part: information
        frame = Frame(window, width = 240, height = 400)
        #frame.pack()
        frame.grid(row = 0, column = 1)

        # display speed
        frame1 = Frame(frame,width =100, height=50)
        frame1.pack()
        lb1 = Label(frame1,justify = "left", text = 'SpeedR: ')
        lb2 = Label(frame1,justify = "left", text = 'SpeedL: ')
        self.lbSpeedR = Label(frame1, fg = 'red',justify = "left",text = str(self.speedR))
        self.lbSpeedL = Label(frame1, fg = 'red',justify = "left", text = str(self.speedL))
        # lbSpeed1['text'] = str()

        # display rules
        frame2 = Frame(frame)
        frame2.pack()
        rule_title = Label(frame2, text = 'RULES:', fg = '#00008B', 
                        height = 3, font = 'Helvetica -18 bold')
        rules = Label(frame2, fg = 'blue', justify = "left", font = 'Normal -16',
            text = "\
                     w:  move forward \n \
                    a:  turn left \n \
                    d:  turn right \n \
                    s:  stop \n \
                    shift+w:  speed up forward \n \
                    shift+a:  speed up left \n \
                    shift+d:  speed up right \n \
                    shift+s:  move backward \n \
                    control+w:  speed down forward \n \
                    control+a:  speed down left \n \
                    control+d:  speed down right \n")
        # ''' rule_title.pack()
        # rules.pack() '''
        
        # frame1.grid(row = 1, column = 1)
        # frame2.grid(row = 2, column = 1)
        rule_title.grid(row = 1, column = 0)
        rules.grid(row = 2, column = 0)

        lb1.grid(row = 1, column = 1)
        lb2.grid(row = 2, column = 1)
        self.lbSpeedR.grid(row = 1, column = 2)
        self.lbSpeedL.grid(row = 2, column = 2)
       # data=socket_tcp.recv(1024)
        #print(data)
        window.mainloop()

    def dirF(self, event):
        inp=b'forward'
        socket_tcp.send(inp)

        self.canvas.delete('w')
        self.canvas.create_text(ori_x+30,ori_y+30,text="W",fill="#FF69B4",font="Normal -25 bold", tags = 'w')

        self.speedL = 1590
        self.speedR = 1560
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)
    
    def dirL(self, event):
        inp=b'left'
        socket_tcp.send(inp)

        self.canvas.delete('a')
        self.canvas.create_text(ori_x-30,ori_y+length+30,text="A",fill="#FF69B4",font="Normal -25 bold", tags = 'a')

        self.speedL = 1500
        self.speedR = 1590
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)
        
    def dirR(self, event):
        inp=b'right'
        socket_tcp.send(inp)

        self.canvas.delete('d')
        self.canvas.create_text(ori_x+length+30,ori_y+length+30,text="D",fill="#FF69B4",font="Normal -25 bold", tags = 'd')

        self.speedL = 1620
        self.speedR = 1500
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)
        
    def stop(self, event):
        inp = b'stop'
        socket_tcp.send(inp)

        self.canvas.delete('s')
        self.canvas.create_text(ori_x+30,ori_y+length+30,text="S",fill="#FF69B4",font="Normal -25 bold", tags = 's')

        self.speedL = 1500
        self.speedR = 1500
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)

    def back(self, event):
        inp = b'back'
        socket_tcp.send(inp)

        self.canvas.delete('s')
        self.canvas.delete('shift')
        self.canvas.create_text(ori_x+30,ori_y+length+30,text="S",fill="#FF69B4",font="Normal -25 bold", tags = 's')
        self.canvas.create_text(80,205,text="Shift",fill="#FF69B4",font="Normal -25 bold", tags = 'shift')
        self.shift_tag = 1

        self.speedL = 1380
        self.speedR = 1410
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)
        
    def speedupF(self, event):
        inp=b'speedupforward'
        socket_tcp.send(inp)

        self.canvas.delete('w')
        self.canvas.delete('shift')
        self.canvas.create_text(ori_x+30,ori_y+30,text="W",fill="#FF69B4",font="Normal -25 bold", tags = 'w')
        self.canvas.create_text(80,205,text="Shift",fill="#FF69B4",font="Normal -25 bold", tags = 'shift')
        self.shift_tag = 1

        self.speedL += 20
        self.speedR += 20
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)
        
    def speedupL(self, event):
        inp=b'speedupleft'
        socket_tcp.send(inp)

        self.canvas.delete('a')
        self.canvas.delete('shift')
        self.canvas.create_text(80,205,text="Shift",fill="#FF69B4",font="Normal -25 bold", tags = 'shift')
        self.canvas.create_text(ori_x-30,ori_y+length+30,text="A",fill="#FF69B4",font="Normal -25 bold", tags = 'a')
        self.shift_tag = 1

        self.speedR += 20
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)
        
    def speedupR(self, event):
        inp=b'speedupright'
        socket_tcp.send(inp)

        self.canvas.delete('d')
        self.canvas.delete('shift')
        self.canvas.create_text(80,205,text="Shift",fill="#FF69B4",font="Normal -25 bold", tags = 'shift')
        self.canvas.create_text(ori_x+length+30,ori_y+length+30,text="D",fill="#FF69B4",font="Normal -25 bold", tags = 'd')
        self.shift_tag = 1

        self.speedL += 20
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)
        
    def speeddownF(self, event):
        inp=b'speeddownforward'
        socket_tcp.send(inp)

        self.canvas.delete('w')
        self.canvas.delete('control')
        self.canvas.create_text(ori_x+30,ori_y+30,text="W",fill="#FF69B4",font="Normal -25 bold", tags = 'w')
        self.canvas.create_text(80,265,text="Ctrl",fill="#FF69B4",font="Normal -25 bold", tags = 'control')
        self.control_tag = 1

        self.speedL -= 20
        self.speedR -= 20
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)
        
    def speeddownL(self, event):
        inp=b'speeddownleft'
        socket_tcp.send(inp)

        self.canvas.delete('a')
        self.canvas.delete('control')
        self.canvas.create_text(ori_x-30,ori_y+length+30,text="A",fill="#FF69B4",font="Normal -25 bold", tags = 'a')
        self.canvas.create_text(80,265,text="Ctrl",fill="#FF69B4",font="Normal -25 bold", tags = 'control')

        self.speedR -= 20
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)

        
    def speeddownR(self, event):
        inp=b'speeddownright'
        socket_tcp.send(inp)

        self.canvas.delete('d')
        self.canvas.delete('control')
        self.canvas.create_text(ori_x+length+30,ori_y+length+30,text="D",fill="#FF69B4",font="Normal -25 bold", tags = 'd')
        self.canvas.create_text(80,265,text="Ctrl",fill="#FF69B4",font="Normal -25 bold", tags = 'control')

        self.speedL -= 20
        self.lbSpeedR['text'] = str(self.speedR)
        self.lbSpeedL['text'] = str(self.speedL)

    def releaseW(self, event):
        self.canvas.delete('w')
        self.canvas.create_text(ori_x+30,ori_y+30,text="W",fill="#66CCFF",font="Normal -25 bold", tags = 'w')
        if self.shift_tag == 1:
            self.canvas.delete('shift')
            self.canvas.create_text(80,205,text="Shift",fill="#66CCFF",font="Normal -25 bold", tags = 'shift')
            self.shift_tag = 0
        self.canvas.delete('control')
        self.canvas.create_text(80,265,text="Ctrl",fill="#66CCFF",font="Normal -25 bold", tags = 'control')

    def releaseA(self, event):
        self.canvas.delete('a')
        self.canvas.create_text(ori_x-30,ori_y+length+30,text="A",fill="#66CCFF",font="Normal -25 bold", tags = 'a')
        if self.shift_tag == 1:
            self.canvas.delete('shift')
            self.canvas.create_text(80,205,text="Shift",fill="#66CCFF",font="Normal -25 bold", tags = 'shift')
            self.shift_tag = 0
        self.canvas.delete('control')
        self.canvas.create_text(80,265,text="Ctrl",fill="#66CCFF",font="Normal -25 bold", tags = 'control')
        
    def releaseS(self, event):
        self.canvas.delete('s')
        self.canvas.create_text(ori_x+30,ori_y+length+30,text="S",fill="#66CCFF",font="Normal -25 bold", tags = 's')
        if self.shift_tag == 1:
            self.canvas.delete('shift')
            self.canvas.create_text(80,205,text="Shift",fill="#66CCFF",font="Normal -25 bold", tags = 'shift')
            self.shift_tag = 0
        self.canvas.delete('control')
        self.canvas.create_text(80,265,text="Ctrl",fill="#66CCFF",font="Normal -25 bold", tags = 'control')
        
    def releaseD(self, event):
        self.canvas.delete('d')
        self.canvas.create_text(ori_x+length+30,ori_y+length+30,text="D",fill="#66CCFF",font="Normal -25 bold", tags = 'd')
        if self.shift_tag == 1:
            self.canvas.delete('shift')
            self.canvas.create_text(80,205,text="Shift",fill="#66CCFF",font="Normal -25 bold", tags = 'shift')
            self.shift_tag = 0
        self.canvas.delete('control')
        self.canvas.create_text(80,265,text="Ctrl",fill="#66CCFF",font="Normal -25 bold", tags = 'control')
        
    def releaseShiftW(self, event):
        self.canvas.delete('shift')
        self.canvas.create_text(80,205,text="Shift",fill="#66CCFF",font="Normal -25 bold", tags = 'shift')
        self.canvas.delete('w')
        self.canvas.create_text(ori_x+30,ori_y+30,text="W",fill="#66CCFF",font="Normal -25 bold", tags = 'w')

    def releaseShiftA(self, event):
        self.canvas.delete('a')
        self.canvas.create_text(ori_x-30,ori_y+length+30,text="A",fill="#66CCFF",font="Normal -25 bold", tags = 'a')
        self.canvas.delete('shift')
        self.canvas.create_text(80,205,text="Shift",fill="#66CCFF",font="Normal -25 bold", tags = 'shift')
        
    def releaseShiftS(self, event):
        self.canvas.delete('s')
        self.canvas.create_text(ori_x+30,ori_y+length+30,text="S",fill="#66CCFF",font="Normal -25 bold", tags = 's')
        self.canvas.delete('shift')
        self.canvas.create_text(80,205,text="Shift",fill="#66CCFF",font="Normal -25 bold", tags = 'shift')
        
    def releaseShiftD(self, event):
        self.canvas.delete('d')
        self.canvas.create_text(ori_x+length+30,ori_y+length+30,text="D",fill="#66CCFF",font="Normal -25 bold", tags = 'd')
        self.canvas.delete('shift')
        self.canvas.create_text(80,205,text="Shift",fill="#66CCFF",font="Normal -25 bold", tags = 'shift')
        

if __name__ == '__main__':
    ori_x=120
    ori_y=50
    length=60
    
    # connect
    SERVER_IP = "192.168.0.102"
    SERVER_PORT = 7786
    
    print("Starting socket: TCP...")
    server_addr = (SERVER_IP, SERVER_PORT)
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:  
        try:
            print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
            socket_tcp.connect(server_addr)  
            break  
        except Exception:
            print("Can't connect to server, try it latter!")
            time.sleep(1)
            #break
            continue  
    
    print("Receiving package...") 

    HybridSailBoat()
    
