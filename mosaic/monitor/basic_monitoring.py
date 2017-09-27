#!/usr/bin/env python3.6

import time


class BasicMonitoring:
    def __init__(self, **kwargs):
        self.arguments = kwargs

    def msg_received(self):
        print('MosaicMessage received at', time.time())

    def msg_dispatched(self):
        print('MosaicMessage dispatched at', time.time())

    def msg_reached_final_destination(self):
        print('MosaicMessage reached final destination at', time.time())
