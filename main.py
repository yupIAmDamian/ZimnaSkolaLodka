from server import WIFI
from machine import Pin, PWM
from time import sleep
from math import cos, sin, pi
from neopixel import NeoPixel

buttonPin = Pin(7, Pin.IN, Pin.PULL_UP)
buttonPin = Pin(16, Pin.IN, Pin.PULL_DOWN)

motors = [
    [PWM(Pin(10, Pin.OUT), freq=1000, duty= 0), PWM(Pin(11, Pin.OUT), freq=1000, duty= 0)],
    [PWM(Pin(12, Pin.OUT), freq=1000, duty= 0), PWM(Pin(13, Pin.OUT), freq=1000, duty= 0)]
]
    
np = NeoPixel(Pin(14), 1)
np.fill((0,5,0))
np.write()


def defeated(pin):
    np.fill((5,0,0))
    np.write()
    for motor in motors:
        for direction in motor:
            direction.duty(0)
            
    sleep(10)
    np.fill((0,0,0))
    np.write()
    while True:
        pass
    
buttonPin.irq(trigger=Pin.IRQ_RISING, handler=defeated)
buttonPin.irq(trigger=Pin.IRQ_RISING, handler=defeated)
    

from math import pi

def move(a, s, sMax):
    angle = a;
    speedMax = mapping(s, 0, sMax, 0, 1000)
    sL = speedMax
    sR = speedMax
    
    if angle >= 0:
        if angle <= pi/4:
            sL = mapping(angle, 0, pi/4, speedMax, 0)
        elif angle <= pi/2:
            sL = mapping(angle, pi/4, pi/2, 0, -speedMax)
    elif angle < 0:
        if angle >= -pi/4:
            sR = mapping(-angle, 0, pi/4, speedMax, 0)
        elif angle >= -pi/2:
            sR = mapping(-angle, pi/4, pi/2, 0, -speedMax)
    if angle > pi/2:
        sR = -sR
        if angle <= pi*(3/4):
            sL = mapping(angle, pi/2, pi*(3/4), speedMax, 0)
        elif angle <= pi:
            sL = mapping(angle, pi*(3/4), pi, 0, -speedMax)
    elif angle < -pi/2:
        sL = -sL
        sR = -sR
        if angle >= -pi*(3/4):
            sR = mapping(-angle, pi/2, pi*(3/4), speedMax, 0)
        elif angle >= -pi:
            sR = mapping(-angle, pi*(3/4), pi, 0, -speedMax)
    
    if sL >= 0:
        motors[0][0].duty(int(sL))
    else:
        motors[0][1].duty(int(-sL))
        
    if sR >= 0:
        motors[1][0].duty(int(sR))
    else:
        motors[1][1].duty(int(-sR))
        
    print(angle, sL, sR)

def mapping(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
       

def start():
    wifi = WIFI()
    wifi.init()
    while True:
        try:
            angle, distance, max_dist = wifi.check_connection();
            move(angle, distance, max_dist)
        except:
            pass


