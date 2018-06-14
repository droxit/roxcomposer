# Elasticstack integration

In order to make it easier to get started with the ROXcomposer we inluded an Elasticstack pipeline as a docker compose setup which provides you with handy dashboards for monitoring the status
of your microservices.

## The pipeline

### Filebeats

We included three filebeats to ship logs via logstash into elasticsearch:

* Trace beat: this beat's purpose is to ship message traces. It's configuration is located under `elastic/tracebeat/filebeat.yml`.

## Logstash

This container receives the log information from the filebeats in dedicated processing pipeliens and feeds them into elasticsearch. The configuration is under `elastic/logstash/*`.
The separate pipelines for the different input beats are located in `elastic/logstash/pipelines/*.conf`.
