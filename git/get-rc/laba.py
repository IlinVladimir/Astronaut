import RPi.GPIO as GPIO
import adc_plot
import mcp3021_driver as mcp
import time
import csv

if __name__ == "__main__":
    adc = mcp.MCP3021(5.19)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.OUT)
    voltage_values = []
    time_values = []
    flag = True
    GPIO.output(14, 1)

    f = open("data.csv", mode="w", newline="")
    writer = csv.writer(f)
    writer.writerow(["Время[с]", "Напряжение[В]"])

    try:
        
        start_time = time.time()
        while True:
            otn_time = time.time() - start_time
            voltage_values.append(adc.get_voltage())
            time_values.append(otn_time)
            #print(voltage_values[-1])
            if (voltage_values[-1] > 4.78 and flag):
                flag = False
                GPIO.output(14, 0)
            elif (voltage_values[-1] == 0.0 and not flag):
                break
        rows = zip(time_values, voltage_values)
        writer.writerows(rows)
        adc_plot.plot_voltage_vs_time(time_values, voltage_values, adc.dynamic_range)


    finally:
        adc.deinit()
        GPIO.cleanup()
        f.close()
