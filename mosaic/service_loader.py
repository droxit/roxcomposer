#!/usr/bin/env python3

import sys
import json
import importlib

def load_class(classpath):
    components = classpath.split('.')
    modpath = ".".join(components[:-1])
    classname = components[-1]
    mod = importlib.import_module(modpath)
    c = getattr(mod, classname)

    return c

def start_service(classpath, argstring):
    params = json.loads(argstring)
    c = load_class(classpath)

    c(params)

