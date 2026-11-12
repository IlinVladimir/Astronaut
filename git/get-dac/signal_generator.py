import numpy as np
import time

def get_sin_wave_amplitude(freq, time):
    return (np.sin(2 * freq * time) + 1) / 2

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)

def get_trg_wave_amplitude(freq, time):
    return abs(2 * np.mod(freq*time, 1) - 1)