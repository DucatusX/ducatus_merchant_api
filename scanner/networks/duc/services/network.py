from __future__ import annotations

from scanner.blockchain_common.wrapper_network import WrapperNetwork
from scanner.blockchain_common.litecoin_rpc import DucatuscoreInterface

from . import DucBlock


class DucNetwork(WrapperNetwork):

    def __init__(self, net_type: str):
        super().__init__(net_type)
        self.interface = DucatuscoreInterface()

    def get_last_block(self):
        return self.interface.rpc.getblockcount()

    def get_block(self, number: int) -> DucBlock:
        block_hash = self.interface.rpc.getblockhash(number)
        block = self.interface.rpc.getblock(block_hash)
        block['tx'] = [self.interface.rpc.getrawtransaction(t, 1) for t in block['tx']]
        return DucBlock.build(block)
