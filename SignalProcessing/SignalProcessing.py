import numpy
import matplotlib.pyplot as plt
import scipy
from scipy import signal
a = 0
b = 10
n = 500
Fs = 1000
F_max = 17
F_filter = 24
# Signal generation
x = numpy.random.normal(a, b, n)
# Determination of time counts
time = numpy.arange(n)/Fs
w = F_max / (Fs / 2)
parameters = signal.butter(3, w, 'low', output='sos')
y = signal.sosfiltfilt(parameters, x)
# Displaying the results
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(time, y, linewidth=1)
ax.set_xlabel("Час (секунди)", fontsize=14)
ax.set_ylabel("Амплітуда сигналу", fontsize=14)
plt.title("Сигнал з максимальною частотою F_max = 17", fontsize=14)
fig.savefig("./figures/" + "Сигнал з максимальною частотою F_max = 17" + ".png", dpi=600)
# Calculation of the signal spectrum
spectrum = scipy.fft.fft(y)
t_spectrum = numpy.abs(scipy.fft.fftshift(spectrum))
f_readings = scipy.fft.fftfreq(n, 1 / n)
readings = scipy.fft.fftshift(f_readings)
# Displaying the results
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(readings, t_spectrum, linewidth=1)
ax.set_xlabel("Частота (Гц)", fontsize=14)
ax.set_ylabel("Амплітуда сигналу", fontsize=14)
plt.title("Сигнал з максимальною частотою F_max = 17", fontsize=14)
fig.savefig("./figures/" + "Спектр сигналу з максимальною частотою F_max = 17" + ".png", dpi=600)

# practice 3
discrete_signals = []
discrete_spectrums = []
filtered_signals = []
dispersion_dif = []
signal_noise = []
for Dt in [2, 4, 8, 16]:
    discrete_signal = numpy.zeros(n)
    for i in range(0, round(n / Dt)):
        discrete_signal[i * Dt] = y[i * Dt]
    discrete_signals += [list(discrete_signal)]
    # signal spectra
    spectrum = scipy.fft.fft(discrete_signal)
    t_spectrum = numpy.abs(scipy.fft.fftshift(spectrum))
    discrete_spectrums += [list(t_spectrum)]
    # restoration of the initial signal
    w = F_filter / (Fs / 2)
    parameters_filter = signal.butter(3, w, 'low', output='sos')
    filtered_signal = signal.sosfiltfilt(parameters_filter, discrete_signal)
    filtered_signals += [list(filtered_signal)]
    # variance calculation and signal-to-noise ratio
    E1 = filtered_signal - y
    dispersion_1 = numpy.var(y)
    dispersion_2 = numpy.var(E1)
    dispersion_dif += [dispersion_2]
    signal_noise += [dispersion_1 / numpy.var(E1)]

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(time, discrete_signals[s], linewidth=1)
        s += 1

fig.supxlabel("Час (секунди)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig("./figures/" + "Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)" + ".png", dpi=600)

#  Displaying the results of signal spectra
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(readings, discrete_spectrums[s], linewidth=1)
        s += 1
