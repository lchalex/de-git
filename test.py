import os
import shutil
from degit import DEGIT
from EthereumClient import EthereumClient
from datetime import datetime


class ArgparseMimic:
    pass


def create_test_file(default_filename='test.txt'):
    with open(default_filename, 'w') as f:
        f.write('this is a test file for testing degit.')

    file_last_modified_time = datetime.utcfromtimestamp(os.path.getmtime(default_filename)).strftime(
        '%Y-%m-%d %H:%M:%S')
    print(f'File last modified time on Owner machine: {file_last_modified_time}')


def clear_all_cache():
    # files
    to_delete = ['.degit', '.ethclient', 'repo_config.pkl', 'test.txt']
    for file in to_delete:
        if os.path.exists(file):
            os.remove(file)

    # dirs
    if os.path.exists('.snapshot'):
        shutil.rmtree('.snapshot', ignore_errors=True)


def run_test():
    friend_private_key_path = './.second_user_key'
    client = EthereumClient(friend_private_key_path)
    friend_address = client.account.address
    del client

    # setup for test
    clear_all_cache()

    # Owner has written some code
    create_test_file()

    def owner_action():
        degit = DEGIT()
        mimic = ArgparseMimic()

        setattr(mimic, 'repository_name', ['test'])
        degit.init(mimic)

        setattr(mimic, 'file_list', ['test.txt'])
        setattr(mimic, 'v', True)
        degit.add(mimic)

        degit.commit()

        setattr(mimic, 'branch_name', ['master'])
        degit.push(mimic)

        # Owner whitelist his friend to access his repository
        setattr(mimic, 'address', [friend_address])
        degit.whitelist_add_user(mimic)

        clear_all_cache()
        # Owner dump his repository connection details (address & abi) for his friend
        degit.dump_repository_config()

    owner_action()

    def friend_action():
        # Friend uses degit
        degit = DEGIT(private_key_path=friend_private_key_path)
        # Friend loads the config the 1st user gave him
        degit.load_repository_config()
        # Friend pulls from the repository created by the owner.
        degit.pull([])

        file_last_modified_time = datetime.utcfromtimestamp(os.path.getmtime('test.txt')).strftime(
            '%Y-%m-%d %H:%M:%S')
        print(f'File last modified time on friend machine: {file_last_modified_time}')

        clear_all_cache()

    friend_action()


if __name__ == '__main__':
    run_test()
