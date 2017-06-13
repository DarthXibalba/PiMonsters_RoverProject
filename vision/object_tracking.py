"""
Created on 06/04/2017
Python 2.7.13

@author: Javier Urquizu
"""

import numpy as np
import cv2


TEST_IMAGE_PATH = "../tf_classifier/ImageDataset/Calibration/Pepsi/capture_pepsi_can_2.jpg"
#TEST_IMAGE_PATH = "../tf_classifier/ImageDataset/Calibration/Pepsi/pepsi_can_6.jpg"

hsv_high = np.array([128, 255, 255])
hsv_low = np.array([46, 100, 65])

COLORS = [(0,0,255), (0,128,255), (0,255,255), (0,255,0), (255,0,0),    # Red, Orange, Yellow, Green, Blue
                  (255,255,0), (255,0,128), (255,0,255), (150,50,255), (0,75,150)] # Cyan, Purple, Magenta, Rose, Brown



def findROI(image, mask_hsv):   
    # Create some copies for displaying later
    image_filtered = cv2.bitwise_and(image, image, mask = mask_hsv)
    image_gray = cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY)

    # Morphological Opening and Closing
    kernel = np.ones((7,7))
    image_gray = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, kernel)
    image_gray = cv2.morphologyEx(image_gray, cv2.MORPH_CLOSE, kernel)     

    # Find All Contours & Remove Contour children
    # if hierarchy[0][i][2] == this contour's child if >= 0
    # if hierarchy[0][i][3] == this contour's parent if >= 0
    _, contours, hierarchy = cv2.findContours(image_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  
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
    #cv2.drawContours(image_drawObjCntr, obj_contour, -1, COLORS[3], thickness=3)

    # Fit rectangles
    x,y,w,h = cv2.boundingRect(obj_contour)
    #cv2.rectangle(image_fitShapes, (x,y), (x+w,y+h), COLORS[0], thickness=3)
    
    rotatedRect = cv2.minAreaRect(obj_contour)
    #box = cv2.boxPoints(rotatedRect)
    #box = np.int0(box)
    #cv2.drawContours(image_fitShapes, [box], -1, COLORS[1], thickness=3)

    rtn = {
        'obj_contour': obj_contour,
        'boundingRect': [x,y,w,h],
        'rotatedRect': rotatedRect
    }
    return rtn



def findROI_demo(image_path, hsv_high, hsv_low, saveBoundingRect=False, displayResults=False):
    image = cv2.imread(image_path)
    image = cv2.GaussianBlur(image, (5,5), 0)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask_hsv = cv2.inRange(image_hsv, hsv_low, hsv_high)    # Get mask
    
    # Create some copies for displaying later
    image_filtered = cv2.bitwise_and(image, image, mask = mask_hsv)
    image_gray = cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY)
    image_drawCntr = image_filtered.copy()
    image_drawObjCntr = image.copy()    
    
    
    # Morphological Opening and Closing
    #kernel = np.ones((5,5))
    #image_opening1 = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, kernel)
    #image_closing1 = cv2.morphologyEx(image_opening1, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow("Cycle 1", image_closing1)
    
    
    # Find Contours and plot them by color
    _, contours, hierarchy = cv2.findContours(image_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for i in xrange(0,len(COLORS)):
            cv2.drawContours(image_drawCntr, contours[i::len(COLORS)], -1, COLORS[i], thickness=3)
           
    
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
    cv2.drawContours(image_drawObjCntr, obj_contour, -1, COLORS[3], thickness=3)
    
    # Fill in object contour - Maybe not needed
    #image_object = image_gray.copy()
    #cv2.fillPoly(image_object, pts=[obj_contour], color=255)
    
    # Fit rotated rectangle and ellipse
    image_fitShapes = image.copy()
    x,y,w,h = cv2.boundingRect(obj_contour)
    cv2.rectangle(image_fitShapes, (x,y), (x+w,y+h), COLORS[0], thickness=3)
    
    rotatedRect = cv2.minAreaRect(obj_contour)
    box = cv2.boxPoints(rotatedRect)
    box = np.int0(box)
    cv2.drawContours(image_fitShapes, [box], -1, COLORS[1], thickness=3)
    
    minEllipse = cv2.fitEllipse(obj_contour)
    cv2.ellipse(image_fitShapes, minEllipse, COLORS[2], thickness=3)
    
    if (saveBoundingRect):
        boundedRect = image[y:y+h, x:x+w, :]
        cv2.imwrite("boundedRectangle.jpg", boundedRect)
    
    if (displayResults):
        cv2.imshow("Original Image", image)
        cv2.waitKey(0)
        cv2.imshow("Filtered Image", image_filtered)
        cv2.waitKey(0)
        cv2.imshow("Grayscale", image_gray)
        cv2.waitKey(0)
        cv2.imshow("All Contours", image_drawCntr) 
        cv2.waitKey(0)
        cv2.imshow("Object Contour", image_drawObjCntr)
        cv2.waitKey(0)
        cv2.imshow("Fitted Shapes", image_fitShapes)
        cv2.waitKey(0)
        #cv2.imshow("Filled Object", image_object)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    return [x,y,w,h]
          
          

if __name__ == '__main__':
    findROI_demo(TEST_IMAGE_PATH, hsv_high, hsv_low, True, True)
    
