## De-Github

### Installing dependencies
We are using Python 3.8 for development.

Install required packages by running
```
pip install -r requirements.txt
```

### Setup
We are also using Ganache to create a blockchain network at local environment for development and testing.

Please head to the [Ganache website](https://trufflesuite.com/ganache/) and download it.

Once you have installed Ganache, you can simple click on quickstart and you should be able to call degit functions.

Remember to define the `RPC_SERVER` environment variable, by default the value is `http://127.0.0.1:7545` which is the default network of Ganache.

Also please put your private key in the `.key` file. Degit will automatically load the key and use it for git operations.

### How to run tests
We have prepare a `test.py` for your convenient.

Before you run the tests, you must put in two different private key to `.key` and `.second_user_key` (you can randomly pick 2 from Ganache).

Then run:
```
python test.py
```

You should obtain a console output similar to this one:
```
File last modified time on Owner machine: 2022-05-08 12:14:58
Initialized Repository. State file created in current directory.
Committed files:


Staged files:

	test.txt

Commit 076bb1b40881a287b47ca56d7d17d2c54815dd36 was successful.
Contract deployed to chain, contract address: 0x956462648eD458079CBEf6323E5CcE390285E7C4. 
Pushed commits "076bb1b40881a287b47ca56d7d17d2c54815dd36" to repository "test".
Whitelisted user of address: 0xbe2545A975e8A6Efd0BA5c4600aE4CfA228DA8b5
Dumped repository config to ./repo_config.pkl.
Loaded repository config from ./repo_config.pkl
Replace your repository by commit 076bb1b40881a287b47ca56d7d17d2c54815dd36
File last modified time on friend machine: 2022-05-08 12:15:06

Process finished with exit code 0
```

This `test.py` mimic two users (1 owner and 1 collaborator):
1. The owner has written some code in `test.txt`
1. The owner runs `degit init test` (`test` is the repository name)
1. The owner runs `degit add test.txt`
1. The owner runs `degit commit`
1. The owner runs `degit push` to push `test.txt` to the blockchain network
1. The owner gets his friend account address and runs `degit whitelist_add_user <friend_address>`
1. The owner runs `degit dump_repository_config`
1. The friend runs `degit load_repository_config`
1. The friend runs `degit pull`
1. The friend now has the `test.txt` in his machine

The printed file last modified time shows that the file is truly replaced by the one pulled from the repository.

### FileStorage
At the moment we are using HKUST provided endpoint to upload file and download file. 

In the future, we might deploy a smart contract ourselves as a decentralized filestorage.

### Smart Contract
At the moment we have `./contracts/Repository.sol` only.

This is the template repository we defined to allow user to create repository with access control.

### Limited Functions
It is unfortunate that due to limited time and team members, we are unable to replicate git fully.
