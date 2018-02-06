#!/bin/bash

#
# script to local mosaic build, deploy and run
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

MOSAIC_PACKAGE=$1
API_PLUGIN_PATH=$2
MOSAIC_DEPLOY_DIR=$3

BUILD_DIR="mosaic_demo"

function usage {
    echo "usage: build_deploy_mosaic_demo_local <MOSAIC_PACKAGE_PATH> <IMPRESS_PLUGING_PATH> <TO_INSTALL_DEMO_PATH>"
    exit 0
}

### EXECUTION ###
if [[ ($# -lt 1) ]]
    then usage
else
    ./build_mosaic_demo_local.sh $MOSAIC_PACKAGE $API_PLUGIN_PATH
    ./deploy_mosaic_demo_local.sh $MOSAIC_DEPLOY_DIR

    # mosasic-demo run
    cd $MOSAIC_DEPLOY_DIR/$BUILD_DIR/
    echo "start mosaic"
    ./start_server.sh
fi