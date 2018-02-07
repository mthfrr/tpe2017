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

swShowGraph = False
swShowGraph = True

def plotSamples(samples):
   if swShowGraph:
      plt.plot(samples)
      plt.show()


def makeSilence(duration, RATE):
   return np.zeros(math.ceil(duration*RATE)) # np.zeros -> fct de numpy, retourne un tableau (1D) de 0s, avec param valeurs

def genOOK(binMsg, freq, carLen, RATE):
   carLen = int(carLen)
   X = np.arange( carLen )  # contruction d'un tableau (array) pour le temps de 0 à carLen-1
   Z = np.zeros( carLen ) ## silence d'un car + gap (nbr de points de mesure)
   F = np.sin(2*np.pi*( freq*(X)/RATE ) )

   sampLst = []

   for i in binMsg:
      if i == "1":
         sampLst.append(F)
      else:
         sampLst.append(Z)

   return np.concatenate(sampLst)


def txt2modulation(msg):
   bitstream = binarise(msg)
   signaux = []
   #print ('bitstream', bitstream)
   for i in range(8):
      selectedBits = bitstream[i::8]  # avec un pas de 8
      #print ('selectedBits', selectedBits)
      signaux.append( genOOK(selectedBits, 500+100*i, RATE*.1, RATE) )

   l = max( sig.size for sig in signaux )
   data = np.zeros( l )
   for sig in signaux:
      data += sig

   return data

RATE = 44100

pattern =  genOOK('10000', 500, RATE*.1, RATE)
pattern += genOOK('01000', 600, RATE*.1, RATE)
pattern += genOOK('00100', 700, RATE*.1, RATE)
pattern += genOOK('00010', 800, RATE*.1, RATE)
pattern += genOOK('00001', 900, RATE*.1, RATE)
pattern /= 8

data = txt2modulation("Hoche, c'est chouette !!!")

data /= 8

data = np.concatenate([ makeSilence( 2.66, RATE), pattern, data])

if 1:
   sd.play(data, RATE, blocking=True)

if 0:
   saveAsWave('test.wav', data)
   exit()

if 0:
   plt.plot(data)
   plt.show()


## demodulation

def creneaux(data, baseFreq, carLen, RATE):
   sigs = []
   for i in range(8):
      porteuse = 500+100*i # Hz
      lowcut  = porteuse - 50
      highcut = porteuse + 50
      sig = butter_bandpass_filter(data, lowcut, highcut, RATE, 4)

      #plt.plot(sig)
      #plt.show()

      sig = abs(sig)

      sig = butter_lowpass_filter(sig, 300, RATE, order=3)

      coupure = max(sig)/2
      sig[sig < coupure] = 0
      sig[sig >=coupure] = 1

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
      charStream.append(bitWord)
      i += carLen
   return charStream



sigs = creneaux(data, 500, 500*.1, RATE)

charStream = toDigits8(sigs, RATE*.1)

print(charStream)


print((bytes(charStream)).decode('utf8'))


