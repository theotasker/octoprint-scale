from RPLCD.gpio import CharLCD


class LCD():
    FIRST_LINE = 'Filament:{}g'
    SECOND_LINE_LIST = ['►zero◄add:|{}|', '|zero►add:◄{}|','|zero|add:►{}◄']

    def __init__(self, pin_rs, pin_rw, pin_e, pins_data, numbering_mode):
        self.lcd = CharLCD(pin_rs=pin_rs, pin_rw=pin_rw, pin_e=pin_e, 
                           pins_data=pins_data, numbering_mode=numbering_mode)
        self.lcd.clear()
        self.current_text = ''
        self.current_option = 0
        self.editing = False
        self.display_add_int = 930
        return

    def format_first_line(self, current_weight_int) -> str:
        return self.first_line_temp.format(f'{current_weight_int:04d}')
    
    def format_second_line(self) -> str:
        if self.display_add_int >= 0:
            display_add_str = f'+{self.display_add_int:03d}'
        else:
            display_add_str = f'-{self.display_add_int:03d}'
        return self.second_line_list[self.current_option].format(display_add_str)

    def write(self, first_line, second_line) -> None:
        self.lcd.clear()
        self.lcd.write_string(first_line)
        self.lcd.crlf()
        self.lcd.write_string(second_line)
        return
    
    def blink_cursor(self, on=False, cursor_pos=[1,13]) -> None:
        if on:
            self.lcd.cursor_pos = (cursor_pos[0], cursor_pos[1])
            self.lcd.cursor_mode = 'blink'
        else:
            self.lcd.cursor_mode = 'hide'
    
    def update(self, current_weight_int) -> None:
        if self.editing:
            self.blink_cursor(on=True)
        else:
            self.blink_cursor(on=False)
        first_line = self.format_first_line(current_weight_int)
        second_line = self.format_second_line(self.display_add_int, self.current_option)
        if self.current_text == f'{first_line}\n{second_line}':
            return
        
        self.write(first_line, second_line)
        self.current_text = f'{first_line}\n{second_line}'
        return