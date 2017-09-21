#!/usr/bin/env python3

import sys
import json
import mosaic.service_loader

def usage():
    print("usage: python3 " + sys.argv[0] + " <CLASSPATH> <JSON-ARGS>")
    sys.exit(0)

if len(sys.argv) < 3:
    usage()

classpath = sys.argv[1]
args = json.loads(sys.argv[2])

mosaic.service_loader.start_service(classpath, args)
