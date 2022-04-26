## De-Github
```bash
docker build -t 5017 .

docker run --rm \
           -it \
           -v $PWD:/workspace \
           -w /workspace \
           -e TESTNET=https://rpc.debugchain.net \
           -e MAINNET=https://rpc.etdchain.net \
           5017 bash

```