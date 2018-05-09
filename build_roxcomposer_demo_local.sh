#!/bin/bash

#
# script to roxcomposer build
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

ROXCOMPOSER_PACKAGE=$1
API_PLUGIN_PATH=$2
BUILD_DIR="roxcomposer_demo"

function usage {
    echo "usage: build_roxcomposer_demo_local <ROXCOMPOSER_PACKAGE_PATH> <IMPRESS_PLUGING_PATH>"
    exit 0
}

### EXECUTION ###
if [[ ($# -lt 1) ]]
    then usage
else
    echo "build roxcomposer"
    # roxcomposer package
    rm -rf $ROXCOMPOSER_PACKAGE
    rm *.tar.gz
    python3.6 setup.py sdist

    # clean build directory
    rm -fr $BUILD_DIR
    mkdir $BUILD_DIR

    cd $BUILD_DIR
    mkdir services
    mkdir packages
    cp ../dist/*.tar.gz ./packages/.

    # copy files
    cp ../cli/*.py .
    cp ../.circleci/roxcomposer-deploy/scripts/* .
    if [[ $OSTYPE = *"darwin"* ]]
        then
            echo "macOS detected - switching handling..."
            cp -R ../.circleci/roxcomposer-deploy/api-server/ ./api-server/
        else
			cp -r ../.circleci/roxcomposer-deploy/api-server/ .
    fi
    cp ../$API_PLUGIN_PATH/*.js ./api-server/plugins
    cp ../$API_PLUGIN_PATH/package.json ./api-server/plugins
    cp ../$ROXCOMPOSER_PACKAGE ./packages/
    cp ../.circleci/roxcomposer-deploy/services/*.json ./services
    cp ../util/service_container.py ./api-server/plugins/.

    cd ..

    # create package archive
    tar -czf $(echo ${ROXCOMPOSER_PACKAGE##*/} | sed -e 's/roxcomposer-/roxcomposer-demo-/') $BUILD_DIR

fi
