# built-in libs
import os
import copy
import shutil
import pickle
import hashlib
from EthereumClient import EthereumClient
from utils import bcolors, get_files, clear_text_color, unique


class DEGIT:

    def __init__(self):
        # defaults
        self.default_cache_file = './.degit'
        self.default_snapshot_dir = './.snapshot'
        self.default_init_branch = 'master'

        # use debug chain by default unless set in environment variable 'BLOCKCHAIN_URL'
        self.block_chain_url = os.environ.get('BLOCKCHAIN_URL', 'https://rpc.debugchain.net')
        self.block_chain_id = os.environ.get('BLOCKCHAIN_ID', 8348)
        self.db_url = os.environ.get('DB_URL', 'http://39.98.50.209:5145/')

        # init etherdata client
        self.client = EthereumClient()

        # get current repo state
        self.state = {}
        if os.path.exists(self.default_cache_file):
            with open(self.default_cache_file, 'rb') as f:
                self.state = pickle.load(f)

        # create snapshot directory
        if not os.path.exists(self.default_snapshot_dir):
            os.mkdir(self.default_snapshot_dir)

    def _init_check(self):
        if not self.state:
            raise Exception('The repository has not yet been initalized.')

    def _save_state(self):
        with open(self.default_cache_file, 'wb') as f:
            pickle.dump(self.state, f)

    def validate_and_persist(func):
        """To check if repo has been initalized before calling a function. Also persists state after the function call."""

        def inner1(self, *args, **kwargs):
            self._init_check()
            returned_values = func(self, *args, **kwargs)
            self._save_state()
            return returned_values

        return inner1

    def init(self):
        """Initialize repository with branch master if not already initialized."""
        if os.path.exists(self.default_cache_file):
            raise Exception('The current directory contains a repository that has already been initialized.')
        else:
            self.state = {
                "branch": {
                    self.default_init_branch: {'commit_history': []},
                },
                'repo': '',
                'head': self.default_init_branch,
                'file_list': []}

            self._save_state()
            print('Initialized Repository. State file created in current directory.')

    def checkout(self):
        """Checkout a branch or commit base on user input."""
        pass

    def get_current_state(self):
        print(self.state)

    @validate_and_persist
    def branch(self, args):
        # switch branch should pull latest snapshot and overwrite any uncommitted changes
        """Create branch if not yet exists. List out existing branches if no branch name is given."""
        if args.branch_name:
            branch_name = args.branch_name[0]
            if branch_name in self.state:
                raise Exception(f'Branch {branch_name} already exists.')
            else:
                current_branch = self.state['head']
                self.state['branch'][branch_name] = self.state['branch'][current_branch]
                self.state['head'] = branch_name
        else:
            current_branch = self.state['head']
            for branch in self.state['branch']:
                if branch == current_branch:
                    print('*' + branch)
                else:
                    print(branch)

    @validate_and_persist
    def add(self, args):
        """
        python3 main.py add 2.txt -v

        stage_lists:           list - files going to stage
        staged_file_list:      list - staged files
        unstaged_file_list:    list - files not staged
        last_commit_file_list: list - files in latest commit
        snapshot_file_list:    list - file list in latest commit
        """
        stage_lists = args.file_list
        head = self.state['head']
        current_branch = self.state["branch"][head]
        if current_branch["commit_history"]:
            last_commit_file_list = current_branch["commit_history"][-1]["file_list"]
        else:
            last_commit_file_list = []

        # list the snapshot files.
        snapshot_file_list = self.state["file_list"]
        # list all files in all dir and sub_dir, and ommit ignored file
        unstaged_file_list = get_files(ommit=snapshot_file_list)
        # list the uncommitted, but staged files.
        staged_file_list = [file_path for file_path in snapshot_file_list if file_path not in last_commit_file_list]

        # find stage and unstage file.
        for file_path in stage_lists:
            if file_path in last_commit_file_list:
                unstaged_file_list.remove(file_path)
                continue
            elif file_path in unstaged_file_list:
                staged_file_list.append(file_path)
                unstaged_file_list.remove(file_path)
            else:
                if not os.path.exists(file_path):
                    raise Exception(f"{file_path} not found.")

        # remove duplicate and sort
        staged_file_list = sorted(unique(staged_file_list))
        unstaged_file_list = sorted(unique(unstaged_file_list))

        # print the staged and unstaged file list
        def stage_msg(start: str, file_list: list, color):

            msg = start
            for i in file_list:
                msg += f"\t{color}{i}\n"
            print(msg)
            clear_text_color()

        if args.v:
            stage_msg(f"Committed files:\n\n", last_commit_file_list, bcolors.ENDC)
        stage_msg(f"Staged files:\n\n", staged_file_list, bcolors.GREEN)
        # stage_msg(f"Unstaged files:\n\n", unstaged_file_list ,bcolors.RED)

        snapshot_file_list = unique(staged_file_list + last_commit_file_list)
        self.state["file_list"] = staged_file_list

    @validate_and_persist
    def commit(self):
        # generate local commit hash
        if len(self.state.get("file_list", [])) == 0:
            print("No files added")
            return

        self.state["file_list"] = sorted(self.state["file_list"])
        data = ""
        for file in self.state["file_list"]:
            f = open(file, 'r')
            data += f.read()
        hashfunc = hashlib.sha1()
        hashfunc.update(data.encode())
        commit_hash = hashfunc.hexdigest()
        snapshot_dir = os.path.join(self.default_snapshot_dir, commit_hash)
        if os.path.exists(snapshot_dir):
            print("commit hash already exists")
            return

        # Save snapshot locally
        os.makedir(snapshot_dir)
        for file in self.state["file_list"]:
            shutil.copyfile(file, os.path.join(snapshot_dir, file))

        package_path = self._save_archive(snapshot_dir)
        self.state['branch'][self.head]['commit_history'].append({
            'file_id': None,
            'commit_hash': commit_hash,
            'snapshot_path': package_path,
            'is_pushed': False
        })

    @validate_and_persist
    def push(self):
        '''
        create ether transaction
        upload [code files] to ETD ( return file id)
        writes [file id, previous, current commit hash] to transaction
        new transaction hash = hash(previous commit hash)
        previous and current commit acts like a linked list
        '''
        is_changes = False
        success_push = True
        tmp_state = copy.deepcopy(self.state)
        for branch_name, branch_dict in self.state['branch'].items():
            for i, commit in enumerate(branch_dict['commit_history']):
                if not commit["is_push"]:
                    is_changes = True
                    file_id = self.account.upload_file(file_path=commit["package_path"])
                    if file_id is not None:
                        tmp_state['branch'][branch_name][i]['file_id'] = file_id
                        tmp_state['branch'][branch_name][i]['is_pushed'] = True
                    else:
                        success_push = False

        if not is_changes:
            print('No new commits to push')
            return

        # if push succeed
        if success_push:
            self.state = tmp_state

            # download origin state

            # check if there is commit in origin BUT NOT IN local

            # if yes DENY push and ask for resolve conflicts

            # if no accept push to blockchain

        else:
            print('Failed upload to blockchain')

    @validate_and_persist
    def pull(self, args):
        # update current snapshot file list by last commit plz
        # self.state["file_list"] =
        pass

    def logs(self):
        pass

    def _save_archive(self, path):
        package_path = shutil.make_archive(
            path,
            'zip',
            path
        )
        return package_path

    # def _zip(self, files: list):
    #     # pack-up the files
    #     pass
