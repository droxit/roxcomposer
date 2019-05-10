# Introduction

*roxcomposer* is a software development framework for building microservice architectures. It consists of various interlocking parts:

* a service communication and routing protocol based on Google protocol buffers
* a service base class written in Python which allows easy implementation of Python services
* a Node.js control process that provides configurable REST endpoints for starting services, defining pipelines and injecting messages into a pipeline via HTTP
* a dockerized monitoring environment based on the Elasticstack (optional)

## Contents

[Installation](installation.md)

[Implementation](implementation.md)

[Interfacing with the framework (REST API)](rest.md)

[Logging and monitoring](logging_monitoring.md)

[Elasticstack integration](elastic.md)

[Appendix](appendix.md)

[Demo](demo.md)
