from time import sleep
import cv2
import os
import numpy as np
import imutils
import RPi.GPIO as GPIO

cam = cv2.VideoCapture(0)
run=1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

MOTOR1B=20  #Left Motor
MOTOR1E=21   

MOTOR2B=16  #Right Motor
MOTOR2E=12



GPIO.setup(MOTOR1B, GPIO.OUT)
GPIO.setup(MOTOR1E, GPIO.OUT)

GPIO.setup(MOTOR2B, GPIO.OUT)
GPIO.setup(MOTOR2E, GPIO.OUT)


def reverse():
     
      GPIO.output(MOTOR1B, GPIO.HIGH)
      GPIO.output(MOTOR1E, GPIO.LOW)
      GPIO.output(MOTOR2B, GPIO.HIGH)
      GPIO.output(MOTOR2E, GPIO.LOW)
      
     
def forward():
      GPIO.output(MOTOR1B, GPIO.LOW)
      GPIO.output(MOTOR1E, GPIO.HIGH)
      GPIO.output(MOTOR2B, GPIO.LOW)
      GPIO.output(MOTOR2E, GPIO.HIGH)
      
def right():
    

      GPIO.output(MOTOR1B,GPIO.LOW)
      GPIO.output(MOTOR1E,GPIO.HIGH)
      GPIO.output(MOTOR2B,GPIO.HIGH)
      GPIO.output(MOTOR2E,GPIO.LOW)
      #time.sleep(0.1)
      #print("right")
     
def left():
     

      GPIO.output(MOTOR1B,GPIO.HIGH)
      GPIO.output(MOTOR1E,GPIO.LOW)
      GPIO.output(MOTOR2B,GPIO.LOW)
      GPIO.output(MOTOR2E,GPIO.HIGH)
      #print("left ")
      #time.sleep(0.1)
def stop():
      GPIO.output(MOTOR1E,GPIO.LOW)
      GPIO.output(MOTOR1B,GPIO.LOW)
      GPIO.output(MOTOR2E,GPIO.LOW)
      GPIO.output(MOTOR2B,GPIO.LOW)
      #print("stop") 


def color_segment_pick(img):
    global des
    global mask_1
    frame=img
    hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #mask_1 = cv2.inRange(hsv_roi, np.array([36, 203, 27]), np.array([109, 255, 255])) # green colour [[33, 92, 0], [93, 255, 255]] [[68, 152, 51], [68, 152, 51]
    #mask_11=cv2.inRange(hsv_roi, np.array([70, 177, 10]), np.array([92, 255, 255]))
    #yellow [[23, 88, 110], [179, 255, 255]]
    print("color",des)
    if(des==0):
          #mask_1 = cv2.inRange(hsv_roi, np.array([70, 200, 92]), np.array([120, 255, 243]))
          mask_1 = cv2.inRange(hsv_roi, np.array([80, 129, 45]), np.array([126, 255, 245]))  #[84, 129, 45, 126, 255, 255]
    elif(des==1):
          #mask_1 = cv2.inRange(hsv_roi, np.array([33, 92, 0]), np.array([93, 255, 255])) #[62, 63, 0], [179, 255, 255]  [63, 132, 52, 94, 255, 185]
          mask_1 = cv2.inRange(hsv_roi, np.array([22, 134, 12]), np.array([93, 255, 255])) #[22, 134, 12, 93, 255, 255]
    mask1 = mask_1 
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, kernel)
    mask1 = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('mask',mask1)
    return mask1

