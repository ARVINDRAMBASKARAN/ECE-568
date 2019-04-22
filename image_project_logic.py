
import sys
import cv2 as cv
import numpy as np
import time
import wiringpi

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

def detect(filename,a):
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
            if(a[0].x == i[0] and a[0].y == i[1]):
                print("Lot 1 is free")
                a[0].status = 1
            elif(a[1].x == i[0] and a[1].y == i[1]):
                print("Lot 2 is free")
                a[1].status = 1
            elif(a[2].x == i[0] and a[2].y == i[1]):
                print("Lot 3 is free")
                a[2].status = 1
            elif(a[3].x == i[0] and a[3].y == i[1]):
                print("Lot 4 is free")
                a[3].status = 1
            elif(a[4].x == i[0] and a[4].y == i[1]):
                print("Lot 5 is free")
                a[4].status = 1
            elif(a[5].x == i[0] and a[5].y == i[1]):
                print("Lot 6 is free")
                a[5].status = 1
            elif(a[6].x == i[0] and a[6].y == i[1]):
                print("Lot 7 is free")
                a[6].status = 1
            elif(a[7].x == i[0] and a[7].y == i[1]):
                print("Lot 8 is free")
                a[7].status = 1
            elif(a[8].x == i[0] and a[8].y == i[1]):
                print("Lot 9 is free")
                a[8].status = 1
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
    for i in range(0,9):
        if (a[i].status ==1):
            print("Now slot")
            print(i+1)
            print("is free")
            break

    return 0

def main(argv):
    if (wiringpi.wiringPiSetup()== -1):
        print ("error in setup")
    wiringpi.pinMode(27,0)
    i=0
    #dict = {'196':'342','174':'204','116':'288','286':'282','164':'402','254':'214','266':'354','106':'214','280':'478']
    x=[132,174,116,286,164,254,266,106,280]
    y=[158,204,288,282,402,214,354,214,478]
    a=[]
    for i in range (1,10):
        z=lot(i,x[i-1],y[i-1],0)
        a.append(z)
        #print("hi\n")
        #a[i-1].print_values()
        #print("hi2\n")
    while(1):
        if(wiringpi.digitalRead(27) == 0):
            #print ("input")
            default_file = '/home/pi/opencv/samples/data/detect_blob.png'
            filename = argv[0] if len(argv) >0 else default_file
            i = i +1
            detect(filename,a)
            time.sleep(10)
            print(i)
            print("end")



if __name__ == "__main__":
    main(sys.argv[1:])

