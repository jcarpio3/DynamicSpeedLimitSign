###############################################################################
# Imports
###############################################################################
from machine import Pin, SPI
import max7219
from time import sleep

###############################################################################
# Constants
###############################################################################

###############################################################################
# Settings
###############################################################################

spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=1,
                  phase=1,
                  bits=8,
                  sck=machine.Pin(2),
                  mosi=machine.Pin(3))

cs = Pin(5, Pin.OUT)
###############################################################################
# Functions
###############################################################################

def TestCode():
    display.fill(0)
    display.text("cntCNT",1,1,1) #The sign goes from top right to bottom left 
    display.show()
    sleep(0.5)
    display.fill(0)
    display.text("CNTcnt",1,1,1) #The sign goes from top right to bottom left 
    display.show()
    sleep(0.5)
def ScrollingTest(message):
     for x in range(50, -len(message), -1):     
         display.fill(0)
         display.text(message ,x,0,1)
         display.show()
         sleep(0.1)

    
def SlowDown():
    #fill (col)
    #pixel (x, y[, c])
    #hline (x, y, w, col)
    #vline (x, y, h, col)
    #line (x1, y1, x2, y2, col)
    #rect (x, y, w, h, col)
    #fill_rect (x, y, w, h, col)
    #text (string, x, y, col=1)
    #scroll (dx, dy)
    #blit (fbuf, x, y[, key])
    display.pixel(0,0,1)
    display.pixel(1,1,1)
    display.hline(0,4,8,1)
    display.vline(0,0,8,1)
    display.show()
    
def SpeedUp():
    #fill (col)
    #pixel (x, y[, c])
    #hline (x, y, w, col)
    #vline (x, y, h, col)
    #line (x1, y1, x2, y2, col)
    #rect (x, y, w, h, col)
    #fill_rect (x, y, w, h, col)
    #text (string, x, y, col=1)
    #scroll (dx, dy)
    #blit (fbuf, x, y[, key])
    display.pixel(0,0,1)
    display.pixel(1,1,1)
    display.hline(0,4,8,1)
    display.vline(0,0,8,1)
    display.show()

def DisplaySpeed():
    display.text("KPH123",1,0,1)
    display.show()
###############################################################################
# Initialization
###############################################################################
#Initializes the display to 6 matrix modules
display = max7219.Matrix8x8(spi,cs,6)

#Sets brightness to the maximum setting (0-15)
display.brightness(15)

# Clears Screen
display.fill(0)
display.show()
sleep(1)
###############################################################################
# Main
###############################################################################
while True:
    #TestCode()
    #ScrollingTest("CNT")
    DisplaySpeed()
    #SlowDown()

