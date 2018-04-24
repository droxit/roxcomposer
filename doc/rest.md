# Inferfacing via the REST API

## Starting the API server

The production package includes a NodeJS server that provides an interface to your services. You can easily start it from within the mosaic folder:

```bash
cd mosaic
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

| Endpoint | HTTP verb  | Data | Description |
| -------- | ---------- | ---- | ----------- |
| start\_service | POST | <ul><li>path (string): the path to the python module to start.</li><li>classpath (string): the python package to load</li><li>params (json string): see the chapter on implementing a service for details</li></ul> | This starts a new service. Either `path` or `classpath` is required to find the right python module (see below for details). |
| services | GET |  | Get information on the running services |
| set\_pipeline | POST | <ul><li>name (string) - the pipelines name (pipelines under the same name will be overridden)</li><li>services (array of strings) - the names of the services the pipeline should consist of. Messages sent to this pipeline will pass through all services mentioned here in the same sequence</li></ul> | Define a pipeline |
| pipelines | GET | | Show defined pipelines |
| post\_to\_pipeline | POST | <ul><li>name (string) - the name of the pipeline that the data should put in</li><li>data (string) - the payload that should be transported</li><ul> | Send a message into a pipeline |
| shutdown\_service | POST | name (string) - the services name in the pipeline | Shuts down a service with the SIGTERM os signal |
| get\_msg\_history | POST | message\_id (string) - the message id of the message in question | Retrieves all monitoring information for this message |
| get\_msg\_status | POST | message\_id (string) - the message id of the message in question | Retrieves the last known status for this message |
| dump\_services\_and\_pipelines | GET | | Returns a JSON object that represents the currently active services and defined pipelines |
| load\_services\_and\_pipelines | POST | service and pipeline dump  | This takes a generated dump and tries to restore the services and pipelines. If a service under the same name is already running it is skipped and inactive pipelines are skipped as well |

### Loading via classpath

If you choose to provide a module path, e.g. `somepackage.subpackge.module`, a service container will be started that loads the module with the parameters provided and call the `listen()` method. There is no version of that
container that calls `listen_thread()` at this point since we would need to impose a standard way of constructing the main thread functionality in order to call it generically.


### Using the mosaic-cli

Since writing curl requests can be quite cumbersome the mosaic package includes a cli shell that streamlines the process.

You can easily start it from within the mosaic folder:
python mosaic-cli.py

The cli-window is divided in three parts, the Log-window there collect the responses, the Command-history it show the last seven commands and the the last part is the command-line for the input

With the command help it will print usage information:

```bash
python mosaic-cli.py

command-line usage : <COMMAND> [ARGUMENTS]
commands:
  dump
  restore_pipeline <ABSOLUTE_PIPELINE_PATH>
  restore_server <DUMP_PATH>
  start_service <SERVICE>
  services
  set_pipeline <NAME> <SERVICE> [...]
  pipelines
  post_to_pipeline <PIPELINE> <MESSAGE>
  shutdown_service <SERVICE>
```

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
./mosaic-cli start_service myservice
```

The myservice argument refers to the file name - `myservice.json` - without the suffix. Please note that the service will be deployed under the name `AwesomeService` and not as `myservice`.

#### services

Lists the active services

#### set\_pipeline

This allows you to set a pipeline by naming it and listing the name's of the services it should contain:

```command-line
set_pipeline pipe myservice myotherservice gotanotherone
```

#### pipelines

List the defined pipelines.

#### post\_to\_pipeline

Post a message to a pipeline of your choice:

```command-line
post_to_pipeline pipe "Hello world!"
```

#### shutdown\_service

Shutdown a service and set all pipelines to inactive if the service is part of their pipeline.

```command-line
shutdown_service my_service.service
```

#### dump

Retrieve a dump of the running services and defined pipelines as dump.json file in <MOSAIC_HOME>

```command-line
dump
```

#### restore\_server

Restore a previously taken service and pipeline dump

```command-line
restore_server /path/to/dump.json
```

#### restore\_pipeline

Load the pipelines configuration from (server) path and activate this.

```command-line
restore_pipeline path_pipe
```

