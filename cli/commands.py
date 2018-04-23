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
logobs_session = None
logobs_session_timeout = 3600

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
        service_args = json.load(f)
    except Exception as e:
        return 'ERROR unable to load service {} - {}'.format(service, e)

    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://{}/start_service'.format(roxconnector), json=service_args, headers=headers)
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
    r = requests.post('http://{}/shutdown_service'.format(roxconnector),json=d, headers=headers)
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

def watch_services(*services):
    if len(services) is 0:
        return "No services specified"

    global logobs_session
    global logobs_session_timeout

    if logobs_session is None:
        logobs_session = dict()
        logobs_session['services'] = set()
        data = { 'lines': 100, 'timeout': logobs_session_timeout, 'services': services }
        headers = {'Content-Type': 'application/json'}
        r = requests.put('http://{}/log_observer'.format(roxconnector), headers=headers, json=data)

        if r.status_code != 200:
            return 'ERROR: {}'.format(r.text)

        logobs_session['id'] = r.json()['sessionid']

        for s in services:
            logobs_session['services'].add(s)

        return { 'response': 'service observation initiated - session timout is {}s'.format(logobs_session_timeout), 'callback': get_service_logs }

    else:
        s = [x for x in filter(lambda s: s not in logobs_session['services'], services)]

        if len(s):
            data = { 'sessionid': logobs_session['id'], 'services': s }
            headers = {'Content-Type': 'application/json'}
            r = requests.post('http://{}/log_observer'.format(roxconnector), headers=headers, json=data)

            if r.status_code != 200:
                return 'ERROR: {}'.format(r.text)

            return 'services added {}'.format(s)

        return 'services already watched'

def get_service_logs():
    if logobs_session is None:
        return 'no services are currently under observation'

    data = { 'sessionid': logobs_session['id'] }
    headers = {'Content-Type': 'application/json'}
    r = requests.get('http://{}/log_observer'.format(roxconnector), headers=headers, json=data)

    if r.status_code != 200:
        return 'ERROR: {}'.format(r.text)

    return "\n".join(r.json()['loglines'])



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
        'watch_services': watch_services,
        'help': list_commands
}


def run_cmd(*args):
    if len(args) == 0:
        raise RuntimeError('no command given')
    if args[0] not in cmd_map:
        raise RuntimeError("command '{}' is not defined".format(args[0]))

    return cmd_map[args[0]](*args[1:])
