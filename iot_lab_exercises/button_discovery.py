import RPi.GPIO as GPIO
from gpiozero import LED, Button
import time

button4 = Button(4, pull_up = False)

button4.wait_for_press()
print("Pressed!")
button4.wait_for_press()
print("Pressed!")

