from RPi import GPIO

from LCD import LCD
from rotary import Rotary
from load_cell import LoadCell

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

RAW_ZERO_VALUE = 9478 # load cell raw value when scale is empty
RAW_CALIB_VALUE = 51485    # load cell raw value when calibration weight is on

##############################################################################
# Init
##############################################################################

# init peripherals, giving pin numbers on the Pi

print('Init peripherals...')
try:
    LoadCell = LoadCell(dout_pin=LC_DOUT_PIN, pd_sck_pin=LC_SCK_PIN)
    LoadCell.set_calib_values(RAW_ZERO_VALUE, RAW_CALIB_VALUE)
    
    LCD = LCD(LCD_PIN_RS, LCD_PIN_RW, LCD_PIN_E, LCD_PINS_DATA, GPIO.BCM)

    Rotary = Rotary(ROT_CLK, ROT_DT, ROT_SW)

except Exception as e:
    Rotary.stop()
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
    if Rotary.switch:
        print('switch')
        Rotary.switch = False
        Rotary.change = 0
        if LCD.current_option == 2:
            if LCD.editing:
                LCD.editing = False
            else:   
                LCD.editing = True
            
        elif LCD.current_option == 0:
            LoadCell.zero()

        elif LCD.current_option == 1:
            LoadCell.set_add_mass += LCD.display_add_int

    elif Rotary.change != 0:
        print(f'Rotary change: {Rotary.change}')
        if LCD.editing:
            LCD.display_add_int += (Rotary.change * 10)

        else:
            LCD.current_option += Rotary.change
            if LCD.current_option > 2:
                LCD.current_option = 2
            elif LCD.current_option < 0:
                LCD.current_option = 0

        Rotary.change = 0

        print(f'current_option: {LCD.current_option}')
        print(f'section: {LCD.SECOND_LINE_LIST[LCD.current_option]}')

    current_weight = LoadCell.get_adjusted_weight()
    LCD.update(current_weight)

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
        Rotary.stop()
        raise e
    
    finally:
        GPIO.cleanup()