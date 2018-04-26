#!/bin/bash

MOSAIC_PACKAGE=$1
API_PLUGIN_PATH=$2
BUILD_DIR="mosaic"

# clean build directory
mkdir $BUILD_DIR

cd $BUILD_DIR
mkdir packages
mkdir services

# copy files
cp ../../../cli/mosaic-cli.py .
cp ../scripts/* .
cp -r ../api-server/ .
cp ../$API_PLUGIN_PATH/*.js ./api-server/plugins
cp ../$API_PLUGIN_PATH/package.json ./api-server/plugins
cp ../$MOSAIC_PACKAGE ./packages/
cp ../services/*.json ./services
cp ../util/service_container.py ./api-server/plugins/.

cd ..

# create package archive
tar -czf $(echo ${MOSAIC_PACKAGE##*/} | sed -e 's/mosaic-/mosaic-demo-/') $BUILD_DIR
