import network
import socket

class WIFI:

    def __init__(self):
        # Configure Access Point
        self.ssid = 'ESP32_AP'        # Network name
        self.password = '12345678'    # Password (minimum 8 characters)
        self.html_content = self.import_html()
        self.sock = None
        
    def create_ap(self):
        ap = network.WLAN(network.AP_IF)  # Create Access Point interface
        ap.active(True)                  # Activate the AP
        ap.config(essid=self.ssid, password=self.password)  # Set network name and password
        ap.config(channel=6, max_clients=5)       # Optional: set channel and max clients
        
        while not ap.active():
            pass  # Wait for the AP to become active

        print('Access Point created successfully!')
        print('Network details:', ap.ifconfig())

    def import_html(self): 
        with open('./index.html', 'r', encoding='utf-8') as file:
            return file.read()
        
    def parse_post_data(self, request):
        request_str = request.decode('utf-8')

        post_data = request_str.split("\r\n\r\n")[-1]

        data = post_data.split(" ")

        angle = float(data[0])
        distance = float(data[1])
        max_dist = float(data[2])

        return angle, distance, max_dist

    
    def http_server(self):
        # Create socket for HTTP server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', 80))
        self.sock.listen(5)
        print('HTTP server running...')
        
            
    def check_connection(self):
        distance, angle, max_dist = -1,0,0
        client, addr = self.sock.accept()
        print(f'Client connected: {addr}')
        
        request = client.recv(1024)
        
        if 'POST' in request:
            angle, distance, max_dist = self.parse_post_data(request)
        
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html\n')
        client.send('Connection: close\n\n')
        client.sendall(self.html_content.encode('utf-8'))
        client.close()
        
        if distance is not -1:
            return angle, distance, max_dist

    def init(self):
        self.create_ap()
        self.http_server()


