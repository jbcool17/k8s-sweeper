import importlib.metadata as importlib_metadata

import click
from sweeper import auto_sweeper
from sweeper.logging import logging
from sweeper.sweeper import Sweeper


# -----------------------------------------------------------------------------------------------
@click.group("k8s-cli")
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
    default="cloud.google.com/gke-nodepool=default",
    required=True,
    help="Source node pool label(cloud.google.com/gke-nodepool=spot-n2d-24596e2a05b0fbd8)",
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
def sweep(**kwargs: any) -> None:
    """
    Cordon and drain nodes with a specific label
    sweeper sweep -s "kubernetes.io/os=linux"
    """

    logging.info("Initiating Sweep...")
    Sweeper(**kwargs).sweep()


@cli.command("auto-sweep")
@click.option("-nbs", "--node-batch-size", "node_batch_size", default=1, help="Number of nodes in each batch")
@click.option("-pbs", "--pod-batch-size", "pod_batch_size", default=5, help="Number of pod to evict in a batch")
@click.option("-nbt", "--node-batch-time", "node_batch_time", default=40, help="Seconds between each node batch")
@click.option("-pbt", "--pod-batch-time", "pod_batch_time", default=2, help="Seconds between each pod batch")
@click.option("-nt", "--node-time", "node_time", default=10, help="Seconds between each node")
@click.option("-dr", "--dry-run", "dry_run", is_flag=True, help="Perform a dry run without evicting pods")
@click.option(
    "-w",
    "--warmup-node-pool",
    "warmup_node_pool",
    is_flag=True,
    help="(Currently Disabled) - Warm up a node pool by spinning up pause pods",
)
@click.option(
    "-s",
    "--strategies",
    "strategies",
    multiple=True,
    default=["spot-od-backup", "spot-od-backup-legacy", "non-n2d"],
    help="Run specific strategies(list)",
)
def auto_sweep(**kwargs: any) -> None:
    """
    Automatically find backup pools and process them
    """

    logging.info("Initiating Auto Sweep...")
    auto_sweeper.auto_sweep(**kwargs)


if __name__ == "__main__":
    cli()
