kind create cluster --config=kind.yaml


kubectl taint no -l cloud.google.com/gke-nodepool=spot node-type=spot:NoSchedule
