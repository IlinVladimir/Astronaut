import time
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021
from adc_plot import plot_voltage_vs_time

import numpy as np

data = np.loadtxt('data.csv',
				   delimiter=',',
				   skiprows=1,
				   encoding='utf-8')

time = data[:, 0].astype(float)
voltage = data[:, 1].astype(float)

print(time)  # [0.01 0.02 0.03 0.04 0.05]
print(voltage)  # [0.1   1.2   2.3   3.45  4.678]

dynamic_range = 5.5
adc = MCP3021(dynamic_range=5.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)#14 пин на плате adc подает ток для зарядки конденсатора

voltage_values = []
time_values = []
duration = 60.0

try:
    GPIO.output(14, True)
    start_time = time.time()
    while (time.time() - start_time) < duration: #пока не прошло 60 секунд
        voltage_values.append(adc.get_voltage()) #читаем напряжение с АЦП и заносим в список
        time_values.append(time.time() - start_time)#запоминаем время измерения
    GPIO.output(14, False) #по истечении 60 секунд перестаем подавать ток
    
    while (time.time() - start_time) < (duration * 2):
        voltage_values.append(adc.get_voltage())
        time_values.append(time.time() - start_time)
        
    plot_voltage_vs_time(time_values, voltage_values, dynamic_range)

finally:
    adc.deinit()
