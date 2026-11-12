import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

class PWM_DAC:
    def __init__(self, gpio_bits, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.pwm_frequency = pwm_frequency 

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)

        self.pwm = GPIO.PWM(self.gpio_bits, self.pwm_frequency)
        self.pwm.start(0.0)

    def set_voltage(self, voltage):
            
        if not (0.0 <= voltage <= self.dynamic_range):
            voltage = 0.0

        self.pwm.ChangeDutyCycle(voltage / self.dynamic_range * 100.0)
        
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        dac = PWM_DAC(12,1000, 3.290, True)
        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        dac.deinit()