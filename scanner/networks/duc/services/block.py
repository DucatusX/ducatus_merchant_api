from __future__ import annotations

from scanner.blockchain_common.wrapper_block import WrapperBlock
from . import DucTransaction


class DucBlock(WrapperBlock):

    @staticmethod
    def build(block: dict) -> DucBlock:
        hash = block['hash']
        number = block['height']
        timestamp = block['time']
        transactions = [DucTransaction.build(t) for t in block['tx']]
        return DucBlock(hash, number, timestamp, transactions)
