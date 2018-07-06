# encoding: utf-8
#
# dummy logging class - for testing purposes only
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#


class DummyLog:
    def __init__(self, name, **kwargs):
        self.name = name
        self.file = kwargs['logpath']

    def debug(self, msg, **kwargs):
        f = open(self.file, 'w')
        f.write(msg)
        f.close()

    def info(self, msg, **kwargs):
        pass

    def warn(self, msg, **kwargs):
        pass

    def error(self, msg, **kwargs):
        pass

    def critical(self, msg, **kwargs):
        pass


def not_a_class():
    pass
