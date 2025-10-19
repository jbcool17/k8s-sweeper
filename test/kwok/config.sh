#!/bin/bash

function setup_kwok() {
  kwokctl start cluster \
    && ./test/kwok/kwok-node-default.sh \
    && ./test/kwok/kwok-node-spot.sh \
    && ./test/kwok/kwok-pods.sh \
    && kubectl get no && sleep 5 && kubectl get pods -A
}
function get_pod_counts() {
    # for n in $(kubectl get nodes --no-headers | awk '{print $1}'); do 
    #     echo -n "${n}: "; 
    #     kubectl get pod -A --field-selector spec.nodeName=$n --no-headers | awk '{print $1}' | wc -w; 
    # done
    kubectl get pods -A -o jsonpath='{range .items[?(@.spec.nodeName)]}{.spec.nodeName}{"\n"}{end}' | sort | uniq -c | sort -rn

}
# Common Configuration
CPU_COUNT=32
POD_COUNT=32
MACHINE_FAMILY_N2D="n2d"
MACHINE_FAMILY_N2="n2"

# Generic function to apply a kwok config given a set of node parameters
apply_kwok_config() {
  local node_name_prefix=$1
  local machine_family=$2
  local node_pool=$3
  local provisioning=$4
  local jbcool_type=$5
  local i=$6

  INSTANCE_TYPE="${machine_family}-standard-${CPU_COUNT}"

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
    kubernetes.io/hostname: ${node_name_prefix}-${machine_family}-${i}
    kubernetes.io/os: linux
    kubernetes.io/role: agent
    node.kubernetes.io/instance-type: ${INSTANCE_TYPE}
    node-role.kubernetes.io/agent: ""
    cloud.google.com/gke-nodepool: ${node_pool}
    cloud.google.com/machine-family: ${machine_family}
    cloud.google.com/gke-provisioning: ${provisioning}
    jbcool.io/type: ${jbcool_type}
  name: ${node_name_prefix}-${machine_family}-${i}
spec:
  taints: # Avoid scheduling actual running pods to fake Node
  - effect: NoSchedule
    key: jbcool.io/type
    value: ${jbcool_type}
EOF
}
