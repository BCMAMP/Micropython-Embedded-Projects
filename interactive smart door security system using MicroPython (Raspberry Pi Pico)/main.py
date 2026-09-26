import time
import machine
import ili9341

spi = machine.SPI(0,
                baudrate=40000000,
                polarity=1,
                phase=0,
                sck=machine.Pin(18),
                mosi=machine.Pin(19))


tft_cs = machine.Pin(17, machine.Pin.OUT)
tft_dc = machine.Pin(20, machine.Pin.OUT)
tft_rst = machine.Pin(21, machine.Pin.OUT)

display = ili9341.ILI9341(spi, cs=tft_cs, dc=tft_dc, rst=tft_rst, w=240, h=320, r=0)
bg_color = ili9341.color565(0, 0, 0)
text_color = ili9341.color565(255, 255, 0)
button_color = ili9341.color565(255, 255, 255)
right_password_color = ili9341.color565(0, 255, 0)
wrong_password_color = ili9341.color565(255, 0, 0)
display.fill(bg_color)

servo_pin = machine.Pin(22)
servo = machine.PWM(servo_pin)
servo.freq(50)

def rotation_servo(sudut):
    duty = int(1638 + (sudut / 180) * (8192 - 1638))
    servo.duty_u16(duty)

rotation_servo(0)

row_pins = [
    machine.Pin(2, machine.Pin.OUT),
    machine.Pin(3, machine.Pin.OUT),
    machine.Pin(4, machine.Pin.OUT),
    machine.Pin(5, machine.Pin.OUT)]

col_pins =[
    machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_DOWN),
    machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_DOWN),
    machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_DOWN),
    machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_DOWN)]

keys = [
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D']]

def keypad():
    for r_idx, row in enumerate(row_pins):
        row.high()
    
        for c_idx, col in enumerate(col_pins):
            if col.value() == 1:
                row.low()
                return keys[r_idx][c_idx]
    
        row.low()
    return None

password_default = '1234'
input_password = ''

def position_x_input(text_lenght_on_screen):
    screen_width = text_lenght_on_screen * 28
    return int((240 - screen_width) / 2)

def reset_display():
    global input_password
    input_password = ''
    display.fill(bg_color)
    display.text('password', 70, 120, text_color, bg_color, 2)

reset_display()

while True:
    tombol = keypad()

    if tombol is not None:
        print('active', tombol)

        if tombol != '#' and tombol != '*':
            if len(input_password) > 0:
                old_location = position_x_input(len(input_password))
                display.text(" " * len(input_password), old_location, 160, bg_color, bg_color, 4)

            input_password += tombol

            location_text = position_x_input(len(input_password))     
            display.text(input_password, location_text, 160, button_color, bg_color, 4)

            if len(input_password) == 4:

                if input_password == password_default:
                    display.fill(right_password_color)
                    display.text('Welcome', 55, 145, bg_color, right_password_color, 3)
                    rotation_servo(90)
                    time.sleep(3)
                    rotation_servo(0)
                    time.sleep(3)
                    reset_display()
                    
                else:
                    display.fill(wrong_password_color)
                    display.text('Try again', 40, 145, bg_color, wrong_password_color, 2)
                    time.sleep(1.5)
                    reset_display()

        time.sleep(0.5)

    else:
        time.sleep(0.05)