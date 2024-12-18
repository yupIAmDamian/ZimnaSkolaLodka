from machine import Pin, SoftI2C, PWM
from neopixel import NeoPixel
#from ssd1306 import SSD1306_I2C
from time import sleep, sleep_ms, time, time_ns
import math
from math import pi, sin
import socket
from server import WIFI
WIFI.connect_to_wifi()
# i2c = SoftI2C(sda=Pin(8), scl=Pin(9))
# display = SSD1306_I2C(128, 32, i2c)

# display.fill(0)
# display.text("Hello", 0,0)
# display.show()


from server import WIFI

if __name__ == "__main__":
    wifi = WIFI()
    wifi.main()


def web_page():
    """Create a simple HTML page."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Web Server</title>
    </head>
    <body>
        <h1>Welcome to ESP32 Web Server!</h1>
        <p>Click the button to toggle the LED:</p>
        <form action="/led_on">
            <button type="submit">Turn LED ON</button>
        </form>
        <form action="/led_off">
            <button type="submit">Turn LED OFF</button>
        </form>
    </body>
    </html>
    """
    return html

# Set up the socket
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print("Listening on", addr)

    while True:
        client, addr = s.accept()
        print("Client connected from", addr)
        request = client.recv(1024).decode()
        print("Request:", request)
        
        # Handle LED actions (if connected)
        if '/led_on' in request:
            print("LED ON")
        elif '/led_off' in request:
            print("LED OFF")
        
        # Send the web page
        response = web_page()
        client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response)
        client.close()

#start_server()

np = NeoPixel(Pin(14), 1)
np[0] = (0, 0, 0, 0)
np.write()

buttonPin = Pin(7, Pin.IN, Pin.PULL_UP)

def lower_higher(offset_r, offset_g, offset_b):
    r,b,g = 0,0,0
    for i in range(40):
            sleep(0.2)
            r += int(10*borderedSine(offset_r,i/20*2*pi))
            g += int(10*borderedSine(offset_g,i/20*2*pi))
            b += int(10*borderedSine(offset_b,i/20*2*pi))
            np.fill((r,g,b))
            np.write()

def borderedSine(start, movement):
    end = start*pi + 2*pi
    act_pos = movement 
    #print(start*pi, end, movement)
    if  act_pos <= end and start*pi <= act_pos: 
      x = sin(act_pos- start*pi)
      return x
    else:
        return 0

ms = 0
pressed = False
def handle_interrupt(pin):
    global pressed
    pressed = True
    
        
    
buttonPin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handle_interrupt)
#buttonPin.irq(trigger=Pin.IRQ_FALLING, handler = handle_interrupt2)

while True:
    if pressed:
        if ms == 0:
            ms = time_ns()
        else:
            ms = (time_ns()-ms)//1000000
            print(ms)
            if ms > 2000:
                lower_higher(0,1,2)
            elif ms > 500:
                lower_higher(2,0,1)
            else:
                lower_higher(1,2,0)
            ms = 0
        
        pressed = False
        
pin = Pin(16, Pin.OUT)
led = PWM(pin, freq=1000)

def pulse(l, t):
    for i in range(20):
        l.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        sleep_ms(t)
        