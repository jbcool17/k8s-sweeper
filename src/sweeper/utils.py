import math
import sys
from time import sleep

from .logging import logging


def parse_context(context):
    return {"project": context.split("_")[1], "location": context.split("_")[2], "name": context.split("_")[3]}


def build_context(cluster):
    # gke_PROJECT_REGION_CLUSTER
    return f'gke_{cluster["project"]}_{cluster["location"]}_{cluster["name"]}'


def time_it(sleep_time, print_countdown=False):
    logging.info(f"Waiting {sleep_time} seconds...")

    if print_countdown:
        for remaining in range(sleep_time, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(remaining))
            sys.stdout.flush()
            sleep(1)
        # os.system("clear")
        sys.stdout.write("\r")
        sys.stdout.write("******* waiting complete *******")
        sys.stdout.flush()
    else:
        sleep(sleep_time)

    # print()


def check_label(labels, key, value):
    """Return if label and key match"""
    if key in labels.keys() and labels[key] == value:
        return True
    else:
        return False


def create_batches(list_to_batch: list, batch_size: int, batch_type: str) -> dict:
    list_to_batch_count = len(list_to_batch)
    batch_count = math.ceil(list_to_batch_count / batch_size)
    logging.info(f"Batching a list of {list_to_batch_count} {batch_type}(s) into {batch_count} batches of {batch_size}")
    batches = []
    for i in range(batch_count):
        # SET UP BATCH
        start_index = i * batch_size
        end_index = min(start_index + batch_size, list_to_batch_count)
        batched_nodes = list_to_batch[start_index:end_index]
        batches.append(batched_nodes)

    return {"batches": batches, "total_batch_count": len(batches), "size_per_batch": batch_size}
