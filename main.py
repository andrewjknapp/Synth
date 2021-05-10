import time
import math
from ADCDevice import *
from  soundplayer import SoundPlayer
import pyaudio
import itertools
import numpy as np
from Oscillator import Oscillator
from sine_oscillator import SineOscillator
from square_oscillator import SquareOscillator
from sawtooth_oscillator import SawtoothOscillator
from triangle_oscillator import TriangleOscillator
from wave_adder import WaveAdder
import RPi.GPIO as GPIO

BUTTON_PIN = 40

BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMP = 0.1

# -- HELPER FUNCTIONS --

#def my_get_samples(oscillator, num_samples=BUFFER_SIZE):
#    sampleList = []
#    for _ in range(num_samples):
#        sampleList.append(next(oscillator) * 32767)
#        
#    return sampleList

def my_get_samples(waveAdder, num_samples=BUFFER_SIZE):
    oscillators = waveAdder.oscillators
    sampleList = []
    sum = 0;
    for _ in range(num_samples):
        sampleList.append(next(oscillators[0][0]) * 32767)
        
#        sum = 0
#        for x in range(waveAdder.n):
#            sum = (sum + next(oscillators[0][x])) / 2
            
#        sampleList.append(sum * 32767)
        
    return sampleList

def setNote(oscillators, note):
    for x in range(len(oscillators)):
        oscillators[x]._f = note
        oscillators[x]._post_freq_set()

# -- INITIALIZION --
def initializeOscillators(oscillators):
    for x in range(len(oscillators)):
        oscillators[x]._post_freq_set()
        oscillators[x]._post_phase_set()
        oscillators[x]._initialize_osc()

stream = pyaudio.PyAudio().open(
    rate=SAMPLE_RATE,
    channels=1,
    format=pyaudio.paInt16,
    output=True,
    frames_per_buffer=BUFFER_SIZE
)


dev = 0


notes = [587.33, 523.25, 493.88, 440.00, 392.00, 349.23, 329.63, 293.66, 261.63, 246.94, 220.00, 196.00, 174.61, 164.81, 146.83, 130.81, 123.47, 110.00]

adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
def loop():
    global notes
    global dev
    sine1 = SineOscillator(freq=440, phase=0, amp=1)
    square1 = SquareOscillator(freq=440, phase=0, amp=0.5)
    sawtooth1 = SawtoothOscillator()
    triangle1 = TriangleOscillator()
    
    allOscillators = [sine1, square1, sawtooth1, triangle1]
    oscillators = [square1]
    
    initializeOscillators(allOscillators)
    
    waveAdder = WaveAdder(oscillators)
    
    buttonIsPressed = False
    oscIndex = 0
    oscillators[0] = allOscillators[oscIndex]
    
    while True:
        if not buttonIsPressed:
           if GPIO.input(BUTTON_PIN)==GPIO.LOW:
               buttonIsPressed = True
               print(buttonIsPressed)
               oscIndex = oscIndex + 1
               oscIndex = oscIndex % len(allOscillators)
               oscillators[0] = allOscillators[oscIndex]
        else:
            if GPIO.input(BUTTON_PIN)==GPIO.HIGH:
                buttonIsPressed = False

        value = adc.analogRead(0)    # read the ADC value of channel 0
        arrIndex = math.floor(value / 15)
        note = notes[arrIndex]
                
        setNote(oscillators, note)        
                
        samples = my_get_samples(waveAdder)
        samples = np.int16(samples).tobytes()
        stream.write(samples)
        

def destroy():
    adc.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()