from RPi import GPIO

from LCD import LCD
from rotary import Rotary
from load_cell import LoadCell
from hsensor import HSensor
import board

import time

##############################################################################
# Pi GPIO setup (GPIO numbering mode on the Pi is set to BCM)
##############################################################################

print('Setting up GPIO...')

LC_DOUT_PIN = 17
LC_SCK_PIN = 27

LCD_PIN_RS = 21
LCD_PIN_RW = 19 # not used
LCD_PIN_E = 20
LCD_PINS_DATA = [26, 19, 13, 6]

ROT_CLK = 23
ROT_DT = 24
ROT_SW = 25

HSENSOR_PIN = board.D18

RAW_ZERO_VALUE = 9478 # load cell raw value when scale is empty
RAW_CALIB_VALUE = 51485    # load cell raw value when calibration weight is on

##############################################################################
# Init
##############################################################################

# init peripherals, giving pin numbers on the Pi

print('Init peripherals...')
try:
    load_cell = LoadCell(dout_pin=LC_DOUT_PIN, pd_sck_pin=LC_SCK_PIN)
    load_cell.set_calib_values(RAW_ZERO_VALUE, RAW_CALIB_VALUE)
    
    lcd = LCD(LCD_PIN_RS, LCD_PIN_RW, LCD_PIN_E, LCD_PINS_DATA, GPIO.BCM)

    rotary = Rotary(ROT_CLK, ROT_DT, ROT_SW)

    hsensor = HSensor(HSENSOR_PIN)

except Exception as e:
    rotary.stop()
    GPIO.cleanup() 
    raise e

##############################################################################
# Functions
##############################################################################



##############################################################################
# Main loop
##############################################################################

def main():
    start_time = time.time()
    if rotary.switch:
        print('switch')
        rotary.switch = False
        rotary.change = 0
        if lcd.current_option == 2:
            if lcd.editing:
                lcd.editing = False
            else:   
                lcd.editing = True
            
        elif lcd.current_option == 0:
            load_cell.zero()

        elif lcd.current_option == 1:
            load_cell.set_add_mass += lcd.display_add_int

    elif rotary.change != 0:
        print(f'Rotary change: {rotary.change}')
        if lcd.editing:
            lcd.display_add_int += (rotary.change * 10)

        else:
            lcd.current_option += rotary.change
            if lcd.current_option > 2:
                lcd.current_option = 2
            elif lcd.current_option < 0:
                lcd.current_option = 0

        rotary.change = 0

        print(f'current_option: {lcd.current_option}')
        print(f'section: {lcd.SECOND_LINE_LIST[lcd.current_option]}')

    current_weight = load_cell.get_adjusted_weight()
    lcd.update(current_weight)

    cycle_time = time.time() - start_time
    if cycle_time < 0.1:
        sleep_time = 0.1 - cycle_time
        print(f'Sleeping for {sleep_time} seconds')
        time.sleep(sleep_time)
    else:
        print(f'Cycle time too long: {cycle_time}')


##############################################################################
# Main call
##############################################################################

if __name__ == '__main__':
    try:
        while True:
            main()
    except Exception as e:
        rotary.stop()
        raise e
    
    finally:
        GPIO.cleanup()