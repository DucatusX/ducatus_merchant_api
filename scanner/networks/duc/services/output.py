from __future__ import annotations

from scanner.blockchain_common.wrapper_output import WrapperOutput


class DucOutput(WrapperOutput):

    @staticmethod
    def build(transaction) -> [DucOutput]:
        vout = transaction['vout']
        return [
            DucOutput(
                transaction['hash'],
                v['n'],
                v['scriptPubKey']['addresses'],
                int(v['valueSat']),
                None
            ) for v in vout if v['scriptPubKey']['type'] != 'nulldata'
        ]
