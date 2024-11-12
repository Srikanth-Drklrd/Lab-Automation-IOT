import time # for delay
import adafruit_dht # library for reading sensor
import board # adafruit_dht uses BCM based numbering for pins
import psutil # for killing the processes that conflicts with sensor
import RPi.GPIO as GPIO # for other purposes (LEDs, buzzer actuation)
import requests as r # for cloud purposes
GPIO.cleanup() # to refresh the GPIOs

#-----------------------> for killing conflicting processes
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
#----------------------------------------------------------

sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False) # sensor setup with pins configures * mandatory to set pulseio process to False
while True: # open a forever loop
    try: # for handling sensor errors
        temp = sensor.temperature  # for reading temperature and humidity
        humidity = sensor.humidity #
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        
    except RuntimeError as error: #handling the sensor errors
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error: # for handling library conflicts or platform conflicts
        sensor.exit() # once sensor is exited and it can be again reconfigured here using line
        raise error   # sensor = adafruit_dht.DHT11(board.D23, use_pulseio=False)
    time.sleep(2.0)   # -----> delay for the super loop for stability

