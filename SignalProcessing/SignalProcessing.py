import numpy
import matplotlib.pyplot as plt
import scipy
from scipy import signal
a = 0
b = 10
n = 500
Fs = 1000
F_max = 17
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
