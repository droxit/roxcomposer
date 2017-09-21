#!/usr/bin/env python3

import sys
import importlib
import inspect
from mosaic import exceptions

def load_class(classpath):
    if classpath is None:
        raise exceptions.ParameterMissing("classpath is empty")

    components = classpath.split('.')
    modpath = ".".join(components[:-1])
    classname = components[-1]
    mod = importlib.import_module(modpath)
    c = getattr(mod, classname)

    if not inspect.isclass(c):
        raise exceptions.NotAClass(classpath)

    return c

def start_service(classpath, args):
    c = load_class(classpath)

    c(args)

