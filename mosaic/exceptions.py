#!/usr/bin/env python3


class ParameterMissingException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
