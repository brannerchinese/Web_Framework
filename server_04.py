#!/usr/bin/env python
# server_04.py
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

    python server_04.py 1234

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
        """Provide functionality for GET requests."""
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()
        self.files = 'files/'
        file_contents = None
        # Special case: no path given.
        print(self.path)
        if self.path == '/':
            self.path = 'index.html'
        # Special case: path (stripped of .html) is function name.
        self.url_is_func()
        print('finished self.url_is_func()')
        # Special case: Not a function, but path is HTML file.
        if self.path.endswith('.html'):
            print('ends with html')
            try:
                with open (self.files + self.path, 'rb') as f:
                    file_contents = f.read()
                    print('got it:', file_contents)
            except IOError:
                self.send_error(404, 'File {} not found'.format(self.path))
        else:
            file_contents = b'Path must end with ".html"; try again.'
        if file_contents:
            # self.wfile is a socket.SocketIO object
            self.wfile.write(file_contents)

    def url_is_func(self):
        """Treat stripped path-name as possible function call."""
        # Remove left-most slash.
        path = self.path.lstrip('/')
        # Separate path into its parts.
        fn_name, *args = path.split('/')
        print(fn_name, args)
        if args and '.html' in args[-1]:
            # It is possible the slash denotes a subdirectory, not a function.
            sudirectory_possible = True
        else:
            sudirectory_possible = False
        # Check validity of prospective function name.
        imp.reload(functions)
        F = functions.Functions()
        # If we have html extension on fn_name, remove it.
        fn_name = fn_name.split('.')[0]
        print(fn_name)
        if (fn_name[0] not in string.ascii_letters or
                any([i not in string.ascii_letters + string.digits + '_' for
                    i in fn_name]) or
                fn_name not in F.funcs):
            print('here')
            return
        if not args:
            # Treat zero-argument case together with the case with arguments.
            args = ''
            fn_name = fn_name.split('.')[0]
        # Call the function on any arguments. Report exception in file.
        try:
            content = eval('F.' + fn_name + '(*args)')
        except Exception as e:
            if sudirectory_possible:
                # t was in fact a subdirectory; don't report exception.
                return
            content = 'Exception: ' + str(e)
        # Save to file and ensure that path name is set to that HTML filname.
        with open(self.files + fn_name + '.html', 'w') as f:
            f.write(content)
        self.path = fn_name + '.html'

def run(port):
    """Run the server indefinitely."""
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
