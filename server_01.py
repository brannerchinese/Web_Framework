#!/usr/bin/env python
# server_01.py
# David Prager Branner
# 20140525

"""Construct simple web server."""

import sys
if sys.version_info[0] != 3:
    print('Python 3 required.')
    sys.exit()
import os
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        files = 'files'
        file_contents = None
        if self.path.endswith('.html'):
            print(self.path)
            try:
                with open (files + self.path) as f:
                    file_contents = f.read()
            except IOError:
                self.send_error(404, 'file not found!')
                file_contents = b'You should have received an error.'
        else:
            file_contents = b'Nothing received.'
        if file_contents:
            self.wfile.write(file_contents)

def run(port):
    print('Server starting on port {}.'.format(port))
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, CustomHandler)
    print('Server running on port {}.'.format(port))
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', nargs='?',
            help='Specify port to listen on.', type=int)
    try:
        args = parser.parse_args()
    except Exception as e:
        print(e)
    if args.port:
        port = args.port
    else:
        port = 8000
    run(port)
