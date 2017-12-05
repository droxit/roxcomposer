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
cp ../../../cli/mosaic-cli .
cp ../scripts/* .
cp -r ../api-server/ .
cp $API_PLUGIN_PATH/*.js ./api-server/plugins
cp $MOSAIC_PACKAGE ./packages/
cp ../services/*.json ./services

cd ..

# create package archive
tar -czf $(echo ${MOSAIC_PACKGE##*/} | sed -e 's/mosaic-/mosaic-demo-/').tar.gz $BUILD_DIR
