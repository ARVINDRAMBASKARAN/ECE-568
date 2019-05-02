from picamera import PiCamera
from time import sleep
import sys
import cv2 as cv
import numpy as np
import time
import wiringpi
import requests
import json
from operator import itemgetter
import math
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
        #print("\nthe values obtained\n")
        #print(self.ltn,self.x,self.y,self.status)
        return 1

def detect(k,a,length):
    #camera = PiCamera()
    #camera.start_preview()
    #sleep(2)
    #camera.capture('foo1.jpg')
    #camera.stop_preview()
    #camera.close()
    #default_file = '/home/pi/foo1.jpg'

   # a[0].print_values()
   # default_file = '/home/pi/opencv/samples/data/detect_blob.png'
    #Loadsanimage
    print(k);
    default_file = '/home/pi/ECE-568/hidden'+str(k)+'.jpg'
    src = cv.imread(cv.samples.findFile(default_file),cv.IMREAD_COLOR)
    #Checkifimageisloadedfine
    if src is None:
        print('Erroropeningimage!')
        print('Usage:hough_circle.py[image_name--default'+default_file+']\n')
        return -1

   # cv.imshow("circles",src)

    gray = cv.cvtColor(src,cv.COLOR_BGR2GRAY)


    gray = cv.medianBlur(gray,5)


    rows = gray.shape[0]
    circles = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,rows/8,
    param1 = 100,param2 = 30,
    minRadius = 0,maxRadius = 200)
    cnt=0
    #print("i'm printing the length")
    print(default_file)
    #print(length)
    if circles is None:
        print('no circle to detect')
        update_no_free(a,length)
        cv.imshow("detectedcircles",src)
        cv.waitKey(0)
        return -1
    for m in range (0,length):
        detected=0
        if circles is not None:
            circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            center = (i[0],i[1])
            cnt=cnt+1;
   #circlecenter
            cv.circle(src,center,1,(0,100,100),3)
    #circleoutline
            radius = i[2]
            cv.circle(src,center,radius,(255,0,255),3)
            if((a[m].x >= 0.9*i[0] and a[m].x<=1.1*i[0]) and (a[m].y >= 0.9*i[1]
                    and a[m].y <=1.1*i[1])):
                #print("the value captured is")
                #print(i[0],i[1])

                print("Lot",m+1 ," is free")
                detected=1
                if(a[m].status==0):
                    print('Now this slot is made free')
                    a[m].status = 1
                    a[m].update=1
                    break
            #else:
                #print("the value captured is")
                #print(i[0],i[1])
                #print ("wrong coordinates ")
                #print(a[m].x,a[m].y)
                #continue
        if(detected==0):
            if(a[m].status==1):
                a[m].status=0
                a[m].update=1
        #print("the value captured is")
        #print(i[0],i[1])

            #print("i'm printing the update")
            #print(a[m].update)

    #print (cnt);
    for i in range(0,length):
        if (a[i].status ==1):
            print("Now slot")
            print(i+1)
            print("is free")
            break
    post(a,length,0)
    cv.imshow("detectedcircles",src)
    cv.waitKey(0)
    return 0





def startup(argv,x,y):
    print("Hello")
    #camera=PiCamera()
    #camera.start_preview()
    #sleep(30)
    #camera.capture('foo.jpg')
    #camera.stop_preview()
    #camera.close()
    default_file = 'full.jpg'
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
            print("the sartup detected vaules")
            print(i[0],i[1])
            x.append(i[0])
            y.append(i[1])
            
    
    cv.imshow("detectedcircles",src)
    cv.waitKey(0)
    return x,y

def post(a,length,posflag):
# defining the api-endpoint
    print("im in the POST SIDE ")
    url = "http://192.168.43.117:3200/updateSpaces"
# data to be sent to api
    
    data = {"spaceList": [ ]}
    for i in range (0,length):
        if(a[i].update==1 or  posflag==1):
             add={"spaceId":(i+1),"isEmpty":a[i].status}
             data["spaceList"].append(add)
             a[i].update=0
    headers ={'Content-type':'application/json'}
    # sending post request and saving response as response object
    r = requests.post(url, data = json.dumps(data),headers=headers)
     
#: extracting response text
    print(r.json()['responseStatus'])

def lcd_print_init():
    spi=spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz=32768
    spi.mode=0b11
    spi.writebytes([254,81])
    spi.close()

