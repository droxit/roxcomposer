#!/bin/bash

#
# script to mosaic build
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

MOSAIC_PACKAGE=$1
API_PLUGIN_PATH=$2
BUILD_DIR="mosaic_demo"

function usage {
    echo "usage: build_mosaic_demo_local <MOSAIC_PACKAGE_PATH> <IMPRESS_PLUGING_PATH>"
    exit 0
}

### EXECUTION ###
if [[ ($# -lt 1) ]]
    then usage
else
    echo "build mosaic"
    # mosaic package
    rm -rf $MOSAIC_PACKAGE
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
    cp ../cli/mosaic-cli .
    cp ../.circleci/mosaic-deploy/scripts/* .
    if [[ $OSTYPE = *"darwin"* ]]
        then
            echo "macOS detected - switching handling..."
            cp -R ../.circleci/mosaic-deploy/api-server/ ./api-server/
        else
			cp -r ../.circleci/mosaic-deploy/api-server/ .
    fi
    cp ../$API_PLUGIN_PATH/*.js ./api-server/plugins
    cp ../$API_PLUGIN_PATH/package.json ./api-server/plugins
    cp ../$MOSAIC_PACKAGE ./packages/
    cp ../.circleci/mosaic-deploy/services/*.json ./services

    cd ..

    # create package archive
    tar -czf $(echo ${MOSAIC_PACKAGE##*/} | sed -e 's/mosaic-/mosaic-demo-/') $BUILD_DIR

fi
