## Comments by [Stacey Sern](https://github.com/staceysern), 20140526

### To consider for the future

 3. The following comments are not coding issues, rather design issues for a web framework.

   I don't love the solution of putting all the possible functions that could be called to generate dynamic content in the Functions class.  Reloading Functions on every get request seems very inefficient.  If there was a lot of traffic, I'm guessing it would slow things down quite a bit.  And, it seems a bit restrictive for all functions used in the web server to be in one file.  You could imagine a function to be quite involved and it might be nice to have it in its own file.

   This scheme also restricts the format of urls to a function name followed by arguments.  You could easily imagine that a site might want both /productA/userinfo/NAME and /productA/userinfo/NAME where NAME is the variable in both cases.  You could also imagine that someone might want /user/NAME/productA/OPTION and /user/NAME/productB/OPTION where NAME and OPTION are variables.  Neither of these schemes is supported in your web framework.

   As a general principle, I think that the user should be able to explicitly specify what urls they want and the urls should be independent of whether they are static or dynamic.  So, if someone wanted foo.html to be a url which is generated dynamically that should be possible.  And if they wanted a url named foo that is static, it should be possible just by putting a foo file in the static directory.  The way the .html extension is handled in your framework violates this principle.  It's not possible to have both foo and foo.html as separate urls and it's impossible to have a static url that does not end in .html.

 4. Having dynamic content written to a file and then read from a file also seems inefficient.  File operations can be slow.  Also, the content may be too big to fit in memory.  To address this problem for static files, I used a generator which reads the file in chunks.

### Done

 1. **Done**. An exception can occur when the server is being started if an invalid port is provided (> 65536).  After looking at your code, I realized I did the same thing.  My solution was to catch the exception and raise a new one:

        try:
            serve(self, host=host, port=port)
        except Exception as e:
            raise RuntimeError("Unable to start server on "
                               "{}:{} ({})".format(host, port, e))

 2. **Done**. Port 0 seems to be generally acknowledged to mean some random available port and is accepted as such by HTTPServer.  If 0 is entered as the argument for port, it is converted to the default port.  To fix this 'if args.port:' in main should be 'if args.port != None'.  Further, if you make this change, the server will be started on some random port but the program will print that it is running on port 0.  You can get the port number through httpd.socket.getsockname()[1]

 5. **Done**. The 404 file not found message is being actually being sent as a 200 message.  The problem is that the send_response sequence is being sent  before send_error is called.  Those calls should only be made in the success case.

[end]
