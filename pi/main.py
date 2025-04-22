from dht11 import DHT11Reader
from adc_reader import ADCReader
from firebase_helper import FirebaseHelper
import RPi.GPIO as GPIO
import time

# GPIO pin config
FAN_RELAY_PIN = 17
LIGHT_RELAY_PIN = 27

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_RELAY_PIN, GPIO.OUT)
GPIO.setup(LIGHT_RELAY_PIN, GPIO.OUT)

# Initialize devices
dht = DHT11Reader(pin=21)
adc = ADCReader(clk=26, miso=19, mosi=13, cs=6, use_hardware_spi=False)
fb = FirebaseHelper(
    key_path="key.json",
    db_url="https://smart-lab-2025-default-rtdb.asia-southeast1.firebasedatabase.app/"
)

def read_sensor_data():
    try:
        temp, hum = dht.read()
        voltage = adc.read_channel(1)
        current = adc.read_channel(2)
        air_quality = 100 - (adc.read_channel(0) / 1023 * 100)
        brightness = adc.read_channel(7)

        return {
            "temperature": temp,
            "humidity": hum,
            "voltage": voltage,
            "current": current,
            "air_quality": round(air_quality, 2),
            "brightness": brightness
        }
    except Exception as e:
        print(f"[ERROR] Sensor read failed: {e}")
        return None

def update_firebase(data):
    if data:
        fb.update_value("lab1/sensors", data)
        for param in ["voltage", "current"]:
            hist_path = f"lab1/{param}_history"
            history = fb.get_value(hist_path) or []
            history.append(data[param])
            if len(history) > 300:
                history = history[-300:]
            fb.set_value(hist_path, history)
        print("[INFO] Firebase updated with sensor data.")

def appliance_listener(event):
    try:
        data = event.data
        if data is None:
            return
        print(f"[EVENT] Firebase appliance update: {data}")

        # Actuate individually
        if "fan" in data:
            fan_state = data["fan"]
            GPIO.output(FAN_RELAY_PIN, GPIO.HIGH if fan_state else GPIO.LOW)
            print(f"[ACTUATE] Fan: {'ON' if fan_state else 'OFF'}")

        if "light" in data:
            light_state = data["light"]
            GPIO.output(LIGHT_RELAY_PIN, GPIO.HIGH if light_state else GPIO.LOW)
            print(f"[ACTUATE] Light: {'ON' if light_state else 'OFF'}")

    except Exception as e:
        print(f"[ERROR] Actuation listener error: {e}")

if __name__ == "__main__":
    try:
        print("[INFO] Smart Lab Controller Started")
        
        # Start Firebase listener for appliances
        fb.add_listener("lab1/appliances", appliance_listener)

        while True:
            sensor_data = read_sensor_data()
            update_firebase(sensor_data)
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n[EXIT] Graceful Shutdown")
    finally:
        del dht
        del adc
        del fb
        GPIO.cleanup()
