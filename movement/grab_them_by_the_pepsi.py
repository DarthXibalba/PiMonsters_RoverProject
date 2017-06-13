"""
Created on 06/10/2017
Python 2.7.13

@author: Javier Urquizu
"""

import numpy as np
import os, sys
from time import sleep
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
import Adafruit_PCA9685

sys.path.append('../vision/')
import object_tracking as objtrack
import RPiArm



COLORS = [(0,0,255), (0,128,255), (0,255,255), (0,255,0), (255,0,0),    # Red, Orange, Yellow, Green, Blue
        (255,255,0), (255,0,128), (255,0,255), (150,50,255), (0,75,150)] # Cyan, Purple, Magenta, Rose, Brown

HSV = {
'coke':  { 'lower':np.array([130, 100, 25]), 'upper':np.array([179, 255, 255]) },
'pepsi': { 'lower':np.array([85, 187, 68]), 'upper':np.array([142, 255, 255]) },
'sprite':{ 'lower':np.array([67, 150, 14]), 'upper':np.array([102, 255, 192]) }
}

WIDTH = 640 #840
HEIGHT = 480 #600
FRAMERATE = 30

WND_FILTER= 'Filtered Image Feed'
WND_LIVE = 'Live Feed'

WAIT_SEC = 0.1


def find_obj_in_feed():
    obj_classes = HSV.keys()
    classIdx = 0
    for cam_frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        rawCapture.truncate()
        rawCapture.seek(0)
        
        frame = cam_frame.array
        frame = cv2.warpAffine(frame, rotMat, (WIDTH, HEIGHT))
        frame = cv2.GaussianBlur(frame, (5,5), 0)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get HSV range and mask
        hsv_low = HSV[obj_classes[classIdx]]['lower']
        hsv_high = HSV[obj_classes[classIdx]]['upper']
        hsv_mask = cv2.inRange(frame_hsv, hsv_low, hsv_high)
        frame_filtered = cv2.bitwise_and(frame, frame, mask=hsv_mask)

        # Find ROI and draw results onto image
        ROI = objtrack.findROI(frame, hsv_mask)
        if (ROI.has_key('obj_contour')):
            print("Contour length = " + str(len(ROI['obj_contour'])))
            cv2.drawContours(frame_filtered, ROI['obj_contour'], -1, COLORS[3], thickness=3)

            [x,y,w,h] = ROI['boundingRect']
            print("x = " +str(x) +"\ny= " +str(y) +"\nw = " +str(w) +"\nh = " + str(h) +"\n") 
            cv2.rectangle(frame_filtered, (x,y), (x+w,y+h), COLORS[0], thickness=3)

            box = cv2.boxPoints(ROI['rotatedRect'])
            box = np.int0(box)
            cv2.drawContours(frame_filtered, [box], -1, COLORS[1], thickness=3)
            return obj_classes[classIdx]

        # If nothing is detected, switch to the next HSV filter
        else:
            classIdx = (classIdx +1) % len(obj_classes)


        cv2.imshow(WND_LIVE, frame)
        cv2.imshow(WND_FILTER, frame_filtered)

        key = cv2.waitKey(5)
        if (key == ord('q')):
            on_exit()

def align_base(detectedClass):
    hsv_low = HSV[detectedClass]['lower']
    hsv_high = HSV[detectedClass]['upper']

    for cam_frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        rawCapture.truncate()
        rawCapture.seek(0)
        
        frame = cam_frame.array
        frame = cv2.warpAffine(frame, rotMat, (WIDTH, HEIGHT))
        frame = cv2.GaussianBlur(frame, (5,5), 0)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get HSV range and mask
        hsv_mask = cv2.inRange(frame_hsv, hsv_low, hsv_high)
        frame_filtered = cv2.bitwise_and(frame, frame, mask=hsv_mask)

        # Find ROI and draw results onto image
        ROI = objtrack.findROI(frame, hsv_mask)
        if (ROI.has_key('obj_contour')):
            cv2.drawContours(frame_filtered, ROI['obj_contour'], -1, COLORS[3], thickness=3)

            [x,y,w,h] = ROI['boundingRect']
            print("x = " +str(x) +"\ny= " +str(y) +"\nw = " +str(w) +"\nh = " + str(h)) 
            cv2.rectangle(frame_filtered, (x,y), (x+w,y+h), COLORS[0], thickness=3)

            box = cv2.boxPoints(ROI['rotatedRect'])
            box = np.int0(box)
            cv2.drawContours(frame_filtered, [box], -1, COLORS[1], thickness=3)

            # Calculate base rotation needed for alignment
            obj_ctr = [x + w/2, y + h/2]
            print("object center = [" +str(obj_ctr[0]) +" , " +str(obj_ctr[1]) +"]\n")

            if (obj_ctr[0] < WND_CTR[0] - WND_BUFF[0]):
                arm.align_base("left")
            elif (obj_ctr[0] > WND_CTR[0] + WND_BUFF[0]):
                arm.align_base("right")
            else:
                return 0

        cv2.imshow(WND_LIVE, frame)
        cv2.imshow(WND_FILTER, frame_filtered)

        key = cv2.waitKey(5)
        if (key == ord('q')):
            on_exit()

    

def on_exit():
    cv2.destroyAllWindows()
    arm.reset_all()
    sys.exit(0)


if __name__ == '__main__':     
    camera = PiCamera()
    camera.resolution = (WIDTH,HEIGHT)
    camera.framerate = FRAMERATE

    rotMat = cv2.getRotationMatrix2D((WIDTH/2, HEIGHT/2), -90, 1)
    
    rawCapture = PiRGBArray(camera, size=(WIDTH,HEIGHT))
    sleep(0.5)

    WND_CTR = [WIDTH/2, HEIGHT/2]
    WND_BUFF = [WIDTH/50, HEIGHT/50]

    arm = RPiArm.RPiArm()
    arm.reset_all()

    while(True):
        obj_class = find_obj_in_feed()
        align_base(obj_class)
        sleep(WAIT_SEC)
        
        arm.pick_up()
        sleep(WAIT_SEC)
        arm.stand_up()
        sleep(WAIT_SEC) 
        
        if (obj_class == 'coke'):
            arm.drop_can("left")
        elif (obj_class == 'pepsi'):
            arm.drop_can("center")
        elif (obj_class == 'sprite'):
            arm.drop_can("right")
            
        sleep(WAIT_SEC)
        arm.reset_all()
        
    
   
        
