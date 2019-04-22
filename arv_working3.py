from picamera import PiCamera
from time import sleep
import sys
import cv2 as cv
import numpy as np
import time
import wiringpi
import requests
import json

class lot:
    def __init__(self,ltn,x,y,status):
        self.ltn=ltn
        self.x=x
        self.y=y
        self.status=status
        #dict = [self.x:self.y]
    def print_values(self):
        print("\nthe values obtained\n")
        print(self.ltn,self.x,self.y,self.status)

def detect(filename,a,length):
   # a[0].print_values()
   # default_file = '/home/pi/opencv/samples/data/detect_blob.png'
    #Loadsanimage
    src = cv.imread(cv.samples.findFile(filename),cv.IMREAD_COLOR)
    #Checkifimageisloadedfine
    if src is None:
        print('Erroropeningimage!')
        print('Usage:hough_circle.py[image_name--default'+default_file+']\n')
        return-1

   # cv.imshow("circles",src)

    gray = cv.cvtColor(src,cv.COLOR_BGR2GRAY)


    gray = cv.medianBlur(gray,5)


    rows = gray.shape[0]
    circles = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,rows/8,
    param1 = 100,param2 = 30,
    minRadius = 0,maxRadius = 200)
    cnt=0

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            center = (i[0],i[1])
            cnt=cnt+1;
            for m in range (0,length-1):
                if(a[m].x == i[0] and a[m].y == i[1]):
                    print("Lot",m+1 ," is free")
                    a[m].status = 1
                else:
                    print ("wrong coordinates")

   #circlecenter
            cv.circle(src,center,1,(0,100,100),3)
    #circleoutline
            radius = i[2]
            cv.circle(src,center,radius,(255,0,255),3)
            print(i[0],i[1]);

    print (cnt);
    cv.imshow("detectedcircles",src)
    cv.waitKey(0)
    for i in range(0,length):
        if (a[i].status ==1):
            print("Now slot")
            print(i+1)
            print("is free")
            break
    post(a,length)
    return 0





def startup(argv,x,y):
    print("Hello")
    camera=PiCamera()
    camera.start_preview()
    sleep(10)
    camera.capture('foo.jpg')
    camera.stop_preview()
    camera.close()
    default_file = '/home/pi/project/foo.jpg'
    filename = argv[0] if len(argv) >0 else default_file
    
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
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            center = (i[0],i[1])
    #circlecenter
            cv.circle(src,center,1,(0,100,100),3)
    #circleoutline
            radius = i[2]
            cv.circle(src,center,radius,(255,0,255),3)
            print(i[0],i[1])
            x.append(i[0])
            y.append(i[1])
            
   # print (count);
    cv.imshow("detectedcircles",src)
    cv.waitKey(0)
    return x,y

def post(a,length):
# defining the api-endpoint
    url = "http://localhost:3200/updateSpaces"
# data to be sent to api
    data = {"spaceList": [ ]}
    for i in range (0,length-1):
        add={"spaceId":(i+1),"isEmpty":a[i].status}
        data["spaceList"].append(add)
    
    headers ={'Content-type':'application/json'}
    # sending post request and saving response as response object
    r = requests.post(url, data = json.dumps(data),headers=headers).text
     
# extracting response text
    data = json.loads(r)
    print("The pastebin URL is:%s"%data['responseStatus'])





def main(argv):
    if (wiringpi.wiringPiSetup()== -1):
        print ("error in setup")
    wiringpi.pinMode(27,0)
    i=0
    #dict = {'196':'342','174':'204','116':'288','286':'282','164':'402','254':'214','266':'354','106':'214','280':'478']
    x=[]
    y=[]
    x,y = startup(argv,x,y) 
    a=[]
    for i in range (1,len(x)+1):
        z=lot(i,x[i-1],y[i-1],0)
        a.append(z)
        #print("hi\n")
        #a[i-1].print_values()
        #print("hi2\n")
    while(1):
        if(wiringpi.digitalRead(27) == 0):
            print ("INPUT START")
            camera = PiCamera()
            camera.start_preview()
            sleep(10)
            camera.capture('foo.jpg')
            camera.stop_preview()
            camera.close()
            default_file = '/home/pi/project/foo.jpg'
            filename = argv[0] if len(argv) >0 else default_file
            i = i +1
            detect(filename,a,len(x))
            #time.sleep(4)
            print("hello")
            cv.destroyWindow("detectedcircles")
            print("FINISHED")



if __name__ == "__main__":
    main(sys.argv[1:])

