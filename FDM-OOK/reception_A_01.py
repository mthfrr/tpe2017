# vim:set encoding=latin1

import numpy as np
import matplotlib.pyplot as plt
import math

import wave

import msvcrt

import sounddevice as sd
import math

import scipy.signal

from queue import Queue

from myLib import *


RATE = 44100

duration = 10 # sec

print ('enregistrement')
samples = sd.rec(int(duration * RATE), samplerate=RATE, channels=1, blocking=True)
print ('début décodage')

## samples est une liste de liste [[x],[x],[x]] prévu pour avoir chaque canal pour chaque échantillon
data = [x[0] for x in samples]

data = np.array(data)

if 1:
   saveAsWave('reception.wav', np.array(samples), RATE)

carLen = .1*RATE

## demodulation

def creneaux(data, baseFreq, RATE, carLen):
   sigs = []
   saveAsWave('signal.wav', data)
   for i in range(8):
      porteuse = 500+100*i # Hz
      lowcut  = porteuse - 50
      highcut = porteuse + 50
      sig = butter_bandpass_filter(data, lowcut, highcut, RATE, 4)
      saveAsWave('signal_%i_s1.wav'%(i), sig)

      #plt.plot(sig)
      #plt.show()

      sig = abs(sig)
      saveAsWave('signal_%i_s2.wav'%(i), sig)

      sig = butter_lowpass_filter(sig, 300, RATE, order=3)
      saveAsWave('signal_%i_s3.wav'%(i), sig)

      coupure = max(sig)/2
      sig[sig < coupure] = 0
      sig[sig >=coupure] = 1

      saveAsWave('signal_%i_s4.wav'%(i), sig)

      sigs.append(sig)

   plt.clf()
   if 0:
      for s in sigs:
         plt.plot(range(len(s)), s)
      plt.show()

   return sigs


def toDigits8(data, carLen):
   i = 0

   while (  (data[0][i] == 0)
            and (data[1][int(i+carLen)] == 0)
            and (data[2][int(i+2*carLen)] == 0)
            and (data[3][int(i+3*carLen)] == 0)
            and (data[4][int(i+3*carLen)] == 0)
         ):
      i += 1

   i += int(carLen/2)
   i += 5*carLen

   N = data[0].size
   charStream = []
   while i < N:
      bitWord = 0
      for chan in range(8):
         bitWord *= 2
         bitWord += int(data[chan][int(i)])

      #print ('{0:08b}'.format(bitWord))
      if bitWord == 0 and len(charStream) > 0 and charStream[-1] == 0:
         return charStream
      charStream.append(bitWord)
      i += carLen
   return charStream



sigs = creneaux(data, 500, RATE, carLen)

charStream = toDigits8(sigs, carLen)

print(charStream)


print((bytes(charStream)).decode('utf8'))

