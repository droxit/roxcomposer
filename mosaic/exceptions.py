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
