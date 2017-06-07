"""
Created on 05/25/2017
Python 2.7.13

@author: Javier Urquizu
"""

import numpy as np
import cv2



TEST_IMAGE_PATH = "../tf_classifier/ImageDataset/Capture/capture_pepsi_can_1.jpg"


def blob_detection(img):
    # Set up the detector with default parameters
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 150
    detector = cv2.SimpleBlobDetector_create(params)
    
    # Detect blobs
    keypts = detector.detect(img)
    
    # Draw detected blobs as red circles
    img_keypts = cv2.drawKeypoints(img, keypts, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # Show blobs
    cv2.imshow("Keypoints", img_keypts)
    
    
def canny_edge_detection(img, choice, thresh1, thresh2):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    red_img = img[:,:,0]
    green_img = img[:,:,1]
    blue_img = img[:,:,2]
    '''
    choice = "blue"
    thresh1 = 50
    thresh2 = 150
    '''
    if choice == "red":
        cv2.imshow("Red", red_img)
        edgesImg = cv2.Canny(red_img, thresh1, thresh2)
    elif choice == "green":
        cv2.imshow("Green", green_img)
        edgesImg = cv2.Canny(green_img, thresh1, thresh2)
    elif choice == "blue":
        cv2.imshow("Blue", blue_img)
        edgesImg = cv2.Canny(blue_img, thresh1, thresh2)
    else:
        cv2.imshow("Gray", gray_img)
        edgesImg = cv2.Canny(gray_img, thresh1, thresh2)
        
    cv2.imshow("Edges", edgesImg)
    


if __name__ == '__main__': 
    img = cv2.imread(TEST_IMAGE_PATH)
    
    
    
