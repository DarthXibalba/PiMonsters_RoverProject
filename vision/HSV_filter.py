"""
Created on 05/25/2017
Python 2.7.13

@author: Javier Urquizu
"""

import numpy as np
import os, sys
import cv2


TEST_IMAGE_PATH = "../tf_classifier/ImageDataset/Capture/Pepsi/capture_pepsi_can_2.jpg"
CALIBRATION_SET_PATH = "../tf_classifier/ImageDataset/Calibration/"

'''
[[hsv_low], [hsv_high]]
Coke:  [119, 101, 134], [113, 218, 209]
Pepsi: [73, 40, 56], [123, 201, 201]
Sprite:[51, 62, 53], [101, 195, 168] 
'''

# Set global variables for windows and trackbars
HL = 'Hue Low'
HH = 'Hue High'
SL = 'Sat Low'
SH = 'Sat High'
VL = 'Value Low'
VH = 'Value High'
WND_TRACK= 'Colorbars'
WND_FRAME= 'Image Feed'



def do_nothing():
    pass

def preview_liveFeed():
    pass


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
        cv2.imshow(WND_FRAME, frame_filtered)
        
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
    cv2.namedWindow(WND_FRAME, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(WND_TRACK, cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(WND_TRACK, 600, 360)
    
    cv2.createTrackbar(HL, WND_TRACK, 0, 179, do_nothing)
    cv2.createTrackbar(HH, WND_TRACK, 179, 179, do_nothing)
    cv2.createTrackbar(SL, WND_TRACK, 0, 255, do_nothing)
    cv2.createTrackbar(SH, WND_TRACK, 255, 255, do_nothing)
    cv2.createTrackbar(VL, WND_TRACK, 0, 255, do_nothing)
    cv2.createTrackbar(VH, WND_TRACK, 255, 255, do_nothing)
    
    rtn = preview_image(TEST_IMAGE_PATH)
    #calib_dict = calibrate_class(CALIBRATION_SET_PATH)
            
    cv2.destroyAllWindows()
   
        