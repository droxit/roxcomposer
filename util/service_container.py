# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This program is free software: you can redistribute it and/or modify |
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
#
#!/usr/bin/env python3

import sys
import json
import roxcomposer.service_loader

def usage():
    print("usage: python3 " + sys.argv[0] + " <CLASSPATH> <JSON-ARGS>")
    sys.exit(0)

if len(sys.argv) < 3:
    usage()

classpath = sys.argv[1]
args = json.loads(sys.argv[2])

srv = roxcomposer.service_loader.make_service_instance(classpath, args)
srv.listen()
