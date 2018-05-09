#!/bin/bash

#
# script to local roxcomposer-cli deploy
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

ROXCOMPOSER_DEPLOY_DIR=$1
BUILD_DIR="roxcomposer_demo"

function usage {
    echo "usage: deploy_local_cli <TO_INSTALL_DEMO_PATH>"
    exit 0
}

### EXECUTION ###
if [[ ($# -lt 1) ]]
    then usage
else
    rm -rf $ROXCOMPOSER_DEPLOY_DIR/$BUILD_DIR/roxcomposer-cli*
    cp ./cli/*.py $ROXCOMPOSER_DEPLOY_DIR/$BUILD_DIR/.
    cp ../$API_PLUGIN_PATH/package.json ./api-server/plugins

fi