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
NODE_COUNT=5
CPU_COUNT=32
POD_COUNT=32
MACHINE_FAMILY_N2D="n2d"
MACHINE_FAMILY_N2="n2"

apply_kwok_config() {
  local node_name_prefix machine_family node_pool provisioning jbcool_type i

  # Parse named arguments
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --node-name-prefix) node_name_prefix="$2"; shift 2;;
      --machine-family) machine_family="$2"; shift 2;;
      --node-pool) node_pool="$2"; shift 2;;
      --provisioning) provisioning="$2"; shift 2;;
      --jbcool-type) jbcool_type="$2"; shift 2;;
      --i) i="$2"; shift 2;;
      *) echo "Unknown parameter passed: $1"; exit 1;;
    esac
  done

  local instance_type="${machine_family}-standard-${CPU_COUNT}"
  local node_name="${node_name_prefix}-${machine_family}-${i}"

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
    kubernetes.io/hostname: ${node_name}
    kubernetes.io/os: linux
    kubernetes.io/role: agent
    node.kubernetes.io/instance-type: ${instance_type}
    node-role.kubernetes.io/agent: ""
    cloud.google.com/gke-nodepool: ${node_pool}
    cloud.google.com/machine-family: ${machine_family}
    cloud.google.com/gke-provisioning: ${provisioning}
    jbcool.io/type: ${jbcool_type}
  name: ${node_name}
spec: {}
EOF

  # Conditionally apply taints if jbcool_type is not 'default'
  if [ "${jbcool_type}" != "default" ]; then
    kubectl patch node "${node_name}" --type=json -p="[{\"op\": \"add\", \"path\": \"/spec/taints\", \"value\": [{\"effect\": \"NoSchedule\", \"key\": \"jbcool.io/type\", \"value\": \"${jbcool_type}\"}]}]"
  fi
}

apply_kwok_deployment() {
  local deployment_name=$1
  local replicas=$2
  local type=$3 # 'default' or 'spot'

  kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${deployment_name}
  namespace: default
spec:
  replicas: ${replicas:-1}
  selector:
    matchLabels:
      app: ${deployment_name}
  template:
    metadata:
      labels:
        app: ${deployment_name}
    spec:
      tolerations:
      - key: "kwok.x-k8s.io/node"
        operator: "Exists"
        effect: "NoSchedule"
$(if [ "${type}" == "spot" ]; then cat <<EOM
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: jbcool.io/type
                operator: In
                values:
                - spot
      tolerations:
      - key: "jbcool.io/type"
        value: "spot"
        effect: "NoSchedule"
EOM
fi)
      containers:
      - name: fake-container
        image: fake-image
EOF
}
