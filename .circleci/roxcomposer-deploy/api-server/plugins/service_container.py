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
