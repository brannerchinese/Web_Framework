## Simple Web Framework

Assignment at https://hackpad.com/Week-1-Make-a-Web-Framework-qJOpEzlYJZY.

### Working versions

 * Part 2: `xerver_03.py`. Works.

   Run as

        python server_03.py 1234

   where 1234 is a port to listen on. If no port is found, the default is 1924.

   Functions corresponding to URLs should be added to `functions.py`. The class will keep track of those functions, and should they occur as the rightmost part of the path in a URL, less the extension .html, they will be called as functions and their return value saved to a file which is then served to the user. For instance, if the user sends a GET request

        http://localhost:1234/time.html

   the function `time()` will be run; it returns current Unix time formatted for human readability, and this value is saved to an actual file `time.html` which is then served as the response to the original request.


### Superseded

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

[end]
