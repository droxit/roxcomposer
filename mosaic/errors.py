#!/usr/bin/env python3
from mosaic.error import basic_error

class ParameterMissing(basic_error.BasicError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidMosaicMessage(basic_error.BasicError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NotAClass(basic_error.BasicError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
