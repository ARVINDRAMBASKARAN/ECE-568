
import sys
import cv2 as cv
import numpy as np
from picamera import PiCamera
from time import sleep

def main(argv):
    camera = PiCamera()
    camera.resolution = (1024,768)
    while(1):
        camera.start_preview()
        sleep(10)
        camera.capture('foo.jpg')
        camera.stop_preview()


        #default_file = '/home/pi/opencv/samples/data/detect_blob.png'
       # default_file = '/home/pi/opencv/samples/data/detect_blob.png'
        default_file = '/home/pi/project/foo.jpg'
        
        filename = argv[0] if len(argv) >0 else default_file
        #Loadsanimage
        src = cv.imread(cv.samples.findFile(filename),cv.IMREAD_COLOR)
        #Checkifimageisloadedfine
        if src is None:
            print('Erroropeningimage!')
            print('Usage:hough_circle.py[image_name--default'+default_file+']\n')
            return-1
        
        
        gray = cv.cvtColor(src,cv.COLOR_BGR2GRAY)
        
        
        gray = cv.medianBlur(gray,5)
        
        
        rows = gray.shape[0]
        circles = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,rows/8,
        param1 = 100,param2 = 30,
        minRadius = 0,maxRadius = 200)
        count=0;
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                center = (i[0],i[1])
                count=count+1;
        #circlecenter
                cv.circle(src,center,1,(0,100,100),3)
        #circleoutline
                radius = i[2]
                cv.circle(src,center,radius,(255,0,255),3)
                print(i[0],i[1]);
                
        print (count);
        cv.imshow("detectedcircles",src)
        cv.waitKey(0)
    
    return 0
if __name__ == "__main__":
    main(sys.argv[1:])
    
