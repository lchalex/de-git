import json
import os
import pickle
from web3 import Web3, HTTPProvider
from web3.gas_strategies.rpc import rpc_gas_price_strategy

url = os.environ.get('RPC_SERVER', 'http://127.0.0.1:7545')
storage_address = os.environ.get('storage_address')


class EthereumClient:

    def __init__(self, private_key_path='./.key'):
        self.w3 = Web3(HTTPProvider(url))
        self.w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
        self.private_key_path = private_key_path
        self.cache_file_path = './.ethclient'
        self.cache_default = dict(contracts=[])
        self.cache = self.cache_default
        if os.path.exists(self.cache_file_path):
            with open(self.cache_file_path, 'rb') as f:
                self.cache = pickle.load(f)
        self._login()

    def _login(self):
        if not os.path.exists(self.private_key_path):
            raise Exception(f'Private key not found at {self.private_key_path}.')
        private_key = open(self.private_key_path, 'r').read()
        if not private_key or private_key == '':
            raise Exception(f'Private key is empty. Please put your private key under {self.private_key_path}.')
        self.account = self.w3.eth.account.privateKeyToAccount(private_key)
        self.w3.eth.default_account = self.account.address

    def _auto_cache(func):
        """Automatically load the account from the private key stored in the same directory"""

        def inner1(self, *args, **kwargs):

            returned_values = func(self, *args, **kwargs)

            with open(self.cache_file_path, 'wb') as f:
                pickle.dump(self.cache, f)

            return returned_values
        return inner1

    @_auto_cache
    def deploy_repository(self, repository_name, abi=None, bytecode=None):

        for contract in self.cache['contracts']:
            if repository_name in contract['repository_name']:
                raise Exception(f'Repository {repository_name} already deployed. '
                                'Please use a different repository name.')

        if not abi or not bytecode:
            with open('./compiled_contracts/repository_abi.json', 'r') as f:
                abi = json.load(f)
            with open('./compiled_contracts/repository_bytecode.txt', 'r') as f:
                bytecode = f.read()

        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = contract.constructor().transact()
        contract_return = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = contract_return['contractAddress']
        self.cache['contracts'].append(
            {'repository_name': repository_name, 'repository_address': contract_address, 'abi': abi})
        print(f"Contract deployed to chain, contract address: {contract_address}. "
              "Get your deployed contracts by running 'degit list_repositories'")

    def list_repositories(self):
        for contract in self.cache.get('contracts', []):
            print(f'{contract["repository_name"]}: {contract["repository_address"]}')

    def _repository_input_check(self, repository_name=None, contract_address=None, abi=None):
        if not repository_name and not contract_address:
            raise Exception('Please provide either a repository name or a contract address.')

        for contract in self.cache['contracts']:
            if repository_name:
                if contract['repository_name'] == repository_name:
                    contract_address = contract['repository_address']
                    abi = contract['abi']
                    break
            if contract_address == contract['repository_address']:
                abi = contract['abi']
                break

        if not abi or not contract_address:
            raise Exception(f'Repository is not found. Please input a valid contract address and ABI.')

        return contract_address, abi

    def get_repository_state(self, repository_name=None, contract_address=None, abi=None):

        contract_address, abi = self._repository_input_check(repository_name, contract_address, abi)

        contract = self.w3.eth.contract(
            address=contract_address,
            abi=abi
        )

        contract_response = contract.functions.git_pull().call()
        if contract_response == '':
            print(f'Repository {repository_name} is empty.')
            return None
        else:
            return json.loads(contract_response)

    def update_repository_state(self, state: dict, repository_name=None, contract_address=None, abi=None):
        if not isinstance(state, dict):
            raise Exception('State must be a dictionary.')

        contract_address, abi = self._repository_input_check(repository_name, contract_address, abi)

        contract = self.w3.eth.contract(
            address=contract_address,
            abi=abi
        )

        tx_hash = contract.functions.git_push(json.dumps(state)).transact({'from': self.account.address})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def list_cache(self):
        print(self.cache)

    def clear_cache(self):
        """For debugging purposes only"""
        with open(self.cache_file_path, 'wb') as f:
            pickle.dump(self.cache_default, f)


if __name__ == '__main__':
    client = EthereumClient()
    # client.clear_cache()
    # client.deploy_repository('test_repo')
    client.list_repositories()
    print(client.get_repository_state('test_repo'))
    print(client.update_repository_state({'test': 'abcdefg'}, 'test_repo'))
    print(client.get_repository_state('test_repo'))
    print(client.update_repository_state({'test': 'CHANGED STATE'}, 'test_repo'))
    print(client.get_repository_state('test_repo'))
    # client.clear_cache()
