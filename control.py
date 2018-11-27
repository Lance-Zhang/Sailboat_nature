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
#from boatclass import sailboat

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
try:
    while True:
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        heading, roll, pitch= bno.read_euler()
        print(heading)
            # Print everything out.
        ws.write(i,0,'{0:0.2F}'.format(heading, roll, pitch))
        ws.write(i,1,'{1:0.2F}'.format(heading, roll, pitch))
        ws.write(i,2,'{2:0.2F}'.format(heading, roll, pitch))
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
