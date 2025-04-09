import serial
from func_timeout import func_timeout, FunctionTimedOut

class RFIDReader:
    def __init__(self, port="/dev/ttyS0", baudrate=9600, timeout=12):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            print(f"[INFO] RFID reader initialized on {self.port}")
        except Exception as e:
            print(f"[ERROR] Failed to initialize RFID reader: {e}")
            self.ser = None

    def read(self):
        """Reads 12 bytes from RFID tag with a timeout."""
        if self.ser is None:
            print("[ERROR] Serial connection not initialized.")
            return None
        try:
            data = func_timeout(self.timeout, self.ser.read, args=(12,))
            return data.decode('utf-8', errors='ignore')  # Assumes UTF-8 clean tags
        except FunctionTimedOut:
            print("[WARN] RFID read timed out.")
            return None
        except Exception as e:
            print(f"[ERROR] Failed to read RFID: {e}")
            return None

    def __del__(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"[INFO] Closed RFID serial port {self.port}")

# Test run
if __name__ == "__main__":
    reader = RFIDReader("/dev/ttyS0")
    print("[INFO] Waiting for RFID tag...")
    tag_data = reader.read()
    if tag_data:
        print(f"RFID Tag: {tag_data}")
    else:
        print("No tag read or timed out.")
