# Inferfacing via the REST API

## Starting the API server

The production package includes a NodeJS server that provides an interface to your services. You can easily start it from within the roxcomposer folder:

```bash
cd roxcomposer
./start_server.sh
```

By default it will listen on port `7475` and log into the file `api-server.log`.

## Making requests

### Using an HTTP client

You can use the HTTP client to talk to the API server. I will show a sample request with curl.

```bash
curl -XPOST http://localhost:7475/start_service -H 'Content-Type: application/json' -d '{"path": "/path/to/myservice.py", "params": {"name": "myservice_instance", "ip": "127.0.0.1", "port": 1337}}'
```

The params section of the JSON string will be passed on to the invocation of myservice.py analogous to the implementation example in the Implementation section.

In the default configuration the following endpoints are available:

#### /start\_service

- Description: Start a service.
- Method: `POST`
- Parameters:
  - Required:
    - `path|classpath` - either a *path* to a python module or a qualified *class* (see below).
    - `params.name` - the name of ther service.
    - `params.ip` - the service's IP.
    - `params.port` - the service's port number.
  - Optional: the `params` field can contain arbitrary subfields. The whole structure will be passed on to the service.

#### /services

- Description: Get a list of the currently running services along with their invokation parameters.
- Method: `GET`
- Parameters: none

#### /shutdown\_service

- Description: Shutdown a running service.
- Method: `POST`
- Parameters:
  - Required:
    - `name`: the name of the service.

#### /set\_pipeline

- Description: Define a pipeline, overriding a previous pipeline with the same name if present.
- Method: `POST`
- Parameters:
  - Required:
    - `name`: the name of the pipeline.
    - `services`: an array of service names that make up the pipeline in their intended order.

#### /delete\_pipeline

- Description: Delete a previously defined pipeline
- Method: `DELETE`
- Parameters:
  - Required:
    - `name`: the name of the pipeline.
    
#### /pipelines

- Description: Get a list of the currently defined pipelines.
- Method: `GET`
- Parameters: none

#### /post\_to\_pipeline

- Description: Send data into a pipeline. The response will contain a `message-id` which can be used to track the status of the message.
- Method: `POST`
- Parameters:
  - Required:
    - `name`: the name of the pipeline.
    - `data`: A string to send into the pipeline.

#### /get\_message\_history

- Description: Retrieve the message trace for a message.
- Method: `POST`
- Parameters:
  - Required:
    - `message_id`: the id of the message.

#### /get\_message\_status

- Description: Retrieve the staus of a message. The status is one of `in_transit`, `processing` or `finalized`.
- Method: `POST`
- Parameters:
  - Required:
    - `message_id`: the id of the message.

#### /dump\_services\_and\_pipelines

- Description: Dump the currently running service configs and the defined pipelines.
- Method: `GET`
- Parameters: none

#### /load\_services\_and\_pipelines

- Description: Restore a previsously dumped state. Services will be attempted to start and pipelines restored if possible.
- Method: `POST`
- Parameters: a previously saved dump.

#### /get\_logsession

- Description: Retrieve information about a specific session.
- Method: `POST`
- Parameters:
  - Required:
    - `id`: the id of the log session.
   
#### /roxcomposer_log_observer

- Description: Retrieve server logs.
- Method: `GET`
- Parameters: none

#### /roxcomposer_log_observer

- Description: Create a log session for server logs.
- Method: `PUT`
- Parameters: none

#### /log\_observer

- Description: Start a new service log observation session. Returns a `sessionid` for reference.
- Method: `PUT`
- Parameters:
  - Required:
    - `lines`: the number of log lines that are buffered internally.
    - `timeout`: the number of seconds of inactivity after which the session will be cleaned up.
  - Optional:
    - `services`: an array of service names that will be observed

- Description: Add additional services to a log session
- Method: `POST`
- Parameters:
  - Required:
    - `sessionid`: the id of the log session.
    - `services`: an array of service names that will be observed

- Description: Retrieve log lines from observed services.
- Method: `GET`
- Parameters:
  - Required:
    - `sessionid`: the id of the log session.

- Description: Remove services from this log session or delete the whole session if no services are specified.
- Method: `DELETE`
- Parameters:
  - Required:
    - `sessionid`: the id of the log session.
  - Optional:
    - `services`: an array of service names that will removed from observation.

### Loading via classpath

If you choose to provide a module path, e.g. `somepackage.subpackge.module`, a service container will be started that loads the module with the parameters provided and call the `listen()` method. There is no version of that
container that calls `listen_thread()` at this point since we would need to impose a standard way of constructing the main thread functionality in order to call it generically.


### Using the roxcomposer-cli

Since writing curl requests can be quite cumbersome the roxcomposer package includes a cli shell that streamlines the process.

```bash
./roxcomposer-cli.py
```

This will open an new terminal ui with two windows and a text input. The first window is for logging while the second is a command history.  
`help` will provide you with a list of available commands. Most of them mimick the underlying REST API:

#### start\_service

Assuming you want to start a service with the following parmeters:

```json
{
  "classpath": "pack.services.MyService",
  "params": {
    "name": "AwesomeService",
    "ip": "127.0.0.1",
    "port": 5001,
    "the_answer": 42
  }
}
```

The package directory contains a services folder. If you write the above configuration into services/myservice.json you can easily start that service with the following call:

```bash
start_service myservice
```

The myservice argument refers to the file name - `myservice.json` - without the suffix. Please note that the service will be deployed under the name `AwesomeService` and not as `myservice`.

#### services

Lists the active services

#### set\_pipeline

This allows you to set a pipeline by naming it and listing the name's of the services it should contain:

```bash
set_pipeline pipe myservice myotherservice gotanotherone
```

#### pipelines

List the defined pipelines.

#### post\_to\_pipeline

Post a message to a pipeline of your choice:

```bash
post_to_pipeline pipe "Hello world!"
```

#### shutdown\_service

Shutdown a service and set all pipelines to inactive if the service is part of their pipeline.

```bash
shutdown_service my_service.service
```

#### dump

Retrieve a dump of the running services and defined pipelines and write it into a file. If the filename is omitted a `dump.json` will be used.

```bash
dump dump.json
```

#### get\_msg\_history

Retrieve a message trace given a message id

```bash
get_msg_history 3af-3413fa-234faa-908a-394800
```

#### restore\_server

```command-line
restore_server /path/to/dump.json
```

#### restore\_pipeline

Load the pipelines configuration from (server) path and activate this.

```bash
restore_pipeline path_pipe
```

#### watch\_services

Starts a new log observation session for the provided services or adds them to an existing session. The cli manages the session in the background and regularly polls the
API for new log lines which will be written into the log window.

```bash
watch_services serv1 serv2 serv3
```

#### unwatch\_services

Remove watched services from the session.

```bash
unwatch_services serv2 serv3
```

#### watch\_pipelines

Starts a new log observation session for the provided pipelines or adds them to an existing session. The cli manages the session in the background and regularly polls the
API for new log lines which will be written into the log window.

```bash
watch_pipelines pipe1 pipe2 pipe3
```

#### unwatch\_pipelines

Remove watched pipelines from the session.

```bash
unwatch_pipelines pipe2 pipe3
```

#### reset\_watchers

This cleans up the log session - services are no longer watched.

```bash
reset_watchers
```

