# brew install kwok
echo "Starting scripts..."
kwokctl create cluster \
    && ./test/kwok/kwok-node-default.sh \
    && ./test/kwok/kwok-node-spot.sh \
    && ./test/kwok/kwok-pods.sh \
    && kubectl get no && sleep 5 && kubectl get pods -A -o wide

echo "Getting ready to sweep"
echo
sleep 3

uv run sweeper sweep -s cloud.google.com/gke-provisioning=standard -s jbcool.io/type=spot --node-batch-size 5 --node-batch-time 10 --node-time 0 --pod-batch-time 0 --disable-node-removal-wait

uv run sweeper sweep -s cloud.google.com/machine-family=n2 --node-batch-size 5 --node-batch-time 10 --node-time 0 --pod-batch-time 0 --disable-node-removal-wait --max-node-limit 2

# Cleanup
kwokctl delete cluster

echo "Script Complete"
