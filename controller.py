from sine_oscillator import SineOscillator

x = SineOscillator(freq=440)
x._post_freq_set()
x._post_phase_set()
x._initialize_osc()

for y in range(50):
    print(next(x))

    