import time
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021
from adc_plot import plot_voltage_vs_time

dynamic_range = 5.5
adc = MCP3021(dynamic_range=5.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)

voltage_values = []
time_values = []
duration = 60.0

try:
    GPIO.output(14, True)
    start_time = time.time()
    while (time.time() - start_time) < duration:
        voltage_values.append(adc.get_voltage())
        time_values.append(time.time() - start_time)
    GPIO.output(14, False)
    
    while (time.time() - start_time) < (duration * 2):
        voltage_values.append(adc.get_voltage())
        time_values.append(time.time() - start_time)
        
    plot_voltage_vs_time(time_values, voltage_values, dynamic_range)

finally:
    adc.deinit()