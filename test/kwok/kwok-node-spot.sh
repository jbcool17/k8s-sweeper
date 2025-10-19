#!/bin/bash

set -e

source $PWD/test/kwok/config.sh

# N2D SPOT
MACHINE_FAMILY="${MACHINE_FAMILY_N2D}"
NODE_POOL="spot-${MACHINE_FAMILY}-12345"
PROVISIONING="spot"
JBCOOL_TYPE="spot"

for i in `seq 0 ${NODE_COUNT}`; do
  apply_kwok_config \
    --node-name-prefix "kwok-node-spot" \
    --machine-family "${MACHINE_FAMILY}" \
    --node-pool "${NODE_POOL}" \
    --provisioning "${PROVISIONING}" \
    --jbcool-type "${JBCOOL_TYPE}" \
    --i "${i}"
done

# N2D SPOT BACKUP (simulating on-demand fallback)
MACHINE_FAMILY="${MACHINE_FAMILY_N2D}"
NODE_POOL="spot-${MACHINE_FAMILY}-backup-12345"
PROVISIONING="standard"
JBCOOL_TYPE="spot"

for i in `seq 0 ${NODE_COUNT}`; do
  apply_kwok_config \
    --node-name-prefix "kwok-node-spot-backup" \
    --machine-family "${MACHINE_FAMILY}" \
    --node-pool "${NODE_POOL}" \
    --provisioning "${PROVISIONING}" \
    --jbcool-type "${JBCOOL_TYPE}" \
    --i "${i}"
done

# N2 SPOT
MACHINE_FAMILY="${MACHINE_FAMILY_N2}"
NODE_POOL="spot-${MACHINE_FAMILY}-12345"
JBCOOL_TYPE="spot"
PROVISIONING="spot"

for i in `seq 0 ${NODE_COUNT}`; do
  apply_kwok_config \
    --node-name-prefix "kwok-node-spot" \
    --machine-family "${MACHINE_FAMILY}" \
    --node-pool "${NODE_POOL}" \
    --provisioning "${PROVISIONING}" \
    --jbcool-type "${JBCOOL_TYPE}" \
    --i "${i}"
done