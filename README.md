# droxIT - roxcomposer

This is droxits microservice framework repository. It yields a python framework to set up microservices easily.

## Status

Dev:

[![CircleCI](https://circleci.com/gh/droxit/roxcomposer/tree/dev.svg?style=svg&circle-token=8abde3cd460a4a044d7c3de054e757853e03a6c3)](https://circleci.com/gh/droxit/roxcomposer/tree/dev)

Master:

[![CircleCI](https://circleci.com/gh/droxit/roxcomposer/tree/master.svg?style=svg&circle-token=8abde3cd460a4a044d7c3de054e757853e03a6c3)](https://circleci.com/gh/droxit/roxcomposer/tree/master)

## Dependencies

Please execute 

```bash
pip3.6 install -r requirements.txt
```

to install all python requirements.

## Setup

To setup the framework and to use it, you can use our local pip package on gru. Please execute the following command

>>> pip3.6 install -i http://localhost:4040/droxit/dev roxcomposer

Remember that you need to open an ssh tunnel to gru, to use this command.

## Versioning scheme

The version is generated via the `version.sh` script which is called from the Makefile. The resulting version depends on the current branch:  

* on `master` the version number in `VERSION` will be used.
* on `dev` the version number will be `VERSION.devN` where `N` is the number of revisions that `dev` is ahead of `master`.
* on any other branch it will be `VERSION.devN+<NORMALIZED_BRANCH_NAME>M`. `M` is the number of revisions that this branch is ahead of dev. While `N` is the number of revisions that this branch is ahead of `master` minus `M`. This is meant to ensure that `N` is the number of revisions that `dev` was ahead of master when this branch was forked. The normalized branch name is the branch name stripped from any non-alphanumeric characters. At the moment effectively only `-` and `_` are stripped. If you use any additional non-alphanumeric characters in your branch names, please adjust the `version.sh`. Otherwise version inconsitencies will occur and the build process might fail.

## Running Tests

In order to run tests, please use

```bash
make test
```

# Build

The whole package:

```bash
make demo-package
```

the built package will be under `build/roxcomposer-demo-<VERSION>`.

Only the python package:

```bash
make python-package
```

The package will be in the `dist` folder.

## Further documentation

For further documentation please consider reading the [handbook](doc/handbook.md).

