import RPi.GPIO as GPIO
from gpiozero import LED
import time

BUTTON_IN_NUMBER = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(BUTTON_IN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prev_button_status = GPIO.LOW
while True:
  button_status = GPIO.input(BUTTON_IN_NUMBER)
  if(button_status != prev_button_status):
      print("New button status!", button_status)
      prev_button_status = button_status
  time.sleep(0.1)
  
