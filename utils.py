import os


class bcolors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def unique(ls: list) -> list:
    return list(set(ls))


def get_files(ommit: list) -> list:
    all_file_list = get_all_files()
    # remove the staged items
    for file_path in ommit:
        try:
            all_file_list.remove(file_path)
        except:
            pass
    return all_file_list


def get_all_files() -> list:
    if os.path.exists(".dgitignore"):
        with open(".dgitignore", 'r') as f:
            k = f.read()
    ignore_list = ["__pycache__",
                   ".pyc",
                   ".git",
                   ".dgit", ]
    PWD = os.path.join(os.getcwd(), "*")

    all_file_list = []
    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            full = os.path.join(root, f)  # absolute file path
            file_path = os.path.join(*(full.split("/")[2:]))  # relative file path
            if not any(word in file_path for word in ignore_list):
                all_file_list.append(file_path)
    return all_file_list


def clear_text_color():
    print("\033[0m", end="")


if __name__ == '__main__':
    print(get_files())
