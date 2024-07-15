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

RAW_ZERO_VALUE = 123 # load cell raw value when scale is empty
RAW_CALIB_VALUE = 145373    # load cell raw value when calibration weight is on


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
    while True:
        if Rotary.switch:
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
            Rotary.change = 0
            if LCD.editing:
                LCD.display_add_int += (Rotary.change * 10)

            else:
                LCD.current_option += Rotary.change
                if LCD.current_option > 2:
                    LCD.current_option = 0
                elif LCD.current_option < 0:
                    LCD.current_option = 2

        current_weight = LoadCell.get_adjusted_weight()
        LCD.update(current_weight)

        time.sleep(0.1)
        print('cycle')


##############################################################################
# Main call
##############################################################################

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        Rotary.stop()
        GPIO.cleanup() 
        raise e