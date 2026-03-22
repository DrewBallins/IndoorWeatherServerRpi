#!/bin/bash

cd ~/IndoorWeatherServerRpi

./kill_server.sh

nohup python3 src/server.py &
