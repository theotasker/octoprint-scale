import time
import adafruit_dht

class HSensor():  
    def __init__(self, pin):
        # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
        # This may be necessary on a Linux single board computer like the Raspberry Pi,
        # but it will not work in CircuitPython.
        # use the "board" libary to specify the pin number
        self.dhtDevice = adafruit_dht.DHT11(pin, use_pulseio=False)
        return
    
    def get_temperature(self, unit='c'):
        if unit == 'f':
            return self.dhtDevice.temperature * (9 / 5) + 32
        elif unit == 'c':
            return self.dhtDevice.temperature
        else:
            raise ValueError('unit must be "c" or "f"')
    
    def get_humidity(self):
        return self.dhtDevice.humidity
    
    def exit(self):
        self.dhtDevice.exit()
        return

if __name__ == '__main__':
    try:
        print('Testing HSensor')
        import board
        hsensor = HSensor(board.D18)
        while True:
            print(f'Temperature: {hsensor.get_temperature()}C')
            print(f'Humidity: {hsensor.get_humidity()}%')
            time.sleep(2)
    except Exception as e:
        hsensor.exit()
        raise e