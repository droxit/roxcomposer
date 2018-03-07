# v0.3.0

* changed the pipeline processing within BaseService: messages that are sent to a service must this service as their first element of the pipeline.

# v0.2.1

* Fixed interal storage of service parameters in `mosaic_control.js`
* Removed multiple `done()` call from  `load_and_start_pipeline` tests

# v0.2.0

* Added new endpoints `dump_services_and_pipelines` and `load_services_and_pipelines` to dump and restore the current service pipeline setup
* Added new endpoint `load_and_start_pipeline` which allows pipelines to be read from files on the impress host
* Logging and monitoring classes can now be injected
* Improved error handling and reporting
* Reworked `mosaic.communication.mosaic_message.MosaicMessage`. It now has it's own internal data structure and serialization functions for JSON, protobuf and a default binary format which is a protobuf binary message
  with a 4 Byte frame that contains the length of the message
* Added `mosaic_message.js` to the Javascript files - it contains a message implementation similar to the Python class.
* Messages now have a unique id which will be returned by calls to `post_to_pipeline`
* Added `mosaic.monitor.basic_monitoring`. It contains a `BasicMonitoring` class which is used by `BaseService` to write message tracking information into a file. It also contains the `BasicReporting` class which can
  be used to query tracking information for messages given their id.
* Added a `BasicReportingService` which exposes `BasicReporting` to the `mosaic_control` Plugin.
* Added message monitoring endpoints to `mosaic_control`
* mosaic now supports IPv6 addresses for services, except the monitoring reporting service. The feature is currently not used because of problems on systems without dual stack support.
* `BaseService` now supports config loading by key via a `config_loader` module. impress got a similar plugin to mirror the python functionality.
* `mosaic_control` can now be required multiple times. Each time a new set of internal data structures is created so the instances can coexist.

