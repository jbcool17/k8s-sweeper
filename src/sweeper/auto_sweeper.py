# from . import k8s
# from .event import Event
from .logging import logging
# from .sweeper import Sweeper


def auto_sweep(
    node_batch_size: int,
    node_batch_time: int,
    pod_batch_size: int,
    pod_batch_time: int,
    node_time: int,
    dry_run: bool,
    warmup_node_pool: bool,
    strategies: list,
) -> None:
    """
    Find backup pools with nodes and process
    """

    logging.info("THIS IS NOT SETUP YET")
