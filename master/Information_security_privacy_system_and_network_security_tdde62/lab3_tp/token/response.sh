#!/bin/bash

# Imports. (Do not remove.)
source /usr/local/etc/bash.aliases
source util.sh

#mkdir -p scratch
# Store challenge to file for later use by tpm2_... tools
echo -n "$1" > scratch/challenge.dat

# Start implementing here...
#echo Response computation not yet implemented!

# 1. Write the challenge string ($1) into a temporary file
#echo -n $1 > scratch/challenge.txt

#------New Auth Session Creation -----
#open a policy session and prove the current state of PCR 15
tpm2_startauthsession -Q --policy-session -S scratch/session.ctx
tpm2_policypcr -Q -S scratch/session.ctx -l sha256:15 

# 2. Instruct the TPM to compute the HMAC using the persistent key at handle 0x81000000
##tpm2_hmac -Q -c 0x81000000 scratch/challenge.dat -o scratch/hmac.dat
tpm2_hmac -Q -c 0x81000000 -p session:scratch/session.ctx scratch/challenge.dat -o scratch/hmac.dat 
tpm2_flushcontext -Q scratch/session.ctx

# 3. Format the raw binary output into an 8-digit decimal number
binary_to_decimal scratch/hmac.dat

