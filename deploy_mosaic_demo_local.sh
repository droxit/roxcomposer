#!/bin/bash

#
# script to local mosaic deploy
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

MOSAIC_DEPLOY_DIR=$1
DEPLOY_LOG_DIR=$MOSAIC_DEPLOY_DIR/logs

BUILD_DIR="mosaic_demo"

function usage {
    echo "usage: deploy_mosaic_demo_local <TO_INSTALL_DEMO_PATH>"
    exit 0
}

### EXECUTION ###
if [[ ($# -lt 1) ]]
    then usage
else
    echo "deploy mosaic"
    # clean logs
    rm -rf $DEPLOY_LOG_DIR
    mkdir $DEPLOY_LOG_DIR

    # copy mosaic for deploy
    rm $MOSAIC_DEPLOY_DIR/mosaic-demo-*.tar.gz
    cp mosaic-demo-*.tar.gz $MOSAIC_DEPLOY_DIR/.

    # deploy mosaic_demo
    cd $MOSAIC_DEPLOY_DIR

    rm -rf $BUILD_DIR
    tar xf mosaic-demo*.tar.gz

    cd $BUILD_DIR
    pip3 uninstall -y mosaic > $DEPLOY_LOG_DIR/mosaic_uninstall.log
    ./install.sh --user > $DEPLOY_LOG_DIR/mosaic_install.log
fi