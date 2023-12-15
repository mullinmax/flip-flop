from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

class ServerHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add necessary headers here if needed
        SimpleHTTPRequestHandler.end_headers(self)

def run(server_class=HTTPServer, handler_class=ServerHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
