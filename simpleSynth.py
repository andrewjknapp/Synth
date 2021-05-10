import math
import pyaudio
import itertools
import numpy as np

BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMP = 0.1

# -- HELPER FUNCTIONS --
def get_sin_oscillator(freq=55, amp=1, sample_rate=SAMPLE_RATE):
    increment = (2 * math.pi * freq)/ sample_rate
    return (math.sin(v) * amp * NOTE_AMP \
            for v in itertools.count(start=0, step=increment))

def get_samples(notes_dict, num_samples=BUFFER_SIZE):
    return [sum([int(next(osc) * 32767) \
            for _, osc in notes_dict.items()]) \
            for _ in range(num_samples)]

# -- INITIALIZION --

stream = pyaudio.PyAudio().open(
    rate=SAMPLE_RATE,
    channels=1,
    format=pyaudio.paInt16,
    output=True,
    frames_per_buffer=BUFFER_SIZE
)

# -- RUN THE SYNTH --
try:
    freq = 261
    print("Starting...")
    notes_dict = {}
    while True:
        if notes_dict:
            # Play the notes
            samples = get_samples(notes_dict)
            samples = np.int16(samples).tobytes()
            stream.write(samples)

        notes_dict["note"] = get_sin_oscillator(freq=freq, amp=127/127)
            

                    
except KeyboardInterrupt as err:
    #midi_input.close()
    stream.close()
    print("Stopping...")