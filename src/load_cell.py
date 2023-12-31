from hx711 import HX711


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
        raw_value = self.load_cell.get_raw_data(times=3)
        mapped_weight = round(self.remap(raw_value))
        adjusted_weight = mapped_weight + self.zero_offset + self.set_add_mass
        return adjusted_weight
    
    def zero(self):
        self.load_cell.reset()
        self.load_cell.tare()
        return