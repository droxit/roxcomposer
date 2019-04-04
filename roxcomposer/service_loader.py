import importlib
import inspect
from roxcomposer import exceptions


def load_class(classpath):
    if classpath is None:
        #FixMe: how is it to be logged here?
        #self.logger.critical('_classpath: ' + classpath)
        raise exceptions.ParameterMissing("classpath is empty")

    try:
        components = classpath.split('.')
        modpath = ".".join(components[:-1])
        classname = components[-1]
        mod = importlib.import_module(modpath)
        c = getattr(mod, classname)
    except Exception as e:
        raise exceptions.ConfigError('Failed to load the specified logging class: {} - {}'.format(classpath, e)) from e

    if not inspect.isclass(c):
        #FixMe: how is it to be logged here?
        #self.logger.critical('_classpath: ' + classpath)
        raise exceptions.NotAClass(classpath)

    return c


def make_service_instance(classpath, args):
    try:
        c = load_class(classpath)
        return c(args)
    except Exception as e:
        raise exceptions.EmptyModule("Could not load module with classpath {} - {}".format(classpath, e)) from e
