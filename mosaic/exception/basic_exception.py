#!/usr/bin/env python3.6

class BasicException(Exception):
#args should ba a exception or error
    def __init__(self, args):
        self.args = args
        self.message = '[%(asctime)-15s][%(created)s]: ' + args.message + ' - ' + args.trace

    def __str__(self):
        return repr(self.message)
