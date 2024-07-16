from hx711 import HX711
from RPi import GPIO

from statistics import mean

class LoadCell():

    def __init__(self, dout_pin, pd_sck_pin, channel='A', gain=64):
        self.load_cell = HX711(dout_pin=dout_pin, pd_sck_pin=pd_sck_pin, 
                               channel=channel, gain=gain)
        self.load_cell.reset()
        return
    
    def set_calib_values(self, raw_zero_value, raw_calib_value, 
                         calib_grams=1000, lc_max_grams=9999):
        self.RAW_ZERO_VALUE = raw_zero_value # load cell raw value when scale is empty
        self.RAW_CALIB_VALUE = raw_calib_value    # load cell raw value when calibration weight is on
        self.CALIB_GRAMS = calib_grams # weight used for calibration
        self.LC_MAX_GRAMS = lc_max_grams # max weight of load cell
        self.RAW_MAX_VALUE = raw_calib_value * lc_max_grams / calib_grams
        self.zero_offset = 0
        self.set_add_mass = 0
        return
    
    def remap(self, value):
        from_min = self.RAW_ZERO_VALUE
        from_max = self.RAW_MAX_VALUE
        to_min = 0
        to_max = self.LC_MAX_GRAMS
        return ((value - from_min) * (to_max - to_min) / 
                    (from_max - from_min) + to_min)

    def get_adjusted_weight(self):
        raw_value = self.load_cell.get_raw_data(times=5)
        mean_value = self.avg_and_truncate(raw_value)
        mapped_weight = round(self.remap(mean_value))
        adjusted_weight = mapped_weight + self.zero_offset + self.set_add_mass
        return adjusted_weight
    
    def zero(self):
        adjusted_weight = self.get_adjusted_weight()
        self.set_add_mass -= adjusted_weight
        return
    
    def avg_and_truncate(self, raw_data_list):
        mean_value = round(mean(raw_data_list))
        for value in raw_data_list:
            if abs(value - mean_value) > 1000:
                print(f'Value {value} removed')
                raw_data_list.remove(value)
        return round(mean(raw_data_list))

    

if __name__ == '__main__':
    try:
        print('Testing LoadCell')
        import time

        LC_DOUT_PIN = 17
        LC_SCK_PIN = 27

        RAW_ZERO_VALUE = 123 # load cell raw value when scale is empty
        RAW_CALIB_VALUE = 145373    # load cell raw value when calibration weight is on

        LoadCell = LoadCell(dout_pin=LC_DOUT_PIN, pd_sck_pin=LC_SCK_PIN)
        LoadCell.set_calib_values(RAW_ZERO_VALUE, RAW_CALIB_VALUE)

        print('Reading load cell values...')
        while True:
            start_time = time.time()
            print(LoadCell.load_cell.get_raw_data(times=5))
            print(f'adjusted weight: {LoadCell.get_adjusted_weight()}')
            print(f'took {time.time() - start_time} seconds')

    except Exception as e:
        raise e
    
    finally:
        GPIO.cleanup() 
        print('Test done')
        print('Exiting...')
        exit(0)