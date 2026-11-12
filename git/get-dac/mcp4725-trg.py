import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
if __name__ == "__main__":
    try:
        dac = mcp.MCP4725(5.11)
        while True:
            voltage = amplitude * sg.get_trg_wave_amplitude(signal_frequency, time.time())
            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)
    finally:
        dac.deinit()
