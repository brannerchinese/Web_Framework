#!/usr/bin/env python
# functions.py
# David Prager Branner
# 20140526

"""Add functions to this class for use with the simple web server."""

import datetime
import time
import inspect

class Functions():
    def __init__(self):
        dir_contents = self.__dir__()
        self.funcs = {}
        # For each non-"magic" method, register its name and its arg-count.
        for item in dir_contents:
            if len(item) < 5 or (item[0:2] != '__' and item[-2:] != '__'):
                func = self.__getattribute__(item)
                argspec = inspect.getfullargspec(func)
                # Subtract 1, since we never want to count self.
                self.funcs[item] = len(argspec.args) - 1

    #########################
    # Add new functions here. They will be automatically added to self.funcs.
    def hello(self):
        return 'Hello world!'

    def time(self):
        """Convert Unix time to human-readable string."""
        date = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M')
        return date

    def shellfish(self):
        return 'Is it selfish to love shellfish?'

    def macguffin(self):
        return 'This is not the MacGuffin you were looking for.'

    def one_arg(self, arg):
        return 'The argument you supplied was "{}". Am I right?'.format(arg)

    def two_arg(self, a, b):
        import operator
        return str(operator.add(int(a), int(b)))

    #########################

