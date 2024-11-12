import serial
from func_timeout import func_timeout, FunctionTimedOut
ser = serial.Serial ("/dev/ttyS0")                           
ser.baudrate = 9600 
try:
  data=func_timeout(12,ser.read,args=(12,))
  ser.close ()
except:
    print("no")
if data!=b'':
    print("yes")
                       


import time
import serial
          
      
data = serial.Serial(
                    port='/dev/ttyS0',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
