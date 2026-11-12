import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False): #обязательный конструктор
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def number_to_dac(self, number):
        GPIO.output(self.bits_gpio, [int(element) for element in bin(number)[2:].zfill(8)])

    def sequental_counting_adc(self):
        for i in range(256):
            self.number_to_dac(i)
            time.sleep(0.01) #пауза
            if GPIO.input(self.comp_gpio) == 1:
                return i-1
        return 255
    
    def deinit(self):
        GPIO.cleanup()
        GPIO.output(self.bits_gpio, 0)

    def get_sc_voltage(self):
        return self.sequental_counting_adc() * self.dynamic_range / 255

    def succesive_approximation_adc(self):
        num = 0
        for i in range(7, -1, -1):

            num |= (1 << i)

            self.number_to_dac(num)
            if (GPIO.input(self.comp_gpio) == 1):
                num &= ~(1 << i)
        return num

    def get_sar_voltage(self):
        return self.succesive_approximation_adc() * self.dynamic_range / 255

if __name__ == "__main__": #
    try:
        adc = R2R_ADC(3.2)
        while True:
            try:
                print(f"{adc.get_sc_voltage():.2f}")

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
    finally:
        adc.deinit()
