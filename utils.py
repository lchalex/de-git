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
    root = os.getcwd()
    file_set = set()

    ignore_list = []
    if os.path.exists(".degitignore"):
        with open('./.degitignore', 'r') as f:
            ignore_list = f.readlines()
            ignore_list = [line.rstrip() for line in ignore_list]

    dirs_to_ignore = [os.path.normpath(ignore) for ignore in ignore_list if os.path.isdir(ignore)]
    files_to_ignore = list(set(ignore_list) - set(dirs_to_ignore))

    for dir_, _, files in os.walk(root):
        for file_name in files:

            rel_dir = os.path.relpath(dir_, root)
            rel_file = os.path.join(rel_dir, file_name)

            # if the file is in the project directory, there will be '.'. Remove the '.' here
            if rel_dir == os.path.normpath('.'):
                rel_file = rel_file.split(os.path.sep)[1]

            if os.path.normpath(rel_file).split(os.path.sep)[0] in dirs_to_ignore:
                continue
            if rel_file in files_to_ignore:
                continue

            file_set.add(rel_file)

    return list(file_set)


def clear_text_color():
    print("\033[0m", end="")


if __name__ == '__main__':
    print(get_files())
