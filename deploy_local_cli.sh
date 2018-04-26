#!/bin/bash

#
# script to local mosaic-cli deploy
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

MOSAIC_DEPLOY_DIR=$1
BUILD_DIR="mosaic_demo"

function usage {
    echo "usage: deploy_local_cli <TO_INSTALL_DEMO_PATH>"
    exit 0
}

### EXECUTION ###
if [[ ($# -lt 1) ]]
    then usage
else
    rm -rf $MOSAIC_DEPLOY_DIR/$BUILD_DIR/mosaic-cli*
    cp ./cli/*.py $MOSAIC_DEPLOY_DIR/$BUILD_DIR/.
    cp ../$API_PLUGIN_PATH/package.json ./api-server/plugins

fi