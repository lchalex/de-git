# Built-in lib
import os 

# third party lib
from etherdata_sdk.json_rpc import JsonRpcMethods
import json 

if os.getenv("DEBUG",None):
    bc_net = os.getenv("TESTNET","https://rpc.debugchain.net")
else:
    bc_net = os.getenv("MAINNET","https://rpc.etdchain.net")

class DGIT(object):
    def __init__():
        super().__init__()
        self.ether_client = JsonRpcMethods(url)
        self.status = json._read_status()

    def init():
        if os.path.exists(".dgit"):
            raise(".dgit repo already exist")
        else:
            os.mkdir('.dgit')
            y = json.dump()
            json.save('.dgit/', '')

    def _load():
        if os.path.exists(".dgit/"):
            self.status = json.load(".dgit/")
            

    def _read_status(self):


    def _dump_status(self):
        json.dump = self

    def add(self, files: list):
        # add flie to list

        
        return

    def commit(self):
        # generate local commit hash
        pass

    def push(self):
        '''
        create ether transaction 
        upload [code files] to ETD ( return file id)
        writes [file id, previous, current commit hash] to transaction
        new transaction hash = hash(previous commit hash)
        previous and current commit acts like a linked list
        '''
        pass
    def pull(self):
        pass
    def logs(self):
        pass
    def checkout(self):
        pass

    def _count(self):
        return self.ether_client.block_number()

    def _zip(self, files :list):
        # pack-up the files 
