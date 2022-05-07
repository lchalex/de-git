import pickle
import json
from web3 import Web3, HTTPProvider
from web3.gas_strategies.rpc import rpc_gas_price_strategy

net = {"db": "http://39.98.50.209:5145/",
       "debug": {"url": "https://rpc.debugchain.net",
                 "chain_id": 8348},
       "test": {"url": "https://rpc.etdchain.net",
                "chain_id": 3101},
       "local": {"url": "http://127.0.0.1:7545"}}

w3 = Web3(HTTPProvider(net['local']['url']))

with open('test_account.key', 'r') as f:
    key = f.read()

account = w3.eth.account.privateKeyToAccount(key)

with open('test_repo.txt', 'rb') as f:
    data = pickle.load(f)
    abi = data['abi']
    contract_address = data['contract_address']

w3.eth.default_account = account.address

contract = w3.eth.contract(
    address=contract_address,
    abi=abi
)

print(contract)

test_state = {
    'abc': 'THIS IS A STATE FOR TESTING ONLY'
}
json_state = json.dumps(test_state)

repository_state = contract.functions.git_pull().call()
print(repository_state)

contract.functions.git_push(json_state).transact()

repository_state = contract.functions.git_pull().call()
print(repository_state)

test_state = {
    'abc': 'THIS IS ANOTHER STATE FOR TESTING ONLY'
}
json_state = json.dumps(test_state)

contract.functions.git_push(json_state).transact()

repository_state = contract.functions.git_pull().call()
print(repository_state)