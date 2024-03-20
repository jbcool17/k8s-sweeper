import random
import string
from datetime import datetime

from kubernetes import client
from kubernetes.client.rest import ApiException

from .k8s import load_config
from .logging import logging


class Event:
    """
    Create an event
    """

    def __init__(
        self,
        name: str = "sweeper",
        namespace: str = "kube-system",
        reason: str = "SweeperStatus",
        reporting_instance: str = "sweeper-instance",
        reporting_controller: str = "sweeper-controller",
        dry_run: bool = False,
    ):
        self.name = name
        self.namespace = namespace
        self.reason = reason + "DryRun" if dry_run else reason
        self.reporting_instance = reporting_instance
        self.reporting_controller = reporting_controller
        self.dry_run = dry_run

    def create(
        self,
        note: str = "A sweep note",
        action: str = "SweeperAction",
        event_type: str = "Normal",
        regarding: dict = {"kind": "Sweeper", "name": "sweeper-test"},
    ):
        """
        Create an event
        """
        name = self.name
        namespace = self.namespace
        reason = self.reason
        reporting_instance = self.reporting_instance
        reporting_controller = self.reporting_controller
        random_string = "".join(random.choices(string.ascii_uppercase + string.digits, k=7))
        now = f"{datetime.utcnow().isoformat()}+00:00"

        load_config()
        v1 = client.EventsV1Api()
        body = client.EventsV1Event(
            metadata=client.V1ObjectMeta(name=f"{name}-{random_string.lower()}", namespace=namespace),
            reason=reason,
            note=note,
            event_time=now,
            action=action,
            type=event_type,
            reporting_instance=reporting_instance,
            reporting_controller=reporting_controller,
            regarding=client.V1ObjectReference(kind=regarding["kind"], name=regarding["name"], namespace=namespace),
        )

        try:
            v1.create_namespaced_event(namespace, body)
            logging.info(f"Event Created - {namespace} {name} {reason}")
        except ApiException as e:
            logging.error(f"Exception when calling EventsV1Api->create_namespaced_event: {e}\n")
