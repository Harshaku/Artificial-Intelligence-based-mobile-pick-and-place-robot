
import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)


while 1:
   kit.servo[0].angle = 92
   time.sleep(2)
   kit.servo[0].angle = 60
   time.sleep(3)
   break
   """kit.servo[0].angle = 130
   time.sleep(1)
   kit.servo[1].angle = 60
   time.sleep(1)
   kit.servo[1].angle = 28
   time.sleep(1)
   kit.servo[0].angle = 50
   time.sleep(1)
   kit.servo[1].angle = 60
   time.sleep(1)"""
    
