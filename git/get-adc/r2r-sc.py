import RPi.GPIO as GPIO
import time
import adc_plot

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.0001, verbose = False): #обязательный конструктор
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
            time.sleep(self.compare_time) #пауза
            if GPIO.input(self.comp_gpio) == 1:
                return i-1
        return 255
    
    def deinit(self):
        GPIO.cleanup()
        GPIO.output(self.bits_gpio, 0)


    def get_sc_voltage(self):
        return self.sequental_counting_adc() * self.dynamic_range / 255

if __name__ == "__main__": #охранник
    try:
        voltage_values = []
        time_values = []
        duration = 3.0

        a = time.time()
        adc = R2R_ADC(3.2)
        while time.time() - a < duration:
            voltage = adc.get_sc_voltage()
            print(f"{voltage:.2f}")
            voltage_values.append(voltage)
            time_values.append(time.time())
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)
        adc_plot.plot_sampling_period_hist(time_values)
    finally:
        adc.deinit()