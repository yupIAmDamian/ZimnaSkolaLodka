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
        with open('./plain.html', 'r', encoding='utf-8') as file:
            return file.read()
        
    def parse_post_data(self, request):
        # Decode the byte data to a string
        request_str = request.decode('utf-8')
        print(f"Decoded request: {request_str}")
        
        # Extract POST data (simple parsing)
        post_data = request_str.split("\r\n\r\n")[-1]
        print(f"POST Data: {post_data}")
        
        _, post_data = post_data.split("=")
        
        return [int(i) for i in post_data.split("%20")]
    
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
            print(f'Request: {request.decode()}')
            
            if 'POST' in request:
                params = self.parse_post_data(request)
                message = params
                print(f"Received message: {message}")
            
            client.send('HTTP/1.1 200 OK\n')
            client.send('Content-Type: text/html\n')
            client.send('Connection: close\n\n')
            client.sendall(self.html_content.encode('utf-8'))
            client.close()

    def main(self):
        self.create_ap()
        self.http_server()


