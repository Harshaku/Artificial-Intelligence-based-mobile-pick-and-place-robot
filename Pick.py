import time
import os
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
#kit.servo[1].angle = 40
#kit.servo[2].angle = 120
#kit.servo[0].angle = 0
kit.servo[4].angle = 140
time.sleep(.1)

def close():
      for x in range(50, 150, 1):
            kit.servo[4].angle = x
            time.sleep(0.01)

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
      for x in range(60, 80, 1):
            kit.servo[2].angle = x
            time.sleep(0.01)
def down1():
      
      for x in range(80,60, -1):
            kit.servo[2].angle = x
            time.sleep(0.01)      
def center():
      for x in range(175, 80, -1):
            kit.servo[0].angle = x
            time.sleep(0.01)      
def right():
      for x in range(80, 175, 1):
            kit.servo[0].angle = x
            time.sleep(0.01)

open()
print('opened')
time.sleep(0.2)
center()
print('centred')
time.sleep(0.2)
down1()
print('down1')
time.sleep(0.2)
down()
print('down')
time.sleep(5)
close()
print('picked')
time.sleep(0.2)
up()
print('up')
time.sleep(0.2)
up1()
print('up1')
time.sleep(0.2)
right()
print('right')
#center()
#os.system("python3 place.py")
