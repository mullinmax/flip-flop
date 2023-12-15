import docker
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

def get_flip_flop_urls():
    client = docker.from_env()
    containers = client.containers.list()
    urls = []

    for container in containers:
        labels = container.labels
        flip_flop_url = labels.get('flip-flop.url')
        if flip_flop_url:
            urls.append(flip_flop_url)

    return urls

# Example usage
urls = get_flip_flop_urls()
print(urls)


if __name__ == '__main__':
    run()
