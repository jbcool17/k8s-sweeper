# brew install kwok
set -e

source $PWD/test/kwok/config.sh

setup_kwok

INITIAL_COUNTS=$(get_pod_counts)
echo "Getting ready to sweep"
echo
sleep 3

sweeper sweep -s jbcool.io/type=spot --node-batch-size 5 --node-batch-time 1 --node-time 0 --pod-batch-time 0  --nodes-timeout-count 1 --nodes-timeout-seconds 1 --oldest-first \

FINAL_COUNTS=$(get_pod_counts)

echo "INITIAL: $INITIAL_COUNTS"
echo "FINAL:   $FINAL_COUNTS"

echo "Script Complete"
