# v0.4.1

## New

* Service parameters can now be specified when defining a pipeline - when posting to this pipeline the parameters will be embedded into the message.
* REST endpoint for `/` added to demo configuration that returns a short info if the server is running.
* Pipelines can now be deleted using the `/delete_pipeline` endpoint.
* The cli now converts timestamps from service logs and message traces from UTC to the local time zone.

## Fixed

* Stopping the reporting service or a crash of the same don't lead to a server crash anymore upon calls to `/get_message_history` or `/get_message_status`.
* A service crashing on startup is now detected and communicated to the client. If present the service's error ouput is returned to the client.
* Multiple erroneous log statements that caused server crashes were fixed.
* Some minor argument handling fixes.
* Fixed an error in version.sh that caused the build process to fail on occasion.
 
# v0.4.0

## New

* Service log observation API endpoints
* Elasticstack monitoring setup as docker-compose environment

## Changed

* CLI: complete rework (see handbook for details)
* switched message trace output to JSON

# v0.3.0

* added `listen_thread` function that starts `listen()` in a separate thread.
* changed the pipeline processing within BaseService: messages that are sent to a service must this service as their first element of the pipeline.

# v0.2.1

* Fixed interal storage of service parameters in `roxcomposer_control.js`
* Removed multiple `done()` call from  `load_and_start_pipeline` tests

# v0.2.0

* Added new endpoints `dump_services_and_pipelines` and `load_services_and_pipelines` to dump and restore the current service pipeline setup
* Added new endpoint `load_and_start_pipeline` which allows pipelines to be read from files on the roxconnector host
* Logging and monitoring classes can now be injected
* Improved error handling and reporting
* Reworked `roxcomposer.communication.roxcomposer_message.ROXcomposerMessage`. It now has it's own internal data structure and serialization functions for JSON, protobuf and a default binary format which is a protobuf binary message
  with a 4 Byte frame that contains the length of the message
* Added `roxcomposer_message.js` to the Javascript files - it contains a message implementation similar to the Python class.
* Messages now have a unique id which will be returned by calls to `post_to_pipeline`
* Added `roxcomposer.monitor.basic_monitoring`. It contains a `BasicMonitoring` class which is used by `BaseService` to write message tracking information into a file. It also contains the `BasicReporting` class which can
  be used to query tracking information for messages given their id.
* Added a `BasicReportingService` which exposes `BasicReporting` to the `roxcomposer_control` Plugin.
* Added message monitoring endpoints to `roxcomposer_control`
* roxcomposer now supports IPv6 addresses for services, except the monitoring reporting service. The feature is currently not used because of problems on systems without dual stack support.
* `BaseService` now supports config loading by key via a `config_loader` module. roxconnector got a similar plugin to mirror the python functionality.
* `roxcomposer_control` can now be required multiple times. Each time a new set of internal data structures is created so the instances can coexist.

