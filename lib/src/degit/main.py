# built-in libs
import argparse
import sys

# custom lib
from .degit import DEGIT
from .utils import login


def main(argv=sys.argv[1:]):
    argparser = argparse.ArgumentParser()

    argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
    argsubparsers.required = True

    # commands for debugging use only
    argsp = argsubparsers.add_parser("get_current_state")

    argsp = argsubparsers.add_parser("init")
    argsp.add_argument("repository_name", metavar="name", nargs=1, help="Repository name")


    argsp = argsubparsers.add_parser("login", help="login to account")
    argsp.add_argument("key_file", action="store", nargs="+", help="key file path")

    argsp = argsubparsers.add_parser("add", help="Add given filepath to next commit.")
    argsp.add_argument("file_list", action="store", nargs="+", help="Filepaths")
    argsp.add_argument("-v", action="store_true")

    argsp = argsubparsers.add_parser("reset", help="Remove given filepath from next commit.")
    argsp.add_argument("file_list", action="store", nargs="+", help="Filepaths")
    argsp.add_argument("-v", action="store_true")

    argsp = argsubparsers.add_parser("login")
    argsp.add_argument("key_file", metavar="key_file", nargs=1, help="Path to key file")
    
    argsp = argsubparsers.add_parser("push")
    argsp.add_argument("branch_name", metavar="branch_name", nargs=1, help="Branch name")

    argsp = argsubparsers.add_parser("branch")
    argsp.add_argument("branch_name", metavar="branch_name", nargs='?', help="Branch name")

    # whitelist subparser
    argsp_wl_par = argsubparsers.add_parser("whitelist")
    argsp_wl = argsp_wl_par.add_subparsers(title="whitelist command", dest="wl_cmd")

    argsp_wl_cmd = argsp_wl.add_parser("add", help="Add address to smart contract whitelist.")
    argsp_wl_cmd.add_argument("address_list", action="store", nargs="+", help="address list")

    argsp_wl_cmd = argsp_wl.add_parser("remove", help="remove address from smart contract whitelist.")
    argsp_wl_cmd.add_argument("address_list", action="store", nargs="+", help="address list")
    

    argsp = argsubparsers.add_parser("dump_repository_config")

    argsp = argsubparsers.add_parser("load_repository_config")

    argsp = argsubparsers.add_parser("commit")

    argsp = argsubparsers.add_parser("pull", help='Run "degit load_repository_config" before pulling repository.')
    # argsp.add_argument("address", metavar="address", nargs='?', help="Repository contract address")
    # argsp.add_argument("abi", metavar="abi", nargs='?', help="Repository ABI")

    argsp = argsubparsers.add_parser("stash")
    argsp = argsubparsers.add_parser("pop_stash")

    args = argparser.parse_args(argv)

    if args.command == "login":
        login(args)
        return

    git = DEGIT()

    if args.command == "add":
        git.add(args)
    elif args.command == "commit":
        git.commit()
    elif args.command == "reset":
        git.reset(args)
    elif args.command == "init":
        git.init(args)
    elif args.command == "push":
        git.push(args)
    elif args.command == "pull":
        git.pull([])
    elif args.command == "stash":
        git.stash()
    elif args.command == "pop_stash":
        git.pop_stash()
    elif args.command == "branch":
        git.branch(args)
    elif args.command == "get_current_state":
        git.get_current_state()
    elif args.command == "whitelist":
        if args.wl_cmd == "add":
            git.whitelist_add_user(args)
        elif args.wl_cmd == "remove":
            git.whitelist_remove_user(args)
        else:
            print("function is missing, whitelist <add/remove> <pocket address>")
    elif args.command == "dump_repository_config":
        git.dump_repository_config()
    elif args.command == "load_repository_config":
        git.load_repository_config()


if __name__ == '__main__':
    main()
