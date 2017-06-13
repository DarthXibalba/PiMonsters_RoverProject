"""
Created on 05/25/2017
Python 2.7.13

@author: Javier Urquizu
"""

import numpy as np
import os, sys
from time import sleep
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera

import object_tracking as objtrack



COLORS = [(0,0,255), (0,128,255), (0,255,255), (0,255,0), (255,0,0),    # Red, Orange, Yellow, Green, Blue
        (255,255,0), (255,0,128), (255,0,255), (150,50,255), (0,75,150)] # Cyan, Purple, Magenta, Rose, Brown

TEST_IMAGE_PATH = "../tf_classifier/ImageDataset/Capture/Pepsi/capture_pepsi_can_2.jpg"
CALIBRATION_SET_PATH = "../tf_classifier/ImageDataset/Calibration/"

'''
[[hsv_low], [hsv_high]]
<----- GARAGE CALIBRATION ----->
Coke:  [130, 100, 25], [179, 255, 255]
Pepsi: [85, 187, 68], [142, 255, 255]
Sprite:[67, 150, 14], [102, 255, 192]

<----- BOOKER CONF CALIBRATION ----->
Coke:  [130, 100, 25], [179, 255, 255]
Pepsi: [85, 187, 68], [142, 255, 255]
Sprite:[67, 150, 14], [102, 255, 192]
'''

HSV = {
'coke':  { 'lower':np.array([130, 100, 25]), 'upper':np.array([179, 255, 255]) },
'pepsi': { 'lower':np.array([85, 187, 68]), 'upper':np.array([142, 255, 255]) },
'sprite':{ 'lower':np.array([67, 150, 14]), 'upper':np.array([102, 255, 192]) },
'none':  { 'lower':np.array([0, 0, 0]),     'upper':np.array([179, 255, 255]) }
}

# Set global variables for windows and trackbars
HL = 'Hue Low'
HH = 'Hue High'
SL = 'Sat Low'
SH = 'Sat High'
VL = 'Value Low'
VH = 'Value High'
WND_TRACK= 'Colorbars'
WND_FILTER= 'Filtered Image Feed'
WND_LIVE = 'Live Feed'

WIDTH = 840
HEIGHT = 600
FRAMERATE = 30



def do_nothing():
    pass


def preview_calibration():
    camera = PiCamera()
    camera.resolution = (WIDTH,HEIGHT)
    camera.framerate = FRAMERATE
    
    rawCapture = PiRGBArray(camera, size=(WIDTH,HEIGHT))
    sleep(0.5)

    obj_class = 'none'
    
    for cam_frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        rawCapture.truncate()
        rawCapture.seek(0)
        
        frame = cam_frame.array        
        frame = cv2.GaussianBlur(frame, (5,5), 0)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get HSV range and mask
        hsv_low = HSV[obj_class]['lower']
        hsv_high = HSV[obj_class]['upper']
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


        cv2.imshow(WND_LIVE, frame)
        cv2.imshow(WND_FILTER, frame_filtered)

        key = cv2.waitKey(5)
        if (key == ord('c')):
            obj_class = 'coke'
        elif (key == ord('p')):
            obj_class = 'pepsi'
        elif (key == ord('s')):
            obj_class = 'sprite'
        elif (key == ord('n')):
            obj_class = 'none'
        elif (key == ord('q')):
            break


def preview_liveFeed():
    camera = PiCamera()
    camera.resolution = (WIDTH,HEIGHT)
    camera.framerate = FRAMERATE
    
    rawCapture = PiRGBArray(camera, size=(WIDTH,HEIGHT))
    sleep(0.5)
    
    for cam_frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        rawCapture.truncate()
        rawCapture.seek(0)
        
        frame = cam_frame.array
        height, width = frame.shape[:2]
        #frame = cv2.resize(frame, (width/2, height/2), interpolation=cv2.INTER_CUBIC)
        
        frame = cv2.GaussianBlur(frame, (5,5), 0)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow(WND_LIVE, frame)
        
        
        # Get trackbar positions
        hl = cv2.getTrackbarPos(HL, WND_TRACK)
        hh = cv2.getTrackbarPos(HH, WND_TRACK)
        sl = cv2.getTrackbarPos(SL, WND_TRACK)
        sh = cv2.getTrackbarPos(SH, WND_TRACK)
        vl = cv2.getTrackbarPos(VL, WND_TRACK)
        vh = cv2.getTrackbarPos(VH, WND_TRACK)
        
        # Get HSV range and mask
        hsv_low = np.array([hl, sl, vl])
        hsv_high = np.array([hh, sh, vh])
        hsv_mask = cv2.inRange(frame_hsv, hsv_low, hsv_high)
        
        # Display results
        frame_filtered = cv2.bitwise_and(frame, frame, mask=hsv_mask)
        cv2.imshow(WND_FILTER, frame_filtered)

        key = cv2.waitKey(5) 
        if (key == ord('q')):
            break
    
        


