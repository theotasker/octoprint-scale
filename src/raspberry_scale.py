from RPi import GPIO
from ky040.KY040 import KY040
from hx711 import HX711
from RPLCD.gpio import CharLCD

# settings for load cell
DOUT_PIN = 17
PD_SCK_PIN = 21
CHANNEL = 'A'
GAIN = 64

RAW_ZERO_VALUE = 123
RAW_CALIB_VALUE = 145373
CALIB_GRAMS = 1000

# settings for LCD
PIN_RS = 26
PIN_RW = 19
PIN_E = 13
PINS_DATA = [6, 5, 11, 9]

LCD_TEXT = ['Filament: 0000g', 
            '|zero|add:|+000|']
ZERO_OFFSET = 0
ADD_VALUE = 0
CURRENT_WEIGHT = 0

CURRENT_SELECTION = 'zero'

# settings for rotary encoder
ROT_CLK = 23
ROT_DT = 24
ROT_SW = 25

ROTARY_CHANGE = 0
ROTARY_SWITCH = False

def on_rotary_change(direction):
    global ROTARY_CHANGE
    ROTARY_CHANGE+=direction

def on_switch():
    global ROTARY_SWITCH
    ROTARY_SWITCH = True

##############################################################################
# Init
##############################################################################

try:
    LoadCell = HX711(dout_pin=17, pd_sck_pin=21, channel='A', gain=64)
    LoadCell.reset()

    # init LCD
    lcd = CharLCD(pin_rs=PIN_RS, pin_rw=PIN_RW, pin_e=PIN_E, pins_data=PINS_DATA, numbering_mode=GPIO.BOARD)
    lcd.clear()

    # init rotary encoder
    rotary = KY040(ROT_CLK, ROT_DT, ROT_SW, on_rotary_change, on_switch)
    rotary.start()

except Exception as e:
    rotary.stop()
    GPIO.cleanup()  # always do a GPIO cleanup in your scripts!
    raise e


##############################################################################
# Functions
##############################################################################



def get_weight(map_zero, map_calib, calib_grams=1000):
    global CURRENT_WEIGHT

    raw_value = LoadCell.get_raw_data(times=3)

    #remap raw value to grams using zero and calib values
    
    mapped_value = map(raw_value, map_zero, map_calib, 0, calib_grams)



    return 

def write_lcd(option):
    lcd.clear()
    line_one = f'Filament:{CURRENT_WEIGHT:04d}g'

    if ADD_VALUE >= 0:
        add_value = f'+{ADD_VALUE:03d}'
    else:
        add_value = f'{ADD_VALUE:03d}'

    if option == 'zero':
        line_two = f'►zero◄add:|{add_value}|'
    elif option == 'add':
        line_two = f'|zero►add:◄{add_value}|'
    else:
        line_two = f'|zero|add:►{add_value}◄'

    if option == 'value_edit':
        lcd.cursor_pos = (1, 13)
        lcd.cursor_mode = 'blink'
    else:
        lcd.cursor_mode = 'hide'

    lcd.write_string(line_one)
    lcd.crlf()
    lcd.write_string(line_two)

    return



        


##############################################################################
# Main loop
##############################################################################

def main():
    while True:




        if 




    return

##############################################################################
# Main call
##############################################################################

try:





    pass




except Exception as e:
    rotary.stop()
    GPIO.cleanup() 
    raise e