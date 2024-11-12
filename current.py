import Adafruit_MCP3008
#"pip install adafruit-mcp3008"  needed
from time import sleep

#-------> if software SPI used
#--->BCM based pin numbering used
clk = 26  #37
miso = 19 #35
mosi = 13 #33
cs = 6	  #31

mcp = Adafruit_MCP3008.MCP3008(clk=clk, cs=cs, miso=miso, mosi=mosi)

def read_current_avg():
	temp = 0
	for i in range(10):
		temp += mcp.read_adc(1)
		sleep(0.001)
	return temp/10

def read_current(mean):
	temp = 0
	for i in range(10):
		temp += (mcp.read_adc(1) - mean)**2
		sleep(0.001)
	return (temp/10)**0.5
	
print(input('X'))
mean = read_current_avg()
print(input('Y'))
while (1):
	print(read_current(mean))
	sleep(2)
