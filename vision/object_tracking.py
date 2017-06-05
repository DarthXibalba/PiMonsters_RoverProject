"""
Created on 06/04/2017
Python 2.7.13

@author: Javier Urquizu
"""

import numpy as np
import cv2


TEST_IMAGE_PATH = "../tf_classifier/ImageDataset/Calibration/Sprite/sprite_can_6.jpg"
hsv_high = np.array([128, 255, 255])
hsv_low = np.array([46, 100, 65])

COLORS = [(0,0,255), (0,128,255), (0,255,255), (0,255,0), (255,0,0)]   # Red, Orange, Yellow, Green, Blue


if __name__ == '__main__':
    image = cv2.imread(TEST_IMAGE_PATH)
    image = cv2.GaussianBlur(image, (5,5), 0)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Get mask
    mask_hsv = cv2.inRange(image_hsv, hsv_low, hsv_high)
    
    # Display results
    image_filtered = cv2.bitwise_and(image, image, mask = mask_hsv)
    image_drawCntr = image_filtered.copy()
    image_drawObjCntr = image.copy()
    cv2.imshow("Filtered Image", image_filtered)
    
    # Grayscale
    image_gray = cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale", image_gray)
    
    # Morphological Opening and Closing
    #kernel = np.ones((5,5))
    #image_opening1 = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, kernel)
    #image_closing1 = cv2.morphologyEx(image_opening1, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow("Cycle 1", image_closing1)
    

    # Find Contours and plot them by color
    _, contours, hierarchy = cv2.findContours(image_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for i in xrange(0,len(COLORS)):
            cv2.drawContours(image_drawCntr, contours[i::len(COLORS)], -1, COLORS[i], 3)
    cv2.imshow("All Contours", image_drawCntr)        
    

    # Remove Contour children
    # if hierarchy[0][i][2] == this contour's child if >= 0
    # if hierarchy[0][i][3] == this contour's parent if >= 0
    contourFilter = []
    for i in xrange(0, len(contours)):
        # Keep all parents that do not have parents (oldest ancestor)
        if (hierarchy[0][i][2] >= 0) and (hierarchy[0][i][3] == -1):
            contourFilter.append(contours[i])
            
        # Keep all contours that have no relatives
        elif (hierarchy[0][i][2] == -1) and (hierarchy[0][i][3] == -1):
            contourFilter.append(contours[i])
            
    # Find the object contour (should be the longest contour)
    obj_contour = sorted(contourFilter, key=len, reverse=True)[0]
    cv2.drawContours(image_drawObjCntr, obj_contour, -1, COLORS[3], 3)
    cv2.imshow("Object Contour", image_drawObjCntr)