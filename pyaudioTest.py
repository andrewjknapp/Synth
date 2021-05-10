import pyaudio

BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMP = 0.1

stream = pyaudio.PyAudio().open(
    rate=SAMPLE_RATE,
    channels=1,
    format=pyaudio.paInt16,
    output=True,
    frames_per_buffer=BUFFER_SIZE
)

stream.close()