#! /usr/bin/env python3
#
# commands.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

import json
import os
import requests

roxconnector = 'localhost:7475'
service_file_dir = 'services'

def list_service_files(*args):
    ret = []
    for f in os.scandir(service_file_dir):
        if f.is_file() and f.name.endswith('.json'):
            ret.append(f.name)

    return "\n".join(ret)


def get_services(*args):
    r = requests.get('http://{}/services'.format(roxconnector))
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)
    
def start_service(*args):
    if len(args) > 1:
        return 'WARNING: superfluous arguments to start service: {}'.format(args)
    service = args[0]
    print(args)

    service_args = None
    try:
        f = open('./services/{}.json'.format(service))
        service_args = f.read()
    except Exception as e:
        return 'ERROR unable to load service {} - {}'.format(service, e)

    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://{}/start_service'.format(roxconnector), data=service_args, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

def set_pipeline(*args):
    if len(args) < 2:
        return 'ERROR: a pipeline name and at least one service must be specified'
    pipename = args[0]
    services = args[1:]
    d = { 'name': pipename, 'services': services }
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://{}/set_pipeline'.format(roxconnector), data=json.dumps(d), headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)


def list_commands(*args):
    return "available commands: \n\t" + "\n\t".join([x for x in cmd_map])


cmd_map = {
        'list_service_files': list_service_files,
        'services': get_services,
        'start_service': start_service,
        'set_pipeline': set_pipeline,
        'help': list_commands
}


def run_cmd(*args):
    if len(args) == 0:
        raise RuntimeError('no command given')
    if args[0] not in cmd_map:
        raise RuntimeError("command '{}' is not defined".format(args[0]))

    return cmd_map[args[0]](*args[1:])
