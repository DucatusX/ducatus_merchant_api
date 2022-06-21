from __future__ import annotations

from scanner.blockchain_common.wrapper_transaction import WrapperTransaction
from . import DucOutput


class DucTransaction(WrapperTransaction):

    @staticmethod
    def build(transaction: dict) -> DucTransaction:
        hash = transaction['txid']
        inputs = [i for i in transaction['vin']]
        outputs = DucOutput.build(transaction)
        contract_creation = False
        creates = ""

        return DucTransaction(hash, inputs, outputs, contract_creation, creates)
