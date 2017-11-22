# vim:set encoding=latin1

import random
import numpy as np
import wave

from scipy.signal import butter, lfilter, filtfilt


def binarise(txt):
   msg = []
   for c in txt.encode('utf8'):
      msg.append('{0:08b}'.format(c))
   return ''.join(msg)


def unbinarise(binStr):
   words = [binStr[i:i+8] for i in range(0, len(binStr), 8)]
   print (words)
   msg = []
   for w in words:
      msg.append(int(w, 2))  # bin to dec
   return (bytes(msg)).decode('utf8')

### debug
def addNormalNoise(ampl, length):
   noise = np.random.normal(0, .5, size=length)
   noise = ampl * noise
   noise[noise>1] = 1
   noise[noise<-1] = -1
   return noise

### trouvé sur internet
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    #y = lfilter(b, a, data)
    y = filtfilt(b, a, data)
    return y


def butter_bandpass(lowcut, highcut, fs, order=5):
   nyq = 0.5 * fs
   low = lowcut / nyq
   high = highcut / nyq
   b, a = butter(order, [low, high], btype='band')
   return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
   b, a = butter_bandpass(lowcut, highcut, fs, order=order)
   #print ('\n')
   #print('len=', len(data))
   #print('lowcut=', lowcut)
   #print('highcut=', highcut)
   #print('fs=', fs)
   #print('order=', order)
   #y = lfilter(b, a, data)
   y = filtfilt(b, a, data)
   return y


def saveAsWave(fileName, samples, RATE=44100):
   samples[samples> 1] =  1
   samples[samples<-1] = -1
   output_file = fileName
   outfile = wave.open(output_file, mode='wb')
   outfile.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
   samples = (samples*2**15).astype(np.int16)
   outfile.writeframes(samples)
   outfile.close()


### 
def toDigit4(data, n):
   i = 0

   while ((data[0][i] == 0) and (data[1][i+n] == 0) and (data[2][i+2*n] == 0) and (data[3][i+3*n] == 0)):
      i += 1

   i += int(n/2)
   i += 5*n

   bitstream = []
   N = data[0].size
   while i < N:
      w = '1' if data[0][int(i)] == 1 else ''
      w += '2' if data[1][int(i)] == 1 else ''
      w += '3' if data[2][int(i)] == 1 else ''
      w += '4' if data[3][int(i)] == 1 else ''
      bitstream.append(w)
      i += n
   return bitstream

### code mort
def toDigit(data, n):
   """
data : données à analyser
n : largeur en échantillons d'un caractère
"""
   #print (data)
   i = 0 # position dans la chaîne 'data'

   #on avance jusqu'à une donnée non nulle
   while(data[i] == 0):
      i += 1

   i += int(n/2)

   bitstream = []
   N = data.size
   while i < N:
      bitstream.append('1' if data[int(i)] == 1 else '0')
      i += n
   return bitstream

