import pwm_dac as pwm
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
if __name__ == "__main__":
    try:
        dac = pwm.PWM_DAC(gpio_bits=12, pwm_frequency=2500, dynamic_range=3.29, verbose=True)
        while True:
            voltage = amplitude * sg.get_sin_wave_amplitude(signal_frequency, time.time())
            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)
    finally:
        dac.deinit()
