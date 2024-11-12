import Adafruit_MCP3008
import time
import RPi.GPIO as gp
import adafruit_dht
import board

state = {'light':0,'fan':0}
clk = 26  #37
miso = 19 #35
mosi = 13 #33
cs = 6	  #31

mcp = Adafruit_MCP3008.MCP3008(clk=clk, cs=cs, miso=miso, mosi=mosi)
read_analog = mcp.read_adc
dht_device = adafruit_dht.DHT11(board.D21)

light = 15
fan = 14

auto = 1

gp.setmode(gp.BCM)
gp.setup(light,gp.OUT)
gp.setup(fan, gp.OUT)

import tkinter as tk
from tkinter import ttk
import random
import threading
import time

def read_dht_c():
	while (1):
		try:
			return dht_device.temperature, dht_device.humidity
		except:
			time.sleep(0.5)

# Function to simulate getting data for the parameters
def get_parameters():
	temp,humi = read_dht_c()
	return {
	"power_consumption": read_analog(1)*read_analog(2)/10000,
	"air_quality": 100 - read_analog(0)/1023*100,
	"brightness": read_analog(7),
	"temperature": temp,
	"humidity":humi
	}

class App:
	def __init__(self, root):
		self.root = root
		self.root.title("Lab Automation System")

		# Create frames for layout
		self.control_frame = ttk.LabelFrame(root, text="Controls")
		self.control_frame.grid(row=0, column=0, padx=10, pady=10)

		self.param_frame = ttk.LabelFrame(root, text="Parameters")
		self.param_frame.grid(row=0, column=1, padx=10, pady=10)

		# Control buttons
		self.light_button = ttk.Button(self.control_frame, text="Light", command=self.toggle_light)
		self.light_button.grid(row=0, column=0, padx=5, pady=5)

		self.fan_button = ttk.Button(self.control_frame, text="Fan", command=self.toggle_fan)
		self.fan_button.grid(row=0, column=1, padx=5, pady=5)

		self.mode_button = ttk.Button(self.control_frame, text="Automatic", command=self.toggle_mode)
		self.mode_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

	# Parameter labels
		self.params = {
		"power_consumption": tk.StringVar(),
		"air_quality": tk.StringVar(),
		"brightness": tk.StringVar(),
		"temperature": tk.StringVar(),
		"humidity":tk.StringVar()
		}

		ttk.Label(self.param_frame, text="Power Consumption:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
		ttk.Label(self.param_frame, textvariable=self.params["power_consumption"]).grid(row=0, column=1, padx=5, pady=2)

		ttk.Label(self.param_frame, text="Air Quality:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
		ttk.Label(self.param_frame, textvariable=self.params["air_quality"]).grid(row=1, column=1, padx=5, pady=2)

		ttk.Label(self.param_frame, text="Brightness:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
		ttk.Label(self.param_frame, textvariable=self.params["brightness"]).grid(row=2, column=1, padx=5, pady=2)

		ttk.Label(self.param_frame, text="Temperature:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
		ttk.Label(self.param_frame, textvariable=self.params["temperature"]).grid(row=3, column=1, padx=5, pady=2)

		ttk.Label(self.param_frame, text="Humidity:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
		ttk.Label(self.param_frame, textvariable=self.params["humidity"]).grid(row=4, column=1, padx=5, pady=2)

		self.mode = "Automatic"
		self.update_parameters()

	def toggle_light(self):
		global auto
		print("Light toggled")
		if auto == 0:
			gp.output(light,1-state['light'])
			state['light'] = 1 - state['light']


	def toggle_fan(self):
		global auto,state
		print("Fan toggled")
		if auto == 0:
			print("auto",auto) #
			gp.output(fan,1-state['fan'])
			state['fan'] = 1 - state['fan']


	def toggle_mode(self):
		global auto,state
		if self.mode == "Automatic":
			self.mode = "Manual"
			self.mode_button.config(text="Manual")
			auto = 0
			print("manual",auto)
		else:
			self.mode = "Automatic"
			self.mode_button.config(text="Automatic")
			auto = 1
			print("auto",auto)

	def update_parameters(self):
		global auto
		params = get_parameters()
		self.params["power_consumption"].set(f"{params['power_consumption']:.2f} W")
		self.params["air_quality"].set(f"{params['air_quality']:.2f} %")
		self.params["brightness"].set(f"{params['brightness']:.2f} lux")
		self.params["temperature"].set(f"{params['temperature']:.2f} °C")
		self.params["humidity"].set(f"{params['humidity']:.2f} %")
		#checks
		if auto == 1:
			if params["brightness"] > 550:
				gp.output(light,1) #off
				state['light'] = 1
			else:
				gp.output(light,0)
				state['light'] = 0
				
			if params["temperature"] < 25:
				gp.output(fan,1) #off
				state['fan'] = 1
			else:
				gp.output(fan,0)
				state['fan'] = 0
		# Schedule next update
		self.root.after(1000, self.update_parameters)

if __name__ == "__main__":
	root = tk.Tk()
	app = App(root)
	root.mainloop()
