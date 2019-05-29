# Writing a service

Implementing your own service is as simple as sub classing the service base class and implementing the `on_message` function.

```python
from roxcomposer import base_service
 
class MyService(base_service.BaseService):
    def __init__(self, args):
        super().__init__(args)
 
    def on_message(self, msg, msg_id):
        new_msg = do_stuff_with(msg)
        self.dispatch(new_msg)
 
args = json_loads(sys.argv[1])
ms = MyService(args)
ms.listen()
```

The `msg` parameter is the message payload that was posted into the pipeline. The `msg_id` is a unique identifier for this particular message and is provided for logging purposes (explained later).

An example invocation for our service with arguments passed directly would look like this

```bash
python3 myservice.py '{"name": "myservice_instance", "ip": "127.0.0.1", "port": 1337}'
```

**Every** service needs those three parameters: name, ip and port. Those and any additional parameters are available via the `self.params` dictionary from within the service code.

That's all there is to writing services.
After calling `listen` the service will listen on the provided network address and upon receiving a message the message's payload will be fed into the `on_message` function.

There is also an `on_message_ext` function which receives the whole message object not only the payload.
Use this function, if you need more information out of the message the service has received, e.g. some pipeline information. It is possible to manipulate the message object here before dispatching it but this is highly discouraged
since it is invisible to the message initiator.

dispatch will take a payload (possibly even the unchanged message that arrived) and send it off to the next service in the pipeline.The `do_stuff_with` function is a placeholder for an processing you might want to do with the incoming message.

So how do we generate messages and define pipelines? If you want to generate your own messages read the [appendix](appendix.md) on the message format.
Otherwise you can simply use the REST-API to interface with your services (see the this [chapter](rest.md)).

## Config handling

Since passing the configuration manually is cumbersome, services have a mechanism to access their configuration via files:

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

The `service_key` lookup allows you to have central config files containing multiple services and other information. At the moment the service parameters need to nested at least one level down, meaning you can't leave
the `service_key` emtpy.

The `config_file` parameter is optional. If left out the service will look for an environment variable named `DROXIT_ROXCOMPOSER_CONFIG`. If it is defined it is expected to contain a path to a valid configuration.
If the variable is not defined the service will try to load a file named `config.json` from the current working directory as a last resort. If none of this works the service constructor will fail.

## Logging

Logging is explained in its own [section](logging_monitoring.md)

## Threading

The `listen()` function blocks the main thread leaving you unable to do anything beyond processing messages. If you wish to add more interfaces to your service or maybe send a regular heartbeat you should use the
`listen_thread()` function. It will put the `listen()` function into a separate thread leaving the main thread open. Be aware that there are no locking/synchronization mechanisms implemented in the `BaseService` class. You can
easily add some yourself though - should you need them.

