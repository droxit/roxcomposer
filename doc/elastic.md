# Elasticstack integration

In order to make it easier to get started with the ROXcomposer we inluded an Elasticstack pipeline as a docker compose setup which provides you with handy dashboards for monitoring the status
of your microservices. The related files reside in the `elastic` folder.

# The pipeline

### Filebeats

We included three filebeats to ship logs via logstash into elasticsearch. Because of file ownership issues the beats have custom docker images which include their respective `filebeat.yml`. Their Dockerfiles are located in the `docker-images` folder inside the repository.

* Trace beat: this beat's purpose is to ship message traces. It's configuration is located under `elastic/tracebeat/filebeat.yml`. The corresponding Elasticsearch mapping is under `elastic/elasticsearch/trace-template.json`.

## Logstash

This container receives the log information from the filebeats in dedicated processing pipeliens and feeds them into elasticsearch. The configuration is under `elastic/logstash/*`.
The separate pipelines for the different input beats are located in `elastic/logstash/pipelines/*.conf`.

## Elasticsearch

Elasticsearch is used as a backend for all log data. The demo package contains a folder `elastic/elasticsearch/data` which will be used to persist all data.
If you extracted the archive without the `-p` option you will get an error from elasticsearch for not being able to setup the node environment. In this case make sure
the data directory is writable for the elasticsearch process e.g. by setting `chmod 777 data`.

## Kibana

Kibana is a visualization tool for Elasticsearch which can access the data stored allows the creation of dashboards.
