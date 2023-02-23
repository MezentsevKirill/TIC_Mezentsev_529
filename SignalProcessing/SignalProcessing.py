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
plt.title("Сигнал з максимальною частотою F_max = 17", fontsize=14)
fig.savefig("./figures/" + "Залежність дисперсії від кроку дискретизації" + ".png", dpi=600)

# Display of the signal-to-noise ratio from the variance
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot(X, signal_noise, linewidth=1)
ax.set_xlabel("Крок дискретизації", fontsize=14)
ax.set_ylabel("ССШ", fontsize=14)
plt.title("Сигнал з максимальною частотою F_max = 17", fontsize=14)
fig.savefig("./figures/" + "Залежність співвідношення сигнал-шум від кроку дискретизації" + ".png", dpi=600)
