import json
import pickle
from web3 import Web3, HTTPProvider
from web3.gas_strategies.rpc import rpc_gas_price_strategy

net = {"db": "http://39.98.50.209:5145/",
       "debug": {"url": "https://rpc.debugchain.net",
                 "chain_id": 8348},
       "test": {"url": "https://rpc.etdchain.net",
                "chain_id": 3101},
       "local": {"url": "http://127.0.0.1:7545"}}

env = "debug"

# get bytecode / bin
with open('../compiled_contracts/repository_abi.json', 'r') as f:
    abi = json.load(f)
with open('../compiled_contracts/repository_bytecode.txt', 'r') as f:
    bytecode = f.read()

print(abi)
print(bytecode)

# w3 = Web3(EthereumTesterProvider())
w3 = Web3(HTTPProvider(net['local']['url']))

account = w3.eth.account.create('nhaoiujbnwdojawd')

# obtain private key from ganache
# pk = '4ca66dc583c8320582cd2ecb0db0c31fae9867734571cb873f6081b7e3f51fb2'

# with open('./test_account.key', 'w') as f:
#     f.write(pk)

with open('test_account.key', 'r') as f:
    key = f.read()

print(key)

account = w3.eth.account.privateKeyToAccount(key)

print(account.address)

# # set pre-funded account as sender
w3.eth.default_account = account.address

contract = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(account.address)
print(f'Current nonce = {nonce}.')

w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
gas_price = w3.eth.generate_gas_price()
print(f'Gas price: {gas_price}.')

tx_hash = contract.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
contract_return = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = contract_return['contractAddress']

with open('test_repo.txt', 'wb') as f:
    pickle.dump({'abi': abi, 'contract_address': contract_address}, f)
