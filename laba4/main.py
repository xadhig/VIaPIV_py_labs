import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

freq = np.random.uniform(low=10, high=20, size=(1, )) * 1e6
fs = 150 * 1e6
l = 1000

t = np.arange(l)/fs

magnitude = np.random.uniform(low=0.5, high=1, size=(1, ))
noise = np.random.uniform(low=-0.001, high=0.001, size=(1000, ))

signal = magnitude * np.sin(2 * np.pi * t * freq)
signal_noise = signal + noise

fft_noise = abs(sp.fftpack.fft(signal_noise))


# fig1 = plt.figure(label='Signal')
# plt.plot(signal)
# plt.xlim([0,150])

# print(t)
fig_noise = plt.figure(label='Signal with noise')
plt.plot(signal_noise)
plt.xlim([0, l/10])
# np.printoptions(precision=2)
xticks = np.arange(0, l/10+1, 10)/fs * 1e6
xlabels = [f'{x:.2f}' for x in xticks]
plt.xticks(ticks=np.arange(0, l/10+1, 10), labels=xlabels)
plt.xlabel("Время, мкс")
plt.ylabel("Амплитуда")

fig_fft_noise = plt.figure(label='Spectrum in linear scale')
plt.plot(fft_noise/l * 2)
plt.xlim([0, l/2])
xticks = np.arange(0, l/2+1, l/20)
xlabels = [f'{(x/(l))*(fs/1e6):.1f}' for x in xticks]
# print(xlabels)
plt.xticks(ticks=xticks, labels=xlabels)
plt.xlabel("Частота, МГц")
plt.ylabel("Амплитуда")

fig_fft_noise_log = plt.figure(label='Spectrum in logarithm scale')
plt.semilogy(fft_noise/l * 2)
plt.xlim([0, l/2])
# plt.set_yscale('log')
xticks = np.arange(0, l/2+1, l/20)
xlabels = [f'{(x/(l))*(fs/1e6):.1f}' for x in xticks]
# print(xlabels)
plt.xticks(ticks=xticks, labels=xlabels)
plt.xlabel("Частота, МГц")
plt.ylabel("Амплитуда")

window = np.hanning(1000)
signal_windowed = signal_noise * window
fft_sig_window = abs(sp.fftpack.fft(signal_windowed))

fig_fft_window = plt.figure(label='Windowed Spectrum in linear scale')
plt.plot(fft_sig_window/l * 2)
plt.xlim([0, l/2])
xticks = np.arange(0, l/2+1, l/20)
xlabels = [f'{(x/(l))*(fs/1e6):.1f}' for x in xticks]
# print(xlabels)
plt.xticks(ticks=xticks, labels=xlabels)
plt.xlabel("Частота, МГц")
plt.ylabel("Амплитуда")





print('{:.5f}'.format(np.mean(freq/1e6)) + 'MHz')



plt.show()


