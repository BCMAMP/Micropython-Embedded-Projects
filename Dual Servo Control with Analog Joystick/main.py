import time
import machine


joy_horz = machine.ADC(27) 
joy_vert = machine.ADC(26)
joy_sel = machine.Pin(21,machine.Pin.IN)
buzzer = machine.Pin(1,machine.Pin.OUT)

class direction :
    def __init__(self,name,pin, min_duty = 1638, max_duty = 7800):
        self.pwm = machine.PWM(machine.Pin(pin))
        self.name = name
        self.pwm.freq(50)
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.current_angle = 0

    def set_angle(self,angle):
        if angle < 0:
            angle = 0
        elif angle > 180 :
            angle = 180

        self.current_angle = angle
        duty = int(self.min_duty + (angle / 180)*(self.max_duty - self.min_duty))
        self.pwm.duty_u16(duty)

    def control(self,input_joy) :
        target_angle = int((input_joy / 65535)*180)
        self.set_angle(target_angle)


servo_right = direction("right",22)
servo_left = direction("left",8)

servo_right.set_angle(0)
servo_left.set_angle(0)
time.sleep(1)

servo_right.set_angle(90)
servo_left.set_angle(90)
time.sleep(1)

while True:
    val_h = joy_horz.read_u16()
    val_v = joy_vert.read_u16()

    servo_right.control(val_h)
    servo_left.control(val_h)
    
    if joy_sel.value() == 0 :
        buzzer.value(1)
    else :
        buzzer.value(0)
        
    print(f"HORZ (X): {val_h} | VERT (Y): {val_v}")
    time.sleep(0.2)