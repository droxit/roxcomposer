# CircleCI docker image by DroxOps

# Building

In order to build the docker image run

    docker build -t droxops/roxcomposer-node-py:0.0.5 node-py

# Push a new version

Build the image, login as the droxops user and push the new image. Full credentials are documented in Confluence.
If needed update the tag (the 0.0.5 part in this example).

```bash
docker login
docker push droxops/roxcomposer-node-py:0.0.5
```

