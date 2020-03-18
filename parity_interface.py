import json
import requests
from web3 import Web3, HTTPProvider

from merchant_api.settings import NETWORK_SETTINGS


class ParConnectExc(Exception):
    def __init__(self, *args):
        self.value = 'can not connect to parity'

    def __str__(self):
        return self.value


class ParErrorExc(Exception):
    pass


class ParityInterface:
    endpoint = None
    settings = None

    def __init__(self):

        self.settings = NETWORK_SETTINGS['DUC']
        self.setup_endpoint()
        # self.check_connection()

    def setup_endpoint(self):
        self.endpoint = 'http://{host}:{port}'.format(
            host=self.settings['host'],
            port=self.settings['port']
        )
        self.settings['chainId'] = self.eth_chainId()
        print('parity interface', self.settings, flush=True)
        return

    def __getattr__(self, method):
        def f(*args):
            arguments = {
                'method': method,
                'params': args,
                'id': 1,
                'jsonrpc': '2.0',
            }
            try:
                temp = requests.post(
                    self.endpoint,
                    json=arguments,
                    headers={'Content-Type': 'application/json'}
                )
            except requests.exceptions.ConnectionError as e:
                raise ParConnectExc()
            result = json.loads(temp.content.decode())
            if result.get('error'):
                raise ParErrorExc(result['error']['message'])
            return result['result']

        return f

    def transfer(self, address_from, private_key, address_to, amount):
        nonce = int(self.eth_getTransactionCount(address_from, "pending"), 16)

        tx_params = {
            'to': address_to,
            'value': amount,
            'gas': 21000,
            'gasPrice': 2 * 10 ** 9,
            'nonce': nonce,
            'chainId': self.settings['chainId']
        }

        w3 = Web3(HTTPProvider(self.endpoint))

        signed_tx = w3.eth.account.signTransaction(tx_params, private_key)

        try:
            tx = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(tx.hex())
            return tx.hex()
        except Exception as e:
            print('DUCATUS TRANSFER ERROR: transfer for {amount} DUC from {address_from} to {address_to} failed'
                  .format(amount=amount, address_from=address_from, address_to=address_to), flush=True
                  )
            print(e, flush=True)
