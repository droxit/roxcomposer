#!/usr/bin/env python3.6

class BasicError():
    def __init__(self, message):

        self.message = '[%(asctime)-15s][%(created)s]: ' + message
        self.logger.error(self.message)

    def __str__(self):
        return repr(self.message)
