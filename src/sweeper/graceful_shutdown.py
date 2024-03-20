import signal

from src.sweeper.logging import logging


class GracefulKiller:
    """
    Handles gracefull shutdown for app
    """

    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        logging.info("Gracefully shutting down...")
        self.kill_now = True
