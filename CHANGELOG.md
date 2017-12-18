# v0.2.0

* Reworked `mosaic.communication.mosaic_message.MosaicMessage`. It now has it's own internal data structure and serialization functions for JSON, protobuf and a default binary format which is a protobuf binary message
  with a 4 Byte frame that contains the length of the message
* Added `mosaic_message.js` to the Javascript files - it contains a message implementation similar to the Python class.
* messages now have a unique id which will be returned by calls to `post_to_pipeline`
* Added `mosaic.monitor.basic_monitoring`. It contains a `BasicMonitoring` class which is used by `BaseService` to write message tracking information into a file. It also contains the `BasicReporting` class which can
  be used to query tracking information for messages given their id.
* Added a `BasicReportingService` which exposes `BasicReporting` to the `mosaic_control` Plugin.
* Added message monitoring endpoints to `mosaic_control`
* mosaic now supports IPv6 addresses for services
* `BaseService` now supports config loading by key via a `config_loader` module. This feature is at this point not compatible with the `mosaic_control` plugin, since it needs the services ip and port to communicate with it.

