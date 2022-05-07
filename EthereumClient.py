import json
import os
import pickle
import requests
from urllib.parse import urljoin
from http import HTTPStatus
from web3 import Web3, HTTPProvider
from web3.gas_strategies.rpc import rpc_gas_price_strategy

url = os.environ.get('RPC_SERVER', 'http://127.0.0.1:7545')
# will change to smart contract in future versions
file_upload_url = 'http://39.98.50.209:5145/un/file/'
file_download_url = 'http://39.98.50.209:5145/dn/file/'


class EthereumClient:

    def __init__(self, private_key_path='./.key'):

        self.w3 = Web3(HTTPProvider(url))

        if not self.w3.isConnected():
            raise Exception(f'Unable to connect to {url}. Is the given network available?')

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
    def create_repository(self, repository_name, abi=None, bytecode=None):

        for contract in self.cache['contracts']:
            if repository_name in contract['name']:
                raise Exception(f'Repository {repository_name} already deployed. '
                                'Please use a different repository name.')

        if not abi or not bytecode:
            with open('./compiled_contracts/repository_abi.json', 'r') as f:
                abi = json.load(f)
            with open('./compiled_contracts/repository_bytecode.txt', 'r') as f:
                bytecode = f.read()

        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = contract.constructor(repository_name).transact()
        contract_return = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = contract_return['contractAddress']
        self.cache['contracts'].append({'name': repository_name, 'contract_address': contract_address, 'abi': abi})
        print(f"Contract deployed to chain, contract address: {contract_address}. ")
        return contract_address, abi

    def list_repositories(self):
        for contract in self.cache.get('contracts', []):
            print(f'{contract["name"]}: {contract["contract_address"]}')

    def _get_contract(self, name=None, contract_address=None, abi=None):
        if not name and not contract_address:
            raise Exception('Please provide either a contract name or a contract address.')

        for contract in self.cache['contracts']:
            if name:
                if contract['name'] == name:
                    contract_address = contract['contract_address']
                    abi = contract['abi']
                    break
            if contract_address == contract['contract_address']:
                abi = contract['abi']
                break

        if not abi or not contract_address:
            raise Exception(f'Contract is not found. Please input a valid contract address and ABI.')

        contract = self.w3.eth.contract(
            address=contract_address,
            abi=abi
        )

        return contract

    def contract_getter(self, func, args=None, name=None, contract_address=None, abi=None):

        contract = self._get_contract(name, contract_address, abi)

        if not args:
            contract_response = contract.functions[func]().call()
        else:
            contract_response = contract.functions[func](args).call()
        return contract_response

    def contract_setter(self, func, args, name=None, contract_address=None, abi=None):

        contract = self._get_contract(name, contract_address, abi)

        tx_hash = contract.functions[func](args).transact({'from': self.account.address})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    @staticmethod
    def upload_file(file_path, days=999, error_on_exists=False):
        file = {'file': open(file_path, 'rb'), 'days': days}
        request = requests.post(file_upload_url, files=file)
        if request.status_code == HTTPStatus.OK:
            response = request.json()['data']
            file_id = response['afid']
            if 'isExist' in response:
                if error_on_exists and response['isExist']:
                    raise Exception('File already exists.')
            return file_id

    @staticmethod
    def download_file(file_id, download_path):
        with requests.get(urljoin(file_download_url, file_id)) as request:
            request.raise_for_status()
            with open(download_path, 'wb') as f:
                for chunk in request.iter_content(chunk_size=8192):
                    f.write(chunk)

    def list_cache(self):
        print(self.cache)

    def clear_cache(self):
        """For debugging purposes only"""
        with open(self.cache_file_path, 'wb') as f:
            pickle.dump(self.cache_default, f)


if __name__ == '__main__':

    client = EthereumClient()
    # client.clear_cache()
    #
    # file_id_1 = client.upload_file('./compiled_contracts/repository_abi.json')
    # file_id_2 = client.upload_file('./compiled_contracts/repository_bytecode.txt')
    # state = {
    #     'commit_history': [{
    #         'commit_id': 1,
    #         'file_id': file_id_1
    #     }, {
    #         'commit_id': 2,
    #         'file_id': file_id_2
    #     }]
    # }
    #
    # client.create_repository('test_repo')
    #
    # client.list_repositories()
    #
    # print('init repo state', client.contract_getter('git_pull', name='test_repo'))
    # client.contract_setter('git_push', json.dumps(state), name='test_repo')
    print('after 1st push', json.loads(client.contract_getter('git_pull', name='test')))
    #
    # file_id_3 = client.upload_file('./contracts/Repository.sol')
    # state['commit_history'].append({'commit_id': 3, 'file_id': file_id_3})
    #
    # client.contract_setter('git_push', json.dumps(state), name='test_repo')
    #
    # final_state = json.loads(client.contract_getter('git_pull', name='test_repo'))
    #
    # import os
    #
    # download_dir = './poc_drafts/'
    #
    # for commit in final_state['commit_history']:
    #     client.download_file(commit['file_id'], os.path.join(download_dir, f'{commit["commit_id"]}.txt'))
    #
    # print('after 2nd push', final_state)
    # print(os.listdir(download_dir))
    #
    # client.clear_cache()
