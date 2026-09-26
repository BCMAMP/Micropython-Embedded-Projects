import time
import machine
from ssd1306 import SSD1306_I2C
from servo import ServoControl
# CV irfan taufik ==== 2-Axis Pan-Tilt Gimbal with Joystick Control & OLED Lock Status using Raspberry Pi Pico ====
# inisialisasi bus I2C0 (SDA=GP4, SCL=GP5)
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
# inisialisasi layar OLED (Lebar 128, Tinggi 64)
oled = SSD1306_I2C(128, 64, i2c)
# inisialisasi servo right = 10 , left =11 ,top = 12 bottom = 13
servo_upper = ServoControl('top_servo',12)
servo_bottom = ServoControl('bottom_servo',13)
servo_right = ServoControl('right_servo',10)
servo_left = ServoControl('left_servo',11)
# inisialisasi joystick analog ver = 26 , hro =27 , sel 22
joy_horz = machine.ADC(27)
joy_ver = machine.ADC(26)
joy_sel = machine.Pin(22,machine.Pin.IN) # menggunakan external pull-up resistor 4.7k ohm ke 3.3V (active low)

lock = False
last_btn_state = 1 # default HIGH karena menggunakan external pull-up

while True :
    # Toggle status Lock / Live
    btn_state = joy_sel.value()
    if last_btn_state == 1 and btn_state == 0:
        lock = not lock
        time.sleep_ms(30)
    last_btn_state = btn_state # simpan state untuk iterasi berikutnya

    if not lock :
        # kontrol aktuator
        # jika mode LIVE, perbarui posisi servo berdasarkan joystick
        val_h = joy_horz.read_u16()
        val_v = joy_ver.read_u16()

        servo_upper.control(val_v)
        servo_bottom.control(val_v)
        servo_left.control(val_h)
        servo_right.control(val_h)
    
    angle_x = servo_right.current_angle
    angle_y = servo_upper.current_angle
# membersihkan layar dari sisa tampilan sebelumnya
    oled.fill(0)
# menuliskan status & sudut terkini
    status_str = "==== Lock ====" if lock else "==== Live ===="
    oled.text(status_str, 4, 10)
    oled.text(f"X : {angle_x} deg", 10, 30)
    oled.text(f"Y : {angle_y} deg", 10, 45)
# menampilkan data dari buffer ke layar fisik OLED
    oled.show()
    time.sleep_ms(30)




