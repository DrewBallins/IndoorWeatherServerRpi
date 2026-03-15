#!/bin/bash

./src/kill_server.sh

nohup python3 src/server.py &
