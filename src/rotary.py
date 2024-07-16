from ky040.KY040 import KY040


class Rotary():
    def __init__(self, pin_clk, pin_dt, pin_sw):
        self.rotary = KY040(pin_clk, pin_dt, pin_sw, 
                            self.on_change, self.on_switch)
        self.rotary.start()
        self.change = 0
        self.switch = False
        return
    
    def stop(self):
        self.rotary.stop()
        return
    
    def on_change(self, direction):
        print(f'Rotary change: {direction}')
        self.change += direction
        return
    
    def on_switch(self):
        self.switch = True
        return
