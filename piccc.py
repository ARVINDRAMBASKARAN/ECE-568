#!/usr/bin/python3
import sys
from picamera import PiCamera
from time import sleep
import cv2
import time

camera = PiCamera()
rawCapture = PiRGBArray(camera)
time.sleep(10)
camera.picture(rawCapture,formar="bgr")
image = rawCapture.array
cv2.imshow("image",image)
cv2.waitKey(0)
