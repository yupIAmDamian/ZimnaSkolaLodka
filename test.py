from time import sleep
from math import sin, pi



def lower_higher(r, g, b):    
    offset_r = 2
    offset_g = 1
    offset_b = 0
    for i in range(40):
            r += int(10*borderedSine(offset_r,i/20*2*pi))
            #print(int(5*borderedSine(0,i/20*2*pi)))
            g += int(10*borderedSine(offset_g,i/20*2*pi))
            b += int(10*borderedSine(offset_b,i/20*2*pi))
            print(r,g,b)
            #sleep(0.2)

def borderedSine(start, movement):
    end = start*pi + 2*pi
    act_pos = movement 
    #print(start*pi, end, movement)
    if  act_pos <= end and start*pi <= act_pos: 
      x = sin(act_pos- start*pi)
      return x
    else:
        return 0
lower_higher(0,0,0)

#for i in range(21):
#    print(borderedSine(0,i/10*pi))