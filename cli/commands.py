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


# post a message to pipeline
# needs the pipeline name and the message as args
def post_to_pipeline(*args):
    if len(args) < 2:
        raise RuntimeError('ERROR: a pipeline name and a message must be specified')

    d = {'name': args[0], 'data': " ".join(args[1:])}
    headers = {'Content-Type': 'application/json'}

    try:
        r = requests.post('http://{}/post_to_pipeline'.format(roxconnector), data=json.dumps(d), headers=headers)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

    if r.status_code == 200:
        return r.text
    else:
        raise RuntimeError('ERROR: {} - {}'.format(r.status_code, r.text))


def get_services(*args):
    if len(args) != 0:
        return 'WARNING: superfluous arguments to services: {}'.format(args)

    try:
        r = requests.get('http://{}/services'.format(roxconnector))
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

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
        service_args = json.load(f)
    except Exception as e:
        return 'ERROR unable to load service {} - {}'.format(service, e)

    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post('http://{}/start_service'.format(roxconnector), json=service_args, headers=headers)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)
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
    try:
        r = requests.post('http://{}/get_msg_history'.format(roxconnector), data=json.dumps(d), headers=headers)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)
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
    try:
        r = requests.post('http://{}/set_pipeline'.format(roxconnector), data=json.dumps(d), headers=headers)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)
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
    try:
        r = requests.post('http://{}/shutdown_service'.format(roxconnector),json=d, headers=headers)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

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

    try:
        r = requests.get('http://{}/dump_services_and_pipelines'.format(roxconnector))
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

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
        return "ERROR - no services specified"

    global logobs_session
    global logobs_session_timeout

    if logobs_session is None:
        session = dict()
        session['services'] = set()
        data = { 'lines': 100, 'timeout': logobs_session_timeout, 'services': services }
        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.put('http://{}/log_observer'.format(roxconnector), headers=headers, json=data)
        except requests.exceptions.ConnectionError as e:
            return "ERROR: no connection to server - {}".format(e)

        if r.status_code != 200:
            return 'ERROR: {}'.format(r.text)

        session['id'] = r.json()['sessionid']

        for s in services:
            session['services'].add(s)

        logobs_session = session
        return { 'response': r.text, 'callback': get_service_logs }

    else:
        s = [x for x in filter(lambda s: s not in logobs_session['services'], services)]
        nots = [x for x in filter(lambda s: s in logobs_session['services'], services)]

        ret = ''
        if len(nots):
            ret = 'already watched: {}\n'.format(nots)

        if len(s):
            data = { 'sessionid': logobs_session['id'], 'services': s }
            headers = {'Content-Type': 'application/json'}
            try:
                r = requests.post('http://{}/log_observer'.format(roxconnector), headers=headers, json=data)
            except requests.exceptions.ConnectionError as e:
                return ret + "ERROR: no connection to server - {}".format(e)

            if r.status_code != 200:
                return ret + 'ERROR: {}'.format(r.text)

            ml = r.json()
            for s in ml['ok']:
                logobs_session['services'].add(s)

            return ret + r.text

        return 'All services already watched'


def unwatch_services(*services):
    if len(services) is 0:
        return "No services specified"

    global logobs_session

    if logobs_session is None:
        return "No services are being watched at the moment"

    s = [x for x in filter(lambda s: s in logobs_session['services'], services)]

    if len(s) == 0:
        return "The specified services are not being watched"

    data = { 'sessionid': logobs_session['id'], 'services': s }
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.delete('http://{}/log_observer'.format(roxconnector), headers=headers, json=data)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

    if r.status_code != 200:
        return 'ERROR: {}'.format(r.text)

    else:
        logobs_session['services'] = logobs_session['services'].difference(set(s))
        return "Services no longer watched: {}".format(s)


def watch_pipelines(*pipelines):
    if len(pipelines) is 0:
        return "ERROR - no pipelines specified"

    # get pipelines
    r = requests.get('http://{}/pipelines'.format(roxconnector))
    if r.status_code != 200:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

    pipe_list = json.loads(r.text)
    services_lists = [pipe_list[pipe]['services'] for pipe in pipelines if pipe in pipe_list]
    services = list(set([service for sublist in services_lists for service in sublist]))
    nots = list(set([pipe for pipe in pipelines if pipe not in pipe_list]))

    ret = watch_services(*services)
    ret_str = 'not defined: {}\n'.format(nots) if nots else ''
    if isinstance(ret, dict):
        ret_str += ret['response']
        return {'response': ret_str, 'callback': ret['callback']}

    ret_str += ret
    return ret_str


