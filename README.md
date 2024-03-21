# sweeper

A maintenance tool for kubernetes that drains nodes and evicts pods in a controlled and graceful manner. It targets nodes with a specific label and starts to process them.

A cluster-autoscaler feature is required to be enabled to allow the proper downscaling while any kind of scaling up is disabled in the specified node pool or group. After pods are evicted they should migrate to any other availble nodes where auto scaling is enabled.

<https://cloud.google.com/blog/topics/developers-practitioners/running-gke-application-spot-nodes-demand-nodes-fallback>

## Usecases

1. Downscale nodes with a specific label.

2. If you are using a opt-in type of pattern that utilizes taints/toleration to manage nodes/pods in kubernetes. For example, spot nodes with on-demand nodes as fallback. You can utilize a tool like this to sweep or migrate pods back to the spot when needed via a nightly cron.

3. Migration workloads from one pool to another during upgrades or patching

## Setup

```bash
make venv

make activate

make install
```

OR

```bash
python -m venv .env

source .env/bin/activate

pip install .
```

## Usage

**note:** make sure target pool does not have the ability to scale up new nodes, *For example in gke*: setting the max nodes it can scale up to `1`, leaving autoscaling on would allow you to naturally downscale

```
# Sweep pods off of nodes with following label selector (kubernetes.io/os=linux)
sweeper sweep -s "kubernetes.io/os=linux"
sweeper sweep --source-node-pool-label cloud.google.com/gke-nodepool=<NODE_POOL>
```

## Auto Sweeper(NOT IMPLEMENTED)

- uses specific strategies to process a gke cluster's node pools

```
sweeper auto-sweep
```

## Testing

Using `kind` or `kwok` to simulate kubernetes clusters

[TEST README](test/README.md)