def find_contour(mask1):
    global largest_contour
    global cont_index

    contours, hierarchy = cv2.findContours(mask1,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area=cv2.contourArea(contour)
        #print('ar',area)
        if (area >50) :
            if(area>largest_contour):
                largest_contour=area
            else:
                largest_contour=area
           
        cont_index=idx

        #print('LC',largest_contour)                   
    r=(0,0,2,2)
    if len(contours) > 0:
        r = cv2.boundingRect(contours[cont_index])
        #print('LC',r) 
    
    return r,largest_contour

largest_contour=0
cont_index=0
found=0
des=0
left_stat=0
right_stat=0
w_max=108


#reverse()
#sleep(1)
#stop()
while(run):
    global centre_x
    global centre_y
    global mask
    
    _,img= cam.read()
    img=cv2.resize(img,(254,254),interpolation=cv2.INTER_AREA)
    img=cv2.flip(img,0)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.imshow('Live',img)
    cv2.imshow('hsv',hsv)

    mask=color_segment_pick(img)
    
    loct,area= find_contour(mask)
    x,y,w,h=loct
    #print(w)
    if(w<25):
        found=0
        if(left_stat==1 and des==0):
            right()
            sleep(0.01)
            stop()
        elif(right_stat==1 and des==0):
            left()
            sleep(0.01)
            stop()
        if(left_stat==1 and des==1):
            right()
            sleep(0.02)
            stop()
        elif(right_stat==1 and des==1):
            left()
            sleep(0.02)
            stop()
        else:
            stop()
        
        #print('x',x)
    else:
        found=1
        cv2.rectangle(img, (x,y), (x+w,y+h), 255,2)
        centre_x=x+((w)/2)
        centre_y=y+((h)/2)
        cv2.circle(img,(int(centre_x),int(centre_y)),3,(0,110,255),-1)
        #centre_x-=80
        #centre_y=6--centre_y
        #print('centre',centre_x)
    
    if(found ==1 and des==0):
        print(w)
        if(w>w_max and w<(w_max+20)):
            
            if(centre_x>128):
                print('left')
                left()
                sleep(0.01)
                stop()
            elif(centre_x<126):
                print('right')
                right()
                sleep(0.01)
                stop()
            if(centre_x>=126 and centre_x<=128):
                
                print('stop')
                stop()
                #break
                os.system('python final_1.py')
                os.system('python final_1.py')
                os.system('python pickk.py')
                des=1
                found=0
        elif(w>(w_max+20)):
                reverse()
                sleep(0.01)
                stop()
                    
            
        elif(w<w_max):
            if(centre_x>122 and centre_x<130):
                print('forward')
                forward()
            elif(centre_x>130):
                print('left')
                left()
                left_stat=1
                right_stat=0
                sleep(0.03)
                stop()
                forward()
            elif(centre_x<122):
                print('right')
                right()
                left_stat=0
                right_stat=1
                sleep(0.03)
                stop()
                forward()
    elif(found ==1 and des==1):
              print(w)
              if(w>w_max and w<(w_max+20)):
                  
                  if(centre_x>120):
                      print('left')
                      left()
                      sleep(0.01)
                      stop()
                  elif(centre_x<130):
                      print('right')
                      right()
                      sleep(0.01)
                      stop()
                  if(centre_x>120 and centre_x<134):
                      
                      print('stop')
                      stop()
                      reverse()
                      sleep(0.5)
                      print('stop')
                      stop()
                      os.system('python place.py')
                      des=2
              elif(w>(w_max+20)):
                      reverse()
                      sleep(0.01)
                      stop()
                  
              elif(w<w_max):
                  if(centre_x>122 and centre_x<130):
                      print('forward')
                      forward()
                  elif(centre_x>130):
                      print('left')
                      left()
                      left_stat=1
                      right_stat=0
                      sleep(0.05)
                      stop()
                      forward()
                  elif(centre_x<122):
                      print('right')
                      right()
                      left_stat=0
                      right_stat=1
                      sleep(0.05)
                      stop()
                      forward()
              



    
    
    cv2.imshow('mask',mask)
    cv2.imshow('Live',img)
    
    k=cv2.waitKey(1)
    if(k==27):
        cv2.destroyAllWindows()
        cam.release()
        GPIO.cleanup()
        break
