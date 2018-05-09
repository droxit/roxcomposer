#!/bin/bash

#
# script to local roxcomposer deploy
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

ROXCOMPOSER_DEPLOY_DIR=$1
DEPLOY_LOG_DIR=$ROXCOMPOSER_DEPLOY_DIR/logs

BUILD_DIR="roxcomposer_demo"

function usage {
    echo "usage: deploy_roxcomposer_demo_local <TO_INSTALL_DEMO_PATH>"
    exit 0
}

### EXECUTION ###
if [[ ($# -lt 1) ]]
    then usage
else
    echo "deploy roxcomposer"
    # clean logs
    rm -rf $DEPLOY_LOG_DIR
    mkdir -p $DEPLOY_LOG_DIR

    # copy roxcomposer for deploy
    rm $ROXCOMPOSER_DEPLOY_DIR/roxcomposer-demo-*.tar.gz
    cp roxcomposer-demo-*.tar.gz $ROXCOMPOSER_DEPLOY_DIR/.

    # deploy roxcomposer_demo
    cd $ROXCOMPOSER_DEPLOY_DIR

    rm -rf $BUILD_DIR
    tar xf roxcomposer-demo*.tar.gz

    cd $BUILD_DIR
    pip3 uninstall -y roxcomposer > $DEPLOY_LOG_DIR/roxcomposer_uninstall.log
    ./install.sh --user > $DEPLOY_LOG_DIR/roxcomposer_install.log
fi