import time
import os
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
#kit.servo[1].angle = 80
#kit.servo[2].angle = 30
#kit.servo[0].angle = 90
#kit.servo[4].angle = 90
time.sleep(.1)

def close():
      for x in range(50, 150, 1):
            kit.servo[4].angle = x
            time.sleep(0.01)
      kit.servo[4].angle = 150
def open():
      for x in range(150, 50, -1):
            kit.servo[4].angle = x
            time.sleep(0.01)     
def up():
      for x in range(120,80, -1):
            kit.servo[1].angle = x
            time.sleep(0.01)      
def down():
      for x in range(80, 120, 1):
            kit.servo[1].angle = x
            time.sleep(0.01)
def up1():
      for x in range(30, 80, 1):
            kit.servo[2].angle = x
            time.sleep(0.01)
def down1():
      
      for x in range(80,30, -1):
            kit.servo[2].angle = x
            time.sleep(0.01)      
def center():
      for x in range(175, 90, -1):
            kit.servo[0].angle = x
            time.sleep(0.01)      
def right():
      for x in range(90, 175, 1):
            kit.servo[0].angle = x
            time.sleep(0.01)


            time.sleep(0.01)

open()
print('opened')
up()
center()
print('centred')
time.sleep(0.2)
down()
time.sleep(5)
close()
time.sleep(0.5)
up()
time.sleep(0.5)
up1()
time.sleep(0.5)
right()


