#!/bin/bash

set -e

source $PWD/test/kwok/config.sh

MACHINE_FAMILY="${MACHINE_FAMILY_N2D}"
NODE_POOL="default-${MACHINE_FAMILY}-12345"
PROVISIONING="standard"
JBCOOL_TYPE="default"

for i in `seq 0 ${NODE_COUNT}`; do
  apply_kwok_config \
    --node-name-prefix "kwok-node-default" \
    --machine-family "${MACHINE_FAMILY}" \
    --node-pool "${NODE_POOL}" \
    --provisioning "${PROVISIONING}" \
    --jbcool-type "${JBCOOL_TYPE}" \
    --i "${i}"
done
