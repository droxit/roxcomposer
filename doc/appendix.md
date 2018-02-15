# Message Format

Currently the message protocol is based on Google protocol buffers. The message definition looks like this:
```javascript
syntax = "proto3";
 
package service_communication;
 
message MosaicMessage {
    Pipeline pipeline = 1;
    Payload payload = 2;
    string id = 3;
}
 
message Pipeline {
    repeated Service services = 4;
}
 
message Service {
    string id = 1;
    repeated Parameter parameters = 5;
}
 
message Parameter {
    string serviceParams = 6;
}
 
message Payload {
    string body = 7;
}
```

You can use this snippet to generate (de)serialization code in all supported languages (see the respective documentation).

The individual fields server the following purposes:

| Name | Function |
| ---- | -------- |
| MosaicMessage	| This is a container for the message as a whole. It has the subfields `payload`, `pipeline` and `id`. |
| Pipeline | A pipeline is an array of services. This defines the message flow through the micro services (see below for a more detailed description of the process). |
| Service | A service consists of an id and an optional list of parameters. `id` is a string containing a network address as ip and port separated by a colon. A parameter is simply a string containing options to be passed along to the service with this message |
| Payload | This is a string that is passed on through the pipeline possibly being transformed along the way. |
| id | This is a python unique id formatted as a string. It ensures a unique identifier to track a message. |

# Message routing

A message contains a list of services the message should be routed through. Upon receivuing a message a service is supposed to pop the first element from the list (which should refer to itself) and process the payload.

If the pipeline empy the pipeline ends here. Otherwise the processed the payload is passed on to the next service in the pipeline.

Any logging class needs to adhere to the following interface to be compatible to the base service:

# Logging injection

mosaic supports injection of logging classes which must adhere to an interface to be compatible to the base service class:

## Initialization

Any logging class must have the following instantiation:

```python
def __init__(self, service_name, **kwargs):
```

The `service_name` is the name of the service that owns this logger instance. The kwargs are passed on from the logging section service's invocation parameters. If omitted the default invocation would be

```python
logger(servicename, filename="pipeline.log", level="INFO")
```

## Log functions

The logger class needs to provide the following log functions: debug, info, warn, error, critical.

## Injection

Upon invocation a logger class can be specified in the logging section of the paramters:

```json
{
    "logging": {
        "level": "ERROR",
        "logger_class": "mosaic.log.basic_logger.BasicLogger"
    }
}
```

The service base class will then attempt to load the class and use it as the logger.