fig.supxlabel("Частота (Гц)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Спектри сигнал з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig("./figures/" + "Спектри сигнал з кроком дискретизації Dt = (2, 4, 8, 16)" + ".png", dpi=600)

# Displaying the results of restoring the initial signal
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(time, filtered_signals[s], linewidth=1)
        s += 1
fig.supxlabel("Час (секунди)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Відновлені аналогові сигнали з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig("./figures/" + "Відновлені аналогові сигнали з кроком дискретизації Dt = (2, 4, 8, 16)" + ".png", dpi=600)

# Display of the dependence of the variance of the difference of the reconstructed signal and
# initial from the discretization step
X = [2, 4, 8, 16]
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(X, dispersion_dif, linewidth=1)
ax.set_xlabel("Крок дискретизації", fontsize=14)
ax.set_ylabel("Дисперсія", fontsize=14)
plt.title("Залежність дисперсії від кроку дискретизації", fontsize=14)
fig.savefig("./figures/" + "Залежність дисперсії від кроку дискретизації" + ".png", dpi=600)

# Display of the signal-to-noise ratio from the variance
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(X, signal_noise, linewidth=1)
ax.set_xlabel("Крок дискретизації", fontsize=14)
ax.set_ylabel("ССШ", fontsize=14)
plt.title("Залежність співвідношення сигнал-шум від кроку дискретизації", fontsize=14)
fig.savefig("./figures/" + "Залежність співвідношення сигнал-шум від кроку дискретизації" + ".png", dpi=600)


# practice 4
dispersion_dif.clear()
signal_noise.clear()
quantize_signals = []
for M in [4, 16, 64, 256]:
    bits = []
    delta = (numpy.max(y) - numpy.min(y)) / (M - 1)
    quantize_signal = delta * numpy.round(y / delta)
    quantize_signals += [quantize_signal]
    quantize_levels = numpy.arange(numpy.min(quantize_signal), numpy.max(quantize_signal) + 1, delta)
    quantize_bit = numpy.arange(0, M)
    quantize_bit = [format(bits, '0' + str(int(numpy.log(M) / numpy.log(2))) + 'b') for bits in quantize_bit]
    quantize_table = numpy.c_[quantize_levels[:M], quantize_bit[:M]]
    # table display
    fig, ax = plt.subplots(figsize=(14 / 2.54, M / 2.54))
    table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    fig.savefig("./figures/" + "Таблиця квантування для " + str(M) + " рівнів" + ".png", dpi=600)

    for signal_value in quantize_signal:
        for index, value in enumerate(quantize_levels[:M]):
            if numpy.round(numpy.abs(signal_value - value), 0) == 0:
                bits.append(quantize_bit[index])
                break
    bits = [int(item) for item in list(''.join(bits))]

    # Display graphics of bit sequences
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.step(numpy.arange(0, len(bits)), bits, linewidth=0.1)
    ax.set_xlabel("Біти", fontsize=14)
    ax.set_ylabel("Амплітуда сигналу", fontsize=14)
    plt.title("Кодова послідовність сигналу при кількості рівнів квантування " + str(M), fontsize=14)
    fig.savefig("./figures/" + "Кодова послідовність сигналу при кількості рівнів квантування " + str(M) + ".png"
                , dpi=600)

    # Variance calculation and signal-to-noise ratio
    E1 = quantize_signal - y
    dispersion_1 = numpy.var(y)
    dispersion_2 = numpy.var(E1)
    dispersion_dif += [dispersion_2]
    signal_noise += [dispersion_1 / numpy.var(E1)]

# Display graphics of quantize signals
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(0, 2):
    for j in range(0, 2):
        ax[i][j].plot(time, quantize_signals[s], linewidth=1)
        s += 1

fig.supxlabel("Час (секунди)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Цифрові сигнали з рівнями квантування (4, 16, 64, 256)", fontsize=14)
fig.savefig("./figures/" + "Цифрові сигнали з рівнями квантування (4, 16, 64, 256)" + ".png", dpi=600)

# Display dependence of dispersion on the number of quantization levels
M = [4, 16, 64, 256]
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(M, dispersion_dif, linewidth=1)
ax.set_xlabel("Кількість рівнів квантування", fontsize=14)
ax.set_ylabel("Дисперсія", fontsize=14)
plt.title("Залежність дисперсії від кількості рівнів квантування", fontsize=14)
fig.savefig("./figures/" + "Залежність дисперсії від кількості рівнів квантування" + ".png", dpi=600)

# Display dependence of the signal-to-noise ratio on the number of quantization levels
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(M, signal_noise, linewidth=1)
ax.set_xlabel("Кількість рівнів квантування", fontsize=14)
ax.set_ylabel("ССШ", fontsize=14)
plt.title("Залежність співвідношення сигнал-шум від кількості рівнів квантування", fontsize=14)
fig.savefig("./figures/" + "Залежність співвідношення сигнал-шум від кількості рівнів квантування" + ".png"
            , dpi=600)
