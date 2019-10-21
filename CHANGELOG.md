# v0.4.3

## New

* Check parameters of a service ("ip", "port") for validity and throw a `roxcomposer.exceptions.ConfigError` if parameters are invalid
* Additional "description" field in logging JSON of BasicLogger - fixes #101

## Fixed 

* Fixed crash when trying to bind to an invalid IP address specified in service parameters
* Server crash when watching too many files
* Fixed false error output in Node tests

# v0.4.2

## New

* License switched to LGPL
* roxcomposer\_plugin: added handler for uncaught exceptions that handles process cleanup and kills child processes
* added new API endpoint `roxcomposer_log_observer` that provides access to the logs of the API gateway itself (ROXconnector)
* added new API endpoint `get_logsession` that provides the watched services for a given log observer session id

# v0.4.1

## New

* added feature: service parameters can now be given at pipeline creation
* added better logging: ROXconnector now forwards service error logs
* added a response when service could not be started
* added `delete_pipeline` API endpoint
* added GET API endpoint on `/` that shows a message saying the ROXcomposer was initialized
* better logging when server crashes in case the server is started twice
* added utc timestamp to timezone aware human readable time string conversion in CLI logs

## Fixed

* fixed bug when querying `check_services_and_logs()` with an empty array
* fixed server crash bug when basic\_reporting is shutdown and `get_msg_history()` or `get_msg_status()` is called 
* fixed server crash when posting to pipe that contains basic reporting service
* fixed server crash when logging a JSON formatted message 
* fixed server crash when logging an exception that does not implement `strerror` (for example when trying to connect to a server with the wrong url)
* fixed bug: address already in use after server crash
* fixed server crash when starting a service with the wrong classpath
* fixed server crash when starting a service with wrong JSON params
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