def preview_image(image_path): 
    # Reset trackbar positions
    cv2.setTrackbarPos(HL, WND_TRACK, 0)
    cv2.setTrackbarPos(HH, WND_TRACK, 179)
    cv2.setTrackbarPos(SL, WND_TRACK, 0)
    cv2.setTrackbarPos(SH, WND_TRACK, 255)
    cv2.setTrackbarPos(VL, WND_TRACK, 0)
    cv2.setTrackbarPos(VH, WND_TRACK, 255)
    
    while(1):
        # Keep rereading image
        frame = cv2.imread(image_path)
        frame = cv2.GaussianBlur(frame, (5,5), 0)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get trackbar positions
        hl = cv2.getTrackbarPos(HL, WND_TRACK)
        hh = cv2.getTrackbarPos(HH, WND_TRACK)
        sl = cv2.getTrackbarPos(SL, WND_TRACK)
        sh = cv2.getTrackbarPos(SH, WND_TRACK)
        vl = cv2.getTrackbarPos(VL, WND_TRACK)
        vh = cv2.getTrackbarPos(VH, WND_TRACK)
        
        # Get HSV range and mask
        hsv_low = np.array([hl, sl, vl])
        hsv_high = np.array([hh, sh, vh])
        hsv_mask = cv2.inRange(frame_hsv, hsv_low, hsv_high)
        
        # Display results
        frame_filtered = cv2.bitwise_and(frame, frame, mask=hsv_mask)
        cv2.imshow(WND_FILTER, frame_filtered)
        
        # Return hsv values or quit-code
        key = cv2.waitKey(5) 
        if (key == ord('s')):
            rtn = { 'code':'save', 'hsv_low':hsv_low, 'hsv_high':hsv_high}
            break
        elif (key == ord('q')):
            rtn = { 'code':'quit' }
            break
            
    return rtn
            

def calibrate_class(query_path):
    calib_dict = {}
    classes = os.listdir(query_path)
    for clss in classes:
        class_dict = {}
        print("\n"+clss)
        for imgFile in os.listdir(query_path +clss):
            print (imgFile)
            img_path = query_path +clss +"/" +imgFile
            
            rtn = preview_image(img_path)
            if (rtn['code'] == 'quit'):
                sys.exit(0)
            else:
                class_dict[imgFile.split(".")[0]] = { 'path':img_path, 'hsv_low':rtn['hsv_low'], 'hsv_high':rtn['hsv_high']}
                           
        # Find class avg hsv_low & hsv_high
        class_hsv_low = np.array([0,0,0])
        class_hsv_high = np.array([0,0,0])
        for img in class_dict.keys():
            class_hsv_low = class_hsv_low + class_dict[img]['hsv_low']
            class_hsv_high= class_hsv_high +class_dict[img]['hsv_high']

        class_dict['hsv_low'] = class_hsv_low / len(class_dict.keys())
        class_dict['hsv_high']= class_hsv_high/ len(class_dict.keys())
        
        calib_dict[clss] = class_dict      
    
    return calib_dict
        





if __name__ == '__main__':     
    # Create window and trackbars
    cv2.namedWindow(WND_FILTER, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(WND_TRACK, cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(WND_TRACK, 600, 360)
    
    cv2.createTrackbar(HL, WND_TRACK, 0, 179, do_nothing)
    cv2.createTrackbar(HH, WND_TRACK, 179, 179, do_nothing)
    cv2.createTrackbar(SL, WND_TRACK, 0, 255, do_nothing)
    cv2.createTrackbar(SH, WND_TRACK, 255, 255, do_nothing)
    cv2.createTrackbar(VL, WND_TRACK, 0, 255, do_nothing)
    cv2.createTrackbar(VH, WND_TRACK, 255, 255, do_nothing)
    
    #rtn = preview_image(TEST_IMAGE_PATH)
    #calib_dict = calibrate_class(CALIBRATION_SET_PATH)
    #preview_liveFeed()
    preview_calibration()
        
    cv2.destroyAllWindows()
   
        
