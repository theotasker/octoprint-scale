import time
import adafruit_dht

class HSensor():  
    def __init__(self, pin):
        # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
        # This may be necessary on a Linux single board computer like the Raspberry Pi,
        # but it will not work in CircuitPython.
        # use the "board" libary to specify the pin number
        self.dhtDevice = adafruit_dht.DHT22(pin, use_pulseio=False)
        self.temtemp_c = 0
        self.temp_f = 0
        self.humidity = 0
        return
    
    def get_temp_c(self):
        return self.dhtDevice.temperature 

    def c_to_f(self, celsius):
        return celsius * (9 / 5) + 32
    
    def get_humidity(self):
        return self.dhtDevice.humidity
    

    
    def update_stored_values(self):
        try:
            self.temp_c = self.get_temperature(unit='c')
            self.temp_f = self.c_to_f(self.temp_c)
            self.humidity = self.get_humidity()
        except RuntimeError as error:
            print(error.args[0])
            return
    
    def exit(self):
        self.dhtDevice.exit()
        return

if __name__ == '__main__':
    try:
        print('Testing HSensor')
        import board
        hsensor = HSensor(board.D18)
        while True:
            hsensor.update_stored_values()
            print(f'Temperature: {hsensor.temp_c}C / {hsensor.temp_f}F')
            print(f'Humidity: {hsensor.humidity}%')
            time.sleep(1)
    except Exception as e:
        hsensor.exit()
        raise e