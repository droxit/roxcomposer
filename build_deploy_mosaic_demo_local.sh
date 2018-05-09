#!/bin/bash

#
# script to local roxcomposer build, deploy and run
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

ROXCOMPOSER_PACKAGE=$1
API_PLUGIN_PATH=$2
ROXCOMPOSER_DEPLOY_DIR=$3

BUILD_DIR="roxcomposer_demo"

function usage {
    echo "usage: build_deploy_roxcomposer_demo_local <ROXCOMPOSER_PACKAGE_PATH> <IMPRESS_PLUGING_PATH> <TO_INSTALL_DEMO_PATH>"
    exit 0
}

### EXECUTION ###
if [[ ($# -lt 1) ]]
    then usage
else
    ./build_roxcomposer_demo_local.sh $ROXCOMPOSER_PACKAGE $API_PLUGIN_PATH
    ./deploy_roxcomposer_demo_local.sh $ROXCOMPOSER_DEPLOY_DIR

    # mosasic-demo run
    cd $ROXCOMPOSER_DEPLOY_DIR/$BUILD_DIR/
#    echo "start roxcomposer"
#    ./start_server.sh
fi