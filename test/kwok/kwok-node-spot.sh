#!/bin/bash

# SPOT
CPU_COUNT=32
POD_COUNT=32
MACHINE_FAMILY="n2d"
INSTANCE_TYPE="${MACHINE_FAMILY}-standard-${CPU_COUNT}"
NODE_POOL="spot-${MACHINE_FAMILY}-12345"
PROVISIONING="spot"
JBCOOL_TYPE="spot"

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
    kubernetes.io/hostname: kwok-node-spot-${MACHINE_FAMILY}-${i}
    kubernetes.io/os: linux
    kubernetes.io/role: agent
    node.kubernetes.io/instance-type: ${INSTANCE_TYPE}
    node-role.kubernetes.io/agent: ""
    cloud.google.com/gke-nodepool: ${NODE_POOL}
    cloud.google.com/machine-family: ${MACHINE_FAMILY}
    cloud.google.com/gke-provisioning: ${PROVISIONING}
    jbcool.io/type: ${JBCOOL_TYPE}
  name: kwok-node-spot-${MACHINE_FAMILY}-${i}
spec:
  taints: # Avoid scheduling actual running pods to fake Node
  - effect: NoSchedule
    key: jbcool.io/type
    value: spot
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

# SPOT BACKUP
INSTANCE_TYPE="${MACHINE_FAMILY}-standard-${CPU_COUNT}"
NODE_POOL="spot-${MACHINE_FAMILY}-backup-12345"
PROVISIONING="standard"

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
    kubernetes.io/hostname: kwok-node-spot-${MACHINE_FAMILY}-backup-${i}
    kubernetes.io/os: linux
    kubernetes.io/role: agent
    node.kubernetes.io/instance-type: ${INSTANCE_TYPE}
    node-role.kubernetes.io/agent: ""
    cloud.google.com/gke-nodepool: ${NODE_POOL}
    cloud.google.com/machine-family: ${MACHINE_FAMILY}
    cloud.google.com/gke-provisioning: ${PROVISIONING}
    jbcool.io/type: ${JBCOOL_TYPE}
  name: kwok-node-spot-${MACHINE_FAMILY}-backup-${i}
spec:
  taints: # Avoid scheduling actual running pods to fake Node
  - effect: NoSchedule
    key: jbcool.io/type
    value: spot
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

#  NON N2D
MACHINE_FAMILY="n2"
INSTANCE_TYPE="${MACHINE_FAMILY}-standard-${CPU_COUNT}"
NODE_POOL="spot-${MACHINE_FAMILY}-12345"
PROVISIONING="spot"

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
    kubernetes.io/hostname: kwok-node-spot-${MACHINE_FAMILY}-${i}
    kubernetes.io/os: linux
    kubernetes.io/role: agent
    node.kubernetes.io/instance-type: ${INSTANCE_TYPE}
    node-role.kubernetes.io/agent: ""
    cloud.google.com/gke-nodepool: ${NODE_POOL}
    cloud.google.com/machine-family: ${MACHINE_FAMILY}
    cloud.google.com/gke-provisioning: ${PROVISIONING}
    jbcool.io/type: ${JBCOOL_TYPE}
  name: kwok-node-spot-${MACHINE_FAMILY}-${i}
spec:
  taints: # Avoid scheduling actual running pods to fake Node
  - effect: NoSchedule
    key: jbcool.io/type
    value: spot
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