import RPi.GPIO as GPIO
from gpiozero import LED, Button
import time

# GPIO pin numbers
RED_PIN_NUMBER = 23
AMBER_PIN_NUMBER = 24
GREEN_PIN_NUMBER = 25
BUTTON_PIN_NUMBER = 4

button = Button(BUTTON_PIN_NUMBER, pull_up = False)
red_led = LED(RED_PIN_NUMBER)
amber_led = LED(AMBER_PIN_NUMBER)
green_led = LED(GREEN_PIN_NUMBER)

traffic_lights_on = True
                           
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

def test_on():
    print("Turning all lights on")
    red_led.on()
    amber_led.on()
    green_led.on()

def test_off():
    print("Turning all lights off")
    red_led.off()
    amber_led.off()
    green_led.off()

def run_traffic_lights(traffic_lights_should_be_running):
  if(traffic_lights_should_be_running):
    test_on()
    time.sleep(3)
    test_off()
    time.sleep(3)
  else:
    test_off()

def respond_to_button_press():
    print("Button was pressed...")
    traffic_lights_on = not traffic_lights_on
    if traffic_lights_on:
        print("Starting the traffic lights application")
    else:
        print("Stopping the traffic lights application")
    run_traffic_lights(traffic_lights_on)
                    


while True:
  #run_traffic_lights(traffic_lights_on)
  button.when_pressed = lambda : respond_to_button_press()

