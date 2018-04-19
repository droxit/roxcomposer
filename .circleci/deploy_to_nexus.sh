#!/bin/bash

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -N -L 8081:localhost:8081 devpi@176.9.144.37 &
pid=$!