def getspace(ret_value):
    url = "http://192.168.43.117:3200/getEmptySpaces"
    free_slot = requests.get(url)
    temp=free_slot.json()['objData']
    empty="wrong"
    for i in temp:
        empty=i['spaceId']
        break
    if(empty == "wrong"):
        lcd_print(0,-1)
    else:
        i =  int(empty)
        if (i!=10):
            i = i +48
        lcd_print(i,ret_value)
    #print(i)

def lcd_print(slot_number,slot):
        spi=spidev.SpiDev()
        spi.open(0,0)
        spi.max_speed_hz=32768

        spi.mode=0b11
        slot_number1 = 48
        slot_number2 = 49
        empty_slot = [69,109,112,116,121,32,83,108,111,116,32,105,115,32]
        no_slot = [78,111,32,70,114,101,101,32,83,108,111,116]
        #spi.clear()
        if(slot_number==10):
            spi.writebytes([254,81])
            sleep(0.0015)
            spi.writebytes(empty_slot)
            spi.writebytes([49])
            spi.writebytes([48])

        elif(slot ==-1):
            spi.writebytes([254,81])
            sleep(0.0015)
            spi.writebytes(no_slot)
        elif(slot==0):
            spi.writebytes([254,81])
            sleep(0.0015)
            spi.writebytes(empty_slot)
            spi.writebytes([slot_number])

def cancel(a,length):

    url = "http://192.168.43.117:3200/cancelReservation"
    
    data = {"spaceList": [ ]}
    for i in range (0,length):
        a[i].status=0
        a[i].update=0
        add={"spaceId":(i+1),"isEmpty":a[i].status}
        data["spaceList"].append(add)
    
    headers ={'Content-type':'application/json'}
    r = requests.post(url, data = json.dumps(data),headers=headers)
    
    print(r.json()['responseStatus'])

def update_no_free(a,length):
    
    url = "http://192.168.43.117:3200/updateSpaces"
    data = {"spaceList": [ ]}
    for i in range (0,length):
        a[i].status=0
        a[i].update=0
        add={"spaceId":(i+1),"isEmpty":a[i].status}
        data["spaceList"].append(add)
    
    headers ={'Content-type':'application/json'}
    r = requests.post(url, data = json.dumps(data),headers=headers)
    print(r.json()['responseStatus'])



def main(argv):
    if (wiringpi.wiringPiSetup()== -1):
        print ("error in setup")
    wiringpi.pinMode(27,0)
    i=0
    ret_value = -2
    #dict = {'196':'342','174':'204','116':'288','286':'282','164':'402','254':'214','266':'354','106':'214','280':'478']
    x=[]
    y=[]
    a=[]
    d = []
    x,y = startup(argv,x,y)
    #xy i=  zip(x,y)
    #merged = zip(x,y)
    #sorted(merged,key = lambda t:t[0])
    #xy.sort(key=operator.itemgetter(0))
    #merged = list(map(xy, zip(x,y)))
    #merged.sort(key=operator.itemgetter(0))
    for i in range(len(x)):
        for j in range(0,len(x)-i-1):
            if(x[j]>x[j+1]):
                x[j],x[j+1]=x[j+1],x[j]
                y[j],y[j+1]=y[j+1],y[j]
    for i in range (1,len(x)+1):
        print(x[i-1],y[i-1])
    print("\n");
    for j in range (0,len(x),2):
        if(y[j]<=y[j+1]):
            x[j],x[j+1]=x[j+1],x[j]
            y[j],y[j+1]=y[j+1],y[j]


    for i in range (1,len(x)+1):
        print(x[i-1],y[i-1])
    print("\n");
    for i in range (1,len(x)+1):
        z=lot(i,x[i-1],y[i-1],1,0)
        a.append(z)
        a[i-1].print_values()

    posflag=1
    post(a,len(x),posflag)
    cancel(a,len(x))
    posflag=0
    for k in range(0,len(a)):
        a[k].status = 1 
    getspace(0)
    lcd_print_init()
    i = 0
    #while(1):
    for i in range(1,23):
        if(wiringpi.digitalRead(27) == 0):
            print ("INPUT START")
            ret_value = detect(i,a,len(x))
            getspace(ret_value)
            i = i +1
            if(ret_value == 0):
                cv.destroyWindow("detectedcircles")
            print("FINISHED")



if __name__ == "__main__":
    main(sys.argv[1:])
