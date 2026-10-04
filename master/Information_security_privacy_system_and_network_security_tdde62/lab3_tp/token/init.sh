#!/bin/bash

# Imports. (Do not remove.)
source /usr/local/etc/bash.aliases
source util.sh

mkdir -p scratch

hex_to_bin $1 scratch/secret.dat


#------New Polic Creation -----
#open a session
tpm2_startauthsession -Q -S scratch/session.ctx 
tpm2_policypcr -Q -S scratch/session.ctx -l sha256:15 -L scratch/policy.dat
tpm2_flushcontext -Q scratch/session.ctx


# 1. Create the primary parent key in the owner hierarchy
tpm2_createprimary -Q -c scratch/primary.ctx

# 2. Import the raw secret as an HMAC SHA256 key protected by the primary key
##tpm2_import -Q -C scratch/primary.ctx -G hmac:sha256 -i scratch/secret.dat -u scratch/hmac.pub -r scratch/hmac.priv
tpm2_import -Q -C scratch/primary.ctx -G hmac:sha256 -i scratch/secret.dat -u scratch/hmac.pub -r scratch/hmac.priv -L scratch/policy.dat

# 3. Load the imported key into the TPM's volatile memory
tpm2_load -Q -C scratch/primary.ctx -u scratch/hmac.pub -r scratch/hmac.priv -c scratch/hmac.ctx

# 4. Save the key permanently to NVRAM at handle 0x81000000
tpm2_evictcontrol -Q -C o -c scratch/hmac.ctx 0x81000000