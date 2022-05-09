# De-Github

- [Setup](#setup)
- [How to run tests](#How-to-run-tests)
	- [test.py](#option-1-testpy)
	- [CLI](#option-2-cli-demo)
- [FileStorage](#filestorage)
- [Smart Contract](#smart-contract)
- [Limited Functions](#limited-functions)

## Setup

1. We are using `Python 3.8` for development.

2. install package from [pypi](https://pypi.org/project/degit/0.0.1/)
	> `pip3 install degit==0.0.1`

3. We are using `Ganache` to create a blockchain network at local environment for development and testing.

	Please head to the [Ganache website](https://trufflesuite.com/ganache/) and download it.

	Once you have installed Ganache, you can simple click on quickstart and you should be able to call degit functions.

	Remember to define the `RPC_SERVER` environment variable, by default the value is `http://127.0.0.1:7545` which is the default network of Ganache.

Also please put your private key in the `.key` file. Degit will automatically load the key and use it for git operations.
Or run `degit login <key path>` under repository folder.

## How to run tests
### Option 1: `test.py`
We have prepare a [`test.py`](test/test.py) for your convenient.

**Before you run the tests, you must put in two different private key to `a.key` and `b.key` under `test/` (you can randomly pick 2 from Ganache).**



You should obtain a console output similar to this one:
```
Owner's Log:
File last modified time on Owner machine: 2022-05-08 12:25:00
Initialized Repository. State file created in current directory.
Committed files:


Staged files:

	test.txt

Commit 076bb1b40881a287b47ca56d7d17d2c54815dd36 was successful.
Contract deployed to chain, contract address: 0x7B9ef343909fD32b8Ad7c9667Dc49Dd4034e4742. 
Pushed commits "076bb1b40881a287b47ca56d7d17d2c54815dd36" to repository "test".
Whitelisted user of address: 0xbe2545A975e8A6Efd0BA5c4600aE4CfA228DA8b5
Dumped repository config to ./repo_config.pkl.

Friend's Log:
Loaded repository config from ./repo_config.pkl
Replace your repository by commit 076bb1b40881a287b47ca56d7d17d2c54815dd36
File last modified time on friend machine: 2022-05-08 12:25:07


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

---
### Option 2: CLI Demo
>User A
```bash
mkdir repo_a 
cd repo_a
# login to A account
degit login ../test/a.key
# Repo init
degit init new_project
# create files to add and commit
touch README.MD 1.txt
degit add README.MD 1.txt
degit reset README.MD

degit commit 

# degit push <branch name>
degit push master 

# add user to the repo whitelist
degit whitelist add 0x6e4C7de1d42b63e5E1946D28aF7393697Ef544aa
# degit whitelist remove 0x6e4C7de1d42b63e5E1946D28aF7393697Ef544aa

# dump ABI and contract address 
degit dump_repository_config
```

>User B
```bash
# create second folder to clone repo
mkdir ../repo_b/ 
cp ./repo_config.pkl ../repo_b/
cd ../repo_b/

degit login ../test/b.key
degit init tester
# restore abi and contract address 
degit load_repository_config

degit pull 
```

## FileStorage
At the moment we are using HKUST provided endpoint to upload file and download file. 

In the future, we might deploy a smart contract ourselves as a decentralized filestorage.

## Smart Contract
At the moment we have `./contracts/Repository.sol` only.

This is the template repository we defined to allow user to create repository with access control.

## Limited Functions
It is unfortunate that due to limited time and team members, we are unable to replicate git fully.
