from RPi import GPIO
from ky040.KY040 import KY040
from hx711 import HX711
from RPLCD.gpio import CharLCD
import time

##############################################################################
# Pi IO setup
##############################################################################

LC_DOUT_PIN = 17
LC_SCK_PIN = 21

LCD_PIN_RS = 26
LCD_PIN_RW = 19
LCD_PIN_E = 13
LCD_PINS_DATA = [6, 5, 11, 9]

ROT_CLK = 23
ROT_DT = 24
ROT_SW = 25

RAW_ZERO_VALUE = 123 # needs to be set
RAW_CALIB_VALUE = 145373    # needs to be set
CALIB_GRAMS = 1000
LC_MAX_GRAMS = 9999
RAW_MAX_VALUE = RAW_CALIB_VALUE * LC_MAX_GRAMS / CALIB_GRAMS

##############################################################################
# Init
##############################################################################
# global variables
zero_offset = 0
set_add_value = 0
display_add_value = 0
current_weight = 0

current_selection = 'zero'

rotary_change = 0
rotary_switch = False

# rotary encoder callbacks
def on_rotary_change(direction):
    global rotary_change
    rotary_change+=direction

def on_switch():
    global rotary_switch
    rotary_switch = True

# init peripherals
try:
    LoadCell = HX711(dout_pin=LC_DOUT_PIN, pd_sck_pin=LC_SCK_PIN, 
                     channel='A', gain=64)
    LoadCell.reset()

    # init LCD
    lcd = CharLCD(pin_rs=LCD_PIN_RS, pin_rw=LCD_PIN_RW, pin_e=LCD_PIN_E, 
                  pins_data=LCD_PINS_DATA, numbering_mode=GPIO.BOARD)
    lcd.clear()

    # init rotary encoder
    rotary = KY040(ROT_CLK, ROT_DT, ROT_SW, on_rotary_change, on_switch)
    rotary.start()

except Exception as e:
    rotary.stop()
    GPIO.cleanup() 
    raise e

##############################################################################
# Functions
##############################################################################

def remap(value, from_min=RAW_ZERO_VALUE, from_max=RAW_MAX_VALUE, 
                to_min=0, to_max=LC_MAX_GRAMS):
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min

def get_weight():
    raw_value = LoadCell.get_raw_data(times=3)
    mapped_weight = round(remap(raw_value))
    adjusted_weight = mapped_weight + zero_offset + set_add_value
    return adjusted_weight

def write_lcd(option):
    lcd.clear()
    line_one = f'Filament:{current_weight:04d}g'

    if display_add_value >= 0:
        display_add_value = f'+{display_add_value:03d}'
    else:
        display_add_value = f'{display_add_value:03d}'

    if option == 'zero':
        line_two = f'►zero◄add:|{display_add_value}|'
    elif option == 'add':
        line_two = f'|zero►add:◄{display_add_value}|'
    else:
        line_two = f'|zero|add:►{display_add_value}◄'

    if option == 'value_edit':
        lcd.cursor_pos = (1, 13)
        lcd.cursor_mode = 'blink'
    else:
        lcd.cursor_mode = 'hide'

    lcd.write_string(line_one)
    lcd.crlf()
    lcd.write_string(line_two)

    return line_one, line_two

def rotary_action(rotary_change):
    global current_selection
    global display_add_value
    if current_selection == 'zero':
        if rotary_change > 0:
            current_selection = 'add'
        elif rotary_change < 0:
            current_selection = 'value'
    elif current_selection == 'add':
        if rotary_change > 0:
            current_selection = 'value'
        elif rotary_change < 0:
            current_selection = 'zero'
    elif current_selection == 'value':
        if rotary_change > 0:
            current_selection = 'zero'
        elif rotary_change < 0:
            current_selection = 'add'
    else:
        display_add_value += rotary_change * 10

    return current_selection



        


##############################################################################
# Main loop
##############################################################################

def main():
    while True:
        if rotary_change != 0:
            rotary_action(rotary_change)
                

        pass





    return

##############################################################################
# Main call
##############################################################################

if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        rotary.stop()
        GPIO.cleanup() 
        raise e