import adafruit_dht
import board
import time

class DHT11Reader:
    def __init__(self, pin):
        # Create a board pin reference dynamically
        self.pin = getattr(board, f"D{pin}")
        self.dht_device = adafruit_dht.DHT11(self.pin)
        print(f"[INFO] DHT11 initialized on pin D{pin}")

    def read(self):
        """Read temperature and humidity from the DHT11 sensor."""
        try:
            temperature = self.dht_device.temperature
            humidity = self.dht_device.humidity
            if temperature is not None and humidity is not None:
                return temperature, humidity
            else:
                print("[WARN] Failed to read DHT11 data.")
                return None, None
        except Exception as e:
            print(f"[ERROR] Exception while reading DHT11: {e}")
            return None, None

    def __del__(self):
        try:
            self.dht_device.exit()
            print("[INFO] DHT11 sensor cleaned up.")
        except Exception as e:
            print(f"[WARN] Error during DHT11 cleanup: {e}")

# Test run
if __name__ == "__main__":
    sensor = DHT11Reader(21)  # GPIO21
    for _ in range(5):
        temp, humidity = sensor.read()
        if temp is not None and humidity is not None:
            print(f"Temperature: {temp}°C, Humidity: {humidity}%")
        else:
            print("Failed to read DHT11 data.")
        time.sleep(2)
