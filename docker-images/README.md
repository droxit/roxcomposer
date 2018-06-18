# docker images for the ROXcomposer project

# CircleCI

This image is used for the CI pipeline.

## Building

In order to build the docker image run

```bash
docker build -t droxops/roxcomposer-node-py:0.0.5 node-py
```

## Push a new version

Build the image, login as the droxops user and push the new image. Full credentials are documented in Confluence.
If needed update the tag (the 0.0.5 part in this example).

```bash
docker login
docker push droxops/roxcomposer-node-py:0.0.5
```

# Elasticsearch

## Beats

These docker images are used for the various filebeats for shipping log data into logstash.

Due to file ownership problems with filebeat the current version of the respective filebeat.yml must be placed inside the folder containing the Dockerfile e.g. `roxcomposer-tracebeat`.

Then the image can be built.

```bash
docker build -t droxops/roxcomposer-tracebeat:0.0.1 roxcomposer-tracebeat
```

