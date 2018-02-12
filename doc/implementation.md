# Writing a service

Implementing your own service is as simple as sub classing our service base class and implementing the `on_message` function.

The basic service provides two options for the configuration of the service. The configuration parameters can be transferred directly:

```python
from mosaic import base_service
 
class MyService(base_service.BaseService):
    def __init__(self, args):
        super().__init__(args)
        self.listen()
 
    def on_message(self, msg):
        new_msg = do_stuff_with(msg)
        self.dispatch(new_msg)
 
args = json_loads(sys.argv[1])
ms = MyService(args)
```

An example invocation for our service with arguments passed directly would look like this

```bash
python3 myservice.py '{"name": "myservice_instance", "ip": "127.0.0.1", "port": 1337}'
```

**Every** service needs those three parameters: name, ip and port. Those and any additional parameters are available via the `self.params` dictionary from within the service code.

That's all there is to writing services. After calling listen the service will listen on the provided network address and upon receiving a message the messages payload will be fed into the `on_message` function. Also there is the option, that you can use the `on_message_ext` function to process a message. Use this function, if you need more information out of the message the service has received, e.g. some pipeline information. dispatch will take a payload (possibly even the unchanged message that arrived) and send it off to the next service in the pipeline.The `do_stuff_with` function is a placeholder for an processing you might want to do with the incoming message.

So how do we generate messages and define pipelines? If you want to generate your own messages read the appendix on the message format. Otherwise you can simply use the REST-API to interface with your services (see the appropriate chapter).

## Config handling

Since passing the configuration manually is cumbersome, services have a machanism to access their configuration via files:

```bash
python3 myservice.py '{"service_key": "services.myservice", "config_file": "/path/to/config.json"}'
```

The service will now try to parse the config file expecting JSON and will try to access the field "services/myservice". The config file corresponding to the invocation above would look like this:

```json
{
  "services": {
    "myservice": {
      "name": "myservice_instance",
      "ip": "127.0.0.1",
      "port": 1337
    }
  }
}
```

The `service_key` lookup allows you to have central config files containing multiple services and other information. At the moment the service parameters need to bested at least on level down, meaning you can't leave
the `service_key` emtpy.

The `config_file` parameter is optional. If left out the service will look for an environment variable named `DROXIT_MOSAIC_CONFIG`. If it is defined it is expected to contain a path to a valid configuration.
If the variable is not defined the service will try to load a file named `config.json` from the current working directory as a last resort. If none of this works the service constructor will fail.

## Logging

mosaic supports multiple logging implementations that can be injected into the service base class (see the appendix for more information).

The package provides a basic logger implementation which will be used out of the box and can be configured upon service invocation:

```json
'{
  "name": "myservice_instance",
  "ip": "127.0.0.1",
  "port": 1337,
  "logging": {
      "filename": "/path/to/file.log",
      "level": "info"
  }
}
```

filename and level would be passed on to the basic logger. When left out the default values provided are:

```json
"logging": {
  "filename": "pipeline.log",
  "level": "INFO"
}
```

The basic logger is based upon the Python logging module. Any initialization parameters for logging.basicConfig can be used as fields in the logging section.

If not overridden upon invocation a sample log message looks like this:

```bash
[ISO8601 TIMESTAMP][TIMESTAMP][INFO] service:myservice_instance - Hello World!
```

### Logging messages

The basic logger has functions for logging on different log levels: debug, info, warn, error and critical which are easily accessible from within the base service class:
self.logger.info("Hello World!")
self.logger.error(errorObject) # we can log anything that has a string representation

## Monitoring

The base class contains a basic monitoring solution, which prints every monitoring message to the service console and writes them to a file. 

### Initialization

By default monitoring messages of the whole pipeline get logged in a `monitoring.log` file. The filename can be set manually by specifying the monitoring field in the service initialization similar to the example below.

```json
{
  "name": "myservice_instance",
  "ip": "127.0.0.1",
  "port": 1337,
  "logging": {
      "filename": "/path/to/file.log",
      "level": "info"
  },
  "monitoring": {
      "filename": "/path/to/monitoring/file.log"
  }
}
```

### Monitoring messages

There are several situations where the basic monitoring is creating messages. Currently the following events trigger a monitoring message automatically:

* a MosaicMessage was received
* a MosaicMessage was dispatched
* a MosaicMessage reached it's final destination

If everything works as expected a monitoring message like the following should be generated:

```bash
{'event': 'message_dispatched', 'status': 'in_transit', 'time': 1513596460.0961697, 'args': {'service_name': 'service1', 'message_id': 'dfa156e3-a8f6-4968-a255-ebd44e41d846', 'destination': '127.0.0.1:10000'}}
```

Furthermore, the basic monitoring can be used to monitor a custom metric.
To monitor a custom metric, use the custom_metric function from the basic monitoring class.
The function expects a service name, a metric name and a metric dictionary as keyword arguments.
Please consider the following example.

```python
custom = {"service_name": "serv1", "metric_name": "some-metric", "metric_dictionary":
                {"metric": "entry", "metric2": "another-entry"}}
monitor.custom_metric(**custom)
```

### Reporting

The basic monitoring class has a counterpart named `BasicReporting`. This class holds the functions to retrieve monitoring information on specific events. Either their whole monitoring history or only the last
known status. See the API [documentation](rest.md) for details on accessing the reporting functionionality.

