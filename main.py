import argparse
import sys
from degit import DEGIT


def main(argv=sys.argv[1:]):
    argparser = argparse.ArgumentParser()

    argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
    argsubparsers.required = True

    # commands for debugging use only
    argsp = argsubparsers.add_parser("get_current_state")

    argsp = argsubparsers.add_parser("init")
    argsp.add_argument("repository_name", metavar="name", nargs=1, help="Repository name")

    argsp = argsubparsers.add_parser("add", help="Add given filepath to version control.")
    argsp.add_argument("file_list", action="store", nargs="+", help="Filepaths")
    argsp.add_argument("-v", action="store_true")

    argsp = argsubparsers.add_parser("push")
    argsp.add_argument("branch_name", metavar="branch_name", nargs=1, help="Branch name")

    argsp = argsubparsers.add_parser("branch")
    argsp.add_argument("branch_name", metavar="branch_name", nargs=1, help="Branch name")

    argsp = argsubparsers.add_parser("commit")

    args = argparser.parse_args(argv)
    git = DEGIT()

    if args.command == "add":
        git.add(args)
    elif args.command == "commit":
        git.commit()
    elif args.command == "init":
        git.init(args)
    elif args.command == "push":
        git.push(args)
    elif args.command == "branch":
        git.branch(args)
    elif args.command == "get_current_state":
        git.get_current_state()


if __name__ == '__main__':
    main()
