# encoding: utf-8
#
# dummy monitoring class - for testing purposes only
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#


class DummyMonitor:
    def __init__(self, **kwargs):
        self.arguments = kwargs

    # monitors msg receiving acitvities
    def msg_received(self):
        fh = open(self.arguments['filename'], 'a')
        fh.write('DUMMY RECEIVE \n')
        fh.close()

    # monitors msg dispatching acitvities
    def msg_dispatched(self):
        fh = open(self.arguments['filename'], 'a')
        fh.write('DUMMY DISPATCH \n')
        fh.close()

    # monitors msgs which reached their final destination
    def msg_reached_final_destination(self):
        fh = open(self.arguments['filename'], 'a')
        fh.write('DUMMY DESTINATION \n')
        fh.close()

    def msg_error(self):
        fh = open(self.arguments['filename'], 'a')
        fh.write('DUMMY ERROR \n')
        fh.close()


def not_a_class():
    pass
