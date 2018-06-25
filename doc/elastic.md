# Elasticstack integration

In order to make it easier to get started with the ROXcomposer we inluded an Elasticstack pipeline as a docker compose setup which provides you with handy dashboards for monitoring the status
of your microservices. The related files reside in the `elastic` folder.

# Prerequesites

In order to use the setup you need the `docker machine` and `docker-compose`.

# Starting the stack

The package contains a folder called `elastic`. Inside you can run `docker-compose up` to spin up the containers. It might take a moment for everything so start up. Once `logstash` is running the pipeline is ready.

# The pipeline

## Filebeats

We plan to include three filebeats to ship logs via logstash into elasticsearch but currently only one has already been integrated.
Because of file ownership issues the beats have custom docker images which include their respective `filebeat.yml`.
Their Dockerfiles are located in the `docker-images` folder inside the repository.

* Trace beat: this beat's purpose is to ship message traces. It's configuration is located under `elastic/tracebeat/filebeat.yml`. The corresponding Elasticsearch mapping is under `elastic/elasticsearch/trace-template.json`.

## Logstash

This container receives the log information from the filebeats in dedicated processing pipeliens and feeds them into elasticsearch. The configuration is under `elastic/logstash/*`.
The separate pipelines for the different input beats are located in `elastic/logstash/pipelines/*.conf`.

## Elasticsearch

Elasticsearch is used as a backend for all log data. The demo package contains a folder `elastic/elasticsearch/data` which will be used to persist all data. The data folder by default already contains some data
so that basic indices already set up with their mappings and kibana dashboards already available.


If you extracted the archive without the `-p` option you will get an error from elasticsearch for not being able to setup the node environment. In this case make sure
the data directory is writable for the elasticsearch process e.g. by setting `chmod -R 777 data`.

## Kibana

Kibana is a visualization tool for Elasticsearch which can access the data stored allows the creation of dashboards.

Currently the following visualizations are included:

* service count: the number of services that processed any messages within the selected time interval
* message count: the number of processed messages within the selected time interval
* message count: the number of processed messages within the selected time interval displayed in a date histogram

The exported dashboard and visualizations are also included inside the `elastic/kibana` folder so they can be imported by hand if needed.

