import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import time

# Less efficient on CPU: try events call back instead
# https://www.modmypi.com/blog/raspberry-pi-gpio-sensing-motion-detection

pir = MotionSensor(4)

print("Ready")

try:
  while True:
    pir.wait_for_motion()
    print("Motion detected")

    time.sleep(1)

except KeyboardInterrupt:
    print ("Quit")
