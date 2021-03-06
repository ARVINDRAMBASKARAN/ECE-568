from picamera import PiCamera
from time import sleep
import sys
import cv2 as cv
import numpy as np
import time
import wiringpi
import requests
import json
import spidev

class lot:
    def __init__(self,ltn,x,y,status,update):
        self.ltn=ltn
        self.x=x
        self.y=y
        self.status=status
        self.update = update
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
    print("i'm printing the length")
    print(length)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for m in range (0,length):
            detected=0
            for i in circles[0,:]:
                center = (i[0],i[1])
                cnt=cnt+1;
                if(a[m].x == i[0] and a[m].y == i[1]):
                    print("Lot",m+1 ," is free")
                    detected=1
                    if(a[m].status==0):
                        a[m].status = 1
                        a[m].update=1
                    break
                else:
                    print ("wrong coordinates")
            if(detected==0):
                if(a[m].status==1):
                    a[m].status=0
                    a[m].update=1

   #circlecenter
            cv.circle(src,center,1,(0,100,100),3)
    #circleoutline
            radius = i[2]
            cv.circle(src,center,radius,(255,0,255),3)
            print(i[0],i[1]);
            print("i'm printing the update")
            print(a[m].update)

    print (cnt);
    cv.imshow("detectedcircles",src)
    cv.waitKey(0)
    for i in range(0,length):
        if (a[i].status ==1):
            print("Now slot")
            print(i+1)
            print("is free")
            break
   #post(a,length)
    return 0





def startup(argv,x,y):
    print("Hello")
    camera=PiCamera()
    camera.start_preview()
    sleep(10)
    camera.capture('foo.jpg')
    camera.stop_preview()
    camera.close()
    default_file = '/home/pi/foo.jpg'
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
    print("im in the POST SIDE ")
    url = "http://192.168.43.117:3200/updateSpaces"
# data to be sent to api
    
    data = {"spaceList": [ ]}
    for i in range (0,length):
        if(a[i].update==1):
             add={"spaceId":(i+1),"isEmpty":a[i].status}
             data["spaceList"].append(add)
             a[i].update=0
    
    headers ={'Content-type':'application/json'}
    # sending post request and saving response as response object
    r = requests.post(url, data = json.dumps(data),headers=headers)
     
#: extracting response text
    print(r.json()['responseStatus'])

def lcd():
    url = "http://192.168.43.117:3200/getEmptySpaces"
    free_slot = requests.get(url)
    temp=free_slot.json()['objData']
    empty="wrong"
    for i in temp:
        empty=i['spaceId']
        break
    #print(empty)
    i =  int(empty)
    i = i +48
    lcd_print(i)
    #print(i)

def lcd_print(slot_number):
	spi=spidev.SpiDev()
	spi.open(0,0)
	spi.max_speed_hz=32768
	
	spi.mode=0b11
	slot = 1
	slot_number1 = 48
	slot_number2 = 49
	empty_slot = [69,109,112,116,121,32,83,108,111,116,32,105,115,32]
	no_slot = [78,111,32,70,114,101,101,32,83,108,111,116]
	#spi.clear()
	if(slot ==0):
	    spi.writebytes([254,81])
	#spi.writebytes([254,69])
	#spi.writebytes([65])
	#spi.writebytes([254,81])
	#spi.writebytes([254,69])
	#spi.writebytes([66])
	#spi.writebytes([254,75])
	    spi.writebytes([254,69])
	    spi.writebytes([254,84])
	    spi.writebytes([254,75])
	#spi.writebytes([69,109,112,116,121])
	    spi.writebytes(no_slot)
	#spi.writebytes([32,83,108,111,116])
	if(slot==1):
	    spi.writebytes([254,81])
	    spi.writebytes([254,69])
	    spi.writebytes([254,84])
	#    spi.writebytes([254,75])
	    spi.writebytes(empty_slot)
	    spi.writebytes([slot_number])


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
    #lcd()
    for i in range (1,len(x)+1):
        z=lot(i,x[i-1],y[i-1],1,0)
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
            default_file = '/home/pi/foo.jpg'
            filename = argv[0] if len(argv) >0 else default_file
            i = i +1
            detect(filename,a,len(x))
            #time.sleep(4)
            print("hello")
            cv.destroyWindow("detectedcircles")
            print("FINISHED")



if __name__ == "__main__":
    main(sys.argv[1:])

