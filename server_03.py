#!/usr/bin/env python
# server_03.py
# David Prager Branner
# 20140525

"""Construct simple web server.

Assignments:

 Part 2:

 1. Without destroying any of the previous functionality, define a special url that returns the result of a function.  For example, define a function called helloworld, and make it so going to localhost:1924/hello.html calls that function instead of looking for a file.

 2. Keep a list or hash table of these special urls, and the function associated with each.  Check each incoming url to see if it's in the table before looking for a file.

 3. Parse the url, so that part of it determines what function gets called, and another part defines the argument(s) to the function - for example, localhost:1924/user/blarg could return information about the user named Blarg.

 4. Turn your framework into a module or library, so someone can import it into their program.  Tell them how to write a function and associate it with a url.

Usage:

    python server_02.py 1234

where 1234 is a port to listen on. If no port is found, the default is 1924.
"""

import sys
if sys.version_info[0] != 3:
    print('Python 3 required.')
    sys.exit()
import argparse
import string
import imp
from http.server import HTTPServer, BaseHTTPRequestHandler
import functions

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.special
        except Exception:
            self.special = ['hello', 'time']
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()
        self.files = 'files/'
        file_contents = None
        # Special case: no path given.
        if self.path == '/':
            self.path = 'index.html'
        # Special case: URL (stripped of .html) is function name.
        self.zero_arg_urls()
        # Special case: Not a function, but path is HTML file.
        if self.path.endswith('.html'):
            try:
                with open (self.files + self.path, 'rb') as f:
                    file_contents = f.read()
            except IOError:
                self.send_error(404, 'File {} not found'.format(self.path))
        else:
            file_contents = b'Path must end with ".html"; try again.'
        if file_contents:
            # self.wfile is a socket.SocketIO object
            self.wfile.write(file_contents)

    def zero_arg_urls(self):
        """If path, less '.html' is a valid function name, 

then check functions.Functions; if found there, run it as a function.
        """
        imp.reload(functions)
        F = functions.Functions()
        fn_name = self.path.lstrip('/').split('/')[0].split('.')[0]
        if (fn_name[0] in string.ascii_letters and
                any([i in string.ascii_letters + string.digits + '_' for
                    i in fn_name]) and
                fn_name in F.funcs):
#                fn_name in self.special):
            content = eval('F.' + fn_name + '()')
            with open(self.files + fn_name + '.html', 'w') as f:
                f.write(content)

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
        port = 1924
    run(port)
