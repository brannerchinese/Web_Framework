#!/usr/bin/env python
# server_02.py
# David Prager Branner
# 20140525

"""Construct simple web server.

Assignments:

 1.     Using your language's http library, make a server that listens on a
certain port (say 1924) and returns a string of text.  Check that your browser
displays that text when you go to localhost:1924.

 2.  Instead of fixed text, have your program look for a file called index.html
in its current directory.  Return its contents, or a 404 error if the file
doesn't exist.

 3.  Read the url the browser sends and serve the appropriate file - for
example, localhost:1924/foo.html should look for foo.html in the current
directory.

 4. Now handle things like localhost:1924/foo/bar/baz.html by searching through
directories.  (Bonus:  What's the security flaw here?)

Usage:

    python server_02.py 1234

where 1234 is a port to listen on. If no port is found, the default is 8000.
"""

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
        self.send_header('Content-type', 'text-html')
        self.end_headers()
        files = 'files/'
        file_contents = None
        if self.path == '/':
            self.path = 'index.html'
        if self.path.endswith('.html'):
            try:
                with open (files + self.path, 'rb') as f:
                    file_contents = f.read()
            except IOError:
                self.send_error(404, 'File {} not found'.format(self.path))
        else:
            file_contents = b'Path must end with ".html"; try again.'
        if file_contents:
            # self.wfile is a socket.SocketIO object
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
