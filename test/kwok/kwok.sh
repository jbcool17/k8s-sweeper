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

sweeper sweep -s jbcool.io/type=spot --node-batch-size 5 --node-batch-time 10 --node-time 0 --pod-batch-time 0  --nodes-timeout-count 1 --nodes-timeout-seconds 10 --oldest-first && kubectl get no -l jbcool.io/type=spot

echo "Script Complete"
