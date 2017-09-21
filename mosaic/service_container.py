#!/usr/bin/env python3

import sys
import json
import importlib

def load_class(classname):
    components = classname.split('.')
    modpath = ".".join(components[:-1])
    classname = components[-1]
    mod = importlib.import_module(modpath)
    c = getattr(mod, classname)

    return c


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('not enough arguments provided')
        exit(1)

    name = sys.argv[1]
    try:
        params = json.loads(sys.argv[2])
    except Exception:
        print('unable to load args - invalid json?')

    c = load_class(sys.argv[1])

    c(params)

