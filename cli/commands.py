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
    if len(args) != 0:
        return 'WARNING: superfluous arguments to services: {}'.format(args)
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

def get_pipelines(*args):
    r = requests.get('http://{}/pipelines'.format(roxconnector))
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

def shutdown_service(*args):
    if len(args) != 1:
        return 'ERROR: exactly one service needs to be specified for shutdown'

    service = args[0]
    d = { 'name': service }
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://{}/shutdown_service'.format(roxconnector), data=json.dumps(d), headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

def dump_everything(*args):
    if len(args) > 1:
        return 'WARNING: superfluous arguments to services: {}'.format(args[1:])
    dumpfile = 'dump.json'
    if len(args) == 1:
        dumpfile = args[0]

    f = None
    try:
        f = open(dumpfile, 'w')
    except Exception as e:
        return 'ERROR unable to open file {} - {}'.format(dumpfile, e)

    r = requests.get('http://{}/dump_services_and_pipelines'.format(roxconnector))
    if r.status_code == 200:
        o = r.json()
        try:
            json.dump(o, f)
        except Exception as e:
            return 'ERROR: unable to write dump to file {} - {}'.format(dumpfile, e)
        finally:
            f.close()
            
        return "dump written to file {}\n{}".format(dumpfile, r.text)
    else:
        f.close()
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

def load_services_and_pipelines(*args):
    if len(args) > 1:
        return 'WARNING: superfluous arguments to services: {}'.format(args[1:])

    if os.path.isfile(args[0]):
        restore_json = json.loads(open(args[0]).read())
        #with open(args[0]) as json_file:
        #    restore_json = json.load(json_file)

    else:
        return 'file {} not found'.format(args[0])

    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://{}/load_services_and_pipelines'.format(roxconnector), data=json.dumps(restore_json), headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

def load_and_start_pipeline(*args):
    if len(args) > 1:
        return 'WARNING: superfluous arguments to services: {}'.format(args[1:])

    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://{}/load_and_start_pipeline'.format(roxconnector), args[0], headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

def list_commands(*args):
    return "available commands: \n\t" + "\n\t".join([x for x in cmd_map])


cmd_map = {
        'list_service_files': list_service_files,
        'services': get_services,
        'pipelines': get_pipelines,
        'start_service': start_service,
        'set_pipeline': set_pipeline,
        'shutdown_service': shutdown_service,
        'dump': dump_everything,
        'restore_server': load_services_and_pipelines,
        'restore_pipeline': load_and_start_pipeline,
        'help': list_commands
}


def run_cmd(*args):
    if len(args) == 0:
        raise RuntimeError('no command given')
    if args[0] not in cmd_map:
        raise RuntimeError("command '{}' is not defined".format(args[0]))

    return cmd_map[args[0]](*args[1:])
