
import Adafruit_MCP3008
import time
import RPi.GPIO as gp
import tkinter as tk
from tkinter import ttk
import threading

state = [1, 1]
clk = 26  # 37
miso = 19 # 35
mosi = 13 # 33
cs = 6    # 31

mcp = Adafruit_MCP3008.MCP3008(clk=clk, cs=cs, miso=miso, mosi=mosi)
read_analog = mcp.read_adc

light = 15
fan = 14
auto = 0

gp.setmode(gp.BCM)
gp.setup(light, gp.OUT)
gp.setup(fan, gp.OUT)

def get_parameters():
    # Replace with actual sensor reading code
    return {
        "power_consumption": read_analog(0),  # Example channel
        "air_quality": read_analog(1),        # Example channel
        "brightness": read_analog(2),         # Example channel
        "temperature": read_analog(3)         # Example channel
    }

class App:
    def _init_(self, root):
        self.root = root
        self.root.title("Home Automation System")

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
            "temperature": tk.StringVar()
        }

        ttk.Label(self.param_frame, text="Power Consumption:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(self.param_frame, textvariable=self.params["power_consumption"]).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(self.param_frame, text="Air Quality:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(self.param_frame, textvariable=self.params["air_quality"]).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(self.param_frame, text="Brightness:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(self.param_frame, textvariable=self.params["brightness"]).grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(self.param_frame, text="Temperature:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(self.param_frame, textvariable=self.params["temperature"]).grid(row=3, column=1, padx=5, pady=2)

        self.mode = "Automatic"
        self.update_parameters()

    def toggle_light(self):
        global auto
        if auto == 0:
            gp.output(light, not gp.input(light))
            state[0] = 1 - state[0]
        print("Light toggled")

    def toggle_fan(self):
        global auto
        if auto == 0:
            gp.output(fan, not gp.input(fan))
            state[1] = 1 - state[1]
        print("Fan toggled")

    def toggle_mode(self):
        global auto
        if self.mode == "Automatic":
            self.mode = "Manual"
            self.mode_button.config(text="Manual")
            auto = 0
        else:
            self.mode = "Automatic"
            self.mode_button.config(text="Automatic")
            auto = 1

    def update_parameters(self):
        params = get_parameters()
        self.params["power_consumption"].set(f"{params['power_consumption']:.2f} W")
        self.params["air_quality"].set(f"{params['air_quality']:.2f} %")
        self.params["brightness"].set(f"{params['brightness']:.2f} lux")
        self.params["temperature"].set(f"{params['temperature']:.2f} °C")

        # Schedule next update
        self.root.after(5000, self.update_parameters)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
