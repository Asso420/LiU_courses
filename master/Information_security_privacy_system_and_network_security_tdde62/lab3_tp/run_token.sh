#!/bin/bash

module add prog/apptainer/1.3.2

container_dir="/courses/TDDE62/lab/tc"

# Find open ports for TPM simulator.
# Suspectible to race condition, but probably good enough...
port=$(shuf -i 1024-65534 -n 1)
while [ $(lsof -t -i:$port) ] || [ $(lsof -t -i:$(( port + 1))) ]; do
   port=$(shuf -i 1024-65534 -n 1)
done

apptainer run --env TPM_SIM_PORT=$port --env LABDIR="$HOME/tdde62/tc/token" "$container_dir/token_container.sif" $@
