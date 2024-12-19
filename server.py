import network
import socket

class WIFI:

    def __init__(self):
        # Configure Access Point
        self.ssid = 'ESP32_AP'        # Network name
        self.password = '12345678'    # Password (minimum 8 characters)
        self.html_content = self.import_html()
        
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
        # Decode the byte data to a string (use utf-8 instead of gzip)
        request_str = request.decode('utf-8')
        print(f"Decoded request: {request_str}")

        # Extract POST data (after the headers, the body is separated by \r\n\r\n)
        post_data = request_str.split("\r\n\r\n")[-1]
        print(f"POST Data: {post_data}")

        # Split the post data by '&' to separate the angle and distance values
        data = post_data.split(" ")

        # Get the angle and distance as floats
        print(data)
        angle = float(data[0])  # Get the angle value
        distance = float(data[1])  # Get the distance value
        max_dist = 1 

        print(f"Parsed values - Angle: {angle}, Distance: {distance}")

        return angle, distance, max_dist

    
    def http_server(self):
        # Create socket for HTTP server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 80))
        sock.listen(5)
        print('HTTP server running...')
        
        while True:
            client, addr = sock.accept()
            print(f'Client connected: {addr}')
            
            request = client.recv(1024)
            
            """
            if b'GET /favicon' or b'GET /apple-touch-icon' in request:
                client.send('HTTP/1.1 204 No Content\n')  # No content, no favicon
                client.send('Connection: close\n\n')
                client.close()
                continue
            """
            
            print('')
            print(f'Request: {request}')
            print('')
            
            if 'POST' in request:
                distance, angle, max_dist = self.parse_post_data(request)
                print(f"Received message: {distance}, {angle}, {max_dist}")
            
            client.send('HTTP/1.1 200 OK\n')
            client.send('Content-Type: text/html\n')
            client.send('Connection: close\n\n')
            client.sendall(self.html_content.encode('utf-8'))
            client.close()

    def init(self):
        self.create_ap()
        self.http_server()


