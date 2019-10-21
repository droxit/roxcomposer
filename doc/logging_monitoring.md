# Logging

The ROXcomposer supports multiple logging implementations that can be injected into the service base class (see the below for more information).

The package provides a basic logger implementation which will be used out of the box and can be configured upon service invocation:

```json
'{
  "name": "myservice_instance",
  "ip": "127.0.0.1",
  "port": 1337,
  "logging": {
      "logpath": "/path/to/file.log",
      "level": "info"
  }
}
```

`logpath` and `level` would be passed to the basic logger. When left out the logger will use `stdout` at level `WARN`

If logpath is an existing directory a logfile will be created within it using the service name suffixed with `.log`.

To overwrite the default values you might add default parameters for logging in the roxconnector plugin parameter configs:

```json
{
  "PLUGINS": {
    "roxcomposer": {
      "params": {
        "default": {
          "logging": {
            "logpath": "pipeline.log",
            "level": "INFO"
          }
        }
      }
    }
  }
}
```

## Logging messages

The basic logger has functions for logging on different log levels: debug, info, warn, error and critical which are easily accessible from within the base service class:

```python
self.logger.info("Hello World!")
self.logger.error('something went wrong', message_id='c534efc0-5065-40ba-8ec8-1186e85a14ef', additional={'stuff': 42}) # we can log anything that is JSON serializable
self.logger.info({"key": "value"}, description="received message") # Use 'description' to separate a parsable JSON-message from its context
```

the resulting log messages would look like this (the time is given in UTC):

```json
{"level": "INFO", "msg": "Hello World!", "time": "2018-07-05T10:28:19+0000", "service": "myservice"}
{"level": "ERROR", "msg": "something went wrong", "time": "2018-07-05T11:55:19+0000", "message_id": "c534efc0-5065-40ba-8ec8-1186e85a14ef", "additional": {"stuff": 42}, "service": "myservice"}
{"level": "INFO", "msg": {"key": "value"}, "time": "2019-06-04T13:34:14+0000", "service": "testservice", "description": "received message"}
```

## Logging exceptions

The BaseService class does not catch any exceptions raised by the logger. This is intentional - being unable to log leaves your infrastructure blind to any errors. If you don't want this behaviour you can always write
your own logging class and catch any exceptions inside it.

## Log access via the API

The API gateway supports observation of service log files via the `log_observer` endpoint (see the [REST documentation](rest.md) for details). Currently the API gateway simply listens on changes on those
files and buffers them in memory (filtering them for the right service(s) if needed) until they are requested. The number of lines buffered can be specified as well as a lifespan for the log session.

# Monitoring

The base class contains a basic monitoring solution which saves message traces to a file.

## Initialization

By default monitoring messages of the whole pipeline get logged in a `monitoring.log` file. The filename can be set manually by specifying the monitoring field in the service initialization similar to the example below.

```json
{
  "name": "myservice_instance",
  "ip": "127.0.0.1",
  "port": 1337,
  "logging": {
      "logpath": "/path/to/file.log",
      "level": "info"
  },
  "monitoring": {
      "filename": "/path/to/monitoring/file.log"
  }
}
```

To overwrite the default values you might add default parameters for logging in the roxconnector plugin parameter configs (similar to default logging params):

```json
"default": {
  "monitoring": {
    "filename": "monitoring.log",
    "monitor_class": "roxcomposer.monitor.basic_monitoring.BasicMonitoring"
  }
}
```

## Monitoring messages

There are several situations where the basic monitoring creates messages. Currently the following events trigger a monitoring message automatically:

* a ROXcomposerMessage was received
* a ROXcomposerMessage was dispatched
* a ROXcomposerMessage reached it's final destination

If everything works as expected a monitoring message like the following should be generated:

```bash
{"event": "message_dispatched", "status": "in_transit", "time": 1513596460.0961697, "args": {"service_name": "service1", "message_id": "dfa156e3-a8f6-4968-a255-ebd44e41d846", "destination": "127.0.0.1:10000"}}
```

Furthermore, the basic monitoring can be used to report an error state for a message:

```python
self.monitoring.msg_error(
    service_name=self.params['name'],
    message_id="dfa156e3-a8f6-4968-a255-ebd44e41d846",
    description=errmsg
)
```

In addition custom metrics can be commited to the monitoring file via the `custom_metric` function from the basic monitoring class.
The function expects a service name, a metric name and a metric dictionary as keyword arguments.
Please consider the following example.

```python
custom = {"service_name": "serv1", "metric_name": "some-metric", "metric_dictionary":
                {"metric": "entry", "metric2": "another-entry"}}
monitor.custom_metric(**custom)
```

## Reporting

The basic monitoring class has a counterpart named `BasicReporting`. This class holds the functions to retrieve monitoring information on specific events. Either their whole monitoring history or only the last
known status. See the API [documentation](rest.md) for details on accessing the reporting functionionality.

# Logging injection

## Initialization

Any logging class must have the following instantiation:

```python
def __init__(self, service_name, **kwargs):
```

The `service_name` is the name of the service that owns this logger instance. The kwargs are passed on from the logging section service's invocation parameters.  
Assuming the following args passed to the service:

```json
{
  "name": "service_name",
  ...
  "logging": {
    "logpath": "logs/service_name.log",
    "level": "INFO"
  }
}
```

The logger would be instantiated the following way:

```python
logger(servicename, logpath="logs/service_name.log", level="INFO"). If `log_path` points to a directory then a logfile is created within it using the service name suffixed with `.log`.
```

## Log functions

The logger class needs to provide the following log functions: debug, info, warn, error, critical.

## Injection

Upon invocation a logger class can be specified in the logging section of the paramters:

```json
{
    "logging": {
        "level": "ERROR",
        "logger_class": "roxcomposer.log.basic_logger.BasicLogger"
    }
}
```

The service base class will then attempt to load the class and use it as the logger. Note: the `logger_class` parameter is also passed on to the logger class as a keyword argument.

# Architecture

Since we're not yet supporting distributed systems logging and monitoring are based on files. Concerning the message traces there is an architectural weakness involved since all services write to the
same trace file - hence presenting the opportunity for file corruption. This will be addressed in future releases - specifically v0.5.X onward.

