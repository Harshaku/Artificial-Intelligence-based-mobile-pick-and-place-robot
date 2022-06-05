from time import sleep
import cv2
import os
import numpy as np
import imutils

cam = cv2.VideoCapture(0)
run=1




def color_segment_pick(img):
    frame=img
    hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ycr_roi=cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)
    mask_1 = cv2.inRange(hsv_roi, np.array([44, 54,63]), np.array([90,255,255])) # green colour
    mask_2=cv2.inRange(ycr_roi, np.array((0.,165.,165.)), np.array((255.,255.,255.))) # green ,brown and orange colour
    mask = mask_1 | mask_2
    kern_dilate = np.ones((8,8),np.uint8)
    kern_erode  = np.ones((3,3),np.uint8)
    mask= cv2.erode(mask,kern_erode)      #Eroding
    mask=cv2.dilate(mask,kern_dilate)     #Dilating
    cv2.imshow('mask',mask)
    return mask

def find_contour(mask):
    global largest_contour
    global cont_index

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
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
while(run):
    global centre_x
    global centre_y
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
    if(w<10):
        found=0
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

        if(w>60):
            
            if(centre_x>128):
                print('left')
            elif(centre_x<126):
                print('right')
            if(centre_x>126 and centre_x<128):
                des=1
                print('stop')
            
        elif(w<100):
            if(centre_x>126 and centre_x<128):
                print('forward')
            elif(centre_x>128):
                print('left')
            elif(centre_x<126):
                print('right')
        
            
    
    
    cv2.imshow('mask',mask)
    cv2.imshow('Live',img)
    
    k=cv2.waitKey(1)
    if(k==27):
        cv2.destroyAllWindows()
        cam.release()
        break
