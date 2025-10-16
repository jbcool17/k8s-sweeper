#!/bin/bash

# Variables
CPU_COUNT=32
POD_COUNT=32
MACHINE_FAMILY="n2d"
INSTANCE_TYPE="${MACHINE_FAMILY}-standard-${CPU_COUNT}"
NODE_POOL="default-${MACHINE_FAMILY}-12345"
PROVISIONING="standard"
JBCOOL_TYPE="default"

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
#   taints: # Avoid scheduling actual running pods to fake Node
#   - effect: NoSchedule
#     key: kwok.x-k8s.io/node
#     value: fake
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
