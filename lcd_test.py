#!/usr/bin/python

import spidev

spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=32768

spi.mode=0b11
slot = 0
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
#
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
    spi.writebytes([slot_number2])
    spi.writebytes([slot_number1])
