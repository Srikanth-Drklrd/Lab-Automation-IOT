import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI

class ADCReader:
    def __init__(self, clk, miso, mosi, cs, use_hardware_spi=False):
        self.use_hardware_spi = use_hardware_spi
        if self.use_hardware_spi:
            # Hardware SPI (bus=0, device=0 is typical)
            self.mcp = Adafruit_MCP3008.MCP3008.spi(spi=SPI.SpiDev(0, 0))
            print("[INFO] Initialized MCP3008 using hardware SPI (bus=0, device=0)")
        else:
            # Software SPI
            self.mcp = Adafruit_MCP3008.MCP3008(clk=clk, cs=cs, miso=miso, mosi=mosi)
            print(f"[INFO] Initialized MCP3008 using software SPI | CLK={clk}, MISO={miso}, MOSI={mosi}, CS={cs}")

    def read_channel(self, channel):
        """Reads analog value from the given ADC channel (0-7)."""
        if not (0 <= channel <= 7):
            raise ValueError("ADC channel must be between 0 and 7")
        try:
            return self.mcp.read_adc(channel)
        except Exception as e:
            print(f"[ERROR] Failed to read channel {channel}: {e}")
            return None

    def __del__(self):
        print("[INFO] ADCReader instance destroyed.")

# Test run
if __name__ == "__main__":
    adc = ADCReader(clk=26, miso=19, mosi=13, cs=6, use_hardware_spi=False)
    for ch in range(8):
        value = adc.read_channel(ch)
        print(f"Channel {ch} : {value}")
