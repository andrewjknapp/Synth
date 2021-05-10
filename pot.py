import time
import math
from ADCDevice import *
from  soundplayer import SoundPlayer
import time

dev = 0
#SoundPlayer.playTone(900, 0.1, True, dev)
#time.sleep(1)
#print("Done")

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
        
def loop():
    global notes
    global dev
    while True:
        value = adc.analogRead(0)    # read the ADC value of channel 0
        #voltage = value / 255.0 * 3.3  # calculate the voltage value
        arrIndex = math.floor(value / 15)
        note = notes[arrIndex]
        print ('Freq : %.2f'%(note))
        if not SoundPlayer.isPlaying():
            SoundPlayer.playTone(note, 1, True, dev)
        
        #print ('ADC Value : %d, Voltage : %.2f, Index : %d'%(value,voltage, arrIndex))
        

def destroy():
    adc.close()
    
if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()