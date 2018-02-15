#!/bin/bash

pip3 install -U $1 ./packages/mosaic*.tar.gz
cd api-server
npm install
cd plugins
npm install
cd ../..

