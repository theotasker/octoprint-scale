
class LCDFormat():
    first_line_temp = 'Filament:{}g'
    second_line_list = ['►zero◄add:|{}|', '|zero►add:◄{}|','|zero|add:►{}◄']

    def format_first_line(self, current_weight_int) -> str:
        return self.first_line_temp.format(f'{current_weight_int:04d}')
    
    def format_second_line(self, display_add_int, current_option) -> str:
        if display_add_int >= 0:
            display_add_str = f'+{display_add_int:03d}'
        else:
            display_add_str = f'-{display_add_int:03d}'
        return self.second_line_list[current_option].format(display_add_str)




def format_display_add_value(display_add_int) -> str:
    if display_add_int >= 0:
        display_add_str = f'+{display_add_int:03d}'
    else:
        display_add_str = f'-{display_add_int:03d}'
    return display_add_str



options_text = ['►zero◄add:|{}|', '|zero►add:◄{}|','|zero|add:►{}◄']

display_add_str = format_display_add_value(543)
current_option = 0

current_text = options_text[current_option].format(display_add_str)

print(current_text)

for i in range(0,6):
    if current_option == 2:
        continue
    
    current_option += 1
    print(options_text[current_option].format(display_add_str))


