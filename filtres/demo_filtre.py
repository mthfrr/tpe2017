# vim:set encoding=latin1

import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import butter, square
from scipy.signal import filtfilt

swSound = False
swShow = True

RATE = 44100

## from
## https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.square.html


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='highpass', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


num_samples = 1*RATE

FREQ = 440
cutoff = FREQ*4.5


t = np.linspace(0, 1, num_samples, endpoint=False)
samples = .5*square(2 * np.pi * FREQ * t)


plt.plot(samples)
if swShow:
   plt.show()
else:
   plt.savefig("white_noise.png",dpi=200)
   plt.clf()

data = samples


fft = np.abs(np.fft.rfft(data))
freq = np.fft.rfftfreq(data.size,1./num_samples)  # [:fft.size]


plt.plot(freq, fft)
if swShow:
   plt.show()
else:
   plt.savefig("white_noise_fft.png",dpi=200)
   plt.clf()


import sounddevice as sd

if swSound:
   sd.play(samples, RATE, blocking=True)




dataFiltered = butter_lowpass_filter(data, cutoff, RATE, order=5)
plt.plot(dataFiltered)
if swShow:
   plt.show()
else:
   plt.savefig("white_noise_filtered_800-900.png",dpi=200)
   plt.clf()



fft = np.abs(np.fft.rfft(dataFiltered))
freq = np.fft.rfftfreq(dataFiltered.size,1./num_samples)  # [:fft.size]


plt.plot(freq, fft)
if swShow:
   plt.show()
else:
   plt.savefig("white_noise_filtered_800-900_fft.png",dpi=200)
   plt.clf()

if swSound:
   sd.play(dataFiltered, RATE, blocking=True)



dataFiltered = butter_highpass_filter(data, cutoff, RATE, order=5)
plt.plot(dataFiltered)
if swShow:
   plt.show()
else:
   plt.savefig("white_noise_filtered_below_800.png",dpi=200)
   plt.clf()

fft = np.abs(np.fft.rfft(dataFiltered))
freq = np.fft.rfftfreq(dataFiltered.size,1./num_samples)  # [:fft.size]
plt.plot(freq, fft)
if swShow:
   plt.show()
else:
   plt.savefig("white_noise_filtered_below_800_fft.png",dpi=200)
   plt.clf()


if swSound:
   sd.play(dataFiltered, RATE, blocking=True)

