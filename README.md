## Simple Web Framework

Assignment at https://hackpad.com/Week-1-Make-a-Web-Framework-qJOpEzlYJZY. Construct an HTTP server and add functionality to allow it to implement a simple web framework.

### How to use this program

 1. Clone the repository and run the HTTP server as

        python server.py 1234

   where 1234 is a port to listen on. Point your browser to `http://localhost:1234` to view the content being served. If no port is found on the command line, the default is 1924. Bear in mind that some ports may require special permissions. 

 1. This program requires Python3. 
 1. There is a requirements file, but at present (20140526) it only loads Ipython, which is not necessary to run the server.

 1. The server will serve named HTML files found in the `files` directory, including those in nested subdirectories. See the section **Results tested for**, below, for examples.

 1.  Functions corresponding to URLs should be added to `functions.py` in the section marked with a row of hash-signs. The server will keep track of those functions — assuming they work as written — without having to be restarted. When one of them occurs as the rightmost part of the path in a URL it will be called as a function; its return value will be saved to a file which is then served to the user. For instance, if the user sends a GET request

        http://localhost:1234/time.html

   the function `time()` will be run; it returns current Unix time formatted for human readability, and this value is saved to an actual file `time.html` which is then served as the response to the original request.

 1.  If a function has arguments, those arguments appear delimited by slashes. For example,

        http://localhost:1234/two_arg/1/2

   calls a function `two_arg()` which adds the arguments integers 1 and 2 and serves the resulting sum, 3.

 1.  Examples of actual functionality appear immediately below.

### Results tested for

 1. 

        http://localhost:1234/
        http://localhost:1234/index.html

   Returns: The contents of file `index.html`.

 1. 

        http://localhost:1234/help.html

   Returns: The contents of file `help.html`.

 1. 

        http://localhost:1234/subdir/file.html

   Returns: The contents of file `file.html` in subdirectory `subdir`.

 1. 

        http://localhost:1234/subdir/

   Returns: Program error message: `Path must end with ".html"; try again.` Assumes a subdirectory was meant but did not find a filename to search for in that subdirectory and did not reveal anything about the content of that subdirectory.

 1. 

        http://localhost:1234/subdir.html

   Returns: 404 error; no such file

 1. 

        http://localhost:1234/time.html
        http://localhost:1234/hello.html
        http://localhost:1234/shellfish.html
        http://localhost:1234/macguffin.html

   Returns: Each of these calls the zero-argument function named (before `.html`). Some of these were added during the running of the server and the server became aware of them without having to be restarted.

 1. 

        http://localhost:1234/one_arg/temperature

   Returns: Calls a function `one_arg(arg)` naming "temperature" as the argument.

 1. 

        http://localhost:1234/two_arg/1/2

   Returns: Calls a function `two_arg(arg1, arg2)` adding the two integer arguments following the function name.

 1. 

        http://localhost:1234/two_arg/1/2/4

   Returns: Reports exception due to the wrong number of arguments for the function `two_arg()`.


### Things to improve later

 1. Method `url_is_func()` assumes that there are no default arguments in the function supplied, when arguments are being counted. This could be wrong. We should use more of the information from `inspect.getfullargspec` in populating `functions.Functions.funcs`.


### Superseded versions 

These old versions, representing intermediate stages in the project, are found in `old_versions/` and are of little interest except to me.

 * Part 1: `server_01.py`. Works. 

   Run as

        python server_01.py 1234

   where 1234 is a port to listen on. If no port is found, the default is 1924.


 * Part 2, questions 1-2: `server02.py`. Works, but can be improved.

   To add new functions, add them below

        ```
#########################
```

   and then add their names to `self.special` in `CustomHandler.do_Get()`.

 * Part 2 question 1-2: `xerver_03.py`. Works.

   Run as

        python server_03.py 1234

   where 1234 is a port to listen on. If no port is found, the default is 1924.

   Functions corresponding to URLs should be added to `functions.py`. The class will keep track of those functions, and should they occur as the rightmost part of the path in a URL, less the extension .html, they will be called as functions and their return value saved to a file which is then served to the user. For instance, if the user sends a GET request

        http://localhost:1234/time.html

   the function `time()` will be run; it returns current Unix time formatted for human readability, and this value is saved to an actual file `time.html` which is then served as the response to the original request.
[end]
