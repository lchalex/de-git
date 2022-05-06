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

### FileStorage
At the moment we are using HKUST provided endpoint to upload file and download file. 

In the future, we might deploy a smart contract ourselves as a decentralized filestorage.

### Smart Contract
At the moment we have `./contracts/Repository.sol` only.

This is the template repository we defined to allow user to create repository with access control.

### Limited Functions
It is unfortunate that due to limited time and team members, we are unable to replicate git fully.
