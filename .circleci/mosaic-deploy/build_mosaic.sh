#!/bin/bash

ROXCOMPOSER_PACKAGE=$1
API_PLUGIN_PATH=$2
BUILD_DIR="roxcomposer"

# clean build directory
mkdir $BUILD_DIR

cd $BUILD_DIR
mkdir packages
mkdir services

# copy files
cp ../../../cli/roxcomposer-cli.py .
cp ../scripts/* .
cp -r ../api-server/ .
cp ../$API_PLUGIN_PATH/*.js ./api-server/plugins
cp ../$API_PLUGIN_PATH/package.json ./api-server/plugins
cp ../$ROXCOMPOSER_PACKAGE ./packages/
cp ../services/*.json ./services
cp ../util/service_container.py ./api-server/plugins/.

cd ..

# create package archive
tar -czf $(echo ${ROXCOMPOSER_PACKAGE##*/} | sed -e 's/roxcomposer-/roxcomposer-demo-/') $BUILD_DIR
