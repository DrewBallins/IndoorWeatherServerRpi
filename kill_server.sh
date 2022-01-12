#!/bin/bash

serverTasks=$(pidof python3 server.py)

for task in $serverTasks
do
   kill $task
done