def unwatch_pipelines(*pipelines):
    if len(pipelines) is 0:
        return "No pipelines specified"

    # get pipelines
    r = requests.get('http://{}/pipelines'.format(roxconnector))
    if r.status_code != 200:
        return 'ERROR: {} - {}'.format(r.status_code, r.text)

    pipe_list = json.loads(r.text)
    services_lists = [pipe_list[pipe]['services'] for pipe in pipelines if pipe in pipe_list]
    services = list(set([service for sublist in services_lists for service in sublist]))
    nots = list(set([pipe for pipe in pipelines if pipe not in pipe_list]))

    ret = unwatch_services(*services)
    ret_str = 'not defined: {}\n'.format(nots) if nots else ''

    ret_str += ret
    return ret_str


def watch_all():
    # get services
    r = json.loads(get_services())
    services = [key for key in r if not key == "basic_reporting"]

    return watch_services(*services)


def reset_watchers():
    global logobs_session

    if logobs_session is None:
        return

    logobs_session = None

    data = { 'sessionid': logobs_session['id'] }
    headers = {'Content-Type': 'application/json'}
    try:
        requests.delete('http://{}/log_observer'.format(roxconnector), headers=headers, json=data)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

    # we don't care about the return value - an error in almost all cases means that the session
    # has expired, in the remaining cases it is ok to abandon the session and to let it time out
    # on the server

    return "Watchers removed"


def get_service_logs():
    if logobs_session is None:
        raise RuntimeError('no services are currently under observation')

    data = { 'sessionid': logobs_session['id'] }
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.get('http://{}/log_observer'.format(roxconnector), headers=headers, json=data)
    except requests.exceptions.ConnectionError as e:
        return "ERROR: no connection to server - {}".format(e)

    if r.status_code != 200:
        raise RuntimeError(r.text)

    return "\n".join(r.json()['loglines'])


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
    return "available commands: \n  " + "\n  ".join([x for x in sorted(cmd_map)])


cmd_map = {
    'help': {
        'function_call': help,
        'doc_string': "help - "
                      + "Use 'help' to get a list of all commands or 'help <COMMAND>' to get help for a certain command."
    },
    'list_service_files': {
        'function_call': list_service_files,
        'doc_string': "list_service_files - "
                      + "Lists the available service files."
    },
    'services': {
        'function_call': get_services,
        'doc_string': "services - "
                      + "Lists the running services."
    },
    'pipelines': {
        'function_call': get_pipelines,
        'doc_string': "pipelines - "
                      + "Lists the stored pipelines."
    },
    'post_to_pipeline': {
        'function_call': post_to_pipeline,
        'doc_string': "post_to_pipeline <PIPELINE_NAME> <MESSAGE> - post the given message into the pipeline"
    },
    'get_msg_history': {
        'function_call': get_msg_history,
        'doc_string': "get_msg_history <MESSAGE ID> - retrieve a message trace for the given message"
    },
    'watch_services': {
        'function_call': watch_services,
        'doc_string': "watch_services <SERVICE1 [,SERVICE2 [,...]]> - add services to log observation"
    },
    'unwatch_services': {
        'function_call': unwatch_services,
        'doc_string': "unwatch_services <SERVICE1 [,SERVICE2 [,...]]> - remove services from log observation"
    },
    'watch_pipelines': {
        'function_call': watch_pipelines,
        'doc_string': "watch_pipelines <PIPELINE1 [,PIPELINE2 [,...]]> - add pipelines to log observation"
    },
    'unwatch_pipelines': {
        'function_call': unwatch_pipelines,
        'doc_string': "unwatch_pipelines <PIPELINE1 [,PIPELINE2 [,...]]> - remove pipelines from log observation"
    },
    'watch_all': {
        'function_call': watch_all,
        'doc_string': "watch_all - complete log observation"
    },
    'reset_watchers': {
        'function_call': reset_watchers,
        'doc_string': "reset_watchers - clear log observation, all services are removed"
    },
    'start_service': {
        'function_call': start_service,
        'doc_string': "start_service <SERVICE_FILE> - "
                      + "Starts a service from the service file."
                      + "Use 'list_service_files' to get a list of available services"
    },
    'set_pipeline': {
        'function_call': set_pipeline,
        'doc_string': "set_pipeline <NAME> [SERVICES] - "
                      + "Sets up a linear pipeline on a given service list.\n"
                      + "Example: 'set_pipeline name serv1 serv2 serv3'"
    },
    'shutdown_service': {
        'function_call': shutdown_service,
        'doc_string': "shutdown_service <NAME> - "
                      + "Shuts down a service and sets all pipelines to inactive if the service is part of it."
                      + "Use 'services' to get a list of all running services."
    },
    'dump': {
        'function_call': dump_everything,
        'doc_string': "dump - "
                      + "Dumps of the running services and defined pipelines."
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
                      + "Example: 'restore_pipeline pipeline_backup.json'"
    }
}


def run_cmd(*args):
    if len(args) == 0:
        raise RuntimeError('no command given')
    if args[0] not in cmd_map:
        raise RuntimeError("command '{}' is not defined".format(args[0]))

    return cmd_map[args[0]]['function_call'](*args[1:])
