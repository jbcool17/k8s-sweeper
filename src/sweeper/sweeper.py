import sys
import time

from . import k8s
from .event import Event
from .logging import logging
from .utils import create_batches, time_it


class Sweeper:
    """
    Sweeper class
    - manage node pool sweep
    """

    def __init__(
        self,
        source_node_pool_label: str = "cloud.google.com/gke-nodepool=default",
        # How many nodes per batch
        node_batch_size: int = 10,
        # How much time in between node batches
        node_batch_time: int = 60,
        # How many pods per node to evict at once
        pod_batch_size: int = 5,
        # How much time in between pod batches
        pod_batch_time: int = 30,
        # How much time in between in node
        node_time: int = 120,
        # Simulate a sweep run
        dry_run: bool = False,
        # Don't check/wait for node to automcally downscale.
        # This will still uncordon nodes that are still running
        disable_node_removal_wait=False,
        # Indicates a sweep has been processed
        processed: bool = False,
        # Add note about the sweep
        note: str = "",
    ):
        # NODE POOL
        self.source_node_pool_label = source_node_pool_label

        # BATCH SETTINGS
        self.node_batch_size = node_batch_size
        self.node_batch_time = node_batch_time
        self.pod_batch_size = pod_batch_size
        self.pod_batch_time = pod_batch_time
        self.node_time = node_time

        # SECONDARY SETTINGS
        self.dry_run = dry_run
        self.disable_node_removal_wait = disable_node_removal_wait
        self.processed = processed
        self.note = note

    def sweep(self):
        """
        Perform migration loop
        - Get node count from source pool
        - Batch nodes into groups
        - Process Node batch
        -  cordon
        -  batch pods and drain/evict pods
        - Wait for nodes to scale down in source pool, uncordon if it times out
        """

        # SETUP - Variables
        start = time.time()
        source_nodes = k8s.get_nodes_by_label(self.source_node_pool_label)
        source_node_count = len(source_nodes)

        # Start Logging
        logging.info(f"Source: {self.source_node_pool_label} {source_node_count}")
        logging.info(f"Attemping to sweep the pods Johnny!! {self.source_node_pool_label}")
        logging.info(f"We're gonna need {source_node_count} body bag(s)!!!")
        sweeper_event = Event(dry_run=self.dry_run)

        # LOOP THROUGH BATCHES
        if source_node_count > 0:

            # TRIGGER KUBERNETS EVENT
            sweeper_event.create(
                note=f"Initiate sweeper start on node pool: {self.source_node_pool_label}",
                action="SweeperInitiated",
                regarding={"kind": "Sweeper", "name": f"sweeper-{self.source_node_pool_label}"},
            )

            # ------------------------------------------------------------------
            # CREATE BATCHES
            node_batch_data = create_batches(
                list_to_batch=source_nodes, batch_size=self.node_batch_size, batch_type="node"
            )

            # ------------------------------------------------------------------
            # PROCESS NODE BATCHES
            logging.info("STARTING BATCH RUNS")
            for i, batch in enumerate(node_batch_data["batches"]):
                batch_length = len(batch)
                logging.info(f"--> Starting node batch {i + 1} of {node_batch_data['total_batch_count']}")
                logging.info(f"Nodes in batch({i + 1}): {batch_length}")

                # TRIGGER KUBERNETS EVENT
                sweeper_event.create(
                    note=f"{self.source_node_pool_label} - Processing node batch {i + 1} of {node_batch_data['total_batch_count']}",
                    action="SweeperNodeBatch",
                    regarding={"kind": "Sweeper", "name": f"sweeper-{self.source_node_pool_label}"},
                )

                time_it(5)

                # ------------------------------------------------------------------
                # MIGRATE PROCESS

                # Cordon all nodes in batch first
                for node in batch:
                    k8s.toggle_node_scheduling(node, dry_run=self.dry_run)

                # PROCESS NODE BATCH
                for j, node in enumerate(batch):
                    logging.info(f"Processing node {j + 1} of {len(batch)} in batch({i+1})")
                    pods = k8s.get_pods_by_node(node, remove_daemonset_pods=True, remove_node_pods=True)
                    pod_batch_data = create_batches(
                        list_to_batch=pods, batch_size=self.pod_batch_size, batch_type="pod"
                    )

                    # PROCESS POD BATCHES
                    for k, pods_to_evict in enumerate(pod_batch_data["batches"]):
                        logging.info(
                            f"Processing Node Batch: {i + 1} of {node_batch_data['total_batch_count']} | Node: {j + 1} of {len(batch)} | Pod Batch {k + 1} of {len(pod_batch_data['batches'])}"
                        )
                        k8s.evict_pods(pods_to_evict, node, dry_run=self.dry_run)

                        # Timeout between nodes in batch
                        if k < pod_batch_data["total_batch_count"] - 1:
                            time_it(self.pod_batch_time)

                    # Timeout between nodes in batch
                    if j < len(batch) - 1:
                        time_it(self.node_time)

                # ------------------------------------------------------------------
                # NATURAL CLEAN UP, WAITING FOR CLUSTER AUTOSCALER
                # Will track nodes until they are removed
                # Will uncordon after timeout, to make nodes avavilble if they aren't removed for some reason
                if node_batch_data["total_batch_count"] == i + 1:
                    if not self.dry_run and not self.disable_node_removal_wait:
                        if k8s.check_for_zero_nodes_by_node_pool(self.source_node_pool_label):
                            logging.info(f"Sweeped - {self.source_node_pool_label} - returned 0 nodes)")
                            sys.exit()
                        else:
                            logging.info("Node check timeout, uncordoning left over nodes")
                            # UNCORDON NODES JUST INCASE
                            for node in k8s.get_nodes_by_label(self.source_node_pool_label):
                                k8s.toggle_node_scheduling(node, cordoned=False, dry_run=self.dry_run)
                    else:
                        if self.dry_run:
                            logging.info("DRY-RUN: Skipping scale down check")
                        elif self.disable_node_removal_wait:
                            logging.info("Scale Down Check Disabled")
                            for node in k8s.get_nodes_by_label(self.source_node_pool_label):
                                k8s.toggle_node_scheduling(node, cordoned=False, dry_run=self.dry_run)

                else:
                    logging.info(f"Skipping clean up until the end: {i + 1}/{node_batch_data['total_batch_count']}")

                # Timeout between node batches / Completion Message & Event
                if i < node_batch_data["total_batch_count"] - 1:
                    time_it(self.node_batch_time)
                else:
                    logging.info("Batches complete")
                    end = time.time()
                    total_time = end - start
                    sweeper_event.create(
                        note=f"Sweeper has completed on node pool {self.source_node_pool_label}- {total_time}",
                        action="SweeperCompleted",
                        regarding={"kind": "Sweeper", "name": f"sweeper-{self.source_node_pool_label}"},
                    )

        else:
            sweeper_event.create(
                note=f"Source pool({self.source_node_pool_label}) returned 0 nodes. Nothing to sweep. Sorry Johnny :-(",
                action="SweeperCheckCompleted",
                regarding={"kind": "Sweeper", "name": f"sweeper-{self.source_node_pool_label}"},
            )

            logging.info(
                f"Crane Kick - Source pool({self.source_node_pool_label}) returned 0 nodes. Nothing to sweep. Sorry Johnny :-("
            )

        # Grab Currrent Time After Running the Code
        end = time.time()

        # Subtract Start Time from The End Time
        total_time = end - start
        logging.info("Total Time: " + str(total_time))

        self.processed = True

        return self.processed
