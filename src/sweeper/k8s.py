from datetime import datetime, timedelta

from kubernetes import client, config

from .logging import logging
from .utils import time_it


def load_config():
    """
    Load k8s config locally or inside a cluster
    """
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()


def get_nodes():
    """
    Get a list of nodes
    """
    load_config()
    v1 = client.CoreV1Api()
    return v1.list_node(watch=False).items


def get_nodes_by_label(label):
    """
    Get a list of node by label
    """
    load_config()
    v1 = client.CoreV1Api()
    return v1.list_node(watch=False, label_selector=f"{label}").items


def get_node_by_name(name):
    """
    Get a specific node by name
    """
    load_config()
    v1 = client.CoreV1Api()
    return v1.read_node(name=name)


def get_contexts():
    """
    Get a list of local contexts
    """
    contexts = config.list_kube_config_contexts()
    contexts = [context["name"] for context in contexts]

    return contexts


def get_current_context():
    """Get current context"""
    return config.list_kube_config_contexts()[1]["name"]


def get_node_age(node):
    """Get Node Age"""
    return datetime.utcnow() - node.metadata.creation_timestamp.replace(tzinfo=None)


def check_for_new_nodes_by_node_pool(node_pool_label):
    """Waiting for new nodes to come up"""
    check_count = 0
    node_age_max = timedelta(minutes=int(10))
    while check_count < 4:
        new_nodes = 0
        logging.info(f"Checking({check_count}/3) for new nodes w/ label ){node_pool_label})...")
        nodes = get_nodes_by_label(node_pool_label)
        for node in nodes:
            node_age = get_node_age(node)
            logging.info("==> ", node.metadata.name, node_age, node_age_max)
            if get_node_age(node) < node_age_max:
                new_nodes += 1

        logging.info(f"New/Total Nodes: {new_nodes}/{len(nodes)}")
        check_count += 1
        if new_nodes >= 2:
            logging.info("New nodes check complete")
            return True
        time_it(20)

    return False


def check_for_zero_nodes_by_node_pool(
    node_pool_label, timeout_count=10, node_limit=None, timeout_seconds=20
) -> bool:
    """
    Waiting for nodes with a certain label to be removed
    """
    check_count = 0
    # print()
    while check_count < timeout_count:
        logging.info(f"Checking({check_count + 1}/{timeout_count}) for removed nodes({node_pool_label})...")
        node_count = len(get_nodes_by_label(node_pool_label))
        if node_limit is not None:
            logging.info(f"Nodes for Removal: {node_count} (max_node_limit: {node_limit})")
        else:
            logging.info(f"Nodes for Removal: {node_count}")
        check_count += 1

        if node_count == 0:
            logging.info("Zero nodes check complete")
            return True
        time_it(timeout_seconds)

    return False


def evict_pods(pods, node, grace_period_seconds=10, dry_run=False):
    """
    Evict pods from node
    """
    v1 = client.CoreV1Api()

    logging.info(f"Evicting pods on node {node.metadata.name}")

    if not pods:
        logging.info("No pods in list")

    pod_count = len(pods)
    logging.info(f"Pods to evict: {pod_count}")

    for pod in pods:
        pod_name = pod.metadata.name
        pod_namespace = pod.metadata.namespace

        if dry_run:
            logging.info(f"DRY-RUN: Would evict pod: {pod.metadata.name} on {node.metadata.name}")
        else:
            delete_options = client.V1DeleteOptions(grace_period_seconds=grace_period_seconds)
            body = client.V1Eviction(
                metadata=client.V1ObjectMeta(name=pod_name, namespace=pod_namespace), delete_options=delete_options
            )

            try:
                v1.create_namespaced_pod_eviction(pod_name, pod_namespace, body)
                logging.info(f"Evicted pod: {pod_name}")
            except Exception as e:
                logging.info(f"Error evicting pod: {pod_name} - {str(e)}")


def get_pods_by_node(node, remove_daemonset_pods=False, remove_node_pods=False):
    """
    Get pods on node
    """
    v1 = client.CoreV1Api()

    node_name = node.metadata.name
    logging.info(f"Getting pods on node {node_name}")
    pods = v1.list_pod_for_all_namespaces(field_selector=f"spec.nodeName={node_name}").items

    if remove_daemonset_pods:
        logging.info("Removing daemonset pods...")
        pods = [pod for pod in pods if not is_daemonset_pod(pod)]

    if remove_node_pods:
        logging.info("Removing node pods...")
        pods = [pod for pod in pods if not is_node_pod(pod)]

    logging.info(f"{len(pods)} pods found")
    return pods


def is_daemonset_pod(pod) -> None:
    """
    Check if pod is a daemonset pod
    """
    return pod.metadata.owner_references and any(owner.kind == "DaemonSet" for owner in pod.metadata.owner_references)


def is_node_pod(pod) -> None:
    """
    Check if pod owner is a node
    """
    return pod.metadata.owner_references and any(owner.kind == "Node" for owner in pod.metadata.owner_references)


def toggle_node_scheduling(node, cordoned=True, dry_run=False) -> None:
    """
    Toggle node scheduling

    Cordon / Uncordon a node
    """
    load_config()
    v1 = client.CoreV1Api()

    # Check for taints that indicate node is marked for deletion
    if not cordoned:
        node_taints = node.spec.taints or []
        deletion_taints = ["ToBeDeletedByClusterAutoscaler", "DeletionCandidateOfClusterAutoscaler"]
        if any(taint.key in deletion_taints for taint in node_taints):
            logging.info(f"Node {node.metadata.name} is marked for deletion, skipping uncordon")
            return

    if dry_run:
        logging.info(f"DRY-RUN: Would cordon:{cordoned} - {node.metadata.name}")
    else:
        try:
            node_name = node.metadata.name
            node = get_node_by_name(node_name)
            node.spec.unschedulable = cordoned
            v1.patch_node(node_name, node)
            action = "cordoned" if cordoned else "uncordoned"
            logging.info(f"Node {node_name} {action} successfully")
        except Exception as e:
            action = "cordoning" if cordoned else "uncordoning"
            logging.info(f"Error {action} node {node_name}: {str(e)}")
