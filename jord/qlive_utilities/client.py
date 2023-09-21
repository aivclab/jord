from typing import Any

import zmq
from draugr.python_utilities import in_docker
from warg import AlsoDecorator

__all__ = ["QliveClient"]


def default_address() -> str:
    if in_docker():
        return "tcp://host.docker.internal:5555"
    return "tcp://localhost:5555"


class QliveClient(AlsoDecorator):
    """
    TODO: MAYBE NOT ALSO A DECORATOR

    Client for sending data to qgis instance
    """

    def __init__(self, address: str = default_address()):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)

        if str.isnumeric(address):  # only port was given
            address = f"{default_address().split(':')[0]}{address}"

        if "://" not in address:  # protocol is missing
            address = f"tcp://{address}"

        self.address = address

    def __enter__(self):
        self.socket.connect(self.address)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def send(self, *args) -> Any:
        self.socket.send(*args)
        return self.socket.recv()
