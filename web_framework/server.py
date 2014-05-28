#!/usr/bin/env python
# server.py
# David Prager Branner
# 20140528, works.

"""Construct simple web server. See the README for details."""

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
        self.files = 'files/'
        file_contents = None
        # Special case: no path given.
        if self.path == '/':
            self.path = 'index.html'
        # Special case: path (stripped of .html) is function name.
        self.url_is_func()
        # Special case: Not a function, but path is HTML file.
        if self.path.endswith('.html'):
            try:
                with open (self.files + self.path, 'rb') as f:
                    file_contents = f.read()
            except IOError:
                self.send_404()
        else:
            self.send_404()
            self.wfile.write(b'Path must end with ".html"; try again.')
        if file_contents:
            # self.wfile is a socket.SocketIO object
            self.send_200()
            self.wfile.write(file_contents)

    def send_200(self):
        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()

    def send_404(self):
        self.send_error(404, 'File {} not found'.format(self.path))

    def url_is_func(self):
        """Treat stripped path-name as possible function call."""
        # Remove left-most slash.
        path = self.path.lstrip('/')
        # Separate path into its parts.
        fn_name, *args = path.split('/')
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
        if (fn_name[0] not in string.ascii_letters or
                any([i not in string.ascii_letters + string.digits + '_' for
                    i in fn_name]) or
                fn_name not in F.funcs):
            return
        if not args:
            # Treat zero-argument case together with the case with arguments.
            args = ''
        # Call the function on any arguments. Report exception in file.
        try:
            content = eval('F.' + fn_name + '(*args)')
        except Exception as e:
            if sudirectory_possible:
                # It was in fact a subdirectory; don't report exception.
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
    print('Server running on port {}.'.format(httpd.socket.getsockname()[1]))
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', nargs='?',
            help='Specify port to listen on.', type=int)
    try:
        args = parser.parse_args()
    except Exception as e:
        print(e)
    if args.port != None:
        port = args.port
    else:
        port = 1924
    if port == 0:
        print('''\nPort 0 specifies the use of a system-allocated (dynamic) '''
                '''port and can be used for remote OS detection. We decline '''
                '''connections on port 0 for that reason.\n''')
        sys.exit(0)
    try:
        run(port)
    except Exception as e:
        raise RuntimeError('Unable to listen on port {}.\n{}'.format(port, e))
