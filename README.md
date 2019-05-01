# droxIT - ROXcomposer

This is droxits microservice framework repository. It yields a python framework to set up microservices easily.
    
Copyright (C) 2019  droxIT GmbH - S. Hanson, M. Villarroya, C. Lamberty, J. Becker, C. Hecktor, E. Heller

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You have received a copy of the GNU General Public License
along with this program. See also <http://www.gnu.org/licenses/>.

## Status

Dev:

[![CircleCI](https://circleci.com/gh/droxit/roxcomposer/tree/dev.svg?style=svg&circle-token=8abde3cd460a4a044d7c3de054e757853e03a6c3)](https://circleci.com/gh/droxit/roxcomposer/tree/dev)

Master:

[![CircleCI](https://circleci.com/gh/droxit/roxcomposer/tree/master.svg?style=svg&circle-token=8abde3cd460a4a044d7c3de054e757853e03a6c3)](https://circleci.com/gh/droxit/roxcomposer/tree/master)

## Dependencies

The Python dependencies are listed in the `requirements.txt` and the Node.js dependencies are listed in `roxconnector_plugin/package.json`.

Please execute 

```bash
make install-deps
```

to install all requirements.


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

## Build

The whole package:

```bash
make demo-package
```

You will be prompted for creadentials for the droxIT artifact repository. Alternatively those can be provided in the `ARTIFACT_AUTH` environment variable as a `username:password` pair.

the built package will be under `build/roxcomposer-demo-<VERSION>`.

Only the python package:

```bash
make python-package
```

The package will be in the `dist` folder.

## Deploy

Running

```bash
make deploy-demo
```

will ask you for a directory to deploy to. It will attempt to extract the package at the given location and install the dependencies.

## Further documentation

For further documentation please consider reading the [handbook](doc/handbook.md).

