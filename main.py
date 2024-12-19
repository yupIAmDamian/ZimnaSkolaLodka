from server import WIFI
from machine import Pin, PWM
from time import sleep
from math import cos, sin, pi
from neopixel import NeoPixel

motors = [
    [PWM(Pin(10, Pin.OUT), freq=1000, duty= 0),
     PWM(Pin(11, Pin.OUT), freq=1000, duty= 0)],
    [ PWM(Pin(12, Pin.OUT), freq=1000, duty= 1000),
      PWM(Pin(13, Pin.OUT), freq=1000, duty= 0)]]
    
np = NeoPixel(Pin(14), 1)
np.fill((0,255,0))
np.write()



def defeated():
    np.fill((255,0,0))
    np.write()
    for motor in motors:
        for direction in motor:
            direction.duty(0)
            
    sleep(5)
    np.fill((0,0,0))
    np.write()
    

def move(angle, distance, max_dist):
    d = cos(angle)
    max_speed = 1
    speed = mapping(distance,0,max_dist, 0, max_speed)
    print(d)
    if d > 0 :
        if d > 0.5:
            print("L ",d*speed, " R ", max_speed - d*speed)
        else:
            print("L ", max_speed - d*speed, " R ",d*speed)
    elif d < 0:
        if d > -0.5:
            print("L -",d*speed, " R -", max_speed - d*speed)
        else:
            print("L -", max_speed - d*speed, " R -",d*speed)
    else:
        print("L", max_speed, " R ",max_speed)
    
def mapping(x,in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
       

#if __name__ == "__main__":
#    wifi = WIFI()
#    wifi.init()
