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


# post a message to pipeline
# needs the pipeline name and the message as args
def post_to_pipeline(*args):
    if len(args) < 2:
        raise RuntimeError('ERROR: a pipeline name and a message must be specified')

    d = {'name': args[0], 'data': " ".join(args[1:])}
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://{}/post_to_pipeline'.format(roxconnector), data=json.dumps(d), headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        raise RuntimeError('ERROR: {} - {}'.format(r.status_code, r.text))


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


# get message history by message id
def get_msg_history(*args):
    if len(args) > 1:
        return 'WARNING: superfluous arguments to get msg history: {}'.format(args)
    msg_id = args[0].strip("'\"")
    d = {'message_id': msg_id}

    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://{}/get_msg_history'.format(roxconnector), data=json.dumps(d), headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)


def set_pipeline(*args):
    if len(args) < 2:
        return 'ERROR: a pipeline name and at least one service must be specified'
    pipename = args[0]
    services = args[1:]
    d = {'name': pipename, 'services': services}
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
    d = {'name': service}
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
        f = open(args[0], "r")
        restore_json = json.loads(f.read())
        f.close()

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

    pipe_path = args[0]
    d = { 'pipe_path': pipe_path }

    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://{}/load_and_start_pipeline'.format(roxconnector), data=json.dumps(d), headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)


def help(*args):
    if len(args) > 1:
        return 'WARNING: superfluous arguments to services: {}'.format(args[1:])
    if len(args) == 1:
        if args[0] not in cmd_map:
            return "command '{}' is not defined".format(args[0])
        return cmd_map[args[0]]['doc_string']
    return "available commands: \n  " + "\n  ".join([x for x in cmd_map])


cmd_map = {
    'list_service_files': {
        'function_call': list_service_files,
        'doc_string': "list_service_files - "
                      +"Lists the available service files."
    },
    'services': {
        'function_call': get_services,
        'doc_string': "services - "
                      +"Lists the running services."
    },
    'pipelines': {
        'function_call': get_pipelines,
        'doc_string': "pipelines - "
                      +"Lists the stored pipelines."
    },
    'start_service': {
        'function_call': start_service,
        'doc_string': "start_service <SERVICE_FILE> - "
                      +"Starts a service from the service file."
                      +"Use 'list_service_files' to get a list of available services"
    },
    'set_pipeline': {
        'function_call': set_pipeline,
        'doc_string': "set_pipeline <NAME> [SERVICES] - "
                      +"Sets up a linear pipeline on a given service list.\n"
                       "Example: 'set_pipeline name serv1 serv2 serv3'"
    },
    'shutdown_service': {
        'function_call': shutdown_service,
        'doc_string': "shutdown_service <NAME> - "
                      +"Shuts down a service and sets all pipelines to inactive if the service is part of it."
                      +"Use 'services' to get a list of all running services."
    },
    'dump': {
        'function_call': dump_everything,
        'doc_string': "dump - "
                      +"Dumps of the running services and defined pipelines."
    },
    'restore_server': {
        'function_call': load_services_and_pipelines,
        'doc_string': "restore_server <DUMP_FILE_PATH> "
                      + "Restore a previously taken service and pipeline dump.\n"
                        "Example: 'restore_server dump.json'"
    },
    'restore_pipeline': {
        'function_call': load_and_start_pipeline,
        'doc_string': "restore_pipeline <PIPELINE_DUMP_FILE_PATH> "
                      + "Load the pipelines configuration from (server) path and activate this.\n"
                        "Example: 'restore_pipeline pipeline_backup.json'"
    },
    'help': {
        'function_call': help,
        'doc_string': "help - "
                      +"Use 'help' to get a list of all commands or 'help <COMMAND>' to get help for a certain command."
    }
}


def run_cmd(*args):
    if len(args) == 0:
        raise RuntimeError('no command given')
    if args[0] not in cmd_map:
        raise RuntimeError("command '{}' is not defined".format(args[0]))

    return cmd_map[args[0]]['function_call'](*args[1:])
