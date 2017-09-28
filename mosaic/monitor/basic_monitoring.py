#!/usr/bin/env python3.6

import time


# This class yields a basic monitoring solution. It offers some functions to monitor service activities in a pipeline.
# The basic version of the monitoring writes every information to one file, which is configurable by defining a para-
# meter in the service parameters.
class BasicMonitoring:
    def __init__(self, **kwargs):
        self.arguments = kwargs

    # monitors msg receiving acitvities
    def msg_received(self, **kwargs):
        msg = '[' + str(kwargs) + ']' + ' MosaicMessage received at' + ' ' + str(time.time())
        print(msg)
        self.write_to_file(msg)

    # monitors msg dispatching acitvities
    def msg_dispatched(self, **kwargs):
        msg = '[' + str(kwargs) + ']' + ' MosaicMessage dispatched at' + ' ' + str(time.time())
        print(msg)
        self.write_to_file(msg)

    # monitors msgs which reached their final destination
    def msg_reached_final_destination(self, **kwargs):
        msg = '[' + str(kwargs) + ']' + ' MosaicMessage reached final destination at' + ' ' + str(time.time())
        print(msg)
        self.write_to_file(msg)

    # a helper function to write to a file
    def write_to_file(self, msg):
        fh = open(self.arguments['filename'], 'a')
        fh.write(msg + '\n')
        fh.close()
