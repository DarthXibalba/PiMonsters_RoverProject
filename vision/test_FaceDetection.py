# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:53:01 2017
Python 2.7.12

@author: Javier
"""

import cv2
import numpy as np

# Camera Imports
from picamera.array import PiRGBArray
from picamera import PiCamera

# Sleep function to wait on Camera
from time import sleep


# Create the Haar Cascade
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')

# Capture Object
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

# Wait for the camera to start up
sleep(1.0)

# Foreground Background
fgbg = cv2.BackgroundSubtractorMOG()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab an image from the camera
    image = frame.array
    
    # Shrink it down
    height, width = image.shape[:2]
    image = cv2.resize(image, (width/2, height/2), interpolation=cv2.INTER_CUBIC)

    # Remove Background
    fgmask = fgbg.apply(image)
    cv2.imshow('Motion Detection', fgmask)
    
    # Face Detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print "Found " +str(len(faces)) +" faces(s)"
    
    for (x,y,w,h) in faces:
        cv2.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color=image[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2)

    cv2.imshow('Face Detection', image)
    
    # Press 'q' to quit
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
