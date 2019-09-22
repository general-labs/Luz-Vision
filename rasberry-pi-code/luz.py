# Luz Vision Hardware Device
# Rasberry Pi with Cloud AI (Artificial Intelligence)
# Author: Didarul

from picamera import PiCamera
import RPi.GPIO as GPIO
import os
import requests
import base64
import pyttsx3
import time

path_img='image.jpg'
endpoint_obj = 'http://XXXXXXXXX/predict_image'
endpoint_scene = 'http://XXXXXXXXX/image_caption'

camera = PiCamera()
engine = pyttsx3.init()

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 40)     # setting up new voice rate

"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)  

def button_callback(channel):
    print("Button was pushed!")
    camera.capture(path_img)

    encoded_string = ""
    with open(path_img, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        r = requests.post(endpoint_obj, data={'url': encoded_string})
        result=r.json()
        print(result['Prediction'])
        engine.say(result['Prediction'])
        engine.runAndWait()

        r = requests.post(endpoint_scene, data={'url': encoded_string})
        result=r.json()
        print(result['captions'][0])
        engine.say(result['captions'][0])
        engine.runAndWait()
        time.sleep(.500)

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up

message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up
