from scanner.scanner.services.last_block_persister import LastBlockPersister

from .services import DucNetwork
from .services import DucScanner


class DucMaker:

    def __init__(self, network_name: str, polling_interval: int, commitment_chain_length: int):
        network = DucNetwork(network_name)
        last_block_persister = LastBlockPersister(network)
        self.scanner = DucScanner(network, last_block_persister,
                                  polling_interval, commitment_chain_length)
