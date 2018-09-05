import RPi.GPIO as GPIO
from gpiozero import LED
import time

# GPIO pin numbers
RED_PIN_NUMBER = 16
AMBER_PIN_NUMBER = 18
GREEN_PIN_NUMBER = 22

BUTTON_IN_NUMBER = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(RED_PIN_NUMBER, GPIO.OUT)
GPIO.setup(GREEN_PIN_NUMBER, GPIO.OUT)
GPIO.setup(AMBER_PIN_NUMBER, GPIO.OUT)

GPIO.setup(BUTTON_IN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#red_led = LED(RED_PIN_NUMBER)

                           
def lights_go_green():
  print("Lights go green")
  print("Turning amber LED on...")
  GPIO.output(AMBER_PIN_NUMBER, GPIO.HIGH)
  time.sleep(2)
  print("Turning amber LED off...")
  GPIO.output(AMBER_PIN_NUMBER, GPIO.LOW)
  print("Turning red LED off...")
  # GPIO.output(RED_PIN_NUMBER, GPIO.LOW)
  #red_led.on()
  print("Turning green LED on...")
  GPIO.output(GREEN_PIN_NUMBER, GPIO.HIGH)

def lights_go_red():
  print("Lights go red")
  print("Turning green LED off...")
  GPIO.output(GREEN_PIN_NUMBER, GPIO.LOW)
  print("Turning amber LED on...")
  GPIO.output(AMBER_PIN_NUMBER, GPIO.HIGH)
  time.sleep(2)
  print("Turning amber LED off...")
  GPIO.output(AMBER_PIN_NUMBER, GPIO.LOW)
  print("Turning red LED on...")
  GPIO.output(RED_PIN_NUMBER, GPIO.HIGH)

def run_traffic_lights():
  lights_go_green()
  time.sleep(3)
  lights_go_red()
  time.sleep(3)

def respond_to_button_press():
  print("Checking button")
  if GPIO.input(BUTTON_IN_NUMBER) == GPIO.HIGH:
    print("Button was pushed!")
  if GPIO.input(BUTTON_IN_NUMBER) == GPIO.LOW:
    print("Button was not pushed!")

prev_button_status = GPIO.LOW
while True:
  button_status = GPIO.input(BUTTON_IN_NUMBER)
  if(button_status != prev_button_status):
      print("New button status!", button_status)
      prev_button_status = button_status
  time.sleep(0.1)
  

  


  #if GPIO.input(BUTTON_IN_NUMBER) == GPIO.HIGH:
  #  print("Button was pushed!")
    #run_traffic_lights()
  #if GPIO.input(BUTTON_IN_NUMBER) == GPIO.LOW:
  #  print("Button not pressed: halting traffic lights")
    
  
  #respond_to_button_press()
  #lights_go_green()
  #time.sleep(3)
  #lights_go_red()
  #time.sleep(3)


