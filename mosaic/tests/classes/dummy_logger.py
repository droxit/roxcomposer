## dummy logging class - for testing purposes only
class DummyLog():
    def __init__(self, name, **kwargs):
        self.file = kwargs['filename']

    def debug(self, msg):
        f = open(self.file, 'w')
        f.write(msg)
        f.close()

    def info(self, msg):
        pass

    def warn(self, msg):
        pass

    def error(self, msg):
        pass

    def critical(self, msg):
        pass

