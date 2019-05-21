# Message Format

Currently the message protocol is based on Google protocol buffers. The message definition looks like this:
```javascript
syntax = "proto3";
 
package service_communication;
 
message ROXcomposerMessage {
    Pipeline pipeline = 1;
    Payload payload = 2;
    string id = 3;
    int64 created = 4;
}
 
message Pipeline {
    repeated Service services = 5;
}
 
message Service {
    string id = 1;
    repeated Parameter parameters = 6;
}
 
message Parameter {
    string serviceParams = 7;
}
 
message Payload {
    string body = 8;
}
```

You can use this snippet to generate (de)serialization code in all supported languages (see the respective documentation).

The individual fields server the following purposes:

| Name | Function |
| ---- | -------- |
| ROXcomposerMessage	| This is a container for the message as a whole. It has the subfields `payload`, `pipeline` and `id`. |
| Pipeline | A pipeline is an array of services. This defines the message flow through the micro services (see below for a more detailed description of the process). |
| Service | A service consists of an id and an optional list of parameters. `id` is a string containing a network address as ip and port separated by a colon. A parameter is simply a string containing options to be passed along to the service with this message |
| Payload | This is a string that is passed on through the pipeline possibly being transformed along the way. |
| id | This is a python unique id formatted as a string. It ensures a unique identifier to track a message. |
| created | The timestamp of the message's creation in milliseconds since epoch. |

# Message routing

A message contains a list of services the message should be routed through. Upon receivuing a message a service is supposed to pop the first element from the list (which should refer to itself) and process the payload.

If the pipeline is empty the pipeline ends here. Otherwise the processed payload is passed on to the next service in the pipeline.

