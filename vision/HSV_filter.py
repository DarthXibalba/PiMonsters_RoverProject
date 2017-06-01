"""
Created on 05/25/2017
Python 2.7.13

@author: Javier Urquizu
"""

import numpy as np
import cv2


TEST_IMAGE_PATH = "../tf_classifier/ImageDataset/Capture/capture_pepsi_can_2.jpg"

def do_nothing():
    pass


if __name__ == '__main__':     
    HL = 'Hue Low'
    HH = 'Hue High'
    SL = 'Sat Low'
    SH = 'Sat High'
    VL = 'Value Low'
    VH = 'Value High'
    WND_TRACK= 'Colorbars'
    WND_FRAME= 'Image Feed'
    
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
    
    # Begin loop
    while(1):
        # Read next frame (or keep rereading image)
        frame = cv2.imread(TEST_IMAGE_PATH)
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
        
        key = cv2.waitKey(5)
        if key == ord('q'):
            break;
            
    cv2.destroyAllWindows()
        
        