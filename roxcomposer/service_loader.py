# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|

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
