import importlib.metadata as importlib_metadata

import click

from sweeper.logging import logging
from sweeper.sweeper import Sweeper


# -----------------------------------------------------------------------------------------------
@click.group()
@click.version_option(version=importlib_metadata.version("sweeper"), prog_name="sweeper")
def cli():
    """
    Tools for kubernetes
    """
    pass


# -----------------------------------------------------------------------------------------------
# SWEEPER
@cli.command("sweep")
@click.option(
    "-s",
    "--source-node-pool-label",
    "source_node_pool_label",
    multiple=True,
    help="Source node pool label. Can be specified multiple times.",
)
@click.option("-nbs", "--node-batch-size", "node_batch_size", default=1, help="(1)Number of nodes in each batch")
@click.option("-pbs", "--pod-batch-size", "pod_batch_size", default=5, help="(5)Number of pod to evict in a batch")
@click.option("-nbt", "--node-batch-time", "node_batch_time", default=40, help="(40)Seconds between each node batch")
@click.option("-pbt", "--pod-batch-time", "pod_batch_time", default=2, help="(2)Seconds between each pod batch")
@click.option("-nt", "--node-time", "node_time", default=10, help="(10)Seconds between each node")
@click.option("-dr", "--dry-run", "dry_run", is_flag=True, help="Perform a dry run without evicting pods")
@click.option(
    "-dnrw",
    "--disable-node-removal-wait",
    "disable_node_removal_wait",
    is_flag=True,
    help="Disables node removal check at the end",
)
@click.option("-mnl", "--max-node-limit", "max_node_limit", default=None, type=int, help="Max node limit to process")
@click.option(
    "-zntc",
    "--zero-nodes-timeout-count",
    "zero_nodes_timeout_count",
    default=10,
    help="(10)Number of times to check for zero nodes",
)
@click.option(
    "-znts",
    "--zero-nodes-timeout-seconds",
    "zero_nodes_timeout_seconds",
    default=20,
    help="(20)Seconds between each zero nodes check",
)

def sweep(**kwargs: any) -> None:
    """
    Cordon and drain nodes with a specific label
    sweeper sweep -s "kubernetes.io/os=linux"
    """

    logging.info("Initiating Sweep...")
    Sweeper(**kwargs).sweep()


if __name__ == "__main__":
    cli()
