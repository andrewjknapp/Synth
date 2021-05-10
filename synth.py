import RPi.GPIO as IO
# from gpiozero import TonalBuzzer
# from gpiozero.tones import Tone
import time

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(19, IO.OUT)

p = IO.PWM(19, 100)

p.start(0)

tone = 100
sleepTime = 0.5

while 1:
    for x in range(tone):
        p.ChangeDutyCycle(x)
        time.sleep(sleepTime)

    for x in range(tone):
        p.ChangeDutyCycle(tone-x)
        time.sleep(sleepTime)

# buzzer = TonalBuzzer(18)

# while True:
#     buzzer.play(Tone("A4"))
#     sleep(1)
#     buzzer.off()
#     sleep(1)