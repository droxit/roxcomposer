#!/bin/bash

MOSAIC_PACKAGE=$1
API_PLUGIN_PATH=$2
BUILD_DIR="mosaic_build"

# clean build directory
mkdir $BUILD_DIR

cd $BUILD_DIR
mkdir packages
mkdir services

# copy files
cp ../cli/mosaic-cli .
cp ../.circleci/mosaic-deploy/scripts/* .
cp -r ../.circleci/mosaic-deploy/api-server/ .
cp ../$API_PLUGIN_PATH/*.js ./api-server/plugins
cp ../$API_PLUGIN_PATH/package.json ./api-server/plugins
cp ../$MOSAIC_PACKAGE ./packages/
cp ../.circleci/mosaic-deploy/services/*.json ./services

cd ..

# create package archive
tar -czf $(echo ${MOSAIC_PACKAGE##*/} | sed -e 's/mosaic-/mosaic-demo-/') $BUILD_DIR

# delete build dir
#rm -rf $BUILD_DIR