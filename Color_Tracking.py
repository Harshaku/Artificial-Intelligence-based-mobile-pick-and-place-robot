#Importing Necessary Library
import time
import cv2
import numpy as np

def track_loc(frame,val):
    hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#HSV Hue, Saturaion, Value 
     

    mask_1 = cv2.inRange(hsv_roi, np.array([160, 160,10]), np.array([190,255,255])) # red colour 


    mask = mask_1 
    kern_dilate = np.ones((8,8),np.uint8)
    kern_erode  = np.ones((3,3),np.uint8)
    mask= cv2.erode(mask,kern_erode)      #Eroding
    mask=cv2.dilate(mask,kern_dilate)     #Dilating
    cv2.imshow('mask',mask)
    return mask

def find_blob(blob): #returns the red colored circle
    largest_contour=0
    cont_index=0
    contours, hierarchy = cv2.findContours(blob,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for idx, contour in enumerate(contours):
        area=cv2.contourArea(contour)
       
        if (area >largest_contour) : 
            largest_contour=area
           
            cont_index=idx
            
    r=(0,0,2,2)
    if len(contours) > 0:
        r = cv2.boundingRect(contours[cont_index])
       
    return r,largest_contour

time.sleep(0.001)
cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

run =1
trac_val=0
while (run):
    global center_x,center_y
    _,img = cam.read()
    img=cv2.flip(img,1)
    center_x=0
    center_y=0
    
    tracked_output=track_loc(img,trac_val)

    loct,area=find_blob(tracked_output)
    x,y,w,h=loct
    #print(x)
    


    if (w*h) < 100:
        found=0

    else:
        found=1
        simg2 = cv2.rectangle(img, (x,y), (x+w,y+h), 255,2)
        center_x=x+(w/2)
        center_y=y+(h/2)
        cv2.circle(img,(int(center_x),int(center_y)),3,(0,255,0),-2)
        center_x-=88
        
        
        #center_y=6--center_y

        #directions
        if x>0 and x<640/3:
            print ('right')
        elif x>=640/3 and x<1280/3:
            print ('middle')
        else:
            print ('left')

    cv2.imshow("Tracking",img)    

    if(cv2.waitKey(1) & 0xff == 27):# Press ESC to break the while
        break

cam.release()
cv2.destroyAllWindows()
