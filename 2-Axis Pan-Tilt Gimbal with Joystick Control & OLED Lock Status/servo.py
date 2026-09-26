import machine

class ServoControl :
    def __init__(self,name,pin, min_duty = 1638, max_duty = 7800):
        self.pwm = machine.PWM(machine.Pin(pin))
        self.name = name
        self.pwm.freq(50) # frekuensi standar servo analog (50 Hz / periode 20ms)
        # duty cycle untuk u16 / 16 bit (0-65535):
        # min duty = (lebar pulsa min / periode total) * resolusi
        self.min_duty = min_duty # min_duty ~1638 (0.5 ms -> 0 derajat)
        # max duty = (lebar pulsa max / periode total) * resolusi
        self.max_duty = max_duty # max_duty ~7800 (2.5 ms -> 180 derajat)
        self.current_angle = 0

    def set_angle(self,angle):
        # limiter sudut agar berada di rentang fisik 0 - 180 derajat
        if angle < 0:
            angle = 0
        elif angle > 180 :
            angle = 180

        self.current_angle = angle
        # pemetan sudut derajat ke nilai duty cycle PWM
        # duty = min duty + (angle / 180) x (max duty - min duty)
        duty = int(self.min_duty + (angle / 180)*(self.max_duty - self.min_duty))
        self.pwm.duty_u16(duty)

    def control(self,input_joy) :
        # Konversi nilai ADC 16-bit (0-65535) dari joystick menjadi target sudut (0-180)
        # rasio pergeseran joystik = (nilai adc terbaca / nilai adc max) x rentang sudut servo
        target_angle = int((input_joy / 65535)*180)
        diff = target_angle - self.current_angle
        # untuk mencegah saat nilai target angle = current angle servo terus bergerak - atau +
        # jika selisih lebih kecil dari step, langsung set ke target
        if abs(diff) <= 15: #abs untuk mengubah nilai negatif menjadi absoulte atau menjadi nilai positif
            self.set_angle(target_angle)
        elif diff > 0: # Bergerak naik secara bertahap
            self.set_angle(self.current_angle + 15)
        else: # Bergerak turun secara bertahap
            self.set_angle(self.current_angle - 15)