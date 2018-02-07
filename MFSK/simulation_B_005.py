# vim:set encoding=latin1

import numpy as np
import matplotlib.pyplot as plt
import math

import wave

import msvcrt

import sounddevice as sd

import scipy.signal

from queue import Queue

from myLib import *

np.set_printoptions(suppress=True) # don't use scientific notation

swShowGraph = True
swShowGraph = False

def plotSamples(samples):
   if swShowGraph:
      plt.plot(samples)
      plt.show()



def makeSilence(duration, RATE):
   return np.zeros(math.ceil(duration*RATE)) # np.zeros -> fct de numpy, retourne un tableau (1D) de 0s, avec param valeurs


freq = 1000
RATE = 44100 # nbr de mesure par seconde (Hz)
carDuration = .05 # durée d'un car (sec)
gapDuration = carDuration/5.  # durée d'un trou (sec)
gapDuration = 0



def makeSound(msg, carDuration, gapDuration, RATE):
   carLen = math.ceil(carDuration*RATE)
   carDuration = carLen/RATE
   gapLen = math.ceil(gapDuration*RATE)

   X = np.arange( carLen )  # contruction d'un tableau (array) pour le temps de 0 à carLen-1

   Z = np.zeros( gapLen ) # construction d'une série de 0 pour faire les inter-caractères

   Zc = np.zeros( carLen+gapLen ) ## silence d'un car + gap (nbr de points de mesure)

   F1 = np.sin(2*np.pi*( freq*(X)/RATE ) )
   F2 = np.sin(2*np.pi*( freq*2*(X)/RATE ) )
   F3 = np.sin(2*np.pi*( freq*3*(X)/RATE ) )
   F4 = np.sin(2*np.pi*( freq*4*(X)/RATE ) )


   binMsg = binarise(msg)
   print ('msg=',binMsg)

   samples = [] ## tableau de bouts de sons

   samples.append(F1)
   samples.append(Z)
   samples.append(F2)
   samples.append(Z)
   samples.append(F3)
   samples.append(Z)
   samples.append(F4)
   samples.append(Z)
   samples.append(Zc)



   binWords = [binMsg[i:i+2] for i in range(0, len(binMsg), 2)]
   vol = 1
   for c in binWords:
      if c == '00':
         samples.append(F1)
      elif c == '01':
         samples.append(F2)
      elif c == '10':
         samples.append(F3)
      elif c == '11':
         samples.append(F4)

      samples.append(Z)

   samples = np.concatenate(samples)
   samples *= .9 ## volume ajusté à 90%
   return samples





silence = makeSilence(.5, RATE)
samples = makeSound("Hoche, c'est chouette !!!", carDuration, gapDuration, RATE)

samples = np.concatenate([silence, samples, silence])


## emission
if 1:
   sd.play(samples, RATE, blocking=True)

if 1:
   saveAsWave('MFSK.wav', samples)
   exit()

plotSamples(samples)




#############################################################################################
#############################################################################################
#############################################################################################


## demodulation

n = (carDuration + gapDuration)*RATE  # longueur d'un caractère, avec son 'trou' (nb de mesures)


sigs = []
for f in [freq, freq*2, freq*3, freq*4]:
   data = butter_bandpass_filter(samples, f/1.1, f*1.1, RATE, order=5)
   sigs.append(data)
   #plt.plot(data)
   #plt.show()


sig2s = []
for sig in sigs:
   data = butter_lowpass_filter(sig, freq*1.3, RATE, order=5)
   data = np.abs(data)
   data = scipy.signal.medfilt(data, kernel_size=3)
   data = butter_lowpass_filter(data, 3/(carDuration + gapDuration), RATE, order=2)

   coupure = max(data)/2
   data[data < coupure] = 0
   data[data>=coupure] = 1

   sig2s.append(data)
   #plotSamples(data)
   #plt.plot(data)
   #plt.show()

bitstream = toDigit4(sig2s, n)

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



