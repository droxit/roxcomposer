#!/usr/bin/env python3


class ParameterMissing(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidMosaicMessage(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NotAClass(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# This class yields a basic exception implementation, in this case to warn if a parameter is missing that is asked for
# in the config
class ParameterMissingException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
