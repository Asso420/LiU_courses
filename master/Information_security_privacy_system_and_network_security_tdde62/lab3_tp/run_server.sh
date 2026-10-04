#!/bin/bash

module add prog/apptainer/1.3.2
container_dir="/courses/TDDE62/lab/tc"

# Find open port for web server.
# Suspectible to race condition, but probably good enough...
port=$(shuf -i 1024-65534 -n 1)
while [ $(lsof -t -i:$port) ]; do
   port=$(shuf -i 1024-65534 -n 1)
done

apptainer run --env WEB_PORT=$port --env LABDIR="$HOME/tdde62/tc/server" "$container_dir/server_container.sif" $@
