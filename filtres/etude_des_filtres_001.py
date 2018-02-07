# vim:set encoding=latin1

import numpy as np
import matplotlib.pyplot as plt
import math

import wave

import msvcrt

import sounddevice as sd

from scipy.signal import butter, lfilter, filtfilt, freqz


## basé sur 
## https://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units
##
## https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.signal.freqz.html
##



def butter_bandpass(lowcut, highcut, fs, order=5):
   nyq = 0.5 * fs
   low = lowcut / nyq
   high = highcut / nyq
   b, a = butter(order, [low, high], btype='band')
   return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
   b, a = butter_bandpass(lowcut, highcut, fs, order=order)
   y = filtfilt(b, a, data)
   return y


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


# Filter requirements.
order = 4
fs = 44100.       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz


porteuse = 500. # Hz
lowcut  = porteuse - 50
highcut = porteuse + 50


# Get the filter coefficients so we can check its frequency response.
b, a = butter_bandpass(lowcut, highcut, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=12000)
plt.subplot()
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')

#plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(lowcut, color='k')
plt.axvline(highcut, color='k')

plt.xlim(0, 0.5*fs)
plt.title("Bandpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()

plt.axis([0, 1000, 0, 1.2])

plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.15)
plt.show()

