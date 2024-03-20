# brew install kwok
echo "Starting scripts..."
kwokctl create cluster \
    && ./test/kwok/kwok-node-default.sh \
    && ./test/kwok/kwok-node-spot.sh \
    && ./test/kwok/kwok-pods.sh \
    && kubectl get no && sleep 5 && kubectl get pods -A

echo "Getting ready to sweep"
echo
sleep 3
sweeper sweep -s node-type=spot --node-batch-size 5 --node-batch-time 10 --node-time 0 --pod-batch-time 0 --disable-node-removal-wait && kubectl get no -l node-type=spot
echo "Script Complete"
