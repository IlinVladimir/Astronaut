import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)

    plt.title('График зависимости напряжения на входе АЦП от времени')
    plt.xlabel('Время, с')
    plt.ylabel('Напряжение, В')
    plt.show()

def plot_sampling_period_hist(time):
    sampling_periods = []
    for i in range(len(time) - 1):
        sampling_periods.append(time[1 + i] - time[i])
    plt.title('Распределение периодов дискретизации измерений по времени на одно измерение')
    plt.xlabel('Время, с')
    plt.ylabel('Количество измерений')
    plt.hist(sampling_periods)
    plt.xlim(0, 0.06)
    plt.savefig('rc-plot.png, dpi = 300')
    plt.show()