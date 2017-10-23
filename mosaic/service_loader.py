#!/usr/bin/env python3

import importlib
import inspect
from mosaic import errors


def load_class(classpath):
    if classpath is None:
        raise errors.ParameterMissing("classpath is empty")

    components = classpath.split('.')
    modpath = ".".join(components[:-1])
    classname = components[-1]
    mod = importlib.import_module(modpath)
    c = getattr(mod, classname)

    if not inspect.isclass(c):
        raise errors.NotAClass(classpath)

    return c


def make_service_instance(classpath, args):
    c = load_class(classpath)

    return c(args)

