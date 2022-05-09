
# De-Git


python3 -m pip install -i https://test.pypi.org/simple/ degit

install package with `pip3 install degit==0.0.1` from [pypi](https://pypi.org/project/degit/0.0.1/)

---
### CLI Demo
>User A
```bash
mkdir repo_a 
cd repo_a
# login to A account
degit login ../key/a.key
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

degit login ../key/b.key
degit init tester
# restore abi and contract address 
degit load_repository_config

degit pull 

```
---
### Inline example
```bash
cd test
python3 test.py
```
---

### Build 
```bash
cd lib
python3 -m build
pip3 install dist/degit-0.0.1-py3-none-any.whl
```