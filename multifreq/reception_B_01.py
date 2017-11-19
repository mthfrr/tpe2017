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

samples = sd.rec(int(duration * RATE), samplerate=RATE, channels=1, blocking=True)


## samples est une liste de liste [[x],[x],[x]] prévu pour avoir chaque canal pour chaque échantillon
samples = [x[0] for x in samples]

if 1:
   saveAsWave('test2.wav', np.array(samples), RATE)


## type 'A' : 4 fréquences
## demodulation

freq = 1000
carDuration = .05
gapDuration = carDuration/5.
n = carDuration*RATE

duration = carDuration + gapDuration


if 1:
   plt.plot(samples)
   plt.show()


sigs = []
for f in [freq, freq*2, freq*3, freq*4]:
   print ('doing', f)
   data = butter_bandpass_filter(samples, f/1.1, f*1.1, RATE, order=5)
   sigs.append(data)

if 1:
   for data in sigs:
      plt.plot(data)
   plt.show()


filteredsigs = []
for data in sigs:
   # on met tout en positif
   data = np.abs(data)
   if 0:
      plt.plot(data)
      plt.show()

   # on filtre un peu (filtre basé sur la médiane d'une fenêtre glissante de 3 valeurs)
   data = scipy.signal.medfilt(data, kernel_size=3)
   if 0:
      plt.plot(data)
      plt.show()

   # filtre passe bas pour transformer des séries de 'ponts' fin en créneaux larges
   data = butter_lowpass_filter(data, 3/(duration), RATE, order=1)
   if 0:
      plt.plot(data)
      plt.show()

   # on force le signal à n'avoir que deux valeurs : 0 ou 1
   coupure = max(data)/2  # critère pour 0 ou 1 -> le milieu de la plus grande valeur
   data[data < coupure] = 0
   data[data>=coupure] = 1
   if 0:
      plt.plot(data)
      plt.show()

   filteredsigs.append(data)


bitstream = toDigit4(filteredsigs, n)

print ('bitsteam', bitstream)

binMsg = []
for v in bitstream:
   if v == '1':
      binMsg.append('00')
   elif v == '2':
      binMsg.append('01')
   elif v == '3':
      binMsg.append('10')
   elif v == '4':
      binMsg.append('11')


print (''.join(binMsg))
print (unbinarise(''.join(binMsg)))


