#!/bin/bash

pip3 install -U $1 ./packages/roxcomposer*.tar.gz
pip3 install -r requirements.txt
cd api-server
npm install
cd plugins
npm install
cd ../..

