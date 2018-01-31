#!/bin/bash

#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#


MOSAIC_DEPLOY_DIR=$1
DEPLOY_LOG_DIR=$MOSAIC_DEPLOY_DIR/logs

mkdir $DEPLOY_LOG_DIR
cp mosaic-demo-*.tar.gz $MOSAIC_DEPLOY_DIR/.

cd $MOSAIC_DEPLOY_DIR

rm -rf mosaic_build
tar xf mosaic-demo*.tar.gz
cd mosaic_build
pip3.6 uninstall mosaic
#pip3.6 install --user packages/mosaic-0.2.0.tar.gz > $DEPLOY_LOG_DIR/mosaic_install.log
./install.sh --user > $DEPLOY_LOG_DIR/mosaic_install.log
#./start_server.sh