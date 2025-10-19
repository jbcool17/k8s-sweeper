#!/bin/bash

set -e
source $PWD/test/kwok/config.sh

MACHINE_FAMILY="${MACHINE_FAMILY_N2D}"

for i in `seq 0 5`; do
  kubectl apply -f - <<EOF
apiVersion: v1
kind: Node
metadata:
  annotations:
    node.alpha.kubernetes.io/ttl: "0"
    kwok.x-k8s.io/node: fake
  labels:
    beta.kubernetes.io/arch: amd64
    beta.kubernetes.io/os: linux
    kubernetes.io/arch: amd64
    kubernetes.io/hostname: kwok-node-default-${MACHINE_FAMILY}-${i}
    kubernetes.io/os: linux
    kubernetes.io/role: agent
    node.kubernetes.io/instance-type: ${INSTANCE_TYPE}
    node-role.kubernetes.io/agent: ""
    type: kwok
    cloud.google.com/gke-nodepool: ${NODE_POOL}
    cloud.google.com/machine-family: ${MACHINE_FAMILY}
    cloud.google.com/gke-provisioning: ${PROVISIONING}
    jbcool.io/type: ${JBCOOL_TYPE}
  name: kwok-node-default-${MACHINE_FAMILY}-${i}
spec:
status:
  allocatable:
    cpu: ${CPU_COUNT}
    memory: 256Gi
    pods: ${POD_COUNT}
  capacity:
    cpu: ${CPU_COUNT}
    memory: 256Gi
    pods: ${POD_COUNT}
  nodeInfo:
    architecture: amd64
    bootID: ""
    containerRuntimeVersion: ""
    kernelVersion: ""
    kubeProxyVersion: fake
    kubeletVersion: fake
    machineID: ""
    operatingSystem: linux
    osImage: ""
    systemUUID: ""
  phase: Running
EOF

done
